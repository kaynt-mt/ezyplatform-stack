# postgresql

PostgreSQL administration interface.

- **Marketplace version on core 1.5.9:** `0.0.1`.
- **Verified modules:** `admin-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/postgresql` | `org.youngmonkeys.postgresql` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 6 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /dashboard` | `AdminDashboardController` |
| `GET /api/v1/dashboard/tables` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/overview` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/datasource` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/active-queries` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/connection-states` | `AdminApiDashboardController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `postgresql: /`, `dashboard: /dashboard`.

- **admin-plugin – Template:** `postgresql/dashboard.html`.

- **admin-plugin – Static resources:** `postgresql/css/dashboard.css`, `postgresql/css/style.css`, `postgresql/js/dashboard.js`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `postgresql-42.7.4.jar`, `postgresql-admin-plugin-0.0.1.jar`; 361 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.postgresql.core`, `org.postgresql.util`, `org.postgresql.jdbc` (+46).
- **Other library JARs:** `checker-qual-3.42.0.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiDashboardController`, `AdminDashboardController`, `AdminPostgresqlDashboardControllerService`, `IndexController`, `AdminPostgresqlDashboardControllerService`, `AdminPostgresqlStatisticService`.
- **Configuration and permission classes (sample):** `AdminPostgresqlSqlScriptsConverterConfig`, `ChannelBindingOption`, `CommonOptions`, `ExpressionProperties`, `LogicalReplicationOptions`, `Option`, `PhysicalReplicationOptions`.
- **Potential extension points based on class names:** `ArrayAssistantRegistry`, `AuthenticationPluginManager`, `BatchResultHandler`, `CallableBatchResultHandler`, `ClientFinalProcessor`, `ConnectionFactory`, `CopyManager`, `DbKeyStoreSocketFactory`, `DefaultJavaSSLFactory` (+27).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/postgresql/dashboard` returned 200 on the MySQL stack. No data source was changed and PostgreSQL itself was not tested.

## Integration notes

If you change database engines, retest migrations, pagination, and queries. The Admin dashboard does not prove the data source integration works.

[Back to the plugin index](README.md)
