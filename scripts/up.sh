#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

python3 scripts/sync-upstream.py --runtime-only
docker compose version >/dev/null
(umask 077; touch .env)
python3 - <<'PY' >> .env
import re
from secrets import token_hex
keys = ("MYSQL_ROOT_PASSWORD", "MYSQL_PASSWORD")
with open(".env") as f:
    content = f.read()
existing = set()
for line in content.splitlines():
    m = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
    if m:
        existing.add(m.group(1))
missing = [f"{key}={token_hex(32)}" for key in keys if key not in existing]
if missing:
    if content and not content.endswith("\n"):
        print()
    print("\n".join(missing))
PY
chmod 600 .env

apply_image_overrides() {
    local overrides="$1" variable reference
    [[ -n "$overrides" ]] || return 1
    while IFS='=' read -r variable reference; do
        export "$variable=$reference"
    done <<< "$overrides"
}

apply_image_overrides "$(python3 scripts/docker-image-fallback.py)" || true

compose_log="$(mktemp)"
cleanup_compose_log() {
    rm -f "$compose_log"
}
trap cleanup_compose_log EXIT

if ! docker compose up -d --build 2>&1 | tee "$compose_log"; then
    if grep -qiE '429|too many requests|toomanyrequests' "$compose_log"; then
        echo 'Docker Hub rate-limited the pull; retrying with mirror.gcr.io at the same digests.' >&2
        retry_overrides="$(python3 scripts/docker-image-fallback.py --docker-hub-failed)"
        if apply_image_overrides "$retry_overrides"; then
            docker compose up -d --build
        else
            echo 'No mirror override was available for the rate-limited image.' >&2
            exit 1
        fi
    else
        exit 1
    fi
fi
admin="http://127.0.0.1:$(docker compose port ezyplatform 9090 | cut -d: -f2)"
web="http://127.0.0.1:$(docker compose port ezyplatform 8080 | cut -d: -f2)"

wait_http() {
    local url="$1" deadline=$((SECONDS + $2)) code
    while (( SECONDS < deadline )); do
        code=$(curl --silent --output /dev/null --max-time 5 --write-out '%{http_code}' "$url") || code=000
        [[ "$code" =~ ^[23][0-9][0-9]$ ]] && return 0
        sleep 3
    done
    return 1
}

echo "Waiting for Admin at $admin ..."
if ! wait_http "$admin/login" 600; then
    echo 'Admin not ready. See: docker compose logs ezyplatform mysql' >&2
    exit 1
fi

echo "Waiting for Web at $web ..."
if ! wait_http "$web/" 90; then
    echo 'Restarting EzyPlatform once so Web can pick up the initialized database.'
    docker compose restart ezyplatform
    if ! wait_http "$web/" 300 || ! wait_http "$admin/login" 60; then
        echo 'Admin or Web not ready after restart. See: docker compose logs ezyplatform mysql' >&2
        exit 1
    fi
fi

printf 'Admin: %s/login\nFirst super admin: %s/setup-admin\nWeb: %s/\n' "$admin" "$admin" "$web"
