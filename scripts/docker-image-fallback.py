#!/usr/bin/env python3
"""Emit mirror.gcr.io overrides when Docker Hub cannot serve pinned images."""
import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DEFAULT = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*IMAGE):-([^}\s]+)\}")
ENV_ASSIGNMENT = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
DOCKER_HUB_HOSTS = {"docker.io", "index.docker.io", "registry-1.docker.io"}
DIGEST = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:[+._-][A-Za-z][A-Za-z0-9]*)*:[0-9A-Fa-f]{32,}$")


def image_defaults(compose_text):
    return dict(IMAGE_DEFAULT.findall(compose_text))


def env_values(env_text):
    values = {}
    for line in env_text.splitlines():
        match = ENV_ASSIGNMENT.match(line)
        if not match or line.lstrip().startswith("#"):
            continue
        raw = match.group(2).strip()
        if raw[:1] in ("'", '"'):
            try:
                parts = shlex.split(raw, posix=True)
                value = parts[0] if parts else ""
            except ValueError:
                value = raw.strip(raw[0])
        else:
            value = re.split(r"\s+#", raw, maxsplit=1)[0].strip()
        values[match.group(1)] = value
    return values


def compose_env_files(environ, default_path):
    configured = environ.get("COMPOSE_ENV_FILES", "")
    if configured:
        paths = []
        for entry in configured.split(","):
            entry = entry.strip()
            if not entry:
                continue
            path = Path(entry).expanduser()
            paths.append(path if path.is_absolute() else default_path.parent / path)
        return paths
    if environ.get("COMPOSE_DISABLE_ENV_FILE", "").lower() in {"1", "true"}:
        return []
    return [default_path]


def configured_keys(defaults, env_files, environ):
    values = {}
    for path in env_files:
        if path.is_file():
            values.update(env_values(path.read_text()))
    for variable in defaults:
        if variable in environ:
            values[variable] = environ[variable]
    return {variable for variable in defaults if values.get(variable, "") != ""}


def docker_hub_mirror(reference):
    if not reference or reference == "scratch" or "$" in reference or "://" in reference:
        return None
    name_tag, separator, digest = reference.partition("@")
    if separator and not DIGEST.match(digest):
        return None

    first, slash, remainder = name_tag.partition("/")
    has_registry = slash and ("." in first or ":" in first or first == "localhost")
    if has_registry:
        if first.lower() not in DOCKER_HUB_HOSTS:
            return None
        path = remainder
    else:
        path = name_tag

    last_slash = path.rfind("/")
    last_colon = path.rfind(":")
    if last_colon > last_slash:
        repository = path[:last_colon]
        tag = path[last_colon:]
    else:
        repository = path
        tag = ""
    if not repository or repository.startswith("-") or "//" in repository:
        return None
    if any(not part for part in repository.split("/")):
        return None
    if "/" not in repository:
        repository = f"library/{repository}"
    suffix = f"{tag}@{digest}" if separator else tag
    return f"mirror.gcr.io/{repository}{suffix}"


def local_image_exists(reference, runner=subprocess.run):
    return runner(
        ["docker", "image", "inspect", reference],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=10,
    ).returncode == 0


def remote_image_exists(reference, runner=subprocess.run):
    return runner(
        ["docker", "buildx", "imagetools", "inspect", reference],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=20,
    ).returncode == 0


def buildx_available(runner=subprocess.run):
    try:
        return runner(
            ["docker", "buildx", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        ).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def select_overrides(defaults, configured_keys, local_exists, remote_exists, docker_hub_failed=False):
    overrides = {}
    notices = []
    for variable, canonical in sorted(defaults.items()):
        if variable in configured_keys:
            continue
        mirror = docker_hub_mirror(canonical)
        if not mirror:
            continue
        try:
            if not docker_hub_failed and (local_exists(canonical) or remote_exists(canonical)):
                continue
        except (OSError, subprocess.TimeoutExpired):
            pass
        try:
            if local_exists(mirror) or remote_exists(mirror):
                overrides[variable] = mirror
                notices.append(
                    f"Notice: Docker Hub cannot serve {canonical}; using {mirror} for this run."
                )
            else:
                notices.append(
                    f"Notice: neither Docker Hub nor mirror.gcr.io can serve {canonical}; "
                    "the original Docker error will stop startup."
                )
        except (OSError, subprocess.TimeoutExpired):
            notices.append(
                f"Notice: could not probe a mirror for {canonical}; the original Docker error will stop startup."
            )
    return overrides, notices


def override_assignments(overrides):
    return "\n".join(
        f"{variable}={reference}"
        for variable, reference in sorted(overrides.items())
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--compose", type=Path, default=ROOT / "compose.yaml")
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument(
        "--docker-hub-failed",
        action="store_true",
        help="skip Docker Hub availability probes after Compose has already received a Hub failure",
    )
    args = parser.parse_args(argv)

    defaults = image_defaults(args.compose.read_text())
    env_files = compose_env_files(os.environ, args.env_file)
    configured = configured_keys(defaults, env_files, os.environ)
    if not buildx_available():
        print("Notice: docker buildx is unavailable; Docker image mirror fallback disabled.", file=sys.stderr)
        return 0

    overrides, notices = select_overrides(
        defaults,
        configured,
        local_image_exists,
        remote_image_exists,
        docker_hub_failed=args.docker_hub_failed,
    )
    for notice in notices:
        print(notice, file=sys.stderr)
    assignments = override_assignments(overrides)
    if assignments:
        print(assignments)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
