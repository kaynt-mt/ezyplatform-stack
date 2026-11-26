#!/usr/bin/env python3
import argparse
import base64
import datetime
import hashlib
import http.server
import json
import mimetypes
import os
import platform
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

VERSION = '1.0.0'
USER_AGENT = 'ezyplatform-landing-page/' + VERSION + ' (Python)'
CLIENT_NAME = 'AI landing page builder'
MARKET_URL = os.environ.get('EZY_MARKET_URL', 'https://ezyplatform.com')
DEFAULT_ADMIN_URLS = ['http://localhost:9090', 'http://127.0.0.1:9090']
STATE_DIR = os.path.join(os.path.expanduser('~'), '.ezyplatform')
STATE_FILE = os.path.join(STATE_DIR, 'landing-page.json')
MIN_EZYLOGIN_VERSION = '0.4.1'
CLI_TOKEN_API = '/ezylogin/api/v1/cli/me/token'
SAVE_SIMPLY_API = '/ezyarticle/api/v1/posts/save-simply'
CORE_PROJECTS = ('ezyarticle', 'ezylogin')
LEAD_PROJECTS = ('ezysupport', 'ezymail')
SHOP_PROJECTS = ('ecommerce', 'graphql', 'ezylogin', 'ezypayment')
EXIT_NEED = 3


