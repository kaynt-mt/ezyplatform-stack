#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_CLOUD_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
DEFAULT_LOCAL_DIR="${EZY_PARITY_LOCAL_DIR:-$(dirname -- "$DEFAULT_CLOUD_DIR")/ezy-stack-local}"

export EZY_PARITY_DEFAULT_CLOUD="$DEFAULT_CLOUD_DIR"
export EZY_PARITY_DEFAULT_LOCAL="$DEFAULT_LOCAL_DIR"

exec python3 - "$@" <<'PY'
import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, cwd=None, timeout=30):
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "LC_ALL": "C"},
        )
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired:
        return 124, "", f"command timed out after {timeout}s"
    return proc.returncode, proc.stdout, proc.stderr


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def short_hash(value: str, length: int = 12) -> str:
    if not value:
        return "<missing>"
    if "@sha256:" in value:
        prefix, digest = value.split("@sha256:", 1)
        return f"{prefix}@sha256:{digest[:length]}"
    if value.startswith("sha256:"):
        return f"sha256:{value[7:7 + length]}"
    return value[:length]


def read_env_ports(checkout_dir: Path):
    ports = {"EZY_ADMIN_PORT": "9090", "EZY_WEB_PORT": "8080"}
    env_file = checkout_dir / ".env"
    if not env_file.is_file():
        return ports
    for raw_line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(?:export\s+)?(EZY_ADMIN_PORT|EZY_WEB_PORT)\s*=\s*(.*)$", line)
        if not m:
            continue
        val = m.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        if val:
            ports[m.group(1)] = val
    return ports


def get_commit(checkout_dir: Path):
    if not checkout_dir.is_dir():
        return None, f"dir not found: {checkout_dir}"
    rc, out, err = run_cmd(["git", "-C", str(checkout_dir), "rev-parse", "HEAD"])
    if rc != 0 or not out.strip():
        return None, (err.strip() or "git rev-parse failed")
    return out.strip(), None


def get_compose_container(checkout_dir: Path, service: str):
    if not checkout_dir.is_dir():
        return None, f"dir not found: {checkout_dir}"
    rc, out, err = run_cmd(["docker", "compose", "ps", "-q", service], cwd=str(checkout_dir))
    cid = out.strip().splitlines()[0].strip() if out.strip() else ""
    if rc != 0 or not cid:
        return None, (err.strip() or f"service {service} not running")
    return cid, None


def get_image_digest(checkout_dir: Path):
    cid, err = get_compose_container(checkout_dir, "ezyplatform")
    if err:
        return None, None, err
    rc, out, stderr = run_cmd(["docker", "inspect", "--format", "{{.Image}}", cid])
    img_id = out.strip()
    if rc != 0 or not img_id:
        return None, None, (stderr.strip() or "docker inspect failed")
    rc2, out2, stderr2 = run_cmd(
        [
            "docker",
            "image",
            "inspect",
            "--format",
            "{{if .RepoDigests}}{{index .RepoDigests 0}}{{else}}{{.Id}}{{end}}",
            img_id,
        ]
    )
    digest = out2.strip()
    if rc2 != 0 or not digest:
        return None, img_id, (stderr2.strip() or "docker image inspect failed")
    return digest, img_id, None


