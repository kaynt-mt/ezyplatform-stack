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

    def test_rejects_sdk_success_without_generated_project_and_removes_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(PLUGIN.subprocess, "run"):
            with self.assertRaisesRegex(ValueError, "SDK did not generate the project POM"):
                self.create(Path(temp))
            self.assertFalse((Path(temp) / "pilot-plugin").exists())

    def test_preserves_nonempty_directory_for_inspection_after_scaffold_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "pilot-plugin"

            def sdk(command, *, input, text, check):
                (project / "partial.txt").write_text("partial SDK output", encoding="utf-8")
                return subprocess.CompletedProcess(command, 1)

            with mock.patch.object(PLUGIN.subprocess, "run", side_effect=sdk):
                with self.assertRaisesRegex(ValueError, "inspect any files left"):
                    self.create(Path(temp))
            self.assertEqual((project / "partial.txt").read_text(encoding="utf-8"), "partial SDK output")


class ProjectZipTests(unittest.TestCase):
    def test_accepts_shared_sdk_for_project_with_ezyplatform_prefix(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ezyplatform-inventory-1.0.0.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr(
                    "ezyplatform-inventory/web/plugins/ezyplatform-inventory/lib/"
                    "ezyplatform-inventory-sdk-1.0.0.jar",
                    "project SDK",
                )
            PLUGIN.check_zip(path)

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


class UploadApplyTests(unittest.TestCase):
    def test_upload_apply_checks_zip_and_calls_installer_in_order(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "pilot.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("pilot/web/plugins/pilot/lib/pilot-web-plugin-1.0.0.jar", "sample")
            calls = []

            def request(opener, admin_url, path, method="GET", data=None, headers=None):
                calls.append((path, method, data))
                return 204, ""

            with mock.patch.object(PLUGIN, "open_admin_session", return_value="opener") as login, \
                    mock.patch.object(PLUGIN, "upload_project_zip", return_value=(200, '{"projectName":"pilot"}')), \
                    mock.patch.object(PLUGIN, "admin_request", side_effect=request):
                result = PLUGIN.upload_and_apply_zip(
                    "http://admin.test", "admin", "secret", path
                )
            login.assert_called_once_with("http://admin.test", "admin", "secret")
            self.assertEqual(calls, [
                ("/api/v1/projects/check-dependencies", "GET", None),
                ("/api/v1/platform/install", "POST", b""),
            ])
            self.assertEqual(result["upload_status"], 200)
            self.assertEqual(result["check_dependencies_status"], 204)
            self.assertEqual(result["platform_install_status"], 204)
            self.assertEqual(result["upload_response"], {"projectName": "pilot"})

    def test_upload_apply_rejects_damaged_zip_before_login(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(PLUGIN, "open_admin_session") as login:
            path = Path(temp) / "pilot.zip"
            path.write_text("not a zip", encoding="utf-8")
            with self.assertRaises(Exception):
                PLUGIN.upload_and_apply_zip("http://admin.test", "admin", "secret", path)
            login.assert_not_called()

    def test_rejects_plain_http_remote_admin_before_login(self):
        with self.assertRaisesRegex(ValueError, "must use HTTPS"):
            PLUGIN.open_admin_session("http://admin.example.test", "admin", "secret")

    def test_password_file_preserves_spaces_and_removes_only_newline(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            password = root / "password"
            password.write_text("  secret with spaces  \n", encoding="utf-8")
            archive = root / "pilot.zip"
            archive.touch()
            argv = [
                "ezy-plugin.py", "upload-apply", str(archive),
                "--password-file", str(password),
            ]
            with mock.patch("sys.argv", argv), \
                    mock.patch.object(PLUGIN, "upload_and_apply_zip", return_value={}) as upload:
                PLUGIN.main()
            self.assertEqual(upload.call_args.args[1], "admin")
            self.assertEqual(upload.call_args.args[2], "  secret with spaces  ")
