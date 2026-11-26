# logs-monitor

Console, log directory, and Socket module.

- **Marketplace version on core 1.5.9:** `0.0.5`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/logs-monitor` | `org.youngmonkeys.logsmonitor` | Not declared |
| `web-plugin` — `web/plugins/logs-monitor` | `org.youngmonkeys.logsmonitor` | Not declared |
| `socket-plugin` — `socket/plugins/logs-monitor` | `org.youngmonkeys.logsmonitor` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 12 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /console` | `AdminConsoleController` |
| `GET /settings` | `AdminSettingsController` |
| `GET /log-folder` | `AdminLogFolderController` |
| `GET /api/v1/log-files` | `AdminApiLogFilesController` |
| `GET /api/v1/logs/tail` | `AdminApiLogsController` |
| `GET /api/v1/logs/before` | `AdminApiLogsController` |
| `GET /api/v1/logs/search` | `AdminApiLogsController` |
| `POST /api/v1/slack-logs/test` | `AdminApiSlackLogsController` |
| `PUT /api/v1/settings/log-files` | `AdminApiLogsMonitorSettingController` |
| `PUT /api/v1/settings/slack-logs` | `AdminApiLogsMonitorSettingController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `logs_monitor: /`, `console: /console`, `log_folder: /log-folder`, `settings: /logs-monitor/settings`.

- **admin-plugin – Template:** `logs-monitor/console/index.html`, `logs-monitor/folder/index.html`, `logs-monitor/settings/index.html`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `logs-monitor-admin-plugin-0.0.5.jar`, `logs-monitor-sdk-0.0.5.jar`; 22 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.logsmonitor.admin.controller.view`, `org.youngmonkeys.logsmonitor.admin.controller.api`, `org.youngmonkeys.logsmonitor.admin.response` (+9).
- **Controllers, services, and repositories (sample):** `AdminApiLogFilesController`, `AdminApiLogsController`, `AdminApiLogsMonitorSettingController`, `AdminApiSlackLogsController`, `AdminLogFileService`, `AdminLogsMonitorSettingValidator`.
- **Configuration and permission classes (sample):** `AdminLogFilesDeletionScheduleConfig`, `AdminSlackLogbackAppenderConfig`, `SlackLogbackAppenderConfig`.
- **Potential extension points based on class names:** `AdminLogFileManager`.

### web-plugin

- **JARs inspected:** `logs-monitor-sdk-0.0.5.jar`, `logs-monitor-web-plugin-0.0.5.jar`; 4 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.logsmonitor.web.config`, `org.youngmonkeys.logsmonitor.config`, `org.youngmonkeys.logsmonitor.constant` (+1).
- **Configuration and permission classes (sample):** `SlackLogbackAppenderConfig`, `WebSlackLogbackAppenderConfig`.

### socket-plugin

- **JARs inspected:** `logs-monitor-sdk-0.0.5.jar`, `logs-monitor-socket-plugin-0.0.5.jar`; 5 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.logsmonitor.config`, `org.youngmonkeys.logsmonitor.socket.plugin.config`, `org.youngmonkeys.logsmonitor.constant` (+2).
- **Configuration and permission classes (sample):** `SlackLogbackAppenderConfig`, `SocketSlackLogbackAppenderConfig`.
- **Potential extension points based on class names:** `PluginEntryLoader`.
- **Zone / entry loader:** `admin` / `org.youngmonkeys.logsmonitor.socket.plugin.PluginEntryLoader`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/logs-monitor/console` and `/logs-monitor/log-folder` returned 200.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Use it to diagnose modules and jobs. Keep sensitive business data, tokens, and cookies out of logs.

[Back to the plugin index](README.md)
