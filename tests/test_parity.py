import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


PARITY = Path(__file__).resolve().parents[1] / "scripts" / "parity.sh"


class ParityScriptTests(unittest.TestCase):
    def run_parity(self, overrides=None, extra_args=None):
        overrides = overrides or {}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            cloud = root / "ezyplatform-stack"
            local = root / "ezy-stack-local"

            for checkout, admin_port, web_port in (
                (cloud, overrides.get("cloud_admin_port", "19091"), overrides.get("cloud_web_port", "18081")),
                (local, overrides.get("local_admin_port", "29100"), overrides.get("local_web_port", "28100")),
            ):
                (checkout / "scripts").mkdir(parents=True)
                tsv = overrides.get(f"{checkout.name}_tsv", "ezyarticle\t1.5.8\tadmin-plugin\n")
                (checkout / "scripts" / "plugin-versions.tsv").write_text(tsv, encoding="utf-8")
                (checkout / ".env").write_text(
                    f"EZY_ADMIN_PORT={admin_port}\nEZY_WEB_PORT={web_port}\n",
                    encoding="utf-8",
                )

            git_mock = bin_dir / "git"
            git_mock.write_text(
                "#!/usr/bin/env bash\n"
                'dir="$2"\n'
                'case "$(basename "$dir")" in\n'
                '  ezyplatform-stack) echo "$MOCK_CLOUD_COMMIT" ;;\n'
                '  ezy-stack-local) echo "$MOCK_LOCAL_COMMIT" ;;\n'
                '  *) exit 1 ;;\n'
                "esac\n",
                encoding="utf-8",
            )

            docker_mock = bin_dir / "docker"
            docker_mock.write_text(
                "#!/usr/bin/env bash\n"
                'proj="$(basename "$PWD")"\n'
                'if [[ "$1" == "compose" && "$2" == "ps" ]]; then\n'
                '  echo "${proj}-${4}-1"\n'
                '  exit 0\n'
                'fi\n'
                'if [[ "$1" == "compose" && "$2" == "port" ]]; then\n'
                '  if [[ "$proj" == "ezyplatform-stack" ]]; then\n'
                '    [[ "$4" == "9090" ]] && echo "$MOCK_CLOUD_MAP_9090" || echo "$MOCK_CLOUD_MAP_8080"\n'
                '  else\n'
                '    [[ "$4" == "9090" ]] && echo "$MOCK_LOCAL_MAP_9090" || echo "$MOCK_LOCAL_MAP_8080"\n'
                '  fi\n'
                '  exit 0\n'
                'fi\n'
                'if [[ "$1" == "inspect" ]]; then\n'
                '  cid="$4"\n'
                '  [[ "$cid" == ezyplatform-stack-* ]] && echo "$MOCK_CLOUD_IMG_ID" || echo "$MOCK_LOCAL_IMG_ID"\n'
                '  exit 0\n'
                'fi\n'
                'if [[ "$1" == "image" && "$2" == "inspect" ]]; then\n'
                '  img="$5"\n'
                '  [[ "$img" == "$MOCK_CLOUD_IMG_ID" ]] && echo "$MOCK_CLOUD_DIGEST" || echo "$MOCK_LOCAL_DIGEST"\n'
                '  exit 0\n'
                'fi\n'
                'if [[ "$1" == "exec" ]]; then\n'
                '  cid="$2"\n'
                '  if [[ "$cid" == *-mysql-1 ]]; then\n'
                '    [[ "$cid" == ezyplatform-stack-* ]] && printf "%b" "$MOCK_CLOUD_SCHEMA" || printf "%b" "$MOCK_LOCAL_SCHEMA"\n'
                '  else\n'
                '    [[ "$cid" == ezyplatform-stack-* ]] && printf "%b" "$MOCK_CLOUD_PLUGINS" || printf "%b" "$MOCK_LOCAL_PLUGINS"\n'
                '  fi\n'
                '  exit 0\n'
                'fi\n'
                "exit 2\n",
                encoding="utf-8",
            )

            curl_mock = bin_dir / "curl"
            curl_mock.write_text("#!/usr/bin/env bash\necho 200\n", encoding="utf-8")

            for f in (git_mock, docker_mock, curl_mock):
                f.chmod(f.stat().st_mode | stat.S_IXUSR)

            default_plugins = (
                'MOD\tadmin\tplugins\tezyarticle\t1.5.8\n'
                'RT\tadmin\tplugins.txt\t[{"name":"ezyarticle","active":true}]\n'
            )
            default_schema = (
                "T\tezy_admins\tBASE TABLE\tInnoDB\tutf8mb4_unicode_ci\n"
                "C\tezy_admins\t1\tid\tbigint unsigned\tNO\t<NULL>\tPRI\tauto_increment\t\t\n"
            )

            env = {
                **os.environ,
                "PATH": f"{bin_dir}:{os.environ['PATH']}",
                "MOCK_CLOUD_COMMIT": overrides.get("cloud_commit", "4628b38000000000000000000000000000000000"),
                "MOCK_LOCAL_COMMIT": overrides.get("local_commit", "4628b38000000000000000000000000000000000"),
                "MOCK_CLOUD_IMG_ID": overrides.get("cloud_img_id", "sha256:aaa111"),
                "MOCK_LOCAL_IMG_ID": overrides.get("local_img_id", "sha256:aaa111"),
                "MOCK_CLOUD_DIGEST": overrides.get("cloud_digest", "ezyplatform-stack/core@sha256:aaa111"),
                "MOCK_LOCAL_DIGEST": overrides.get("local_digest", "ezyplatform-stack/core@sha256:aaa111"),
                "MOCK_CLOUD_PLUGINS": overrides.get("cloud_plugins", default_plugins),
                "MOCK_LOCAL_PLUGINS": overrides.get("local_plugins", default_plugins),
                "MOCK_CLOUD_SCHEMA": overrides.get("cloud_schema", default_schema),
                "MOCK_LOCAL_SCHEMA": overrides.get("local_schema", default_schema),
                "MOCK_CLOUD_MAP_9090": overrides.get("cloud_map_9090", "127.0.0.1:19091"),
                "MOCK_CLOUD_MAP_8080": overrides.get("cloud_map_8080", "127.0.0.1:18081"),
                "MOCK_LOCAL_MAP_9090": overrides.get("local_map_9090", "127.0.0.1:29100"),
                "MOCK_LOCAL_MAP_8080": overrides.get("local_map_8080", "127.0.0.1:28100"),
            }
            cmd = ["bash", str(PARITY), str(cloud), str(local)]
            if extra_args:
                cmd.extend(extra_args)
            return subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=15)

    def test_parity_ok(self):
        res = self.run_parity()
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("PARITY OK", res.stdout)

    def test_commit_mismatch_fails(self):
        res = self.run_parity({"local_commit": "deadbeef00000000000000000000000000000000"})
        self.assertEqual(res.returncode, 1)
        self.assertIn("PARITY FAILED (commit)", res.stdout)

    def test_image_digest_mismatch_fails(self):
        res = self.run_parity({"local_img_id": "sha256:bbb222", "local_digest": "ezyplatform-stack/core@sha256:bbb222"})
        self.assertEqual(res.returncode, 1)
        self.assertIn("PARITY FAILED (image)", res.stdout)

    def test_plugin_mismatch_fails(self):
        res = self.run_parity({"local_plugins": "MOD\tadmin\tplugins\tezyarticle\t1.5.7\n"})
        self.assertEqual(res.returncode, 1)
        self.assertIn("PARITY FAILED (plugins)", res.stdout)

    def test_schema_mismatch_fails(self):
        res = self.run_parity({"local_schema": "T\tezy_other\tBASE TABLE\tInnoDB\tutf8mb4_unicode_ci\n"})
        self.assertEqual(res.returncode, 1)
        self.assertIn("PARITY FAILED (schema)", res.stdout)

    def test_port_mismatch_fails(self):
        res = self.run_parity({"local_map_9090": "0.0.0.0:29100"})
        self.assertEqual(res.returncode, 1)
        self.assertIn("PARITY FAILED (ports)", res.stdout)


if __name__ == "__main__":
    unittest.main()
