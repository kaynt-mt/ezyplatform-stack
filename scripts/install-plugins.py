#!/usr/bin/env python3
import argparse
import http.cookiejar
import json
import re
import subprocess
import time
from graphlib import TopologicalSorter
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPCookieProcessor, HTTPRedirectHandler, ProxyHandler, Request, build_opener, urlopen


ROOT = Path(__file__).resolve().parents[1]
CORE = "1.5.9"
MARKET = "https://ezyplatform.com"
COMPOSE = ["docker", "compose"]
CONTAINER = [*COMPOSE, "exec", "-T", "ezyplatform"]
FOLDERS = {
    "admin-plugin": "admin/plugins",
    "web-plugin": "web/plugins",
    "socket-plugin": "socket/plugins",
    "socket-app": "socket/apps",
    "theme": "web/themes",
}
THEME_CACHE = ".runtime/web/themes.txt"
BROWSER_AUTH_MARKER = "ezyplatform-stack-browser-auth-v1"
BROWSER_AUTH_SLUGS = ("login", "register")

BROWSER_AUTH_STYLE = """
<style>
.stack-auth-fixture{max-width:28rem;margin:3rem auto;padding:1.5rem;border:1px solid #d7dce2;border-radius:.5rem;background:#fff;color:#17202a;font-family:system-ui,sans-serif}
.stack-auth-fixture h1{margin-top:0;font-size:1.6rem}
.stack-auth-fixture label{display:block;margin:.85rem 0 .25rem;font-weight:600}
.stack-auth-fixture input{box-sizing:border-box;width:100%;padding:.55rem;border:1px solid #aeb7c2;border-radius:.3rem}
.stack-auth-fixture button{width:100%;margin-top:1rem;padding:.65rem;border:0;border-radius:.3rem;background:#1769aa;color:#fff;font-weight:700;cursor:pointer}
.stack-auth-fixture button:disabled{opacity:.6;cursor:wait}
.stack-auth-fixture .stack-auth-status{min-height:1.5rem;margin-top:1rem;padding:.65rem;border-radius:.3rem;background:#f2f5f7;white-space:pre-wrap}
.stack-auth-fixture .stack-auth-status[data-result="success"]{background:#e6f4ea;color:#146c2e}
.stack-auth-fixture .stack-auth-status[data-result="error"]{background:#fce8e6;color:#a50e0e}
</style>
"""

BROWSER_AUTH_SCRIPT = """
<script>
(function () {
  function submitAuth(form, endpoint, status, successPrefix) {
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      button.disabled = true;
      status.dataset.result = '';
      status.textContent = 'Sending...';
      const payload = {};
      new FormData(form).forEach(function (value, key) {
        if (value) {
          payload[key] = value.toString();
        }
      });
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          credentials: 'same-origin',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const text = await response.text();
        let data = {};
        if (text) {
          try {
            data = JSON.parse(text);
          } catch (parseError) {
            data = {message: text};
          }
        }
        if (!response.ok) {
          throw new Error(data.message || data.error || JSON.stringify(data) || ('HTTP ' + response.status));
        }
        status.dataset.result = 'success';
        status.textContent = successPrefix + ' Access token status: ' + (data.accessTokenStatus || 'unknown') + '.';
        form.reset();
      } catch (error) {
        status.dataset.result = 'error';
        status.textContent = error.message;
      } finally {
        button.disabled = false;
      }
    });
  }

  const loginForm = document.getElementById('stack-login-form');
  if (loginForm) {
    submitAuth(loginForm, '/ezylogin/api/v1/login', document.getElementById('stack-login-status'), 'Signed in.');
  }
  const registerForm = document.getElementById('stack-register-form');
  if (registerForm) {
    submitAuth(registerForm, '/ezylogin/api/v1/register', document.getElementById('stack-register-status'), 'Account created and signed in.');
  }
}());
</script>
"""

