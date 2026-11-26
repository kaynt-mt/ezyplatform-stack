import importlib.util
import re
import shlex
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "docker-image-fallback.py"
SPEC = importlib.util.spec_from_file_location("docker_image_fallback", SCRIPT)
FALLBACK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FALLBACK)

MYSQL = "mysql:8.0@sha256:7dcddc01f13bab2f15cde676d44d01f61fc9f99fe7785e86196dfc07d358ae2b"
PYTHON = "python:3.14-alpine@sha256:5862d971d1f0ae26b258cefa4e893556b1d3aba81bd2ff30888704ad378bab67"
TEMURIN = "eclipse-temurin:11-jre@sha256:7db5776af2396377c8aae2aa124712da7b72a5b6b014c17d77ae37eb5276f37b"


def dockerfile_base_images(text):
    images = []
    stages = set()
    for line in text.splitlines():
        match = re.match(r"^\s*FROM\s+(.+)$", line, re.IGNORECASE)
        if not match:
            continue
        tokens = shlex.split(match.group(1), comments=True)
        while tokens and tokens[0].startswith("--"):
            tokens.pop(0)
        if not tokens:
            continue
        reference = tokens[0]
        stage = tokens[2] if len(tokens) >= 3 and tokens[1].lower() == "as" else None
        if reference.lower() not in stages and reference.lower() != "scratch" and "$" not in reference:
            images.append(reference)
        if stage:
            stages.add(stage.lower())
    return images


class ImageDefaultTests(unittest.TestCase):
    def test_extracts_only_image_variables_with_defaults(self):
        text = """
        image: ${MYSQL_IMAGE:-mysql:8.0@sha256:7dcddc01f13bab2f15cde676d44d01f61fc9f99fe7785e86196dfc07d358ae2b}
        password: ${MYSQL_PASSWORD:?required}
        context: docker-image://${PYTHON_BASE_IMAGE:-python:3.14-alpine@sha256:5862d971d1f0ae26b258cefa4e893556b1d3aba81bd2ff30888704ad378bab67}
        other: ${IMAGE_TAG:-python:3.14-alpine}
        empty: ${EMPTY_IMAGE:-}
        """
        self.assertEqual(
            FALLBACK.image_defaults(text),
            {
                "MYSQL_IMAGE": MYSQL,
                "PYTHON_BASE_IMAGE": PYTHON,
            },
        )

    def test_compose_image_defaults_are_digest_pinned(self):
        defaults = FALLBACK.image_defaults((SCRIPT.parents[1] / "compose.yaml").read_text())
        self.assertEqual(
            defaults,
            {
                "ECLIPSE_TEMURIN_BASE_IMAGE": TEMURIN,
                "MYSQL_IMAGE": MYSQL,
                "PYTHON_BASE_IMAGE": PYTHON,
            },
        )
        for reference in defaults.values():
            with self.subTest(reference=reference):
                self.assertIn("@sha256:", reference)

    def test_additional_context_keys_cover_exact_dockerfile_base_images(self):
        root = SCRIPT.parents[1]
        dockerfile = root / ".upstream" / "ezyplatform-docker" / "Dockerfile"
        expected = set(dockerfile_base_images(dockerfile.read_text()))
        compose_text = (root / "compose.yaml").read_text()
        keys = set(re.findall(r"^\s+[\"']([^\"']+)[\"']:\s*docker-image://", compose_text, re.MULTILINE))
        self.assertEqual(keys, expected)


class MirrorReferenceTests(unittest.TestCase):
    def test_maps_official_docker_hub_images_to_mirror_library(self):
        self.assertEqual(
            FALLBACK.docker_hub_mirror(MYSQL),
            "mirror.gcr.io/library/mysql:8.0@sha256:7dcddc01f13bab2f15cde676d44d01f61fc9f99fe7785e86196dfc07d358ae2b",
        )
        self.assertEqual(
            FALLBACK.docker_hub_mirror(PYTHON),
            "mirror.gcr.io/library/python:3.14-alpine@sha256:5862d971d1f0ae26b258cefa4e893556b1d3aba81bd2ff30888704ad378bab67",
        )

    def test_maps_explicit_docker_hub_and_namespaced_images(self):
        self.assertEqual(
            FALLBACK.docker_hub_mirror("docker.io/library/python:3.14-alpine"),
            "mirror.gcr.io/library/python:3.14-alpine",
        )
        self.assertEqual(
            FALLBACK.docker_hub_mirror("index.docker.io/example/project:1"),
            "mirror.gcr.io/example/project:1",
        )

    def test_rejects_non_docker_hub_dynamic_and_invalid_images(self):
        for reference in (
            "quay.io/example/project:1",
            "${BASE_IMAGE}",
            "scratch",
            "https://example.invalid/image",
            "mysql@sha256:",
        ):
            with self.subTest(reference=reference):
                self.assertIsNone(FALLBACK.docker_hub_mirror(reference))


class SelectOverrideTests(unittest.TestCase):
    def select(self, local, remote, configured=()):
        return FALLBACK.select_overrides(
            {"PYTHON_BASE_IMAGE": PYTHON},
            set(configured),
            lambda reference: reference in local,
            lambda reference: reference in remote,
        )

    def test_keeps_docker_hub_when_image_is_local_or_remote_available(self):
        overrides, notices = self.select(local={PYTHON}, remote=set())
        self.assertEqual((overrides, notices), ({}, []))
        overrides, notices = self.select(local=set(), remote={PYTHON})
        self.assertEqual((overrides, notices), ({}, []))

    def test_uses_mirror_only_when_docker_hub_cannot_serve_image(self):
        mirror = FALLBACK.docker_hub_mirror(PYTHON)
        overrides, notices = self.select(local=set(), remote={mirror})
        self.assertEqual(overrides, {"PYTHON_BASE_IMAGE": mirror})
        self.assertEqual(len(notices), 1)
        self.assertIn("using mirror.gcr.io", notices[0])

    def test_uses_cached_mirror_when_docker_hub_cannot_serve_image(self):
        mirror = FALLBACK.docker_hub_mirror(PYTHON)
        overrides, _ = self.select(local={mirror}, remote=set())
        self.assertEqual(overrides, {"PYTHON_BASE_IMAGE": mirror})

    def test_keeps_docker_hub_when_mirror_is_unavailable(self):
        overrides, notices = self.select(local=set(), remote=set())
        self.assertEqual(overrides, {})
        self.assertEqual(len(notices), 1)
        self.assertIn("neither Docker Hub nor mirror.gcr.io", notices[0])

    def test_never_overrides_user_configured_image(self):
        overrides, notices = self.select(local=set(), remote=set(), configured={"PYTHON_BASE_IMAGE"})
        self.assertEqual((overrides, notices), ({}, []))

    def test_override_assignments_are_shell_safe_lines(self):
        mirror = FALLBACK.docker_hub_mirror(PYTHON)
        self.assertEqual(
            FALLBACK.override_assignments({"PYTHON_BASE_IMAGE": mirror}),
            f"PYTHON_BASE_IMAGE={mirror}",
        )


if __name__ == "__main__":
    unittest.main()
