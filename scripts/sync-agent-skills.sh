#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

if [[ -n "${AGENTKIT_API_KEY:-}" ]]; then
    exec python3 scripts/sync-upstream.py --require-agentkit
fi

echo "AGENTKIT_API_KEY is not set; syncing EzyPlatform skills only." >&2
exec python3 scripts/sync-upstream.py --skip-agentkit
