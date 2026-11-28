import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


UP = Path(__file__).resolve().parents[1] / "scripts" / "up.sh"


class RuntimeVersionTests(unittest.TestCase):
    def run_up(self, version):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / "scripts"
            scripts.mkdir()
            shutil.copyfile(UP, scripts / "up.sh")
            for name in ("sync-upstream.py", "docker-image-fallback.py"):
                (scripts / name).touch()
            docker = root / "docker"
            docker.write_text(
                "#!/usr/bin/env bash\n"
                'case "$1 $2" in\n'
                '  "inspect --format") echo 1.6.1 ;;\n'
                '  "compose version"|"compose up") ;;\n'
                '  "compose ps") echo container-id ;;\n'
                '  "compose exec") echo "$TEST_RUNTIME_VERSION" ;;\n'
                '  "compose port") echo "127.0.0.1:$4" ;;\n'
                '  *) exit 2 ;;\n'
                "esac\n"
            )
            curl = root / "curl"
            curl.write_text("#!/usr/bin/env bash\necho 200\n")
            for command in (docker, curl):
                command.chmod(0o755)
            env = {**os.environ, "PATH": f"{root}:{os.environ['PATH']}", "TEST_RUNTIME_VERSION": version}
            return subprocess.run(
                ["bash", str(scripts / "up.sh")], env=env, capture_output=True, text=True, timeout=10
            )

    def test_existing_volume_on_older_core_requires_explicit_upgrade(self):
        result = self.run_up("1.6.0")
        self.assertEqual(result.returncode, 1)
        self.assertIn("volume is running 1.6.0, but the image pins 1.6.1", result.stderr)
        self.assertIn("README.md", result.stderr)
        self.assertNotIn("Web:", result.stdout)

    def test_matching_runtime_completes_startup(self):
        result = self.run_up("1.6.1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Web: http://127.0.0.1:8080/", result.stdout)
