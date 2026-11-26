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
CREATE_RUN_PATCHED = '''    if ! "${cmd[@]}" <<< "yes" >&2; then
        rmdir "$out/$name" 2>/dev/null || true
        die "ezy.sh create failed"
    fi
'''
CREATE_POM_CHECK = '''    [ -f "$out/$name/pom.xml" ] || die "project was not created"
'''
CREATE_POM_CHECK_PATCHED = '''    if [ ! -f "$out/$name/pom.xml" ]; then
        rmdir "$out/$name" 2>/dev/null || true
        die "project was not created"
    fi
'''


def without_yaml_comment(line):
    """Remove a YAML plain-scalar comment, honoring single and double quotes."""
    quote = None
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = None
        elif quote == "'":
            if char == "'":
                if index + 1 < len(line) and line[index + 1] == "'":
                    index += 1
                else:
                    quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index]
        index += 1
    return line


def yaml_scalar(text):
    """Return the scalar forms used for Compose image tags, without quotes/comments."""
    value = without_yaml_comment(text).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        quote = value[0]
        value = value[1:-1]
        if quote == "'":
            value = value.replace("''", "'")
    return value


def compose_core_image(root):
    """Image tag built by this stack's compose.yaml for the pinned core."""
    in_service = False
    for raw_line in (root / "compose.yaml").read_text(encoding="utf-8").splitlines():
        line = without_yaml_comment(raw_line).rstrip()
        if re.match(r"^  ezyplatform:\s*$", line):
            in_service = True
            continue
        if in_service and re.match(r"^  [A-Za-z0-9_-]+:\s*$", line):
            in_service = False
        if in_service:
            match = re.match(r"^    image:\s*(.*?)\s*$", line)
            if match:
                image = yaml_scalar(match.group(1))
                if image:
                    return image
    raise ValueError("compose.yaml does not define the ezyplatform image")


def requested_new_mode(args):
    """The --mode value as argparse reads it, including unambiguous abbreviations."""
    mode = None
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--":
            break
        option, separator, inline_value = arg.partition("=")
        name = option[2:] if option.startswith("--") else ""
        if name and "mode".startswith(name):
            if separator:
                mode = inline_value
            elif index + 1 < len(args):
                mode = args[index + 1]
                index += 1
        index += 1
    return mode


def needs_local_image(argv):
    """Whether this invocation can create a local Compose project."""
    if len(argv) < 2 or argv[1] != "new":
        return False
    mode = requested_new_mode(argv[2:])
    if mode is not None:
        return mode in {"local", "both"}
    return sys.stdin.isatty()


def patch_ezydev_script(text):
    """Make SDK 0.2.8 project creation write into the directory it expects.

    The SDK writes <out>/<name>/pom.xml without first creating <out>/<name>.
    Creating the empty directory here is safe because the CLI has already
    rejected an existing target; the SDK's overwrite confirmation receives
    "yes" for that empty directory. If creation fails before writing anything,
    rmdir removes only that empty directory so a corrected retry can run.
    """
    originals = (CREATE_SETUP, CREATE_RUN, CREATE_POM_CHECK)
    if any(original not in text for original in originals):
        raise ValueError("pinned ezydev.sh no longer matches the SDK scaffold patch")
    return (
        text.replace(CREATE_SETUP, CREATE_SETUP_PATCHED, 1)
        .replace(CREATE_RUN, CREATE_RUN_PATCHED, 1)
        .replace(CREATE_POM_CHECK, CREATE_POM_CHECK_PATCHED, 1)
    )


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

    if needs_local_image(argv) and "EZY_LOCAL_IMAGE" not in os.environ:
        try:
            os.environ["EZY_LOCAL_IMAGE"] = compose_core_image(root)
        except (OSError, ValueError) as error:
            print(f"ezy: cannot determine the stack's local core image: {error}", file=sys.stderr)
            return 1

    from ezyplatform_cli import cli

    sys.argv = [str(root / "scripts" / "ezy"), *argv[1:]]
    if len(argv) > 2 and argv[1] == "dev" and argv[2] == "create":
        with tempfile.TemporaryDirectory(prefix="ezy-cli-skills-") as temporary:
            cli.SKILLS = str(patched_skills_tree(cli.SKILLS, temporary))
            return cli.main()
    return cli.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
