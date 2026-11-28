#!/usr/bin/env bash
# Rollback EzyPlatform stack from 1.6.1 back to the verified 1.6.0 checkpoint (tag stack-1.6.0).
# Default mode is --dry-run (verifies rollback image, git tag, backup files & SHA-256 without mutating anything).
# Pass --execute to perform rollback on CLOUD_DIR (default: this repo) and optionally --both to also rollback ezy-stack-local.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_CLOUD_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
DEFAULT_LOCAL_DIR="$(dirname -- "$DEFAULT_CLOUD_DIR")/ezy-stack-local"
BACKUP_DIR="${EZY_ROLLBACK_BACKUP_DIR:-$(dirname -- "$DEFAULT_CLOUD_DIR")/backups/2026-11-28-161}"
ROLLBACK_TAG="stack-1.6.0"
ROLLBACK_IMAGE="ezyplatform-stack/core:1.6.0-rollback"
ORIGINAL_IMAGE_TAG="ezyplatform-stack/core:1.6.0-1.5.6-84a5a5d"
BACKUP_STAMP="2026-11-28-1222"

MODE="dry-run"
INCLUDE_LOCAL="false"
CLOUD_DIR="$DEFAULT_CLOUD_DIR"
LOCAL_DIR="$DEFAULT_LOCAL_DIR"

usage() {
    cat <<EOF
Usage: $(basename "$0") [--dry-run | --execute] [--both] [--cloud DIR] [--local DIR] [--backup-dir DIR]
  --dry-run       Verify rollback prerequisites (image, git tag, backup checksums) without changing anything (default).
  --execute       Perform actual rollback to EzyPlatform 1.6.0 (tag $ROLLBACK_TAG).
  --both          Apply rollback to both cloud ($DEFAULT_CLOUD_DIR) and local ($DEFAULT_LOCAL_DIR) checkouts.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) MODE="dry-run"; shift ;;
        --execute) MODE="execute"; shift ;;
        --both) INCLUDE_LOCAL="true"; shift ;;
        --cloud) CLOUD_DIR="$2"; shift 2 ;;
        --local) LOCAL_DIR="$2"; shift 2 ;;
        --backup-dir) BACKUP_DIR="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
    esac
done

echo "=== Rollback 1.6.1 -> 1.6.0 (mode=$MODE) ==="

# 1. Verify rollback image exists
img_id="$(docker image inspect --format '{{.Id}}' "$ROLLBACK_IMAGE")"
echo "[OK] Rollback image present: $ROLLBACK_IMAGE ($img_id)"

# 2. Verify git tag exists
tag_commit="$(git -C "$CLOUD_DIR" rev-list -n 1 "$ROLLBACK_TAG")"
echo "[OK] Git tag present: $ROLLBACK_TAG -> $tag_commit"

# 3. Verify backup directory and SHA-256 checksums
[[ -d "$BACKUP_DIR" ]] || { echo "[FAIL] Missing backup dir: $BACKUP_DIR" >&2; exit 1; }
[[ -f "$BACKUP_DIR/SHA256SUMS.txt" ]] || { echo "[FAIL] Missing $BACKUP_DIR/SHA256SUMS.txt" >&2; exit 1; }
(cd "$BACKUP_DIR" && sha256sum -c SHA256SUMS.txt)

rollback_one() {
    local target_dir="$1"
    local prefix="$2"
    local db_dump="$BACKUP_DIR/${prefix}-db-${BACKUP_STAMP}.sql.gz"
    local rt_tar="$BACKUP_DIR/${prefix}-runtime-${BACKUP_STAMP}.tgz"
    local env_bak="$BACKUP_DIR/${prefix}.env"
    local project_name
    project_name="$(basename "$target_dir")"
    local rt_vol="${project_name}_ezyplatform-data"

    for f in "$db_dump" "$rt_tar" "$env_bak"; do
        [[ -f "$f" ]] || { echo "[FAIL] Missing backup file: $f" >&2; exit 1; }
    done

    echo "--- Rollback target: $target_dir (project=$project_name) ---"
    if [[ "$MODE" == "dry-run" ]]; then
        echo "  [DRY-RUN] docker image tag $ROLLBACK_IMAGE $ORIGINAL_IMAGE_TAG"
        echo "  [DRY-RUN] (cd $target_dir && docker compose stop ezyplatform)"
        echo "  [DRY-RUN] restore runtime volume $rt_vol from $rt_tar"
        echo "  [DRY-RUN] restore MySQL DB ezyplatform from $db_dump"
        echo "  [DRY-RUN] install -m 600 $env_bak $target_dir/.env"
        echo "  [DRY-RUN] git -C $target_dir checkout $ROLLBACK_TAG"
        echo "  [DRY-RUN] (cd $target_dir && docker compose up -d --no-build)"
        return 0
    fi

    docker image tag "$ROLLBACK_IMAGE" "$ORIGINAL_IMAGE_TAG"

    (cd "$target_dir" && docker compose stop ezyplatform)

    # Restore runtime volume cleanly
    docker run --rm -v "${rt_vol}:/v" -v "$BACKUP_DIR:/b:ro" alpine sh -c \
        "find /v -mindepth 1 -maxdepth 1 -exec rm -rf {} + && tar xzf /b/$(basename "$rt_tar") -C /v"

    # Restore MySQL database cleanly
    local mysql_cid
    mysql_cid="$(cd "$target_dir" && docker compose ps -q mysql)"
    [[ -n "$mysql_cid" ]] || { echo "[FAIL] MySQL container not running for $target_dir" >&2; exit 1; }
    docker exec "$mysql_cid" sh -c \
        'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot -e "DROP DATABASE IF EXISTS ezyplatform; CREATE DATABASE ezyplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"'
    gzip -dc "$db_dump" | docker exec -i "$mysql_cid" sh -c \
        'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot ezyplatform'

    # Restore .env (mode 600) and checkout tag stack-1.6.0
    install -m 600 "$env_bak" "$target_dir/.env"
    git -C "$target_dir" checkout "$ROLLBACK_TAG"

    # Bring up 1.6.0 image without rebuilding
    (cd "$target_dir" && docker compose up -d --no-build)

    # Wait for Admin /login 200 and verify runtime version = 1.6.0
    local admin_port
    admin_port="$(cd "$target_dir" && docker compose port ezyplatform 9090 | cut -d: -f2)"
    local deadline=$((SECONDS + 180))
    while (( SECONDS < deadline )); do
        code="$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:${admin_port}/login" || echo 000)"
        [[ "$code" == "200" ]] && break
        sleep 3
    done
    local rt_ver
    rt_ver="$(cd "$target_dir" && docker compose exec -T ezyplatform sed -n 's/^ezyplatform\.version=//p' /app/ezyplatform/settings/platform.properties)"
    echo "[OK] $project_name restored: ezyplatform.version=$rt_ver (admin HTTP $code)"
    [[ "$rt_ver" == "1.6.0" ]] || { echo "[FAIL] Expected 1.6.0 after rollback, got $rt_ver" >&2; exit 1; }
}

rollback_one "$CLOUD_DIR" "ezyplatform-stack"
if [[ "$INCLUDE_LOCAL" == "true" ]]; then
    rollback_one "$LOCAL_DIR" "ezy-stack-local"
fi

echo "=== ROLLBACK ${MODE^^} COMPLETE ==="
