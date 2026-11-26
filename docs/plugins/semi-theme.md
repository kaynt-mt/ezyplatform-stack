# semi-theme

Admin module for interface support; no Web theme.

- **Marketplace version on core 1.5.9:** `1.0.2`. Module metadata reports `1.0.1`.
- **Verified modules:** `admin-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/semi-theme` | `org.ltl.semi_theme` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 1 method/URI combination identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingsController` |

- **admin-plugin – Template:** `modules/list.html`, `semi-theme/dashboards/admin.html`, `semi-theme/dashboards/scripts.html`, `semi-theme/dashboards/socket.html`, `semi-theme/dashboards/web.html`, `semi-theme/settings.html`.

- **admin-plugin – Static resources:** `css/newsemiv4/index.css`, `css/newsemiv4/index.min.css`, `css/recursive.css`, `css/semi/index.css` (+6).

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `semi-theme-admin-plugin-1.0.1.jar`; 3 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.ltl.semi_theme.admin.controller.view`.
- **Controllers, services, and repositories (sample):** `AdminSettingsController`, `IndexController`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/semi-theme/` → 200; ZIP `1.0.2` declares `version=1.0.1` in `module.properties`. This is an Admin module, not a Web theme.

## Integration notes

Compare the Marketplace name, ZIP version, and actual module type. An Admin page titled “Unknown” does not prove that a theme rendered.

[Back to the plugin index](README.md)
