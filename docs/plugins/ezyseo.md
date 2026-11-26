# ezyseo

Sitemaps, links, and robots directives.

- **Marketplace version on core 1.5.9:** `0.1.2`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyseo` | `org.youngmonkeys.ezyseo` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezyseo` | `org.youngmonkeys.ezyseo` | [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 13 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /links` | `AdminLinkController` |
| `GET /settings` | `AdminSettingController` |
| `GET /sitemaps` | `AdminSitemapController` |
| `GET /links/add` | `AdminLinkController` |
| `GET /api/v1/links` | `AdminApiLinkController` |
| `GET /api/v1/sitemaps` | `AdminApiSitemapController` |
| `GET /links/{linkId}/edit` | `AdminLinkController` |
| `POST /api/v1/links/add` | `AdminApiLinkController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/sitemaps` | `AdminApiSitemapController` |
| `PUT /api/v1/links/{linkId}` | `AdminApiLinkController` |
| `DELETE /api/v1/links/{linkId}` | `AdminApiLinkController` |

**web-plugin** — 3 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /robots.txt` | `ApiRobotsController` |
| `GET /api/v1/sitemaps` | `ApiSitemapController` |
| `GET /api/v1/sitemaps/{linkType}` | `ApiSitemapController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyseo: /`, `sitemaps: /sitemaps`, `links: /links`, `links_add: ~/links/add`, `links_edit: ~/links/{linkId}/edit`, `settings: /settings`.

- **admin-plugin – Template:** `ezyseo/links/add-new-type.html`, `ezyseo/links/add.html`, `ezyseo/links/edit.html`, `ezyseo/links/list.html`, `ezyseo/links/scripts.html`, `ezyseo/setting/index.html`, `ezyseo/sitemaps/list.html`.

- **admin-plugin – Static resources:** `css/ezyseo.css`.

- **web-plugin – Static resources:** `css/ezyseo/style.css`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyseo-admin-plugin-0.1.2.jar`, `ezyseo-sdk-0.1.2.jar`; 41 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyseo.admin.response`, `org.youngmonkeys.ezyseo.admin.serializer`, `org.youngmonkeys.ezyseo.admin.controller.view` (+15).
- **Controllers, services, and repositories (sample):** `AdminApiLinkController`, `AdminApiSettingController`, `AdminApiSitemapController`, `AdminIndexController`, `AdminEzySeoLinkService`, `AdminEzySeoLinkValidator`, `AdminEzySeoSettingService`, `AdminEzySeoSettingValidator`, `AdminLinkControllerService`.
- **Configuration and permission classes (sample):** `AdminScheduledSitemapConfig`.
- **Potential extension points based on class names:** `AdminEzySeoFileSystemManager`, `EzySeoFileSystemManager`.

### web-plugin

- **JARs inspected:** `ezyseo-sdk-0.1.2.jar`, `ezyseo-web-plugin-0.1.2.jar`; 9 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyseo.common.constant`, `org.youngmonkeys.ezyseo.web.controller.api`, `org.youngmonkeys.ezyseo.common.service` (+4).
- **Controllers, services, and repositories (sample):** `ApiRobotsController`, `ApiSitemapController`, `EzySeoSettingService`, `WebEzySeoSettingService`.
- **Potential extension points based on class names:** `EzySeoFileSystemManager`, `WebEzySeoFileSystemManager`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyseo/sitemaps` and Web `/robots.txt` and `/api/v1/sitemaps` returned 200.

## Integration notes

See the XML and text export patterns for public data. Do not include private URLs in sitemaps or use robots.txt in place of ACLs.

[Back to the plugin index](README.md)
