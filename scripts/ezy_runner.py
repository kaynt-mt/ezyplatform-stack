#!/usr/bin/env python3
"""Stack integration layer for the pinned upstream ezy CLI.

The upstream checkout under .upstream stays byte-for-byte clean. Runtime-only
compatibility patches are applied to a temporary copy of its small skills tree.
"""
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

CREATE_SETUP = '''    require_dev
    mkdir -p "$out"
    local cmd=(ezy.sh create "$name" -g "$group" -o "$out")
'''
CREATE_SETUP_PATCHED = '''    require_dev
    mkdir -p "$out"
    mkdir "$out/$name"
    local cmd=(ezy.sh create "$name" -g "$group" -o "$out")
'''
CREATE_RUN = '''    "${cmd[@]}" < /dev/null >&2 || die "ezy.sh create failed"
'''
CREATE_RUN_PATCHED = '''    "${cmd[@]}" <<< "yes" >&2 || die "ezy.sh create failed"
'''


def compose_core_image(root):
    """Image tag built by this stack's compose.yaml for the pinned core."""
    in_service = False
    for line in (root / "compose.yaml").read_text(encoding="utf-8").splitlines():
        if re.match(r"^  ezyplatform:\s*$", line):
            in_service = True
            continue
        if in_service and re.match(r"^  [A-Za-z0-9_-]+:\s*$", line):
            in_service = False
        if in_service:
            match = re.match(r"^    image:\s*(\S+)\s*$", line)
            if match:
                return match.group(1).strip('"\'')
    raise ValueError("compose.yaml does not define the ezyplatform image")


def patch_ezydev_script(text):
    """Make SDK 0.2.8 project creation write into the directory it expects.

    The SDK writes <out>/<name>/pom.xml without first creating <out>/<name>.
    Creating the empty directory here is safe because the CLI has already
    rejected an existing target; the SDK's overwrite confirmation receives
    "yes" for that empty directory.
    """
    if CREATE_SETUP not in text or CREATE_RUN not in text:
        raise ValueError("pinned ezydev.sh no longer matches the SDK scaffold patch")
    return text.replace(CREATE_SETUP, CREATE_SETUP_PATCHED, 1).replace(CREATE_RUN, CREATE_RUN_PATCHED, 1)


def patched_skills_tree(source, temporary_root):
    """Copy the CLI's skills tree and apply stack compatibility patches."""
    copied = Path(temporary_root) / "skills"
    shutil.copytree(source, copied)
    ezydev = copied / "ezy-develop" / "scripts" / "ezydev.sh"
    ezydev.write_text(patch_ezydev_script(ezydev.read_text(encoding="utf-8")), encoding="utf-8")
    return copied


def main(argv):
    root = Path(argv[0]).resolve()
    source = root / ".upstream" / "ezyplatform-cli" / "src"
    package = source / "ezyplatform_cli"
    if not package.is_dir():
        print("Run python3 scripts/sync-upstream.py first.", file=sys.stderr)
        return 1
    sys.path.insert(0, str(source))
    os.environ.setdefault("EZY_LOCAL_IMAGE", compose_core_image(root))

    from ezyplatform_cli import cli

    sys.argv = [str(root / "scripts" / "ezy"), *argv[1:]]
    if len(argv) > 1 and argv[1] == "dev":
        with tempfile.TemporaryDirectory(prefix="ezy-cli-skills-") as temporary:
            cli.SKILLS = str(patched_skills_tree(cli.SKILLS, temporary))
            return cli.main()
    return cli.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
