import base64
import importlib.util
import json
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
    "freestyle": ("0.2.9", "0.2.9", ["admin-plugin", "theme"]),
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


class SelectedPluginsTests(unittest.TestCase):
    def test_none_selects_the_default_manifest(self):
        self.assertEqual(INSTALL_PLUGINS.selected_plugins(None, MANIFEST), list(MANIFEST))

    def test_empty_value_is_rejected_instead_of_selecting_the_manifest(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            INSTALL_PLUGINS.selected_plugins("", MANIFEST)


class AddRequestedThemeTests(unittest.TestCase):
    def test_adds_a_requested_marketplace_theme_to_the_install_set(self):
        self.assertEqual(
            INSTALL_PLUGINS.add_requested_theme(["ezylogin"], "freestyle", MANIFEST),
            ["ezylogin", "freestyle"],
        )

    def test_does_not_duplicate_a_theme_or_add_the_core_welcome_theme(self):
        self.assertEqual(
            INSTALL_PLUGINS.add_requested_theme(["ezylogin", "freestyle"], "freestyle", MANIFEST),
            ["ezylogin", "freestyle"],
        )
        self.assertEqual(
            INSTALL_PLUGINS.add_requested_theme(["ezylogin"], "welcome", MANIFEST),
            ["ezylogin"],
        )


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


class BrowserAuthFixtureTests(unittest.TestCase):
    def test_sql_seeds_pages_marker_and_local_activation_setting(self):
        sql = INSTALL_PLUGINS.browser_auth_sql()

        for slug in ("login", "register"):
            self.assertIn(f"'{slug}'", sql)
            self.assertIn(f'data-stack-auth-page="{slug}"'.encode().hex(), sql)
        self.assertIn("ezylogin_activation_required", sql)
        self.assertIn("BOOLEAN", sql)
        self.assertIn(INSTALL_PLUGINS.BROWSER_AUTH_MARKER, sql)
        self.assertIn("START TRANSACTION", sql)
        self.assertIn("COMMIT", sql)

    def test_validate_rejects_existing_unowned_pages(self):
        with self.assertRaisesRegex(ValueError, "/login already exists"):
            INSTALL_PLUGINS.validate_browser_auth_rows([
                ("login", "PAGE", ""),
                ("register", "PAGE", INSTALL_PLUGINS.BROWSER_AUTH_MARKER),
            ])
        with self.assertRaisesRegex(ValueError, "/Login already exists"):
            INSTALL_PLUGINS.validate_browser_auth_rows([
                ("Login", "PAGE", ""),
            ])

    def test_validate_accepts_missing_or_fixture_owned_pages(self):
        INSTALL_PLUGINS.validate_browser_auth_rows([])
        INSTALL_PLUGINS.validate_browser_auth_rows([
            ("login", "PAGE", INSTALL_PLUGINS.BROWSER_AUTH_MARKER),
            ("register", "PAGE", INSTALL_PLUGINS.BROWSER_AUTH_MARKER),
        ])

    def test_page_errors_require_fixture_and_api_endpoint(self):
        body = 'data-stack-auth-page="login" /ezylogin/api/v1/login'

        self.assertEqual(INSTALL_PLUGINS.browser_auth_page_errors("/login", body), [])
        self.assertEqual(len(INSTALL_PLUGINS.browser_auth_page_errors("/login", "Not found")), 2)

    def test_fixture_verification_requires_the_original_callback_in_rendered_login(self):
        responses = [
            (200, 'data-stack-auth-page="login" /ezylogin/api/v1/login'),
            (200, 'data-stack-auth-page="register" /ezylogin/api/v1/register'),
            (200, '{"activationRequired":false}'),
            (200, '<span id="stack-login-return" data-return-url="/wrong-path"></span>'),
        ]
        with mock.patch.object(INSTALL_PLUGINS, "fetch_text", side_effect=responses):
            with self.assertRaisesRegex(ValueError, "login return URL"):
                INSTALL_PLUGINS.verify_browser_auth_fixture("http://127.0.0.1:8080")

    def test_fixture_verification_probes_login_with_a_path_and_query(self):
        class ReadableResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return self.body

        responses = [
            b'data-stack-auth-page="login" /ezylogin/api/v1/login',
            b'data-stack-auth-page="register" /ezylogin/api/v1/register',
            b'{"activationRequired":false}',
            b'<span id="stack-login-return" data-return-url="/__stack_login_return_probe?view=queue&amp;from=qa%20deck"></span>',
        ]

        def respond(*args, **kwargs):
            response = ReadableResponse()
            response.status = 200
            response.body = responses.pop(0)
            return response

        with mock.patch.object(INSTALL_PLUGINS, "urlopen", side_effect=respond) as urlopen:
            INSTALL_PLUGINS.verify_browser_auth_fixture("http://127.0.0.1:8080")
        probe = urlopen.call_args.args[0]
        self.assertEqual(probe.full_url, "http://127.0.0.1:8080/login")
        name, cookie = probe.get_header("Cookie").split("=", 1)
        self.assertEqual(name, "ezyRedirectAttributes")
        self.assertEqual(json.loads(base64.b64decode(cookie)), {
            "callbackUri": "/__stack_login_return_probe?view=queue&from=qa%20deck",
        })

    def test_login_return_bridge_is_scoped_to_the_fixture_and_idempotent(self):
        source = '<th:block layout:fragment="content">original contents</th:block>'
        template = INSTALL_PLUGINS.browser_auth_theme_template(source)

        self.assertIn('id="stack-login-return"', template)
        self.assertIn("page.slug == 'login'", template)
        self.assertIn("'stack-login-form'", template)
        self.assertIn('th:attr="data-return-url=${loginCallbackUrl}"', template)
        self.assertIn("original contents", template)
        self.assertEqual(INSTALL_PLUGINS.browser_auth_theme_template(template), template)
        with self.assertRaisesRegex(ValueError, "EzyArticle page content fragment"):
            INSTALL_PLUGINS.browser_auth_theme_template("<body>Unknown template</body>")

    def test_freestyle_header_gates_only_the_guest_pages_and_renders_a_logout_form(self):
        source = """<ul>
    <li class="nav-item" th:each="pageMeta, iterator : ${pageMetas}">
        <a th:href="${pageMeta.url}">[[${pageMeta.title}]]</a>
    </li>
    <li th:if="${webLanguages.size() > 1}" class="language-dropdown">Languages</li>
</ul>"""
        template = INSTALL_PLUGINS.browser_auth_freestyle_header(source)

        self.assertIn('th:each="pageMeta, iterator : ${pageMetas}"', template)
        self.assertIn(
            'th:if="${loggedIn != true || '
            "(pageMeta.slug != 'login' && pageMeta.slug != 'register')"
            '}"',
            template,
        )
        self.assertIn('<a th:href="${pageMeta.url}">[[${pageMeta.title}]]</a>', template)
        self.assertIn('<li class="nav-item" th:if="${loggedIn == true}">', template)
        self.assertIn('<form action="/logout" method="post">', template)
        self.assertIn('class="language-dropdown">Languages</li>', template)
        self.assertEqual(INSTALL_PLUGINS.browser_auth_freestyle_header(template), template)

    def test_freestyle_header_rejects_an_unrecognized_template(self):
        with self.assertRaisesRegex(ValueError, "standard Freestyle header template"):
            INSTALL_PLUGINS.browser_auth_freestyle_header("<nav>Unexpected header</nav>")


if __name__ == "__main__":
    unittest.main()
