import hashlib
import importlib.util
import io
import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock
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


def make_skill(root, name, content="skill body"):
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(content)
    return skill_dir


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


class EzySnapshotTests(unittest.TestCase):
    def test_refresh_replaces_only_managed_snapshot_with_complete_sources(self):
        body, checksum = package(("SKILL.md", "library skill"), ("scripts/tool.py", "tool"))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugins = root / "plugins"
            make_skill(plugins / "core" / "skills", "ezy-guide", "cppai skill")
            shared = plugins / "core" / "skills" / "ezy-shared"
            shared.mkdir()
            (shared / "helper.py").write_text("helper")
            (plugins / "LICENSE").write_text("CPPAI license")
            make_skill(root / ".agents" / "skills", "ak-plan")
            snapshot = root / "skills" / "upstream"
            make_skill(snapshot, "stale")
            (snapshot / SYNC.MANAGED).touch()
            make_skill(root / "skills", "stack-guide")

            with mock.patch.object(SYNC, "urlopen", return_value=io.BytesIO(body)) as download:
                SYNC.refresh_ezy_skills(plugins, {"42": ["ezyplatform-example", checksum]}, root=root)

            download.assert_called_once_with("https://ezyplatform.com/api/v1/skill-library/skills/42/package", timeout=30)
            self.assertEqual({p.parent.name for p in snapshot.glob("*/SKILL.md")}, {"ezy-guide", "ezyplatform-example"})
            self.assertEqual((snapshot / "ezyplatform-example" / "scripts" / "tool.py").read_text(), "tool")
            self.assertEqual((snapshot / "ezy-shared" / "helper.py").read_text(), "helper")
            self.assertEqual((snapshot / "LICENSE-CPPAI").read_text(), "CPPAI license")
            self.assertTrue((snapshot / SYNC.MANAGED).is_file())
            self.assertTrue((root / ".agents" / "skills" / "ak-plan" / "SKILL.md").is_file())
            self.assertTrue((root / "skills" / "stack-guide" / "SKILL.md").is_file())

    def test_refresh_rejects_unmanaged_snapshot_and_preserves_snapshot_on_checksum_failure(self):
        body, _ = package(("SKILL.md", "library skill"))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugins = root / "plugins"
            snapshot = root / "skills" / "upstream"
            original = make_skill(snapshot, "original", "keep")
            packages = {"42": ["ezyplatform-example", "0" * 64]}
            with mock.patch.object(SYNC, "urlopen") as download:
                with self.assertRaisesRegex(ValueError, "not managed"):
                    SYNC.refresh_ezy_skills(plugins, packages, root=root)
                download.assert_not_called()

            (snapshot / SYNC.MANAGED).touch()
            with mock.patch.object(SYNC, "urlopen", return_value=io.BytesIO(body)):
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    SYNC.refresh_ezy_skills(plugins, packages, root=root)
            self.assertEqual((original / "SKILL.md").read_text(), "keep")


