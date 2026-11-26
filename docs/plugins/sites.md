# sites

Server management and site configuration.

- **Marketplace version on core 1.5.9:** `0.0.3`.
- **Verified modules:** `admin-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/sites` | `org.youngmonkeys.sites` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 17 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /servers` | `AdminSiteServerController` |
| `GET /settings` | `AdminSettingController` |
| `GET /api/v1/servers` | `AdminApiSiteServerController` |
| `GET /api/v1/settings` | `AdminApiSettingController` |
| `GET /api/v1/socket-proxy/permissions` | `AdminApiSocketProxyPermissionController` |
| `GET /api/v1/nodes/{nodeId}/servers/{serverType}/proxy` | `AdminApiSiteServerProxyController` |
| `POST /api/v1/servers/add` | `AdminApiSiteServerController` |
| `POST /api/v1/nodes/{nodeId}/socket-proxy` | `AdminApiSocketProxyController` |
| `POST /api/v1/nodes/{nodeId}/servers/{serverType}/proxy` | `AdminApiSiteServerProxyController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/socket-proxy/permissions` | `AdminApiSocketProxyPermissionController` |
| `PUT /api/v1/settings/server-heartbeat/stop` | `AdminApiSettingController` |
| `PUT /api/v1/settings/server-heartbeat/start` | `AdminApiSettingController` |
| `DELETE /api/v1/servers/{id}` | `AdminApiSiteServerController` |
| `DELETE /api/v1/nodes/{nodeId}/servers/{serverType}/proxy` | `AdminApiSiteServerProxyController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `sites: /`, `servers: /servers`, `settings: /settings`.

- **admin-plugin – Template:** `sites/servers/list.html`, `sites/settings/index.html`.

- **admin-plugin – Static resources:** `sites/css/style.css`.

## Data and migrations

- **Table in the DDL package (1):** `sites_servers`.
- **Class with JPA Entity/MappedSuperclass indication (1):** `SiteServer`.
- **SQL admin-plugin (2 files):** `resources/scripts/scripts.sql`, `resources/scripts/alter_servers_node_statuses.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `sites-admin-plugin-0.0.3.jar`, `sites-sdk-0.0.3.jar`; 71 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.sites.pagination`, `org.youngmonkeys.sites.admin.service`, `org.youngmonkeys.sites.admin.controller.api` (+26).
- **Other library JARs:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiSettingController`, `AdminApiSiteServerController`, `AdminApiSiteServerProxyController`, `AdminApiSocketProxyController`, `AdminPaginationSiteServerRepository`, `AdminPaginationSiteServerService`, `AdminSiteServerControllerService`, `AdminSiteServerProxyControllerService`, `AdminSiteServerProxyValidator`.
- **Configuration and permission classes (sample):** `AdminSitesSettings`, `AdminSocketProxyPermissionSettings`.
- **Potential extension points based on class names:** `AdminServerPropertiesUpdatedEventHandler`, `AdminSiteServerNodeManager`, `AdminSocketConnector`, `AdminSocketConnectorManager`, `AdminSocketProxyPermissionManager`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/sites/servers` and `/sites/settings` returned 200. No new site or host was created.

## Integration notes

See host configuration and multi-site operations. Keep deployment configuration separate from business authorization policy.

[Back to the plugin index](README.md)