BROWSER_AUTH_LOGIN_CONTENT = BROWSER_AUTH_STYLE + """
<div class="stack-auth-fixture" data-stack-auth-page="login">
  <h1>Log in</h1>
  <form id="stack-login-form">
    <label for="stack-login-username">Username or email</label>
    <input id="stack-login-username" name="username" autocomplete="username" required>
    <label for="stack-login-password">Password</label>
    <input id="stack-login-password" name="password" type="password" autocomplete="current-password" required>
    <button type="submit">Log in</button>
  </form>
  <div id="stack-login-status" class="stack-auth-status" data-testid="login-status" aria-live="polite"></div>
  <p>No account yet? <a href="/register">Create one</a>.</p>
</div>
""" + BROWSER_AUTH_SCRIPT

BROWSER_AUTH_REGISTER_CONTENT = BROWSER_AUTH_STYLE + """
<div class="stack-auth-fixture" data-stack-auth-page="register">
  <h1>Create an account</h1>
  <form id="stack-register-form">
    <label for="stack-register-display-name">Display name</label>
    <input id="stack-register-display-name" name="displayName" autocomplete="name" required>
    <label for="stack-register-email">Email</label>
    <input id="stack-register-email" name="email" type="email" autocomplete="email" required>
    <label for="stack-register-username">Username</label>
    <input id="stack-register-username" name="username" autocomplete="username" required>
    <label for="stack-register-password">Password</label>
    <input id="stack-register-password" name="password" type="password" autocomplete="new-password" required>
    <button type="submit">Create account</button>
  </form>
  <div id="stack-register-status" class="stack-auth-status" data-testid="register-status" aria-live="polite"></div>
  <p>Already registered? <a href="/login">Log in</a>.</p>
</div>
""" + BROWSER_AUTH_SCRIPT

BROWSER_AUTH_PAGES = {
    "login": ("Log in", BROWSER_AUTH_LOGIN_CONTENT),
    "register": ("Create an account", BROWSER_AUTH_REGISTER_CONTENT),
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, **kwargs).stdout


def read_files(paths):
    output = run([*CONTAINER, "bash", "-c",
                  'for f; do if [[ -f "$f" ]]; then printf "\\n@@ %s\\n" "$f"; cat "$f"; fi; done',
                  "bash", *paths], capture_output=True)
    return dict(re.findall(r"^@@ ([^\n]+)\n(.*?)(?=^@@ |\Z)", output, re.M | re.S))


def properties(content):
    return dict(line.split("=", 1) for line in content.splitlines()
                if "=" in line and not line.lstrip().startswith("#"))


def modules(name):
    paths = {f"{folder}/{name}/module.properties": kind for kind, folder in FOLDERS.items()}
    return {paths[path]: properties(content) for path, content in read_files(paths).items()}


def active_modules():
    paths = {f".runtime/{folder}.txt": kind for kind, folder in FOLDERS.items()}
    active = {kind: set() for kind in FOLDERS}
    for path, content in read_files(paths).items():
        active[paths[path]] = {item["name"] for item in json.loads(content) if item.get("active") is True}
    return active


def check_release(name, version):
    url = f"{MARKET}/api/v1/released-projects/{name}/latest/download?platformVersion={CORE}"
    with urlopen(Request(url, method="HEAD"), timeout=30) as response:
        filename = response.headers.get_filename()
        if response.headers.get_content_type() != "application/zip" or filename != f"{name}-{version}.zip":
            raise ValueError(f"{name}: marketplace release changed; expected {name}-{version}.zip, got {filename!r}")


def install_from_admin(opener, admin, name, release):
    request = Request(f"{admin}/api/v1/projects/{name}/{release}/install", method="POST")
    with opener.open(request, timeout=600) as response:
        if response.status != 204:
            raise ValueError(f"{name}: expected HTTP 204 from admin installer, got {response.status}")


