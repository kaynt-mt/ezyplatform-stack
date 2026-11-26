import importlib.util
import unittest
from graphlib import TopologicalSorter
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install-plugins.py"
SPEC = importlib.util.spec_from_file_location("install_plugins", SCRIPT)
INSTALL_PLUGINS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL_PLUGINS)


MANIFEST = {
    "ezyarticle": ("1.5.6", "1.5.6", ["admin-plugin", "web-plugin", "socket-plugin"]),
    "ezymail": ("0.3.3", "0.3.3", ["admin-plugin", "web-plugin"]),
    "ezylogin": ("0.4.7", "0.4.7", ["admin-plugin", "web-plugin"]),
    "ezysupport": ("0.6.2", "0.6.2", ["admin-plugin", "web-plugin"]),
}


class ParseOnlyTests(unittest.TestCase):
    def test_accepts_comma_separated_tested_plugins(self):
        self.assertEqual(
            INSTALL_PLUGINS.parse_only(" ezylogin, ezymail ", MANIFEST),
            ["ezylogin", "ezymail"],
        )

    def test_rejects_empty_duplicate_and_unknown_names(self):
        for value, pattern in [
            ("", "at least one"),
            ("ezylogin,ezylogin", "duplicate"),
            ("ezylogin,unknown", "unknown tested plugin"),
        ]:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, pattern):
                INSTALL_PLUGINS.parse_only(value, MANIFEST)


class InstallClosureTests(unittest.TestCase):
    def install_closure(self, names, dependencies):
        def install(name, release, version, kinds, admin, opener):
            self.assertEqual(release, MANIFEST[name][0])
            self.assertEqual(version, MANIFEST[name][1])
            self.assertEqual(kinds, MANIFEST[name][2])
            self.assertIsNone(admin)
            self.assertIsNone(opener)
            return dependencies[name]

        with mock.patch.object(INSTALL_PLUGINS, "install", side_effect=install) as installer:
            graph = INSTALL_PLUGINS.install_closure(MANIFEST, names, None, None)
        return graph, [call.args[0] for call in installer.call_args_list]

    def test_installs_transitive_dependency_closure(self):
        graph, calls = self.install_closure(["ezylogin"], {
            "ezyarticle": set(),
            "ezymail": {"ezyarticle"},
            "ezylogin": {"ezyarticle", "ezymail"},
        })

        self.assertEqual(set(graph), {"ezylogin", "ezymail", "ezyarticle"})
        self.assertCountEqual(calls, ["ezylogin", "ezymail", "ezyarticle"])
        order = list(TopologicalSorter(graph).static_order())
        self.assertLess(order.index("ezymail"), order.index("ezylogin"))
        self.assertLess(order.index("ezyarticle"), order.index("ezymail"))

    def test_does_not_install_a_requested_dependency_twice(self):
        graph, calls = self.install_closure(["ezylogin", "ezymail"], {
            "ezyarticle": set(),
            "ezymail": {"ezyarticle"},
            "ezylogin": {"ezyarticle", "ezymail"},
        })

        self.assertEqual(set(graph), {"ezylogin", "ezymail", "ezyarticle"})
        self.assertEqual(len(calls), len(set(calls)))

    def test_rejects_dependencies_outside_the_tested_set(self):
        with self.assertRaisesRegex(ValueError, "ezylogin: dependencies outside the tested set: custom-plugin"):
            self.install_closure(["ezylogin"], {"ezylogin": {"custom-plugin"}})


if __name__ == "__main__":
    unittest.main()