class AgentKitSyncTests(unittest.TestCase):
    def test_merges_agentkit_skills_and_deduplicates_identical_overlap(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugins = root / "plugins"
            make_skill(plugins / "core" / "skills", "ezy-guide", "ezy")

            eng = root / "ak-eng"
            make_skill(eng, "ak-plan", "shared plan")
            make_skill(eng, "ak-cook", "eng only")

            mkt = root / "ak-mkt"
            make_skill(mkt, "ak-plan", "shared plan")
            make_skill(mkt, "ak-brand", "mkt only")

            SYNC.sync_skills(plugins, {}, agentkit_skill_dirs=[eng, mkt], root=root)
            installed = sorted(p.parent.name for p in (root / ".agents" / "skills").glob("*/SKILL.md"))
            self.assertEqual(installed, ["ak-brand", "ak-cook", "ak-plan", "ezy-guide"])

    def test_rejects_conflicting_agentkit_skill_across_kits(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugins = root / "plugins"
            plugins.mkdir()

            eng = root / "ak-eng"
            make_skill(eng, "ak-plan", "version A")
            mkt = root / "ak-mkt"
            make_skill(mkt, "ak-plan", "version B")

            with self.assertRaisesRegex(ValueError, "Conflicting AgentKit skill"):
                SYNC.sync_skills(plugins, {}, agentkit_skill_dirs=[eng, mkt], root=root)

    def test_rejects_agentkit_collision_with_ezyplatform_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plugins = root / "plugins"
            make_skill(plugins / "core" / "skills", "ezy-guide", "ezy")

            eng = root / "ak-eng"
            make_skill(eng, "ezy-guide", "spoofed")

            with self.assertRaisesRegex(ValueError, "collides with EzyPlatform skill"):
                SYNC.sync_skills(plugins, {}, agentkit_skill_dirs=[eng], root=root)

    def test_rejects_invalid_agentkit_lock_tokens(self):
        good_sha = "a" * 64
        with tempfile.TemporaryDirectory() as temp:
            for bad in (
                {"cli_version": "../bad", "installer_sha256": good_sha, "kits": {"engineer": "3.2.0"}},
                {"cli_version": "3.2.0", "installer_sha256": "not-a-sha", "kits": {"engineer": "3.2.0"}},
                {"cli_version": "3.2.0", "installer_sha256": good_sha, "kits": {"../eng": "3.2.0"}},
                {"cli_version": "3.2.0", "installer_sha256": good_sha, "kits": {"engineer": "3.2.0;rm"}},
            ):
                with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "Invalid"):
                    SYNC.sync_agentkit(bad, root=Path(temp))

    def test_installer_verifies_sha256_and_strips_api_key(self):
        script = b"#!/bin/sh\nexit 0\n"
        good_sha = hashlib.sha256(script).hexdigest()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fake_resp = mock.MagicMock()
            fake_resp.__enter__.return_value = io.BytesIO(script)
            with mock.patch.object(SYNC, "urlopen", return_value=fake_resp):
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    SYNC.ensure_ak_cli("3.2.0", "0" * 64, root=root)

            fake_resp2 = mock.MagicMock()
            fake_resp2.__enter__.return_value = io.BytesIO(script)
            captured_env = {}

            def fake_run(cmd, input=None, env=None, check=False):
                captured_env.update(env or {})
                ak_bin = root / ".upstream" / "agentkit" / "bin" / "ak"
                ak_bin.write_text("#!/bin/sh\necho 'ak 3.2.0'\n")
                ak_bin.chmod(0o755)

            with mock.patch.dict("os.environ", {"AGENTKIT_API_KEY": "secret-val"}), \
                 mock.patch.object(SYNC, "urlopen", return_value=fake_resp2), \
                 mock.patch.object(SYNC.subprocess, "run", side_effect=fake_run):
                with mock.patch.object(SYNC, "ak_version_matches", side_effect=[False, True]):
                    SYNC.ensure_ak_cli("3.2.0", good_sha, root=root)
            self.assertNotIn("AGENTKIT_API_KEY", captured_env)
            self.assertEqual(captured_env["AK_VERSION"], "3.2.0")

    def test_uses_cached_agentkit_kits_without_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = {
                "cli_version": "3.2.0",
                "installer_sha256": "a" * 64,
                "channel": "stable",
                "target": "portable",
                "kits": {"engineer": "3.2.0"},
            }
            ak_bin = root / ".upstream" / "agentkit" / "bin" / "ak"
            ak_bin.parent.mkdir(parents=True)
            ak_bin.write_text("#!/bin/sh\necho 'ak 3.2.0'\n")
            ak_bin.chmod(0o755)

            kit_dir = root / ".upstream" / "agentkit" / "kits" / "engineer"
            make_skill(kit_dir / "skills", "ak-plan", "cached")
            (kit_dir / ".pin.json").write_text(json.dumps({
                "cli_version": "3.2.0",
                "channel": "stable",
                "target": "portable",
                "version": "3.2.0",
            }))

            with mock.patch.object(SYNC, "ensure_ak_auth", side_effect=AssertionError("should not auth")):
                dirs = SYNC.sync_agentkit(config, require=True, root=root)
            self.assertEqual(dirs, [kit_dir / "skills"])

    def test_skips_or_fails_when_unauthenticated(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = {
                "cli_version": "3.2.0",
                "installer_sha256": "a" * 64,
                "channel": "stable",
                "target": "portable",
                "kits": {"engineer": "3.2.0"},
            }
            fake_bin = root / ".upstream" / "agentkit" / "bin" / "ak"
            with mock.patch.dict("os.environ", {"AGENTKIT_API_KEY": "dummy"}), \
                 mock.patch.object(SYNC, "ensure_ak_cli", return_value=fake_bin), \
                 mock.patch.object(SYNC, "ensure_ak_auth", return_value=(False, set())):
                self.assertEqual(SYNC.sync_agentkit(config, require=False, root=root), [])
                with self.assertRaisesRegex(ValueError, "AgentKit not authenticated"):
                    SYNC.sync_agentkit(config, require=True, root=root)

    def test_skips_installer_on_windows(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = {
                "cli_version": "3.2.0",
                "installer_sha256": "a" * 64,
                "channel": "stable",
                "target": "portable",
                "kits": {"engineer": "3.2.0"},
            }
            with mock.patch.object(SYNC.sys, "platform", "win32"), \
                 mock.patch.object(SYNC, "ensure_ak_cli", side_effect=AssertionError("should not install on win32")):
                self.assertEqual(SYNC.sync_agentkit(config, require=False, root=root), [])
                with self.assertRaisesRegex(ValueError, "unsupported on Windows"):
                    SYNC.sync_agentkit(config, require=True, root=root)

    def test_installer_network_error_skips_in_default_mode_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = {
                "cli_version": "3.2.0",
                "installer_sha256": "a" * 64,
                "channel": "stable",
                "target": "portable",
                "kits": {"engineer": "3.2.0"},
            }
            with mock.patch.object(SYNC, "ensure_ak_cli", side_effect=OSError("unreachable")):
                self.assertEqual(SYNC.sync_agentkit(config, require=False, root=root), [])
                with self.assertRaisesRegex(OSError, "unreachable"):
                    SYNC.sync_agentkit(config, require=True, root=root)

    def test_skips_unlicensed_kit_without_blocking_licensed_kit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = {
                "cli_version": "3.2.0",
                "installer_sha256": "a" * 64,
                "channel": "stable",
                "target": "portable",
                "kits": {"engineer": "3.2.0", "marketing": "3.2.0"},
            }
            fake_bin = root / ".upstream" / "agentkit" / "bin" / "ak"
            kit_dir = root / ".upstream" / "agentkit" / "kits" / "engineer"
            make_skill(kit_dir / "skills", "ak-plan", "eng")
            (kit_dir / ".pin.json").write_text(json.dumps({
                "cli_version": "3.2.0",
                "channel": "stable",
                "target": "portable",
                "version": "3.2.0",
            }))

            with mock.patch.dict("os.environ", {"AGENTKIT_API_KEY": "dummy"}), \
                 mock.patch.object(SYNC, "ensure_ak_cli", return_value=fake_bin), \
                 mock.patch.object(SYNC, "ensure_ak_auth", return_value=(True, {"engineer"})):
                dirs = SYNC.sync_agentkit(config, require=False, root=root)
            self.assertEqual(dirs, [kit_dir / "skills"])


if __name__ == "__main__":
    unittest.main()