def get_plugins_snapshot(checkout_dir: Path):
    tsv_path = checkout_dir / "scripts" / "plugin-versions.tsv"
    if not tsv_path.is_file():
        return None, None, f"missing {tsv_path}"
    tsv_entries = []
    for raw_line in tsv_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            tsv_entries.append(f"tsv:{parts[0].strip()}={parts[1].strip()}")
    tsv_entries.sort()

    cid, err = get_compose_container(checkout_dir, "ezyplatform")
    if err:
        return None, None, err

    probe_sh = (
        "for lane in admin web socket; do "
        "  for kind in plugins themes; do "
        "    if [ -d \"/app/ezyplatform/$lane/$kind\" ]; then "
        "      for d in /app/ezyplatform/$lane/$kind/*; do "
        "        [ -d \"$d\" ] || continue; "
        "        name=$(basename \"$d\"); "
        "        ver=$(sed -n 's/^version=//p' \"$d/module.properties\" 2>/dev/null | head -n 1 | tr -d '\\r'); "
        "        printf 'MOD\\t%s\\t%s\\t%s\\t%s\\n' \"$lane\" \"$kind\" \"$name\" \"${ver:-unknown}\"; "
        "      done; "
        "    fi; "
        "  done; "
        "  for mf in plugins.txt themes.txt; do "
        "    p=\"/app/ezyplatform/.runtime/$lane/$mf\"; "
        "    if [ -f \"$p\" ]; then "
        "      printf 'RT\\t%s\\t%s\\t' \"$lane\" \"$mf\"; "
        "      tr -d '\\r\\n' < \"$p\"; "
        "      printf '\\n'; "
        "    fi; "
        "  done; "
        "done"
    )
    rc, out, stderr = run_cmd(["docker", "exec", cid, "sh", "-c", probe_sh])
    if rc != 0:
        return None, None, (stderr.strip() or "docker exec plugin probe failed")

    installed = {}
    active_map = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        if line.startswith("MOD\t"):
            parts5 = line.split("\t", 4)
            if len(parts5) == 5:
                _, lane, kind, name, ver = parts5
                installed[(lane, kind, name)] = ver
        elif line.startswith("RT\t"):
            parts = line.split("\t", 3)
            if len(parts) == 4:
                _, lane, mf, payload = parts
            kind = "plugins" if mf == "plugins.txt" else "themes"
            payload = payload.strip()
            if not payload:
                continue
            try:
                items = json.loads(payload)
            except json.JSONDecodeError:
                return None, None, f"invalid JSON in .runtime/{lane}/{mf}"
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and "name" in item:
                        active_map[(lane, kind, str(item["name"]))] = bool(item.get("active", False))

    all_keys = sorted(set(installed.keys()) | set(active_map.keys()))
    runtime_entries = []
    for lane, kind, name in all_keys:
        ver = installed.get((lane, kind, name), "missing")
        active = active_map.get((lane, kind, name))
        active_str = "unlisted" if active is None else ("true" if active else "false")
        runtime_entries.append(f"runtime:{lane}/{kind}/{name}={ver} active={active_str}")

    canonical_lines = tsv_entries + runtime_entries
    canonical_text = "\n".join(canonical_lines) + "\n"
    digest = sha256_text(canonical_text)
    summary = f"{len(runtime_entries)}rt+{len(tsv_entries)}tsv ({digest[:12]})"
    return {"hash": digest, "summary": summary, "lines": canonical_lines}, None, None


def get_schema_snapshot(checkout_dir: Path):
    cid, err = get_compose_container(checkout_dir, "mysql")
    if err:
        return None, err
    sql = (
        "SELECT 'T', table_name, table_type, COALESCE(engine,''), COALESCE(table_collation,'') "
        "FROM information_schema.tables "
        "WHERE table_schema = 'ezyplatform' "
        "ORDER BY table_name; "
        "SELECT 'C', table_name, ordinal_position, column_name, column_type, is_nullable, "
        "COALESCE(column_default,'<NULL>'), column_key, extra, "
        "COALESCE(character_set_name,''), COALESCE(collation_name,'') "
        "FROM information_schema.columns "
        "WHERE table_schema = 'ezyplatform' "
        "ORDER BY table_name, ordinal_position;"
    )
    rc, out, stderr = run_cmd(
        [
            "docker",
            "exec",
            cid,
            "sh",
            "-c",
            'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot -N -B -e "$1"',
            "sh",
            sql,
        ]
    )
    if rc != 0:
        return None, (stderr.strip() or "mysql schema query failed")
    lines = [ln.rstrip("\r") for ln in out.splitlines() if ln.strip()]
    tables = sum(1 for ln in lines if ln.startswith("T\t"))
    cols = sum(1 for ln in lines if ln.startswith("C\t"))
    if tables == 0:
        return None, "schema ezyplatform has 0 tables"
    canonical = "\n".join(lines) + "\n"
    digest = sha256_text(canonical)
    return {
        "hash": digest,
        "tables": tables,
        "cols": cols,
        "summary": f"{tables}t/{cols}c ({digest[:12]})",
        "lines": lines,
    }, None


def probe_http(url: str):
    rc, out, _ = run_cmd(
        ["curl", "--silent", "--output", "/dev/null", "--max-time", "5", "--write-out", "%{http_code}", url],
        timeout=10,
    )
    code = out.strip()
    if rc != 0 or not re.match(r"^[23][0-9]{2}$", code):
        return False, code or "000"
    return True, code


