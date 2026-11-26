import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ezy_runner.py"
SPEC = importlib.util.spec_from_file_location("ezy_runner", SCRIPT)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)

REPO = Path(__file__).resolve().parents[1]

SCAFFOLD_SNIPPET = '''create_command() {
    require_dev
    mkdir -p "$out"
    local cmd=(ezy.sh create "$name" -g "$group" -o "$out")
    [ -n "$OPT_PACKAGE" ] && cmd+=(-p "$OPT_PACKAGE")
    log "${cmd[*]}"
    "${cmd[@]}" < /dev/null >&2 || die "ezy.sh create failed"
    [ -f "$out/$name/pom.xml" ] || die "project was not created"
}
'''


class ComposeCoreImageTests(unittest.TestCase):
    def write_compose(self, root, image_line):
        (root / "compose.yaml").write_text(
            "services:\n"
            "  mysql:\n"
            "    image: mysql:8.0\n"
            "  ezyplatform:\n"
            f"    image: {image_line}\n"
            "    build:\n"
            "      context: .upstream/ezyplatform-docker\n",
            encoding="utf-8",
        )

    def test_reads_only_ezyplatform_service_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_compose(root, "ezyplatform-stack/core:1.5.9-1.5.6-84a5a5d")
            self.assertEqual(
                RUNNER.compose_core_image(root),
                "ezyplatform-stack/core:1.5.9-1.5.6-84a5a5d",
            )

    def test_accepts_inline_comments_and_quotes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_compose(root, '"ezyplatform-stack/core:1.5.9"  # pinned core')
            self.assertEqual(RUNNER.compose_core_image(root), "ezyplatform-stack/core:1.5.9")

    def test_hash_inside_unquoted_scalar_is_not_a_comment(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_compose(root, "example/core:tag#suffix")
            self.assertEqual(RUNNER.compose_core_image(root), "example/core:tag#suffix")

    def test_rejects_compose_without_core_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "compose.yaml").write_text("services: {}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ezyplatform image"):
                RUNNER.compose_core_image(root)


class LocalImageNeedTests(unittest.TestCase):
    def test_only_new_local_or_both_need_the_image_before_prompting(self):
        self.assertFalse(RUNNER.needs_local_image(["root", "--version"]))
        self.assertFalse(RUNNER.needs_local_image(["root", "new", "app", "--mode", "live"]))
        self.assertTrue(RUNNER.needs_local_image(["root", "new", "app", "--mode", "local"]))
        self.assertTrue(RUNNER.needs_local_image(["root", "new", "app", "--mode=both"]))

    def test_matches_argparse_abbreviations_and_end_of_options(self):
        self.assertEqual(RUNNER.requested_new_mode(["app", "--mo", "local"]), "local")
        self.assertEqual(RUNNER.requested_new_mode(["app", "--mod=both"]), "both")
        self.assertEqual(RUNNER.requested_new_mode(["app", "--m", "local"]), "local")
        self.assertIsNone(RUNNER.requested_new_mode(["app", "--", "--mode", "local"]))
        self.assertIsNone(RUNNER.requested_new_mode(["app", "--modefoo", "local"]))


class EzydevPatchTests(unittest.TestCase):
    def test_precreates_project_directory_and_answers_empty_dir_prompt(self):
        patched = RUNNER.patch_ezydev_script(SCAFFOLD_SNIPPET)
        self.assertIn('mkdir "$out/$name"', patched)
        self.assertIn('if ! "${cmd[@]}" <<< "yes" >&2; then', patched)
        self.assertNotIn('"${cmd[@]}" < /dev/null', patched)

    def test_removes_only_empty_project_directory_after_scaffold_failure(self):
        patched = RUNNER.patch_ezydev_script(SCAFFOLD_SNIPPET)
        self.assertEqual(patched.count('rmdir "$out/$name" 2>/dev/null || true'), 2)
        self.assertIn('if [ ! -f "$out/$name/pom.xml" ]; then', patched)
        self.assertNotIn('[ -f "$out/$name/pom.xml" ] || die', patched)

    def test_rejects_changed_upstream_script_instead_of_silently_skipping(self):
        with self.assertRaisesRegex(ValueError, "scaffold patch"):
            RUNNER.patch_ezydev_script("create_command() {\n}\n")

    def test_copies_skills_tree_and_patches_only_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            script = source / "ezy-develop" / "scripts"
            script.mkdir(parents=True)
            (script / "ezydev.sh").write_text(SCAFFOLD_SNIPPET, encoding="utf-8")
            (source / "VENDORED.json").write_text("{}", encoding="utf-8")

            copied = RUNNER.patched_skills_tree(source, root / "temporary")

            self.assertEqual((source / "ezy-develop" / "scripts" / "ezydev.sh").read_text(encoding="utf-8"), SCAFFOLD_SNIPPET)
            copied_script = (copied / "ezy-develop" / "scripts" / "ezydev.sh").read_text(encoding="utf-8")
            self.assertIn('mkdir "$out/$name"', copied_script)
            self.assertTrue((copied / "VENDORED.json").is_file())


