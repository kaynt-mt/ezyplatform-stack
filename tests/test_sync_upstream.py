import hashlib
import importlib.util
import io
import stat
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZipInfo

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync-upstream.py"
SPEC = importlib.util.spec_from_file_location("sync_upstream", SCRIPT)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


def package(*entries):
    buffer = io.BytesIO()
    with ZipFile(buffer, "w") as archive:
        for name, data in entries:
            archive.writestr(name, data)
    body = buffer.getvalue()
    return body, hashlib.sha256(body).hexdigest()


class SkillPackageTests(unittest.TestCase):
    def test_extracts_complete_skill(self):
        body, checksum = package(("SKILL.md", "skill"), ("scripts/tool.py", "script"))
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "skill"
            SYNC.extract_skill(body, checksum, destination)
            self.assertEqual((destination / "SKILL.md").read_text(), "skill")
            self.assertEqual((destination / "scripts" / "tool.py").read_text(), "script")

    def test_rejects_changed_package(self):
        body, _ = package(("SKILL.md", "skill"))
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                SYNC.extract_skill(body, "0" * 64, Path(temp) / "skill")

    def test_rejects_paths_outside_skill_and_links(self):
        symlink = ZipInfo("script")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        for entry in ("../outside", "/outside", "..\\outside", symlink):
            with self.subTest(entry=entry), tempfile.TemporaryDirectory() as temp:
                destination = Path(temp) / "skill"
                body, checksum = package(("SKILL.md", "skill"), (entry, "outside"))
                with self.assertRaisesRegex(ValueError, "unsafe ZIP path"):
                    SYNC.extract_skill(body, checksum, destination)
                self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