def install(name, release, version, kinds, admin, opener):
    installed = modules(name)
    if not installed:
        if opener is not None:
            install_from_admin(opener, admin, name, release)
        else:
            check_release(name, release)
            run([*CONTAINER, "bash", "cli.sh", f"install {name}"], timeout=600)
        installed = modules(name)
    if set(installed) != set(kinds) or any(meta.get("version") != version for meta in installed.values()):
        found = {kind: meta.get("version") for kind, meta in installed.items()}
        raise ValueError(f"{name}: expected {version} for {', '.join(kinds)}, found {found}")
    return {dep.strip() for meta in installed.values() for dep in meta.get("dependencies", "").split(",") if dep.strip()}


def clear_stale_themes(names):
    paths = {f"web/themes/{name}/module.properties": name for name in names}
    stale = names - {paths[path] for path in read_files(paths)}
    if not stale:
        return stale
    entries = json.loads(read_files([THEME_CACHE])[THEME_CACHE])
    for entry in entries:
        if entry["name"] in stale:
            entry["active"] = False
    run([*CONTAINER, "bash", "-ec",
         """temp=$(mktemp "$1.XXXXXX")
trap 'rm -f "$temp"' EXIT
cat > "$temp"
chmod --reference="$1" "$temp"
mv -f "$temp" "$1" """, "bash", THEME_CACHE], input=json.dumps(entries))
    return stale


def activate(manifest, order, theme):
    before = active_modules()
    other_themes = before["theme"] - {theme} if theme else set()
    stale = clear_stale_themes(other_themes) if other_themes else set()
    deactivate = [("theme", name) for name in sorted(other_themes - stale)]
    required = [(kind, name) for name in order for kind in manifest[name][2] if kind != "theme"]
    if theme:
        required.append(("theme", theme))
    commands = [f"deactivate {kind} {name}" for kind, name in deactivate]
    commands += [f"activate {kind} {name}" for kind, name in required if name not in before[kind]]
    if not commands and not stale:
        return
    if commands:
        run([*CONTAINER, "bash", "cli.sh"], input="\n".join([*commands, "exit", ""]),
            capture_output=True, timeout=120)
    after = active_modules()
    missing = [f"{name}/{kind}" for kind, name in required if name not in after[kind]]
    if missing or (theme and after["theme"] != {theme}):
        raise ValueError(f"activation failed: missing={missing}, active themes={sorted(after['theme'])}")
    print(f"Applied {len(commands) + len(stale)} activation changes", flush=True)


def endpoint(port, path):
    binding = run([*COMPOSE, "port", "ezyplatform", str(port)], capture_output=True).strip()
    if not re.fullmatch(r"127\.0\.0\.1:[0-9]+", binding):
        raise ValueError(f"expected a local loopback binding for container port {port}")
    return f"http://{binding}{path}"


def wait_for_http(urls):
    deadline = time.monotonic() + 180
    pending = set(urls)
    while pending and time.monotonic() < deadline:
        for url in sorted(pending):
            try:
                with urlopen(url, timeout=5) as response:
                    if 200 <= response.status < 400:
                        pending.remove(url)
            except OSError:
                pass
        if pending:
            time.sleep(2)
    if pending:
        raise ValueError(f"not ready: {', '.join(sorted(pending))}; inspect docker compose logs ezyplatform")


def mysql_bytes(value):
    return "X'" + value.encode("utf-8").hex() + "'"


def mysql_text(value):
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def mysql_exec(sql):
    run([*COMPOSE, "exec", "-T", "mysql", "bash", "-lc", 'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"'],
        input=sql, capture_output=True, timeout=60)


def mysql_query(sql):
    return run([*COMPOSE, "exec", "-T", "mysql", "bash", "-lc", 'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -Nse "$1"', "bash", sql],
               capture_output=True, timeout=60).rstrip("\r\n")


def validate_browser_auth_rows(rows):
    for slug, post_type, marker in rows:
        if slug.lower() in BROWSER_AUTH_SLUGS and marker != BROWSER_AUTH_MARKER:
            kind = post_type or "unknown"
            raise ValueError(f"/{slug} already exists as EzyArticle {kind}; move it aside before installing the browser auth fixture")


