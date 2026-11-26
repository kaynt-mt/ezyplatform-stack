import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ezy-plugin.py"
SPEC = importlib.util.spec_from_file_location("ezy_plugin", SCRIPT)
PLUGIN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLUGIN)


class CreateProjectTests(unittest.TestCase):
    def create(self, output, name="pilot-plugin"):
        return PLUGIN.create_project(
            name, ["--dir", "/native"], "com.example", "com.example.pilot",
            "admin-plugin,web-plugin", output,
        )

    def test_scaffolds_into_empty_directory_and_fixes_exclusions(self):
        def sdk(command, *, input, text, check):
            out = Path(command[command.index("-o") + 1])
            project = out / command[command.index("create") + 1]
            self.assertEqual(command[:7], [
                str(PLUGIN.EZY), "dev", "run", "--dir", "/native", "--", "ezy.sh",
            ])
            self.assertEqual(input, "yes\n")
            self.assertTrue(text and check)
            self.assertEqual(list(project.iterdir()), [])
            (project / "pom.xml").touch()
            for lane in ("admin", "web"):
                module = project / f"pilot-plugin-{lane}-plugin"
                module.mkdir()
                (module / "assembly.xml").write_text(
                    f"<assembly><exclude>com.example:ezyplatform-{lane}-sdk</exclude>"
                    "<exclude>com.example:other-library</exclude>"
                    "<exclude>org.youngmonkeys:ezyplatform-common</exclude></assembly>",
                    encoding="utf-8",
                )
            return subprocess.CompletedProcess(command, 0)

        with tempfile.TemporaryDirectory() as temp, mock.patch.object(PLUGIN.subprocess, "run", side_effect=sdk):
            project = self.create(Path(temp))
            for lane in ("admin", "web"):
                assembly = (project / f"pilot-plugin-{lane}-plugin" / "assembly.xml").read_text(encoding="utf-8")
                self.assertIn(f"<exclude>org.youngmonkeys:ezyplatform-{lane}-sdk</exclude>", assembly)
                self.assertIn("<exclude>com.example:other-library</exclude>", assembly)
                self.assertIn("<exclude>org.youngmonkeys:ezyplatform-common</exclude>", assembly)

    def test_never_invokes_sdk_for_existing_directory_or_invalid_name(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(PLUGIN.subprocess, "run") as run:
            output = Path(temp)
            (output / "pilot-plugin").mkdir()
            with self.assertRaisesRegex(ValueError, "already exists"):
                self.create(output)
            with self.assertRaisesRegex(ValueError, "Project name"):
                self.create(output, "../other")
            run.assert_not_called()

    def test_rejects_sdk_success_without_generated_project(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(PLUGIN.subprocess, "run"):
            with self.assertRaisesRegex(ValueError, "SDK did not generate the project POM"):
                self.create(Path(temp))


class ProjectZipTests(unittest.TestCase):
    def test_accepts_sample_jars(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "pilot.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("pilot/web/plugins/pilot/lib/pilot-web-plugin-1.0.0.jar", "sample")
            PLUGIN.check_zip(path)

    def test_rejects_bundled_core_jars(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "pilot.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("pilot/web/plugins/pilot/lib/ezyplatform-web-sdk-0.0.2.jar", "sdk")
                archive.writestr("pilot/admin/plugins/pilot/lib/ezyplatform-admin-0.0.2.jar", "admin")
            with self.assertRaisesRegex(ValueError, "core JARs: .*web-sdk-0.0.2.jar, .*admin-0.0.2.jar"):
                PLUGIN.check_zip(path)

    def test_rejects_empty_zip(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "pilot.zip"
            with ZipFile(path, "w"):
                pass
            with self.assertRaisesRegex(ValueError, "ZIP is empty"):
                PLUGIN.check_zip(path)