class HttpResult:
    def __init__(self, status, body, headers=None):
        self.status = status
        self.body = body
        self.headers = headers or {}

    def text(self):
        return self.body.decode('utf-8', errors='replace')

    def json(self):
        try:
            return json.loads(self.text() or 'null')
        except ValueError:
            return None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def call(method, url, body=None, token=None, timeout=60, content_type='application/json'):
    data = None
    if body is not None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Accept', 'application/json, text/html;q=0.9, */*;q=0.8')
    if data is not None:
        req.add_header('Content-Type', content_type)
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    try:
        with OPENER.open(req, timeout=timeout) as resp:
            return HttpResult(resp.status, resp.read(), dict(resp.headers))
    except urllib.error.HTTPError as e:
        return HttpResult(e.code, e.read() or b'', dict(e.headers or {}))
    except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
        return HttpResult(0, b'')


def out(key, value):
    print('%s=%s' % (key, value))


def need(code, message):
    print('NEED %s: %s' % (code, message))
    sys.exit(EXIT_NEED)


def die(message):
    print('ERROR: ' + message, file=sys.stderr)
    sys.exit(1)


def load_state():
    try:
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = STATE_FILE + '.tmp'
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)
    try:
        os.chmod(STATE_FILE, 0o600)
    except OSError:
        pass


def normalize_url(url):
    url = url.strip().rstrip('/')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url


def resolve_admin_url(args, probe=True):
    if getattr(args, 'admin_url', None):
        url = normalize_url(args.admin_url)
        state = load_state()
        if state.get('default_admin_url') != url:
            state['default_admin_url'] = url
            save_state(state)
        return url
    if os.environ.get('EZY_ADMIN_URL'):
        return normalize_url(os.environ['EZY_ADMIN_URL'])
    state = load_state()
    if state.get('default_admin_url'):
        return state['default_admin_url']
    if probe:
        for url in DEFAULT_ADMIN_URLS:
            if call('GET', url + '/', timeout=5).status:
                return url
        local_home = find_local_home(args)
        if local_home:
            return 'http://localhost:%s' % local_home['admin_port']
    need('admin_url', 'admin URL unknown: ask the user for the address of their EzyPlatform admin '
         '(for example https://admin.example.com or http://localhost:9090) and pass --admin-url')


def get_token(admin_url):
    entry = load_state().get('tokens', {}).get(admin_url)
    if not entry:
        return None
    if entry.get('expiredAt') and entry['expiredAt'] / 1000 < time.time():
        return None
    return entry.get('accessToken')


def require_token(admin_url):
    token = get_token(admin_url)
    if not token:
        need('login', 'no valid admin token for %s: run the login command' % admin_url)
    res = call('GET', admin_url + '/api/v1/admins/me', token=token)
    if res.status == 401:
        need('login', 'the saved admin token was rejected (expired or signed out): run the login command again')
    if res.status == 0:
        need('admin_down', 'admin %s does not answer: start EzyPlatform or check the address' % admin_url)
    return token


def version_tuple(version):
    parts = []
    for p in (version or '').split('.'):
        digits = ''.join(ch for ch in p if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def probe_ezylogin(admin_url):
    res = call('POST', admin_url + CLI_TOKEN_API, body={})
    data = res.json() if res.status else None
    if res.status == 0:
        return 'admin_down'
    if res.status == 404:
        return 'missing'
    if res.status == 403 and isinstance(data, dict) and data.get('cliLogin') == 'notAllowed':
        return 'disabled'
    if res.status == 400:
        return 'enabled'
    if res.status == 401:
        return 'outdated'
    return 'unknown_%s' % res.status


def market_project(name):
    res = call('GET', MARKET_URL + '/api/v1/released-projects/' + urllib.parse.quote(name), timeout=30)
    if res.status != 200:
        return None
    return res.json()


def project_status(admin_url, token, name):
    res = call('GET', admin_url + '/api/v1/projects/' + urllib.parse.quote(name), token=token)
    if res.status == 403:
        return {'error': 'forbidden'}
    if res.status == 404:
        return {'installed': False}
    if res.status != 200:
        return {'error': 'http_%s' % res.status}
    version = (res.json() or {}).get('version')
    types_res = call('GET', admin_url + '/api/v1/projects/%s/module-types' % urllib.parse.quote(name), token=token)
    all_types = types_res.json() if types_res.status == 200 else []
    active_res = call('GET', admin_url + '/api/v1/projects/%s/module-types?active=true' % urllib.parse.quote(name), token=token)
    active_types = active_res.json() if active_res.status == 200 else []
    return {
        'installed': True,
        'version': version,
        'module_types': all_types or [],
        'active_types': active_types or [],
    }


def read_state_env(folder):
    values = {}
    try:
        with open(os.path.join(folder, '.ezy', 'state.env'), encoding='utf-8') as f:
            for line in f:
                key, _, value = line.strip().partition('=')
                if key in ('MODE', 'PROJECT_NAME', 'ADMIN_PORT', 'WEB_PORT'):
                    values[key] = value.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


def describe_home(path):
    if not path:
        return None
    path = os.path.abspath(os.path.expanduser(path))
    for folder in (path, os.path.dirname(path)):
        state = read_state_env(folder)
        if state.get('MODE') == 'docker' and os.path.isfile(os.path.join(folder, 'docker-compose.yml')):
            return {'mode': 'docker', 'dir': folder, 'project': state.get('PROJECT_NAME') or 'ezyplatform',
                    'admin_port': state.get('ADMIN_PORT') or '9090'}
    cli = 'cli.sh' if os.name != 'nt' else 'cli.bat'
    for folder in (path, os.path.join(path, 'ezyplatform')):
        if os.path.isfile(os.path.join(folder, cli)):
            return {'mode': 'native', 'dir': folder, 'admin_port': local_admin_port(folder)}
    return None


def find_local_home(args, admin_url=None):
    candidates = []
    if getattr(args, 'home', None):
        candidates.append(args.home)
    if os.environ.get('EZYPLATFORM_HOME'):
        candidates.append(os.environ['EZYPLATFORM_HOME'])
    home = os.path.expanduser('~')
    candidates += [
        os.path.join(home, 'ezyplatform'),
        os.path.join(home, 'ezyplatform-dev-site'),
        'C:\\ezyplatform',
    ]
    try:
        candidates += [os.path.join(home, n) for n in sorted(os.listdir(home)) if n.startswith('ezyplatform')]
    except OSError:
        pass
    port = str(urllib.parse.urlparse(admin_url).port or '') if admin_url else ''
    for c in candidates:
        info = describe_home(c)
        if info and (not port or info['admin_port'] == port):
            return info
    return None


def local_admin_port(home):
    try:
        with open(os.path.join(home, 'admin', 'settings', 'config.properties'), encoding='utf-8') as f:
            for line in f:
                key, _, value = line.partition('=')
                if key.strip() == 'server.port' and value.strip().isdigit():
                    return value.strip()
    except OSError:
        pass
    return '9090'


def is_local_url(url):
    host = urllib.parse.urlparse(url).hostname or ''
    return host in ('localhost', '127.0.0.1', '::1')

def cmd_login(args):
    admin_url = resolve_admin_url(args)
    state = probe_ezylogin(admin_url)
    if state == 'admin_down':
        need('admin_down', 'admin %s does not answer' % admin_url)
    if state == 'missing':
        need('ezylogin_missing', 'EzyLogin is not installed or not active on %s' % admin_url)
    if state == 'outdated':
        need('ezylogin_outdated', 'EzyLogin is older than %s: update it first' % MIN_EZYLOGIN_VERSION)
    if state == 'disabled':
        need('admin_cli_login_disabled', 'open %s/ezylogin/settings/regular, tick "Allow admins to sign in from the command line (CLI)" and save' % admin_url)
    verifier = secrets.token_urlsafe(64)[:96]
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('ascii')).digest()).decode('ascii').rstrip('=')
    expected_state = secrets.token_urlsafe(24)
    result = {}
    done = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != '/callback':
                self.send_response(404)
                self.end_headers()
                return
            q = urllib.parse.parse_qs(parsed.query)
            ok = q.get('state', [''])[0] == expected_state and q.get('code')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            message = ('Signed in. You can close this tab and go back to your AI assistant.' if ok
                       else 'Sign in failed (state mismatch). Go back to your AI assistant and try again.')
            self.wfile.write(('<!doctype html><meta charset="utf-8"><title>EzyPlatform</title>'
                              '<body style="font-family:sans-serif;padding:40px">%s</body>' % message).encode('utf-8'))
            if ok:
                result['code'] = q['code'][0]
            else:
                result['error'] = 'state'
            done.set()

    server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
    redirect_uri = 'http://127.0.0.1:%d/callback' % server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    authorize_url = admin_url + '/ezylogin/cli/authorize?' + urllib.parse.urlencode({
        'client_name': CLIENT_NAME,
        'redirect_uri': redirect_uri,
        'state': expected_state,
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
    })
    print('OPEN_URL=' + authorize_url, flush=True)
    if not args.no_browser:
        opened = False
        try:
            opened = webbrowser.open(authorize_url)
        except Exception:
            opened = False
        print('BROWSER_OPENED=%s' % ('yes' if opened else 'no'), flush=True)
    print('WAITING: the user signs in to the admin if needed and clicks Approve (up to %d seconds)' % args.timeout, flush=True)
    finished = done.wait(args.timeout)
    server.shutdown()
    if not finished:
        die('no approval within %d seconds; run login again' % args.timeout)
    if result.get('error'):
        die('the callback did not match this login (state mismatch); run login again')
    res = call('POST', admin_url + CLI_TOKEN_API, body={
        'code': result['code'],
        'codeVerifier': verifier,
        'redirectUri': redirect_uri,
    })
    if res.status != 200:
        die('token exchange failed: HTTP %s %s' % (res.status, res.text()[:300]))
    data = res.json() or {}
    if not data.get('accessToken'):
        die('token exchange returned no token')
    st = load_state()
    st.setdefault('tokens', {})[admin_url] = {
        'accessToken': data['accessToken'],
        'expiredAt': data.get('accessTokenExpiredAt'),
        'savedAt': int(time.time() * 1000),
    }
    st['default_admin_url'] = admin_url
    save_state(st)
    expired = data.get('accessTokenExpiredAt')
    out('RESULT_LOGIN', 'ok')
    out('RESULT_TOKEN_FILE', STATE_FILE)
    if expired:
        out('RESULT_EXPIRES_AT', datetime.datetime.fromtimestamp(expired / 1000).isoformat(timespec='minutes'))


def cmd_logout(args):
    admin_url = resolve_admin_url(args, probe=False)
    st = load_state()
    entry = st.get('tokens', {}).pop(admin_url, None)
    save_state(st)
    out('RESULT_LOGOUT', 'removed' if entry else 'none')


def cmd_plugin_status(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    name = args.name
    st = project_status(admin_url, token, name)
    market = market_project(name)
    latest = (market or {}).get('latestVersion', {}) or {}
    out('name', name)
    if st.get('error') == 'forbidden':
        need('plugin_permission', 'this admin account cannot manage plugins: sign in with a super admin '
             '(or an admin with plugin management permission) or ask the user to do it in Modules')
    if st.get('error'):
        die('cannot read %s: %s' % (name, st['error']))
    out('installed', 'yes' if st['installed'] else 'no')
    if st['installed']:
        out('version', st['version'])
        out('module_types', ','.join(st['module_types']))
        out('active_types', ','.join(st['active_types']) or 'none')
    out('latest_version', latest.get('name') or 'unknown')
    out('market_module_types', ','.join((market or {}).get('includeModuleTypes') or []))
    price = (market or {}).get('price') or 0
    out('price', 'free' if not price else price)
    if not st['installed']:
        print('ACTION=install')
    elif latest.get('name') and version_tuple(st['version']) < version_tuple(latest['name']):
        print('ACTION=upgrade')
    elif set((market or {}).get('includeModuleTypes') or st['module_types']) - set(st['active_types']):
        print('ACTION=activate')
    else:
        print('ACTION=none')


def wait_admin(admin_url, seconds):
    start = time.time()
    time.sleep(5)
    while time.time() - start < seconds:
        res = call('GET', admin_url + '/', timeout=5)
        if res.status and res.status < 500:
            return True
        time.sleep(3)
    return False


DEPENDENCY_ERRORS = ('projectMissingDependencies', 'projectInactiveDependencies', 'projectNeedToUpdateDependencies')


def dependency_names(data):
    names = []
    if not isinstance(data, dict):
        return names
    for key in DEPENDENCY_ERRORS:
        for item in data.get(key) or []:
            name = item.get('projectName') if isinstance(item, dict) else item
            if name and name not in names:
                names.append(str(name))
    return names


def install_project(admin_url, token, name, args, version=None, chain=()):
    if name in chain:
        die('dependency loop: %s' % ' -> '.join(chain + (name,)))
    market = market_project(name)
    if not market:
        die('%s is not on the market %s' % (name, MARKET_URL))
    if (market.get('price') or 0) and not args.paid_ok:
        need('paid_plugin', '%s costs %s: ask the user first; buying happens on %s and the market account must be '
             'connected in the admin (Modules > Market), then run again with --paid-ok' % (name, market.get('price'), MARKET_URL))
    version = version or (market.get('latestVersion') or {}).get('name')
    if not version:
        die('cannot find the latest version of %s' % name)
    before = project_status(admin_url, token, name)
    if before.get('error') == 'forbidden':
        need('plugin_permission', 'this admin account cannot manage plugins: use a super admin account or guide the user (Modules > Market)')
    if before.get('installed') and version_tuple(before.get('version')) >= version_tuple(version) and not (args.force and not chain):
        out('RESULT_INSTALL_%s' % name, 'already_%s' % before.get('version'))
    else:
        print('INSTALLING %s %s from %s (this can take a minute)' % (name, version, MARKET_URL), flush=True)
        res = call('POST', admin_url + '/api/v1/projects/%s/%s/install?marketUrl=%s' % (
            urllib.parse.quote(name), urllib.parse.quote(version), urllib.parse.quote(MARKET_URL)),
            body=b'', token=token, timeout=600)
        if res.status == 403:
            need('plugin_permission', 'this admin account cannot install plugins: use a super admin account or guide the user (Modules > Market)')
        if res.status not in (200, 204):
            die('install %s failed: HTTP %s %s' % (name, res.status, res.text()[:300]))
        status_res = call('GET', admin_url + '/api/v1/projects/version-status', token=token)
        installed = [it for it in (status_res.json() or []) if it.get('projectName') == name]
        out('RESULT_INSTALL_%s' % name, ','.join('%s:%s' % (it.get('version'), it.get('status')) for it in installed) or 'unknown')
        if not any(it.get('version') == version for it in installed):
            die('the admin did not install %s %s; read the admin log or install it from Modules > Market' % (name, version))
    module_types = market.get('includeModuleTypes') or before.get('module_types') or []
    for attempt in range(6):
        body = {'moduleTypes': module_types, 'restart': False}
        print('ACTIVATING %s (%s)' % (name, ','.join(module_types)), flush=True)
        res = call('POST', admin_url + '/api/v1/projects/%s/activate' % urllib.parse.quote(name), body=body, token=token, timeout=120)
        if res.status in (0, 200, 204):
            return module_types
        deps = dependency_names(res.json()) if res.status == 403 else []
        if not deps:
            die('activate %s failed: HTTP %s %s' % (name, res.status, res.text()[:300]))
        print('DEPENDENCIES of %s: %s' % (name, ','.join(deps)), flush=True)
        for dep in deps:
            install_project(admin_url, token, dep, args, chain=chain + (name,))
    die('activate %s still fails after installing its dependencies' % name)


def cmd_plugin_install(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    install_project(admin_url, token, args.name, args, version=args.version)
    if args.no_restart:
        out('RESULT_RESTART_NEEDED', 'true')
        return
    print('RESTARTING admin and web (1-3 minutes)', flush=True)
    call('POST', admin_url + '/api/v1/projects/%s/activate' % urllib.parse.quote(args.name),
         body={'moduleTypes': (market_project(args.name) or {}).get('includeModuleTypes') or [], 'restart': True},
         token=token, timeout=120)
    if not wait_admin(admin_url, args.timeout):
        die('the admin did not come back within %d seconds; read the admin log' % args.timeout)
    after = project_status(admin_url, require_token(admin_url), args.name)
    out('RESULT_VERSION', after.get('version'))
    out('RESULT_ACTIVE_TYPES', ','.join(after.get('active_types') or []) or 'none')


def read_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def cmd_open(args):
    admin_url = resolve_admin_url(args)
    url = admin_url + (args.path or '/')
    out('OPEN_URL', url)
    try:
        opened = webbrowser.open(url)
    except Exception:
        opened = False
    out('BROWSER_OPENED', 'yes' if opened else 'no')


def home_label(info):
    if not info:
        return 'none'
    return '%s (%s%s)' % (info['dir'], info['mode'], ', project ' + info['project'] if info['mode'] == 'docker' else '')


def compose_cmd(info):
    base = ['docker', 'compose'] if subprocess.run(['docker', 'compose', 'version'], stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL).returncode == 0 else ['docker-compose']
    cmd = base + ['-p', info['project'], '-f', os.path.join(info['dir'], 'docker-compose.yml')]
    env_file = os.path.join(info['dir'], '.env')
    if os.path.isfile(env_file):
        cmd += ['--env-file', env_file]
    return cmd


def run_cli(info, command):
    if info['mode'] == 'docker':
        cmd = compose_cmd(info) + ['exec', '-T', '-w', '/app/ezyplatform', 'ezyplatform', 'bash', 'cli.sh', command]
        print('RUN docker cli %s' % command, flush=True)
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
        return proc.returncode, proc.stdout.decode('utf-8', errors='replace')
    home = info['dir']
    if os.name == 'nt':
        cmd = ['cmd', '/c', 'cli.bat', command]
    else:
        cmd = ['sh', 'cli.sh', command]
    env = dict(os.environ)
    java_home = env.get('JAVA_HOME')
    if not java_home or not os.path.exists(os.path.join(java_home, 'bin')):
        jdk_root = os.path.join(os.path.dirname(home), 'jdk')
        if os.path.isdir(jdk_root):
            for root, dirs, files in os.walk(jdk_root):
                if os.path.basename(root) == 'bin' and ('java' in files or 'java.exe' in files):
                    java_home = os.path.dirname(root)
                    break
    if java_home:
        env['JAVA_HOME'] = java_home
        env['PATH'] = os.path.join(java_home, 'bin') + os.pathsep + env.get('PATH', '')
    if not shutil.which('java', path=env.get('PATH')):
        need('java', 'java 8 is not on PATH for %s: set JAVA_HOME (the ezyplatform-install skill ships a JDK in <install dir>/jdk)' % home)
    print('RUN cli %s' % command, flush=True)
    proc = subprocess.run(cmd, cwd=home, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    return proc.returncode, proc.stdout.decode('utf-8', errors='replace')


MODULE_FOLDERS = {
    'admin-plugin': ('admin', 'plugins'),
    'web-plugin': ('web', 'plugins'),
    'socket-plugin': ('socket', 'plugins'),
    'theme': ('web', 'themes'),
}


def installed_types(info, name):
    if info['mode'] == 'docker':
        script = ' '.join('[ -f /app/ezyplatform/%s/%s/%s/module.properties ] && echo %s;' % (a, b, name, t)
                          for t, (a, b) in MODULE_FOLDERS.items())
        proc = subprocess.run(compose_cmd(info) + ['exec', '-T', 'ezyplatform', 'sh', '-c', script + ' true'],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return [t for t in proc.stdout.decode('utf-8', errors='replace').split() if t in MODULE_FOLDERS]
    return [t for t, (a, b) in MODULE_FOLDERS.items()
            if os.path.isfile(os.path.join(info['dir'], a, b, name, 'module.properties'))]


def cmd_local_install(args):
    admin_url = resolve_admin_url(args, probe=False)
    info = find_local_home(args, admin_url)
    if not info:
        need('local_home', 'no EzyPlatform installation on this computer answers on %s: pass --home <install folder>, '
             'or install from Modules > Market in the admin' % admin_url)
    name = args.name
    out('home', home_label(info))
    if args.update and installed_types(info, name):
        code, text = run_cli(info, 'update-modules %s' % name)
        print(text[-1500:])
        code, text = run_cli(info, 'run-update')
        print(text[-1500:])
    elif not installed_types(info, name):
        code, text = run_cli(info, 'install %s' % name)
        print(text[-1500:])
    types = installed_types(info, name)
    if not types:
        die('%s is not installed in %s' % (name, info['dir']))
    for t in types:
        code, text = run_cli(info, 'activate %s %s' % (t, name))
        print(text[-600:])
    out('RESULT_INSTALLED_TYPES', ','.join(types))
    out('RESULT_RESTART_NEEDED', 'true')


def cmd_local_restart(args):
    admin_url = resolve_admin_url(args, probe=False)
    info = find_local_home(args, admin_url)
    if not info:
        need('local_home', 'no EzyPlatform installation on this computer answers on %s: pass --home <install folder>' % admin_url)
    if info['mode'] == 'docker':
        subprocess.run(compose_cmd(info) + ['restart', 'ezyplatform'])
    else:
        ctl_name = 'ezyplatform-ctl.sh' if os.name != 'nt' else 'ezyplatform-ctl.ps1'
        ctl = os.path.join(os.path.dirname(info['dir']), ctl_name)
        if os.path.isfile(ctl):
            if os.name == 'nt':
                subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ctl, 'stop'])
                subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ctl, 'start'])
            else:
                subprocess.run(['bash', ctl, 'stop'])
                subprocess.run(['bash', ctl, 'start'])
        else:
            for target in args.targets:
                code, text = run_cli(info, 'restart %s' % target)
                print(text[-600:])
    if not wait_admin(admin_url, args.timeout):
        die('admin %s did not answer within %d seconds; read the logs of the installation' % (admin_url, args.timeout))
    out('RESULT_ADMIN_URL', admin_url)


def web_url_of(admin_url, token):
    saved = load_state().get('web_urls', {}).get(admin_url)
    if saved:
        return saved
    res = call('GET', admin_url + '/api/v1/settings/web-url', token=token)
    url = res.text().strip().strip('"') if res.status == 200 else ''
    return url.rstrip('/') if url.startswith('http') else ''


def site_languages(admin_url, token):
    res = call('GET', admin_url + '/api/v1/settings', token=token)
    items = (res.json() or {}).get('items') or [] if res.status == 200 else []
    settings = {it.get('name'): it.get('value') for it in items if isinstance(it, dict)}
    default = settings.get('web_default_language') or ''
    langs = []
    raw = settings.get('web_languages')
    try:
        parsed = json.loads(raw) if isinstance(raw, str) else (raw or [])
        for it in parsed:
            code = it.get('code') if isinstance(it, dict) else it
            if code:
                langs.append(str(code))
    except (ValueError, TypeError):
        pass
    return default, langs


def cmd_check(args):
    admin_url = resolve_admin_url(args)
    out('admin_url', admin_url)
    res = call('GET', admin_url + '/', timeout=10)
    out('admin_http', res.status)
    if res.status == 0:
        local_home = find_local_home(args, admin_url) if is_local_url(admin_url) else None
        out('local_home', home_label(local_home))
        need('admin_down', 'admin does not answer: if EzyPlatform is on this computer start it '
             '(local-restart, or the ezyplatform-install skill), otherwise ask the user to check the address')
    login_state = probe_ezylogin(admin_url)
    out('ezylogin_cli_login', login_state)
    local_home = find_local_home(args, admin_url) if is_local_url(admin_url) else None
    out('local_home', home_label(local_home))
    token = get_token(admin_url)
    token_ok = False
    if token:
        me = call('GET', admin_url + '/api/v1/admins/me', token=token)
        token_ok = me.status == 200
        if token_ok:
            data = me.json() or {}
            out('admin_username', data.get('username') or data.get('displayName') or '?')
    out('token', 'valid' if token_ok else ('rejected' if token else 'none'))
    if token_ok and getattr(args, 'web_url', None):
        state = load_state()
        state.setdefault('web_urls', {})[admin_url] = normalize_url(args.web_url)
        save_state(state)
    if token_ok:
        web = web_url_of(admin_url, token)
        out('web_url', web or 'unknown')
        web_res = call('GET', web + '/', timeout=10) if web else HttpResult(0, b'')
        out('web_http', web_res.status)
        if not web_res.status:
            print('WARNING: the web URL saved in the admin does not answer from this computer (Docker port mapping, proxy '
                  'or a wrong Settings > Web URL): find the real address and run check --web-url <address>')
        default, langs = site_languages(admin_url, token)
        out('web_default_language', default or 'not set')
        out('web_languages', ','.join(langs) or 'not set (default language only)')
        st = project_status(admin_url, token, 'ezyarticle')
        if st.get('installed'):
            out('ezyarticle_version', st['version'])
            out('ezyarticle_active_types', ','.join(st['active_types']) or 'none')
        else:
            out('ezyarticle', st.get('error') or 'not_installed')
    if login_state == 'missing':
        need('ezylogin_missing', 'EzyLogin is not installed or not active on this admin: install and activate it '
             '(local-install ezylogin when local_home is set, otherwise guide the user), restart, then check again')
    if login_state == 'outdated':
        need('ezylogin_outdated', 'EzyLogin is older than %s and has no CLI login: update it, restart, then check again' % MIN_EZYLOGIN_VERSION)
    if login_state == 'disabled' and not token_ok:
        need('admin_cli_login_disabled', 'open %s/ezylogin/settings/regular, tick "Allow admins to sign in from the command line (CLI)" '
             'and save (only an admin with EzyLogin settings permission can do it)' % admin_url)
    if not token_ok:
        need('login', 'run the login command: the browser opens and the user approves the request')
    print('READY')


def cmd_plugins(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    names = list(args.names or [])
    if args.theme:
        names.insert(0, args.theme)
    names += list(CORE_PROJECTS)
    if args.lead:
        names += list(LEAD_PROJECTS)
    if args.shop:
        names += list(SHOP_PROJECTS)
        if args.delivery:
            names.append('ezydelivery')
    seen = []
    for n in names:
        if n not in seen:
            seen.append(n)
    todo = []
    for name in seen:
        st = project_status(admin_url, token, name)
        if st.get('error') == 'forbidden':
            need('plugin_permission', 'this admin account cannot read plugins: use a super admin account')
        market = market_project(name) or {}
        latest = (market.get('latestVersion') or {}).get('name') or 'unknown'
        price = market.get('price') or 0
        if not st.get('installed'):
            action = 'install'
        elif latest != 'unknown' and version_tuple(st['version']) < version_tuple(latest):
            action = 'upgrade'
        elif set(market.get('includeModuleTypes') or st['module_types']) - set(st['active_types']):
            action = 'activate'
        else:
            action = 'none'
        print('%s installed=%s version=%s latest=%s active=%s price=%s ACTION=%s' % (
            name, 'yes' if st.get('installed') else 'no', st.get('version') or '-', latest,
            ','.join(st.get('active_types') or []) or 'none', 'free' if not price else price, action))
        if action != 'none':
            todo.append(name)
    out('TODO', ','.join(todo) or 'none')


def read_file_or_empty(path):
    return read_file(path) if os.path.isfile(path) else ''


def read_meta(folder, lang=None):
    path = os.path.join(folder, 'meta.%s.json' % lang if lang else 'meta.json')
    if not os.path.isfile(path):
        return {}
    try:
        return json.loads(read_file(path) or '{}')
    except ValueError:
        die('%s is not valid JSON' % path)


def content_file(folder, lang=None):
    return os.path.join(folder, 'content.%s.html' % lang if lang else 'content.html')


def get_page(admin_url, token, slug, lang=None):
    q = '?i18n_lang=' + urllib.parse.quote(lang) if lang else ''
    res = call('GET', admin_url + '/ezyarticle/api/v1/post-by-slug/' + urllib.parse.quote(slug) + q, token=token)
    if res.status == 404:
        return None
    if res.status == 403:
        need('content_permission', 'this admin account cannot manage EzyArticle posts: use an admin with post permissions')
    if res.status != 200:
        die('cannot read page %s: HTTP %s %s' % (slug, res.status, res.text()[:300]))
    return res.json() or {}


def page_langs(folder):
    langs = []
    for name in sorted(os.listdir(folder)):
        if name.startswith('content.') and name.endswith('.html') and name.count('.') == 2:
            langs.append(name.split('.')[1])
    return langs


def cmd_page_pull(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    folder = args.dir or os.path.join('landing-pages', args.slug)
    page = get_page(admin_url, token, args.slug, args.lang)
    if page is None:
        out('RESULT_PAGE', 'not_found')
        return
    target = content_file(folder, args.lang)
    content = page.get('content') or ''
    if os.path.exists(target) and not args.force and read_file(target).strip() != content.strip():
        die('%s exists and differs from the server; use --force to overwrite it' % target)
    write_file(target, content)
    if not args.lang:
        meta = read_meta(folder)
        for key in ('title', 'summary', 'postType', 'contentType', 'status'):
            if page.get(key) is not None:
                meta['pageType' if key == 'postType' else key] = page.get(key)
        meta['slug'] = args.slug
        write_file(os.path.join(folder, 'meta.json'), json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    out('RESULT_PAGE', 'pulled')
    out('RESULT_FILE', os.path.abspath(target))
    out('RESULT_STATUS', page.get('status'))


def backup_page(admin_url, token, folder, slug, langs):
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    target = os.path.join(folder, '.backups', stamp)
    saved = False
    for lang in [None] + langs:
        page = get_page(admin_url, token, slug, lang)
        if page is None:
            continue
        name = 'page.%s.json' % lang if lang else 'page.json'
        write_file(os.path.join(target, name), json.dumps(page, ensure_ascii=False, indent=2))
        saved = True
    return target if saved else ''


def build_body(folder, meta, slug, lang):
    localized = read_meta(folder, lang) if lang else {}
    content = read_file_or_empty(content_file(folder, lang)) or read_file_or_empty(content_file(folder))
    body = {
        'slug': slug,
        'postType': meta.get('pageType') or 'STANDALONE_PAGE',
        'title': localized.get('title', meta.get('title')) or slug,
        'summary': localized.get('summary', meta.get('summary')) or '',
        'content': content,
        'additionalHead': '',
        'additionalFoot': '',
        'contentType': meta.get('contentType') or 'HTML',
        'status': meta.get('status') or 'DRAFT',
    }
    if meta.get('featuredImageName'):
        body['featuredImageName'] = meta['featuredImageName']
    if lang:
        body['language'] = lang
    return body


def cmd_page_push(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    folder = args.dir
    meta = read_meta(folder)
    slug = meta.get('slug') or os.path.basename(os.path.abspath(folder))
    if not os.path.isfile(content_file(folder)):
        die('%s is missing' % content_file(folder))
    if meta.get('pageType', 'STANDALONE_PAGE') != 'STANDALONE_PAGE':
        print('WARNING: pageType is %s, not STANDALONE_PAGE' % meta.get('pageType'))
    if args.publish:
        meta = dict(meta, status='PUBLISHED')
    langs = page_langs(folder) if not args.lang else [args.lang]
    plan = [None] + [l for l in langs if l] if not args.lang else langs
    existing = get_page(admin_url, token, slug)
    out('slug', slug)
    out('server_page', 'exists id=%s status=%s' % (existing.get('id'), existing.get('status')) if existing else 'new')
    out('languages', ','.join(l or 'default' for l in plan))
    out('status', meta.get('status') or 'DRAFT')
    if not args.yes:
        print('DRY_RUN: nothing was saved; show this plan to the user and run again with --yes after they agree')
        return
    saved = backup_page(admin_url, token, folder, slug, [l for l in plan if l]) if existing else ''
    for lang in plan:
        body = build_body(folder, meta, slug, lang)
        publish = body['status'] == 'PUBLISHED'
        res = call('POST', admin_url + SAVE_SIMPLY_API + ('?publish=true' if publish else ''), body=body, token=token, timeout=120)
        if res.status == 403:
            need('content_permission', 'this admin account cannot save EzyArticle posts')
        if res.status not in (200, 204):
            die('save %s failed: HTTP %s %s' % (lang or 'default', res.status, res.text()[:400]))
        data = res.json() or {}
        out('RESULT_SAVED_%s' % (lang or 'default'), 'id=%s status=%s' % (data.get('id'), data.get('status')))
    after = get_page(admin_url, token, slug)
    if after is None or (after.get('content') or '').strip() != read_file(content_file(folder)).strip():
        print('WARNING: the default content read back differs from content.html (a published page may keep a pending revision until published)')
    out('RESULT_BACKUP', saved or 'none (new page)')
    web = web_url_of(admin_url, token)
    if web:
        out('RESULT_URL', web + '/' + slug)
    out('RESULT_PREVIEW', admin_url + '/ezyarticle/pages/%s/preview' % urllib.parse.quote(slug))


def cmd_page_restore(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    folder = args.dir
    root = os.path.join(folder, '.backups')
    source = args.backup
    if not source:
        items = sorted(os.listdir(root)) if os.path.isdir(root) else []
        if not items:
            die('no backup in %s' % root)
        source = os.path.join(root, items[-1])
    files = sorted(f for f in os.listdir(source) if f.startswith('page') and f.endswith('.json'))
    if not args.yes:
        out('restore_from', os.path.abspath(source))
        out('files', ','.join(files))
        print('DRY_RUN: run again with --yes after the user agrees')
        return
    for name in files:
        page = json.loads(read_file(os.path.join(source, name)))
        lang = name[len('page.'):-len('.json')] if name != 'page.json' else None
        body = {
            'slug': page.get('slug'),
            'postType': page.get('postType') or 'STANDALONE_PAGE',
            'title': page.get('title') or '',
            'summary': page.get('summary') or '',
            'content': page.get('content') or '',
            'additionalHead': page.get('additionalHead') or '',
            'additionalFoot': page.get('additionalFoot') or '',
            'contentType': page.get('contentType') or 'HTML',
            'status': page.get('status') or 'DRAFT',
        }
        if lang:
            body['language'] = lang
        publish = body['status'] == 'PUBLISHED'
        res = call('POST', admin_url + SAVE_SIMPLY_API + ('?publish=true' if publish else ''), body=body, token=token, timeout=120)
        if res.status not in (200, 204):
            die('restore %s failed: HTTP %s %s' % (name, res.status, res.text()[:300]))
        out('RESULT_RESTORED', name)


def upload_multipart(url, token, file_name, data):
    boundary = '----EzyLanding' + secrets.token_hex(12)
    mime = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
    head = ('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\n'
            'Content-Type: %s\r\n\r\n' % (boundary, file_name, mime)).encode('utf-8')
    body = head + data + ('\r\n--%s--\r\n' % boundary).encode('utf-8')
    return call('POST', url, body=body, token=token, timeout=300, content_type='multipart/form-data; boundary=' + boundary)


def cmd_media_upload(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    for path in args.files:
        if not os.path.isfile(path):
            die('%s does not exist' % path)
        name = os.path.basename(path)
        if any(ch.isspace() for ch in name) or any(ord(ch) > 127 for ch in name):
            die('%s: use an English file name without accents or spaces (for example brand-logo.svg)' % name)
        res = call('GET', admin_url + '/api/v1/media/%s/contains' % urllib.parse.quote(name), token=token)
        exists = res.status == 200 and (res.json() or {}).get('contains')
        if exists and not args.replace:
            out('media ' + name, 'exists (use --replace to overwrite)')
            continue
        with open(path, 'rb') as f:
            data = f.read()
        url = admin_url + ('/api/v1/media/%s/replace-by-name' % urllib.parse.quote(name) if exists else '/api/v1/media/add?notPublic=false')
        res = upload_multipart(url, token, name, data)
        if res.status not in (200, 204):
            die('upload %s failed: HTTP %s %s' % (name, res.status, res.text()[:300]))
        info = res.json() if res.status == 200 else None
        final = (info or {}).get('name') if isinstance(info, dict) else None
        out('media ' + name, '%s url=/api/v1/media/%s?v=%d' % ('replaced' if exists else 'added', final or name, int(time.time())))


def cmd_web_check(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    web = web_url_of(admin_url, token)
    if not web:
        die('cannot read the web URL of the site')
    failed = False
    for path in args.path or ['/']:
        res = call('GET', web + path, timeout=30)
        html = res.text() if res.status == 200 else ''
        location = res.headers.get('Location') or res.headers.get('location') or ''
        problems = []
        if res.status != 200:
            problems.append('http_%s%s' % (res.status, (' -> ' + location) if location else ''))
        for marker in ('ezy:replace', 'ezy:block', 'th:text', '#{', '${'):
            if marker in html:
                problems.append('unrendered %s' % marker)
        for text in args.expect or []:
            if text not in html:
                problems.append('missing "%s"' % text)
        out('page ' + path, 'ok' if not problems else '; '.join(problems))
        failed = failed or bool(problems)
    if failed:
        sys.exit(1)


def cmd_link_check(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    web = web_url_of(admin_url, token)
    if not web:
        die('cannot read the web URL of the site')
    failed = False
    for link in args.links:
        url = link if link.startswith('http') else web + link
        res = call('GET', url, timeout=30)
        location = res.headers.get('Location') or res.headers.get('location') or ''
        if res.status in (301, 302, 303, 307, 308):
            ok = 'shopping-cart' in location or 'login' in location
            state = 'redirect %s -> %s' % (res.status, location)
        else:
            ok = res.status == 200 and 'not found' not in res.text().lower()[:5000]
            state = 'http_%s' % res.status
        out('link ' + link, ('ok ' if ok else 'CHECK ') + state)
        failed = failed or not ok
    if failed:
        sys.exit(1)


def cmd_contact_test(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    web = web_url_of(admin_url, token)
    if not web:
        die('cannot read the web URL of the site')
    body = {
        'contactUsYourName': args.name,
        'contactUsYourEmail': args.email,
        'contactUsSubject': args.subject,
        'contactUsMessage': args.message,
    }
    for item in args.field or []:
        key, _, value = item.partition('=')
        body[key] = value
    if not args.yes:
        out('post_to', web + '/api/v1/contact-us')
        out('body_keys', ','.join(body.keys()))
        print('DRY_RUN: this sends a real request and real mail; run again with --yes after the user agrees')
        return
    res = call('POST', web + '/api/v1/contact-us', body=body, timeout=60)
    out('RESULT_HTTP', res.status)
    if res.status == 404:
        need('contact_disabled', 'Contact Us is off: tick "Allow contact" in %s/ezysupport/settings and save' % admin_url)
    data = res.json()
    if res.status != 204 or (isinstance(data, dict) and data):
        out('RESULT_ERRORS', json.dumps(data, ensure_ascii=False))
        if isinstance(data, dict) and data.get('captchaToken'):
            print('NOTE: captcha is on for this API; test the form in a browser instead')
        sys.exit(1)
    out('RESULT_CONTACT', 'sent')
    print('NEXT: check %s/ezysupport/contact-us and the inbox of %s' % (admin_url, args.email))


def cmd_site_url(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    res = call('GET', admin_url + '/api/v1/settings/current-server-urls', token=token)
    current = res.json() if res.status == 200 else {}
    current = current if isinstance(current, dict) else {}
    old_web = call('GET', admin_url + '/api/v1/settings/web-url', token=token).text().strip()
    web = normalize_url(args.web) if args.web else None
    admin = normalize_url(args.admin) if args.admin else None
    out('web_url_now', old_web or 'none')
    out('server_web_url_kept', current.get('webUrl') or 'none')
    if web:
        out('web_url_new', web)
    if admin:
        out('admin_url_kept_server', current.get('adminUrl') or 'none')
        out('admin_url_new', admin)
    if not web and not admin:
        return
    if not args.yes:
        print('DRY_RUN: run again with --yes after the user agrees')
        return
    if web:
        res = call('PUT', admin_url + '/api/v1/settings/set-web-urls',
                   body={'webUrl': web, 'currentServerWebUrl': current.get('webUrl') or ''}, token=token)
        if res.status not in (200, 204):
            die('set web URL failed: HTTP %s %s' % (res.status, res.text()[:300]))
        state = load_state()
        state.get('web_urls', {}).pop(admin_url, None)
        save_state(state)
        out('RESULT_WEB_URL', web)
    if admin:
        res = call('PUT', admin_url + '/api/v1/settings/set-admin-url',
                   body={'adminUrl': admin, 'currentServerAdminUrl': current.get('adminUrl') or ''}, token=token)
        if res.status not in (200, 204):
            die('set admin URL failed: HTTP %s %s' % (res.status, res.text()[:300]))
        out('RESULT_ADMIN_URL', admin)


CRM_APPENDER = 'ezysupport_contact_us_user'


def cmd_crm_start(args):
    admin_url = resolve_admin_url(args)
    token = require_token(admin_url)
    res = call('PUT', admin_url + '/api/v1/settings/data-appenders/%s/%s' % (CRM_APPENDER, args.action), body={}, token=token)
    if res.status == 403:
        need('settings_permission', 'this admin account cannot manage background jobs: use a super admin account')
    if res.status == 404:
        need('ezysupport_missing', 'EzySupport is not installed or too old: plugins --lead, then plugin-install ezysupport')
    if res.status not in (200, 204):
        die('%s %s failed: HTTP %s %s' % (args.action, CRM_APPENDER, res.status, res.text()[:300]))
    out('RESULT_CRM_USER_CREATOR', args.action + 'ed' if args.action != 'stop' else 'stopped')


def main():
    parser = argparse.ArgumentParser(prog='ezylanding.py', description='Build a landing page on an EzyPlatform site')
    parser.add_argument('--version', action='version', version=VERSION)
    sub = parser.add_subparsers(dest='command')

    def add(name, func, help_text):
        p = sub.add_parser(name, help=help_text)
        p.add_argument('--admin-url', help='admin address, for example http://localhost:9090')
        p.set_defaults(func=func)
        return p

    p = add('check', cmd_check, 'check the admin, EzyLogin CLI login, the saved token, web URL, languages, EzyArticle')
    p.add_argument('--home')
    p.add_argument('--web-url', help='public site address when the one saved in the admin does not answer from here')
    p = add('login', cmd_login, 'sign in through EzyLogin CLI login (browser approval)')
    p.add_argument('--timeout', type=int, default=600)
    p.add_argument('--no-browser', action='store_true')
    add('logout', cmd_logout, 'forget the saved token of this admin')
    p = add('plugins', cmd_plugins, 'status of the theme and plugins a landing page needs')
    p.add_argument('names', nargs='*')
    p.add_argument('--theme', default='freestyle')
    p.add_argument('--lead', action='store_true', help='contact form: EzySupport + EzyMail')
    p.add_argument('--shop', action='store_true', help='product links: E-Commerce + GraphQL + EzyLogin + EzyPayment')
    p.add_argument('--delivery', action='store_true', help='with --shop: physical goods, add EzyDelivery')
    p = add('plugin-status', cmd_plugin_status, 'installed and latest version of a plugin or theme')
    p.add_argument('name')
    p = add('plugin-install', cmd_plugin_install, 'install or upgrade a plugin or theme from the market, activate and restart')
    p.add_argument('name')
    p.add_argument('--version')
    p.add_argument('--no-restart', action='store_true')
    p.add_argument('--force', action='store_true')
    p.add_argument('--paid-ok', action='store_true')
    p.add_argument('--timeout', type=int, default=420)
    p = add('page-pull', cmd_page_pull, 'download a page from the server into a local folder')
    p.add_argument('slug')
    p.add_argument('--dir')
    p.add_argument('--lang')
    p.add_argument('--force', action='store_true')
    p = add('page-push', cmd_page_push, 'create or update the page of --dir (dry run without --yes)')
    p.add_argument('--dir', required=True)
    p.add_argument('--lang')
    p.add_argument('--publish', action='store_true')
    p.add_argument('--yes', action='store_true')
    p = add('page-restore', cmd_page_restore, 'save a page backup again (latest by default)')
    p.add_argument('--dir', required=True)
    p.add_argument('--backup')
    p.add_argument('--yes', action='store_true')
    p = add('media-upload', cmd_media_upload, 'upload images/files to the media library')
    p.add_argument('files', nargs='+')
    p.add_argument('--replace', action='store_true')
    p = add('web-check', cmd_web_check, 'load public pages and look for errors and expected texts')
    p.add_argument('--path', action='append')
    p.add_argument('--expect', action='append')
    p = add('link-check', cmd_link_check, 'open buy-now / checkout links without following redirects')
    p.add_argument('links', nargs='+')
    p = add('contact-test', cmd_contact_test, 'send one real Contact Us request (dry run without --yes)')
    p.add_argument('--email', required=True)
    p.add_argument('--name', default='Landing page test')
    p.add_argument('--subject', default='Landing page test')
    p.add_argument('--message', default='Test message from the landing page skill.')
    p.add_argument('--field', action='append', help='extra metadata key=value')
    p.add_argument('--yes', action='store_true')
    p = add('site-url', cmd_site_url, 'show or set the public web URL (and admin URL) saved in the admin (dry run without --yes)')
    p.add_argument('--web', help='public site address, for example https://example.com')
    p.add_argument('--admin', help='public admin address, for example https://admin.example.com')
    p.add_argument('--yes', action='store_true')
    p = add('crm-start', cmd_crm_start, 'start the EzySupport "Contact Us user creator" job (every lead becomes a user)')
    p.add_argument('--action', choices=['start', 'restart', 'stop'], default='start')
    p = add('open', cmd_open, 'open an admin page in the default browser')
    p.add_argument('--path')
    p = add('local-install', cmd_local_install, 'install/update and activate a plugin in a local EzyPlatform folder with cli.sh')
    p.add_argument('name')
    p.add_argument('--home')
    p.add_argument('--update', action='store_true')
    p = add('local-restart', cmd_local_restart, 'restart a local EzyPlatform and wait for the admin')
    p.add_argument('--home')
    p.add_argument('--targets', nargs='+', default=['admin', 'web'])
    p.add_argument('--timeout', type=int, default=420)
    args = parser.parse_args()
    if not getattr(args, 'func', None):
        parser.print_help()
        sys.exit(2)
    args.func(args)


if __name__ == '__main__':
    main()