def get_ports_snapshot(checkout_dir: Path):
    env_ports = read_env_ports(checkout_dir)
    expected_admin = f"127.0.0.1:{env_ports['EZY_ADMIN_PORT']}"
    expected_web = f"127.0.0.1:{env_ports['EZY_WEB_PORT']}"

    rc_a, out_a, err_a = run_cmd(["docker", "compose", "port", "ezyplatform", "9090"], cwd=str(checkout_dir))
    rc_w, out_w, err_w = run_cmd(["docker", "compose", "port", "ezyplatform", "8080"], cwd=str(checkout_dir))
    if rc_a != 0 or rc_w != 0:
        return None, (err_a.strip() or err_w.strip() or "docker compose port failed")

    actual_admin_lines = [ln.strip() for ln in out_a.splitlines() if ln.strip()]
    actual_web_lines = [ln.strip() for ln in out_w.splitlines() if ln.strip()]
    actual_admin = actual_admin_lines[0] if actual_admin_lines else ""
    actual_web = actual_web_lines[0] if actual_web_lines else ""

    issues = []
    if len(actual_admin_lines) != 1 or actual_admin != expected_admin:
        issues.append(f"admin mapped={actual_admin or 'none'} expected={expected_admin}")
    if len(actual_web_lines) != 1 or actual_web != expected_web:
        issues.append(f"web mapped={actual_web or 'none'} expected={expected_web}")
    if actual_admin and not actual_admin.startswith("127.0.0.1:"):
        issues.append(f"admin not loopback ({actual_admin})")
    if actual_web and not actual_web.startswith("127.0.0.1:"):
        issues.append(f"web not loopback ({actual_web})")

    admin_code = "skip"
    web_code = "skip"
    if not issues:
        ok_a, admin_code = probe_http(f"http://{actual_admin}/login")
        ok_w, web_code = probe_http(f"http://{actual_web}/")
        if not ok_a:
            issues.append(f"admin /login HTTP {admin_code}")
        if not ok_w:
            issues.append(f"web / HTTP {web_code}")

    admin_p = actual_admin.split(":", 1)[1] if ":" in actual_admin else "?"
    web_p = actual_web.split(":", 1)[1] if ":" in actual_web else "?"
    summary = f"127.0.0.1:{admin_p}/9090,{web_p}/8080"
    if issues:
        summary += f" [{'; '.join(issues)}]"
    return {"ok": len(issues) == 0, "summary": summary, "admin": actual_admin, "web": actual_web, "issues": issues}, None


def clean_err(msg: str, max_len: int = 48) -> str:
    first = " ".join(msg.strip().splitlines())
    if len(first) > max_len:
        return first[: max_len - 3] + "..."
    return first


def render_table(headers, rows):
    sanitized = []
    for row in rows:
        sanitized.append([" ".join(str(cell).splitlines()) for cell in row])
    widths = [len(h) for h in headers]
    for row in sanitized:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    fmt = "| " + " | ".join(f"{{:<{w}}}" for w in widths) + " |"
    out = [sep, fmt.format(*headers), sep]
    for row in sanitized:
        out.append(fmt.format(*row))
    out.append(sep)
    return "\n".join(out)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="parity.sh",
        description="Verify one-source parity between cloud (default: this checkout) and local EzyPlatform stack.",
    )
    parser.add_argument("paths", nargs="*", help="[LOCAL_DIR] or [CLOUD_DIR LOCAL_DIR]")
    parser.add_argument("--cloud", dest="cloud_opt", help="Path to cloud/reference checkout")
    parser.add_argument("--local", dest="local_opt", help="Path to local checkout")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show full hashes and line diffs on mismatch")
    args = parser.parse_args(argv)

    default_cloud = os.environ["EZY_PARITY_DEFAULT_CLOUD"]
    default_local = os.environ["EZY_PARITY_DEFAULT_LOCAL"]

    if len(args.paths) == 0:
        cloud_dir = args.cloud_opt or default_cloud
        local_dir = args.local_opt or default_local
    elif len(args.paths) == 1:
        cloud_dir = args.cloud_opt or default_cloud
        local_dir = args.local_opt or args.paths[0]
    elif len(args.paths) == 2:
        cloud_dir = args.cloud_opt or args.paths[0]
        local_dir = args.local_opt or args.paths[1]
    else:
        parser.error("expected at most 2 positional paths: [LOCAL_DIR] or [CLOUD_DIR LOCAL_DIR]")

    return Path(cloud_dir).resolve(), Path(local_dir).resolve(), args.verbose