def browser_auth_rows():
    slugs = ",".join(mysql_text(slug) for slug in BROWSER_AUTH_SLUGS)
    output = mysql_query(
        "SELECT p.slug,p.post_type,COALESCE(m.meta_value,'') "
        "FROM ezyarticle_posts p "
        "LEFT JOIN ezyarticle_post_meta m ON m.post_id=p.id AND m.meta_key='stack_fixture' "
        f"WHERE p.slug IN ({slugs})"
    )
    rows = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def browser_auth_sql():
    statements = []
    for slug in BROWSER_AUTH_SLUGS:
        title, content = BROWSER_AUTH_PAGES[slug]
        slug_sql = mysql_text(slug)
        statements.append(
            "INSERT INTO ezyarticle_posts "
            "(author_admin_id,author_user_id,post_type,title,content,content_type,status,comment_status,priority,featured_image_id,parent_id,comment_count,slug,created_at,updated_at,published_at) "
            f"VALUES (0,0,'PAGE',{mysql_bytes(title)},{mysql_bytes(content)},'HTML','PUBLISHED','CLOSE',0,0,0,0,{slug_sql},NOW(),NOW(),NOW()) "
            f"ON DUPLICATE KEY UPDATE post_type='PAGE',title={mysql_bytes(title)},content={mysql_bytes(content)},content_type='HTML',status='PUBLISHED',updated_at=NOW(),published_at=COALESCE(published_at,NOW());\n"
            "DELETE m FROM ezyarticle_post_meta m JOIN ezyarticle_posts p ON p.id=m.post_id "
            f"WHERE p.slug={slug_sql} AND m.meta_key='stack_fixture';\n"
            "INSERT INTO ezyarticle_post_meta (post_id,meta_key,meta_value) "
            f"SELECT p.id,'stack_fixture',{mysql_text(BROWSER_AUTH_MARKER)} FROM ezyarticle_posts p WHERE p.slug={slug_sql};\n"
        )
    statements.append(
        "INSERT INTO ezy_settings (setting_name,data_type,setting_value,created_at,updated_at) "
        "VALUES ('ezylogin_activation_required','BOOLEAN','false',NOW(),NOW()) "
        "ON DUPLICATE KEY UPDATE data_type='BOOLEAN',setting_value='false',updated_at=NOW();\n"
    )
    return "START TRANSACTION;\n" + "".join(statements) + "COMMIT;\n"


def install_browser_auth_fixture():
    validate_browser_auth_rows(browser_auth_rows())
    mysql_exec(browser_auth_sql())
    print("Installed browser signup/login fixture pages", flush=True)


def fetch_text(url):
    try:
        with urlopen(url, timeout=10) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except HTTPError as error:
        return error.code, error.read().decode("utf-8", "replace")


def browser_auth_page_errors(path, body):
    slug = path.strip("/")
    required = [f'data-stack-auth-page="{slug}"', f"/ezylogin/api/v1/{slug}"]
    return [f"missing {marker!r} at {path}" for marker in required if marker not in body]


def verify_browser_auth_fixture(web):
    errors = []
    for slug in BROWSER_AUTH_SLUGS:
        status, body = fetch_text(f"{web}/{slug}")
        if status != 200:
            errors.append(f"/{slug} returned HTTP {status}")
        else:
            errors.extend(browser_auth_page_errors(f"/{slug}", body))
    status, body = fetch_text(f"{web}/ezylogin/api/v1/login/settings")
    try:
        activation_required = json.loads(body).get("activationRequired") if status == 200 else None
    except json.JSONDecodeError:
        activation_required = None
    if activation_required is not False:
        errors.append("EzyLogin activationRequired is not false")
    if errors:
        detail = "; ".join(errors)
        raise ValueError(f"browser auth fixture verification failed: {detail}; use --theme freestyle or another EzyArticle page-rendering theme")


