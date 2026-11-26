#!/usr/bin/env python3
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ".generated-by-sync-upstream"
MAX_PACKAGE_SIZE = 16 * 1024 * 1024
MAX_INSTALLER_SIZE = 2 * 1024 * 1024
AGENTKIT_INSTALL_URL = "https://agentkit.best/install.sh"
SAFE_TOKEN = re.compile(r"^[A-Za-z0-9._-]+$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def git(directory, *args):
    return subprocess.run(["git", "-C", str(directory), *args], check=True,
                          text=True, stdout=subprocess.PIPE).stdout.strip()


def validate_token(label, value):
    if not isinstance(value, str) or not SAFE_TOKEN.match(value) or value in {".", ".."}:
        raise ValueError(f"Invalid {label}: {value!r}")
    return value


def checkout(name, revision):
    directory = ROOT / ".upstream" / name
    directory.mkdir(parents=True, exist_ok=True)
    if not (directory / ".git").is_dir():
        git(directory, "init", "-q")
    if git(directory, "status", "--porcelain"):
        raise ValueError(f"{directory}: working tree is not clean")
    head = subprocess.run(["git", "-C", str(directory), "rev-parse", "--quiet", "--verify", "HEAD"],
                          capture_output=True, text=True)
    if head.stdout.strip() != revision:
        git(directory, "fetch", "--depth", "1", f"https://github.com/cppai-vn/{name}.git", revision)
        git(directory, "checkout", "--quiet", "--detach", revision)
    print(f"{name}: {revision}")
    return directory


def extract_skill(body, checksum, destination):
    if hashlib.sha256(body).hexdigest() != checksum:
        raise ValueError(f"{destination.name}: SHA-256 mismatch")
    with ZipFile(io.BytesIO(body)) as archive:
        if sum(entry.file_size for entry in archive.infolist()) > MAX_PACKAGE_SIZE:
            raise ValueError(f"{destination.name}: uncompressed package too large")
        for entry in archive.infolist():
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError(f"{destination.name}: unsafe ZIP path {entry.filename!r}")
        archive.extractall(destination)
    if not (destination / "SKILL.md").is_file():
        raise ValueError(f"{destination.name}: missing SKILL.md")


def tree_digest(directory):
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        rel = path.relative_to(directory).as_posix()
        if path.is_symlink():
            raise ValueError(f"{directory.name}: unexpected symlink {rel!r}")
        if path.is_file():
            digest.update(f"F:{rel}\0".encode())
            digest.update(path.read_bytes())
        elif path.is_dir():
            digest.update(f"D:{rel}\0".encode())
    return digest.hexdigest()


def ak_version_matches(ak_bin, expected_version):
    if not ak_bin.is_file() or not os.access(ak_bin, os.X_OK):
        return False
    probe = subprocess.run([str(ak_bin), "--version"], capture_output=True, text=True)
    return probe.returncode == 0 and probe.stdout.strip() == f"ak {expected_version}"


def ensure_ak_cli(cli_version, installer_sha256, root=ROOT):
    validate_token("agentkit.cli_version", cli_version)
    if not isinstance(installer_sha256, str) or not SHA256_HEX.match(installer_sha256):
        raise ValueError(f"Invalid agentkit.installer_sha256: {installer_sha256!r}")
    bin_dir = root / ".upstream" / "agentkit" / "bin"
    ak_bin = bin_dir / "ak"
    if ak_version_matches(ak_bin, cli_version):
        return ak_bin
    bin_dir.mkdir(parents=True, exist_ok=True)
    request = Request(AGENTKIT_INSTALL_URL, headers={"User-Agent": "curl/8.0"})
    with urlopen(request, timeout=30) as response:
        installer = response.read(MAX_INSTALLER_SIZE + 1)
    if len(installer) > MAX_INSTALLER_SIZE:
        raise ValueError("AgentKit installer script too large")
    if hashlib.sha256(installer).hexdigest() != installer_sha256:
        raise ValueError("AgentKit installer SHA-256 mismatch")
    env = {k: v for k, v in os.environ.items() if k != "AGENTKIT_API_KEY"}
    env["AK_VERSION"] = cli_version
    env["AK_INSTALL_DIR"] = str(bin_dir)
    subprocess.run(["sh"], input=installer, env=env, check=True)
    if not ak_version_matches(ak_bin, cli_version):
        raise ValueError(f"Installed ak binary does not match pinned version {cli_version}")
    return ak_bin


def ensure_ak_auth(ak_bin):
    if os.environ.get("AGENTKIT_API_KEY"):
        login = subprocess.run(
            [str(ak_bin), "login", "--no-interactive", "--json"],
            capture_output=True, text=True,
        )
        if login.returncode != 0:
            raise ValueError("AgentKit login failed (check AGENTKIT_API_KEY)")
    whoami = subprocess.run(
        [str(ak_bin), "whoami", "--json"],
        capture_output=True, text=True,
    )
    if whoami.returncode != 0:
        return False, set()
    try:
        payload = json.loads(whoami.stdout)
    except json.JSONDecodeError:
        return False, set()
    data = payload.get("data", {})
    if not data.get("authenticated"):
        return False, set()
    active_kits = {
        entry["kitId"]
        for entry in data.get("licenses") or []
        if isinstance(entry, dict) and entry.get("status") == "active" and entry.get("kitId")
    }
    return True, active_kits


def kit_pin_matches(kit_dir, expected_pin):
    pin_file = kit_dir / ".pin.json"
    skills_dir = kit_dir / "skills"
    if not pin_file.is_file() or not skills_dir.is_dir():
        return False
    try:
        return json.loads(pin_file.read_text()) == expected_pin
    except (OSError, json.JSONDecodeError):
        return False


def sync_agentkit(config, require=False, root=ROOT):
    if not config:
        return []
    cli_version = validate_token("agentkit.cli_version", config.get("cli_version"))
    installer_sha256 = config.get("installer_sha256")
    if not isinstance(installer_sha256, str) or not SHA256_HEX.match(installer_sha256):
        raise ValueError(f"Invalid agentkit.installer_sha256: {installer_sha256!r}")
    channel = validate_token("agentkit.channel", config.get("channel", "stable"))
    target = validate_token("agentkit.target", config.get("target", "portable"))
    kits = config.get("kits") or {}
    validated_kits = [
        (validate_token("agentkit kit name", name), validate_token(f"agentkit kit version for {name}", version))
        for name, version in kits.items()
    ]
    if not validated_kits:
        return []

    kits_root = root / ".upstream" / "agentkit" / "kits"
    kits_root.mkdir(parents=True, exist_ok=True)
    ak_bin = root / ".upstream" / "agentkit" / "bin" / "ak"

    pins = {
        name: {"cli_version": cli_version, "channel": channel, "target": target, "version": version}
        for name, version in validated_kits
    }
    all_cached = all(kit_pin_matches(kits_root / name, pins[name]) for name, _ in validated_kits)
    if all_cached and ak_version_matches(ak_bin, cli_version):
        for name, version in validated_kits:
            print(f"agentkit/{name}: {version} (cached)")
        return [kits_root / name / "skills" for name, _ in validated_kits]

    ak_bin = ensure_ak_cli(cli_version, installer_sha256, root=root)
    if all_cached:
        for name, version in validated_kits:
            print(f"agentkit/{name}: {version} (cached)")
        return [kits_root / name / "skills" for name, _ in validated_kits]

    authenticated, active_kits = ensure_ak_auth(ak_bin)
    if not authenticated:
        message = "AgentKit not authenticated: set AGENTKIT_API_KEY or run './scripts/ak login'"
        if require:
            raise ValueError(message)
        print(f"Notice: {message}; skipping AgentKit skills.", file=sys.stderr)
        return []

    skill_dirs = []
    for name, version in validated_kits:
        kit_dir = kits_root / name
        if kit_pin_matches(kit_dir, pins[name]):
            print(f"agentkit/{name}: {version} (cached)")
            skill_dirs.append(kit_dir / "skills")
            continue
        if name not in active_kits:
            print(f"Notice: agentkit/{name} is not licensed for this account; skipping.", file=sys.stderr)
            continue
        with tempfile.TemporaryDirectory(dir=kits_root) as temp:
            temp_path = Path(temp)
            export_root = temp_path / "export"
            export_root.mkdir()
            subprocess.run(
                [
                    str(ak_bin), "kit", "init", name,
                    "--target", target,
                    "--channel", channel,
                    "--version", version,
                    "--out", str(export_root),
                    "--yes", "--no-interactive",
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            skills_src = export_root / f"agentkit-{target}" / "skills"
            if not skills_src.is_dir() or not list(skills_src.glob("*/SKILL.md")):
                raise ValueError(f"agentkit/{name}: exported kit has no skills under {skills_src.relative_to(export_root)}")
            staged = temp_path / "staged"
            staged.mkdir()
            shutil.copytree(skills_src, staged / "skills")
            (staged / ".pin.json").write_text(json.dumps(pins[name], indent=2) + "\n")
            if kit_dir.exists():
                kit_dir.rename(temp_path / "previous")
            staged.rename(kit_dir)
        print(f"agentkit/{name}: {version}")
        skill_dirs.append(kit_dir / "skills")
    if require and not skill_dirs:
        raise ValueError("No licensed AgentKit kits available to sync")
    return skill_dirs


def sync_skills(plugins, packages, agentkit_skill_dirs=(), root=ROOT):
    target = root / ".agents" / "skills"
    target.parent.mkdir(exist_ok=True)
    if target.is_symlink() or (target.exists() and not (target / MANAGED).is_file()):
        raise ValueError(f"{target} exists and is not managed by this stack")
    with tempfile.TemporaryDirectory(dir=target.parent) as temp:
        staged = Path(temp) / "skills"
        staged.mkdir()
        for source in sorted(plugins.glob("*/skills/*")):
            if source.is_dir():
                shutil.copytree(source, staged / source.name)
        for skill_id, (name, checksum) in packages.items():
            if not skill_id.isdecimal() or name != Path(name).name or name in {"", ".", ".."}:
                raise ValueError(f"Invalid skill lock entry: {skill_id!r}, {name!r}")
            with urlopen(f"https://ezyplatform.com/api/v1/skill-library/skills/{skill_id}/package", timeout=30) as response:
                body = response.read(MAX_PACKAGE_SIZE + 1)
            if len(body) > MAX_PACKAGE_SIZE:
                raise ValueError(f"{name}: downloaded package too large")
            extract_skill(body, checksum, staged / name)

        ezy_skills = {entry.name for entry in staged.iterdir() if entry.is_dir()}
        for skills_dir in agentkit_skill_dirs:
            for source in sorted(skills_dir.iterdir()):
                if source.is_symlink():
                    raise ValueError(f"AgentKit skill {source.name!r} is a symlink")
                if not source.is_dir() or not (source / "SKILL.md").is_file():
                    continue
                if source.name in ezy_skills:
                    raise ValueError(f"AgentKit skill {source.name!r} collides with EzyPlatform skill")
                destination = staged / source.name
                if destination.exists():
                    if tree_digest(destination) != tree_digest(source):
                        raise ValueError(f"Conflicting AgentKit skill {source.name!r} across kits")
                    continue
                shutil.copytree(source, destination)

        (staged / MANAGED).touch()
        if target.exists():
            target.rename(Path(temp) / "previous")
        staged.rename(target)
    print(f"{len(list(target.glob('*/SKILL.md')))} skills in {target.relative_to(root)}")


def main():
    lock = json.loads((ROOT / "upstream.lock.json").read_text())
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-only", action="store_true", help="Sync Docker and CLI only")
    parser.add_argument("--skip-agentkit", action="store_true", help="Skip syncing AgentKit CLI and kits")
    parser.add_argument("--require-agentkit", action="store_true", help="Fail if AgentKit cannot be synced")
    args = parser.parse_args()
    if args.skip_agentkit and args.require_agentkit:
        raise ValueError("--skip-agentkit and --require-agentkit cannot be combined")
    sources = {name: checkout(name, revision) for name, revision in lock["git"].items()
               if not args.runtime_only or name != "agents-plugins"}
    if not args.runtime_only:
        agentkit_dirs = []
        if not args.skip_agentkit:
            agentkit_dirs = sync_agentkit(lock.get("agentkit"), require=args.require_agentkit)
        sync_skills(sources["agents-plugins"], lock["skill_library"], agentkit_skill_dirs=agentkit_dirs)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Sync failed: {error}") from error