def main(argv):
    cloud_dir, local_dir, verbose = parse_args(argv)
    rows = []
    failed = []
    diffs = []

    # (a) git rev-parse HEAD
    c_commit, c_err = get_commit(cloud_dir)
    l_commit, l_err = get_commit(local_dir)
    if c_err or l_err:
        rows.append(["commit", c_commit[:7] if c_commit else f"ERR: {clean_err(c_err)}", l_commit[:7] if l_commit else f"ERR: {clean_err(l_err)}", "FAIL"])
        failed.append("commit")
    elif c_commit == l_commit:
        rows.append(["commit", c_commit[:7], l_commit[:7], "OK"])
    else:
        rows.append(["commit", c_commit[:7], l_commit[:7], "DIFF"])
        failed.append("commit")
        diffs.append(f"commit: cloud={c_commit} local={l_commit}")

    # (b) image digest
    c_dig, _, c_derr = get_image_digest(cloud_dir)
    l_dig, _, l_derr = get_image_digest(local_dir)
    if c_derr or l_derr:
        rows.append(["image", short_hash(c_dig) if c_dig else f"ERR: {clean_err(c_derr)}", short_hash(l_dig) if l_dig else f"ERR: {clean_err(l_derr)}", "FAIL"])
        failed.append("image")
    elif c_dig == l_dig:
        rows.append(["image", short_hash(c_dig), short_hash(l_dig), "OK"])
    else:
        rows.append(["image", short_hash(c_dig), short_hash(l_dig), "DIFF"])
        failed.append("image")
        diffs.append(f"image: cloud={c_dig} local={l_dig}")

    # (c) plugins hash (plugin-versions.tsv + container lanes)
    c_plug, _, c_perr = get_plugins_snapshot(cloud_dir)
    l_plug, _, l_perr = get_plugins_snapshot(local_dir)
    if c_perr or l_perr:
        rows.append(["plugins", c_plug["summary"] if c_plug else f"ERR: {clean_err(c_perr)}", l_plug["summary"] if l_plug else f"ERR: {clean_err(l_perr)}", "FAIL"])
        failed.append("plugins")
    elif c_plug["hash"] == l_plug["hash"]:
        rows.append(["plugins", c_plug["summary"], l_plug["summary"], "OK"])
    else:
        rows.append(["plugins", c_plug["summary"], l_plug["summary"], "DIFF"])
        failed.append("plugins")
        diff_lines = list(difflib.unified_diff(c_plug["lines"], l_plug["lines"], fromfile="cloud", tofile="local", lineterm=""))
        diffs.append("plugins diff:\n" + "\n".join(diff_lines[:40]))

    # (d) schema hash (information_schema tables + columns)
    c_sch, c_serr = get_schema_snapshot(cloud_dir)
    l_sch, l_serr = get_schema_snapshot(local_dir)
    if c_serr or l_serr:
        rows.append(["schema", c_sch["summary"] if c_sch else f"ERR: {clean_err(c_serr)}", l_sch["summary"] if l_sch else f"ERR: {clean_err(l_serr)}", "FAIL"])
        failed.append("schema")
    elif c_sch["hash"] == l_sch["hash"]:
        rows.append(["schema", c_sch["summary"], l_sch["summary"], "OK"])
    else:
        rows.append(["schema", c_sch["summary"], l_sch["summary"], "DIFF"])
        failed.append("schema")
        diff_lines = list(difflib.unified_diff(c_sch["lines"], l_sch["lines"], fromfile="cloud", tofile="local", lineterm=""))
        diffs.append("schema diff:\n" + "\n".join(diff_lines[:40]))

    # (e) ports (loopback-only, matches .env, container 9090/8080 reachable)
    c_ports, c_pterr = get_ports_snapshot(cloud_dir)
    l_ports, l_pterr = get_ports_snapshot(local_dir)
    if c_pterr or l_pterr:
        rows.append(["ports", c_ports["summary"] if c_ports else f"ERR: {clean_err(c_pterr)}", l_ports["summary"] if l_ports else f"ERR: {clean_err(l_pterr)}", "FAIL"])
        failed.append("ports")
    elif c_ports["ok"] and l_ports["ok"]:
        rows.append(["ports", c_ports["summary"], l_ports["summary"], "OK"])
    else:
        rows.append(["ports", c_ports["summary"], l_ports["summary"], "FAIL"])
        failed.append("ports")
        diffs.append(f"ports: cloud={c_ports['issues']} local={l_ports['issues']}")

    headers = ["CHECK", f"CLOUD ({cloud_dir.name})", f"LOCAL ({local_dir.name})", "STATUS"]
    print(render_table(headers, rows))

    if verbose:
        print(f"cloud_dir: {cloud_dir}")
        print(f"local_dir: {local_dir}")
        if c_commit and l_commit:
            print(f"commit_full: cloud={c_commit} local={l_commit}")
        if c_dig and l_dig:
            print(f"image_full:  cloud={c_dig} local={l_dig}")
        if c_plug and l_plug:
            print(f"plugins_sha: cloud={c_plug['hash']} local={l_plug['hash']}")
        if c_sch and l_sch:
            print(f"schema_sha:  cloud={c_sch['hash']} local={l_sch['hash']}")

    if failed:
        if diffs:
            for d in diffs:
                print(d, file=sys.stderr)
        print(f"PARITY FAILED ({', '.join(failed)})")
        return 1

    print("PARITY OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
PY
