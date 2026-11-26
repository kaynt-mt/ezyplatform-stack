#!/usr/bin/env python3
import argparse
import hashlib
import io
import json
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ".generated-by-sync-upstream"
MAX_PACKAGE_SIZE = 16 * 1024 * 1024


def git(directory, *args):
    return subprocess.run(["git", "-C", str(directory), *args], check=True,
                          text=True, stdout=subprocess.PIPE).stdout.strip()


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


def sync_skills(plugins, packages):
    target = ROOT / ".agents" / "skills"
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
        (staged / MANAGED).touch()
        if target.exists():
            target.rename(Path(temp) / "previous")
        staged.rename(target)
    print(f"{len(list(target.glob('*/SKILL.md')))} skills in {target.relative_to(ROOT)}")


def main():
    lock = json.loads((ROOT / "upstream.lock.json").read_text())
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-only", action="store_true", help="Sync Docker and CLI only")
    args = parser.parse_args()
    sources = {name: checkout(name, revision) for name, revision in lock["git"].items()
               if not args.runtime_only or name != "agents-plugins"}
    if not args.runtime_only:
        sync_skills(sources["agents-plugins"], lock["skill_library"])


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Sync failed: {error}") from error
