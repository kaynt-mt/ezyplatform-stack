#!/usr/bin/env python3
import argparse
import http.cookiejar
import json
import re
import subprocess
import time
from graphlib import TopologicalSorter
from pathlib import Path
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


def activate(manifest, order, theme):
    before = active_modules()
    deactivate = [("theme", name) for name in sorted(before["theme"] - {theme})] if theme else []
    required = [(kind, name) for name in order for kind in manifest[name][2] if kind != "theme"]
    if theme:
        required.append(("theme", theme))
    commands = [f"deactivate {kind} {name}" for kind, name in deactivate]
    commands += [f"activate {kind} {name}" for kind, name in required if name not in before[kind]]
    if not commands:
        return
    run([*CONTAINER, "bash", "cli.sh"], input="\n".join([*commands, "exit", ""]),
        capture_output=True, timeout=120)
    after = active_modules()
    missing = [f"{name}/{kind}" for kind, name in required if name not in after[kind]]
    if missing or (theme and after["theme"] != {theme}):
        raise ValueError(f"activation failed: missing={missing}, active themes={sorted(after['theme'])}")
    print(f"Applied {len(commands)} activation changes", flush=True)


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


def main():
    manifest = {}
    for line in Path(__file__).with_name("plugin-versions.tsv").read_text().splitlines():
        if line and not line.startswith("#"):
            name, versions, kinds = line.split("\t")
            release, _, installed = versions.partition("/")
            manifest[name] = (release, installed or release, kinds.split(","))
    themes = [name for name, (_, _, kinds) in manifest.items() if "theme" in kinds]
    parser = argparse.ArgumentParser(description="Install the tested plugin versions on a local Compose sandbox.")
    parser.add_argument("--theme", choices=["welcome", *themes], help="switch to one theme (default: keep current theme)")
    parser.add_argument("--admin-cookie-jar", type=Path, help="use the signed Admin marketplace installer with a local Netscape cookie jar instead of the CLI")
    args = parser.parse_args()
    admin = endpoint(9090, "")
    urls = [f"{admin}/login", endpoint(8080, "/")]
    core = properties(read_files(["settings/platform.properties"]).get("settings/platform.properties", ""))
    if core.get("ezyplatform.version") != CORE:
        raise ValueError(f"expected EzyPlatform {CORE}; run ./scripts/up.sh first")
    opener = None
    if args.admin_cookie_jar:
        jar = http.cookiejar.MozillaCookieJar(str(args.admin_cookie_jar))
        jar.load(ignore_discard=True)
        opener = build_opener(ProxyHandler({}), HTTPCookieProcessor(jar), NoRedirect())
    graph = {}
    for name, (release, version, kinds) in manifest.items():
        graph[name] = install(name, release, version, kinds, admin, opener)
        if missing := graph[name].difference(manifest):
            raise ValueError(f"{name}: dependencies outside the tested set: {', '.join(sorted(missing))}")
        print(f"Verified {name} {version}: {', '.join(kinds)}", flush=True)
    order = list(TopologicalSorter(graph).static_order())
    activate(manifest, order, args.theme)
    run([*COMPOSE, "restart", "ezyplatform"], timeout=120)
    wait_for_http(urls)
    print("Admin and Web ready; Socket is not started by this Compose service.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Plugin setup failed: {error}") from error
