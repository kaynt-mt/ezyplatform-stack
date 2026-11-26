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
    def test_reads_only_ezyplatform_service_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "compose.yaml").write_text(
                "services:\n"
                "  mysql:\n"
                "    image: mysql:8.0\n"
                "  ezyplatform:\n"
                "    image: ezyplatform-stack/core:1.5.9-1.5.6-84a5a5d\n"
                "    build:\n"
                "      context: .upstream/ezyplatform-docker\n",
                encoding="utf-8",
            )
            self.assertEqual(
                RUNNER.compose_core_image(root),
                "ezyplatform-stack/core:1.5.9-1.5.6-84a5a5d",
            )

    def test_rejects_compose_without_core_image(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "compose.yaml").write_text("services: {}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ezyplatform image"):
                RUNNER.compose_core_image(root)


class EzydevPatchTests(unittest.TestCase):
    def test_precreates_project_directory_and_answers_empty_dir_prompt(self):
        patched = RUNNER.patch_ezydev_script(SCAFFOLD_SNIPPET)
        self.assertIn('mkdir "$out/$name"', patched)
        self.assertIn('"${cmd[@]}" <<< "yes" >&2', patched)
        self.assertNotIn('"${cmd[@]}" < /dev/null', patched)

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
            self.assertIn('mkdir "$out/$name"', (copied / "ezy-develop" / "scripts" / "ezydev.sh").read_text(encoding="utf-8"))
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

    def test_launcher_pins_local_image_and_keeps_user_override(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            ezy = self.make_checkout(root)
            env = os.environ.copy()
            env.pop("EZY_LOCAL_IMAGE", None)

            first = subprocess.run([str(ezy), "--version"], capture_output=True, text=True, env=env, check=True)
            self.assertIn("image=ezyplatform-stack/core:1.5.9-1.5.6-84a5a5d", first.stdout)

            env["EZY_LOCAL_IMAGE"] = "example/custom:1"
            second = subprocess.run([str(ezy), "--version"], capture_output=True, text=True, env=env, check=True)
            self.assertIn("image=example/custom:1", second.stdout)

    def test_dev_uses_patched_copy_without_hiding_normal_skills_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "checkout"
            root.mkdir()
            ezy = self.make_checkout(root)
            original_skills = root / ".upstream" / "ezyplatform-cli" / "src" / "ezyplatform_cli" / "skills"
            env = os.environ.copy()
            env["PRINT_EZYDEV"] = "1"

            dev = subprocess.run([str(ezy), "dev", "create"], capture_output=True, text=True, env=env, check=True)
            self.assertIn('mkdir "$out/$name"', dev.stdout)
            patched_path = next(line.removeprefix("skills=") for line in dev.stdout.splitlines() if line.startswith("skills="))
            self.assertNotEqual(patched_path, str(original_skills))

            plain = subprocess.run([str(ezy), "skills-path"], capture_output=True, text=True, env=env, check=True)
            self.assertIn(f"skills={original_skills}", plain.stdout)
            self.assertNotIn('mkdir "$out/$name"', plain.stdout)


if __name__ == "__main__":
    unittest.main()
