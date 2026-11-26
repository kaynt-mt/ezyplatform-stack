# socket-monitor

Socket monitoring module and entry loader.

- **Marketplace version on core 1.5.9:** `0.0.3`.
- **Verified modules:** `socket-plugin`.
- **Installation:** View the environment and the general limits in [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `socket-plugin` — `socket/plugins/socket-monitor` | `com.ezyplatform.socket.monitor` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

No HTTP annotations were found in the Admin, Web, or theme modules inspected.

No HTML templates or JavaScript and CSS assets were found in the module directory.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### socket-plugin

- **JARs inspected:** `socket-monitor-0.0.3.jar`; 24 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `com.ezyplatform.socket.monitor.plugin.data`, `com.ezyplatform.socket.monitor.plugin.controller`, `com.ezyplatform.socket.monitor.plugin.service` (+7).
- **Controllers, services, and repositories (sample):** `AbstractController`, `AdminLoginController`, `ModuleRequestController`, `SettingsRequestController`, `SocketMonitorAdminPermissionService`, `SocketMonitorAdminRoleRepository`, `SocketMonitorAdminRoleService`.
- **Configuration and permission classes (sample):** `SocketMonitorPostConfig`.
- **Potential extension points based on class names:** `EntryLoader`, `SocketMonitorAdminRequestInterceptor`.
- **Zone / entry loader:** `admin` / `com.ezyplatform.socket.monitor.plugin.EntryLoader`.
- **Controller, handler, event, and request classes (sample):** `AbstractController`, `AdminLoginController`, `ModuleRequestController`, `SettingsRequestController`, `StatisticsRequestController`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

The entry loader registered `AdminLoginController` at Socket startup. The module has no standalone Web page.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

See how packages, zones, and loaders register handlers. Test the handshake, app permissions, and private payload handling separately; a startup log is not enough.

[Back to the plugin index](README.md)
