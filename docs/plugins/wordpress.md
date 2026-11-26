# wordpress

WordPress configuration and data import workflow.

- **Marketplace version on core 1.5.9:** `0.1.4`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/wordpress` | `org.youngmonkeys.wordpress` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/wordpress` | `org.youngmonkeys.wordpress` | [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 16 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `WordpressSettingController` |
| `GET /migration` | `MigrationController` |
| `GET /public/media/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{month}/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{fileName}` | `AdminWpMediaController` |
| `POST /api/v1/connect-database` | `ApiMigrationController` |
| `POST /api/v1/start-data-migration` | `ApiMigrationController` |
| `PUT /api/v1/settings` | `ApiWordpressSettingController` |
| `PUT /api/v1/disconnect-database` | `ApiMigrationController` |
| `PUT /api/v1/stop-data-migration` | `ApiMigrationController` |
| `PUT /api/v1/restart-data-migration` | `ApiMigrationController` |
| `DELETE /api/v1/clear-database-information` | `ApiMigrationController` |

**web-plugin** — 7 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /public/media/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{minute}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{minute}/{second}/{fileName}` | `WebWpMediaController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `wordpress: /`, `migrate_data: /migration`, `settings: /settings`.

- **admin-plugin – Template:** `wordpress/migration/index.html`, `wordpress/setting/index.html`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `wordpress-admin-plugin-0.1.4.jar`, `wordpress-sdk-0.1.4.jar`; 36 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.wordpress.admin.migrator`, `org.youngmonkeys.wordpress.admin.event`, `org.youngmonkeys.wordpress.admin.request` (+10).
- **Other library JARs:** `jwordpress-1.0.5.jar`.
- **Controllers, services, and repositories (sample):** `AdminWpMediaController`, `ApiMigrationController`, `ApiWordpressSettingController`, `IndexController`, `AdminWordpressSettingService`, `MigrationValidator`, `WordpressSettingService`.
- **Potential extension points based on class names:** `WpGetMediaFilePathEventHandler`, `WpMigrationFinishedEventHandler`, `WpMigrationFinshedEvent`, `WpMigrationRestartEvent`, `WpMigrationRestartEventHandler`, `WpMigratorManager`.

### web-plugin

- **JARs inspected:** `wordpress-sdk-0.1.4.jar`, `wordpress-web-plugin-0.1.4.jar`; 4 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.wordpress.web.service`, `org.youngmonkeys.wordpress.web.controller.api`, `org.youngmonkeys.wordpress.service` (+1).
- **Other library JARs:** `jwordpress-1.0.5.jar`.
- **Controllers, services, and repositories (sample):** `WebWpMediaController`, `WebWordpressSettingService`, `WordpressSettingService`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/wordpress/migration` returned 200. No WordPress data was imported.

## Integration notes

The import UI separates a dry run from applying changes and reports errors by record. The sandbox did not verify the WordPress connection.

[Back to the plugin index](README.md)