def read_manifest():
    manifest = {}
    for line in Path(__file__).with_name("plugin-versions.tsv").read_text().splitlines():
        if line and not line.startswith("#"):
            name, versions, kinds = line.split("\t")
            release, _, installed = versions.partition("/")
            manifest[name] = (release, installed or release, kinds.split(","))
    return manifest


def parse_only(value, manifest):
    names = [name.strip() for name in value.split(",") if name.strip()]
    if not names:
        raise ValueError("--only must name at least one plugin")
    if len(set(names)) != len(names):
        raise ValueError("--only contains duplicate plugin names")
    unknown = sorted(set(names).difference(manifest))
    if unknown:
        raise ValueError(f"unknown tested plugin(s): {', '.join(unknown)}")
    return names


def selected_plugins(value, manifest):
    return parse_only(value, manifest) if value is not None else list(manifest)


def add_requested_theme(names, theme, manifest):
    if theme in manifest and theme not in names:
        return [*names, theme]
    return names


def install_closure(manifest, names, admin, opener):
    graph = {}
    queue = list(names)
    while queue:
        name = queue.pop(0)
        if name in graph:
            continue
        release, version, kinds = manifest[name]
        dependencies = install(name, release, version, kinds, admin, opener)
        if missing := dependencies.difference(manifest):
            raise ValueError(f"{name}: dependencies outside the tested set: {', '.join(sorted(missing))}")
        graph[name] = dependencies
        for dependency in sorted(dependencies):
            if dependency not in graph and dependency not in queue:
                queue.append(dependency)
        print(f"Verified {name} {version}: {', '.join(kinds)}", flush=True)
    return graph


def main():
    manifest = read_manifest()
    themes = [name for name, (_, _, kinds) in manifest.items() if "theme" in kinds]
    parser = argparse.ArgumentParser(description="Install the tested plugin versions on a local Compose sandbox.")
    parser.add_argument("--only", help="comma-separated plugins to install with their dependency closure instead of every tested plugin")
    parser.add_argument("--theme", choices=["welcome", *themes], help="switch to one theme (default: keep current theme)")
    parser.add_argument("--admin-cookie-jar", type=Path, help="use the signed Admin marketplace installer with a local Netscape cookie jar instead of the CLI")
    parser.add_argument("--browser-auth", action="store_true", help="seed disposable /login and /register EzyArticle pages and disable local email activation for browser QA")
    args = parser.parse_args()
    admin = endpoint(9090, "")
    web = endpoint(8080, "")
    urls = [f"{admin}/login", f"{web}/"]
    core = properties(read_files(["settings/platform.properties"]).get("settings/platform.properties", ""))
    if core.get("ezyplatform.version") != CORE:
        raise ValueError(f"expected EzyPlatform {CORE}; run ./scripts/up.sh first")
    opener = None
    if args.admin_cookie_jar:
        jar = http.cookiejar.MozillaCookieJar(str(args.admin_cookie_jar))
        jar.load(ignore_discard=True)
        opener = build_opener(ProxyHandler({}), HTTPCookieProcessor(jar), NoRedirect())
    names = add_requested_theme(selected_plugins(args.only, manifest), args.theme, manifest)
    graph = install_closure(manifest, names, admin, opener)
    order = list(TopologicalSorter(graph).static_order())
    if args.browser_auth and "ezylogin" not in graph:
        raise ValueError("--browser-auth requires ezylogin; use --only ezylogin or include it in the installed set")
    if args.browser_auth:
        install_browser_auth_fixture()
    activate(manifest, order, args.theme)
    run([*COMPOSE, "restart", "ezyplatform"], timeout=120)
    wait_for_http(urls)
    if args.browser_auth:
        verify_browser_auth_fixture(web)
    print("Admin and Web ready; Socket is not started by this Compose service.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Plugin setup failed: {error}") from error
