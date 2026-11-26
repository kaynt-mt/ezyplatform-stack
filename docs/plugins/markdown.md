# markdown

Markdown interface and Web module.

- **Marketplace version on core 1.5.9:** `0.2.6`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/markdown` | `org.youngmonkeys.markdown` | Not declared |
| `web-plugin` — `web/plugins/markdown` | `org.youngmonkeys.markdown` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 2 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `IndexController` |
| `POST /api/v1/convert-to-html` | `AdminApiMarkdownController` |

**web-plugin** — 2 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `POST /api/v1/markdown/convert-to-html` | `WebApiMarkdownController` |
| `POST /markdown/api/v1/convert-to-html` | `WebApiMarkdownController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `markdown: /`.

- **admin-plugin – Template:** `markdown/index.html`.

- **admin-plugin – Static resources:** `markdown/css/editor.css`, `markdown/css/syntax.css`, `markdown/js/editor.js`.

- **web-plugin – Static resources:** `markdown/css/editor.css`, `markdown/css/style.css`, `markdown/js/editor.js`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `markdown-admin-plugin-0.2.6.jar`, `markdown-sdk-0.2.6.jar`; 45 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.markdown.block`, `org.youngmonkeys.markdown.event`, `org.youngmonkeys.markdown.admin.event` (+17).
- **Controllers, services, and repositories (sample):** `AdminApiMarkdownController`, `IndexController`, `AdminConvertMarkdownToHtmlEventSchemaFetcher`, `AdminMarkdownSettingService`, `ConvertMarkdownToHtmlEventSchemaFetcher`, `MarkdownSettingService`.
- **Configuration and permission classes (sample):** `AdminMarkdownEditorConfig`.
- **Potential extension points based on class names:** `AdminConvertMarkdownToHtmlEventHandler`, `AdminProgrammingKeywordManager`, `ConvertMarkdownToHtmlEventHandler`, `ProgrammingKeywordManager`.

### web-plugin

- **JARs inspected:** `markdown-sdk-0.2.6.jar`, `markdown-web-plugin-0.2.6.jar`; 46 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.markdown.block`, `org.youngmonkeys.markdown.event`, `org.youngmonkeys.markdown.web.view` (+17).
- **Controllers, services, and repositories (sample):** `WebApiMarkdownController`, `WebMarkdownControllerService`, `ConvertMarkdownToHtmlEventSchemaFetcher`, `MarkdownSettingService`, `WebConvertMarkdownToHtmlEventSchemaFetcher`, `WebMarkdownControllerService`, `WebMarkdownSettingService`.
- **Potential extension points based on class names:** `ConvertMarkdownToHtmlEventHandler`, `ProgrammingKeywordManager`, `WebConvertMarkdownToHtmlEventHandler`, `WebProgrammingKeywordManager`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/markdown/` displayed the Markdown page (200).

## Integration notes

Sanitize output, block active content, and enforce access controls on files and images. Opening the editor does not prove rendering is safe.

[Back to the plugin index](README.md)