class LauncherIntegrationTests(unittest.TestCase):
    def make_checkout(self, root):
        scripts = root / "scripts"
        scripts.mkdir()
        for name in ("ezy", "ezy_runner.py"):
            shutil.copy2(REPO / "scripts" / name, scripts / name)
        (root / "compose.yaml").write_text((REPO / "compose.yaml").read_text(encoding="utf-8"), encoding="utf-8")
        package = root / ".upstream" / "ezyplatform-cli" / "src" / "ezyplatform_cli"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        skills = package / "skills" / "ezy-develop" / "scripts"
        skills.mkdir(parents=True)
        (skills / "ezydev.sh").write_text(SCAFFOLD_SNIPPET, encoding="utf-8")
        (package / "cli.py").write_text(
            "import os\n"
            f"SKILLS = {str(package / 'skills')!r}\n"
            "def main():\n"
            "    print('image=' + os.environ.get('EZY_LOCAL_IMAGE', ''))\n"
            "    print('skills=' + SKILLS)\n"
            "    if os.environ.get('PRINT_EZYDEV'):\n"
            "        print(open(os.path.join(SKILLS, 'ezy-develop/scripts/ezydev.sh')).read())\n"
            "    return 0\n",
            encoding="utf-8",
        )
        return scripts / "ezy"

    def run_ezy(self, ezy, *args, env=None, check=True):
        env = os.environ.copy() if env is None else env
        env.pop("EZY_LOCAL_IMAGE", None)
        return subprocess.run([str(ezy), *args], capture_output=True, text=True, env=env, check=check)

    def test_local_new_pins_local_image_and_keeps_user_override(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            ezy = self.make_checkout(root)

            for mode_args in (("--mode", "local"), ("--mo", "local"), ("--mod=both",)):
                first = self.run_ezy(ezy, "new", "app", *mode_args)
                self.assertIn("image=ezyplatform-stack/core:1.5.9-1.5.6-84a5a5d", first.stdout)

            env = os.environ.copy()
            env["EZY_LOCAL_IMAGE"] = "example/custom:1"
            second = subprocess.run(
                [str(ezy), "new", "app", "--mode", "local"],
                capture_output=True,
                text=True,
                env=env,
                check=True,
            )
            self.assertIn("image=example/custom:1", second.stdout)

    def test_unrelated_live_and_override_commands_do_not_read_compose_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            ezy = self.make_checkout(root)
            (root / "compose.yaml").write_text("services: {}\n", encoding="utf-8")

            version = self.run_ezy(ezy, "--version")
            self.assertIn("image=\n", version.stdout)
            live = self.run_ezy(ezy, "new", "app", "--mode", "live")
            self.assertIn("image=\n", live.stdout)

            env = os.environ.copy()
            env["EZY_LOCAL_IMAGE"] = "example/custom:1"
            override = subprocess.run(
                [str(ezy), "new", "app", "--mode", "local"],
                capture_output=True,
                text=True,
                env=env,
                check=True,
            )
            self.assertIn("image=example/custom:1", override.stdout)

    def test_local_new_reports_missing_compose_image_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            ezy = self.make_checkout(root)
            (root / "compose.yaml").write_text("services: {}\n", encoding="utf-8")

            result = self.run_ezy(ezy, "new", "app", "--mode", "local", check=False)

            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot determine the stack's local core image", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_only_dev_create_uses_patched_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            ezy = self.make_checkout(root)
            original_skills = root / ".upstream" / "ezyplatform-cli" / "src" / "ezyplatform_cli" / "skills"
            env = os.environ.copy()
            env["PRINT_EZYDEV"] = "1"

            create = subprocess.run(
                [str(ezy), "dev", "create"], capture_output=True, text=True, env=env, check=True,
            )
            self.assertIn('mkdir "$out/$name"', create.stdout)
            patched_path = next(
                line.removeprefix("skills=") for line in create.stdout.splitlines() if line.startswith("skills=")
            )
            self.assertNotEqual(patched_path, str(original_skills))

            status = subprocess.run(
                [str(ezy), "dev", "status"], capture_output=True, text=True, env=env, check=True,
            )
            self.assertIn(f"skills={original_skills}", status.stdout)
            self.assertNotIn('mkdir "$out/$name"', status.stdout)

            plain = subprocess.run(
                [str(ezy), "skills-path"], capture_output=True, text=True, env=env, check=True,
            )
            self.assertIn(f"skills={original_skills}", plain.stdout)
            self.assertNotIn('mkdir "$out/$name"', plain.stdout)


if __name__ == "__main__":
    unittest.main()
