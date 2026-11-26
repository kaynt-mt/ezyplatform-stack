# game-master-server

Game master and instance management.

- **Marketplace version on core 1.5.9:** `0.0.7`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/game-master-server` | `org.youngmonkeys.masterserver` | Not declared |
| `web-plugin` — `web/plugins/game-master-server` | `org.youngmonkeys.masterserver` | Not declared |
| `socket-plugin` — `socket/plugins/game-master-server` | `org.youngmonkeys.masterserver.socket.plugin` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 14 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingsController` |
| `GET /instances` | `AdminInstancesController` |
| `GET /api/v1/instances/` | `AdminApiAuthenticatedInstanceController` |
| `GET /api/v1/instances/{instanceId}` | `AdminApiAuthenticatedInstanceController` |
| `POST /api/v1/instances/` | `AdminApiAuthenticatedInstanceController` |
| `POST /api/v1/room-instances/` | `AdminApiRoomInstanceController` |
| `POST /api/v1/settings/broker-connection-settings` | `AdminApiSettingController` |
| `POST /api/v1/settings/game-master-server-admin-url` | `AdminApiSettingController` |
| `PUT /api/v1/settings/api-key` | `AdminApiSettingController` |
| `PUT /api/v1/instances/{instanceId}` | `AdminApiAuthenticatedInstanceController` |
| `PUT /api/v1/room-instances/{instanceId}/status` | `AdminApiRoomInstanceController` |
| `PUT /api/v1/room-instances/{instanceId}/player-count` | `AdminApiRoomInstanceController` |
| `DELETE /api/v1/room-instances/{instanceId}` | `AdminApiRoomInstanceController` |

**web-plugin** — 3 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/game-master-server/instances` | `WebInstanceController` |
| `GET /api/v1/game-master-server/validate-token` | `AuthenticationController` |
| `GET /api/v1/game-master-server/instances/allocation` | `WebInstanceController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `game_master_server: /game-master-server`, `instances: /game-master-server/instances`, `settings: /game-master-server/settings`.

- **admin-plugin – Template:** `game-master-server/instances/index.html`, `game-master-server/settings/index.html`.

- **admin-plugin – Static resources:** `game-master-server/js/main.js`.

## Data and migrations

- **Table in the DDL package (1):** `game_master_server_instances`.
- **Class with JPA Entity/MappedSuperclass indication (1):** `Instance`.
- **SQL admin-plugin (2 files):** `resources/scripts/scripts.sql`, `resources/scripts/alter_instances.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `game-master-server-admin-plugin-0.0.7.jar`, `game-master-server-sdk-0.0.7.jar`; 64 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.masterserver.admin.request`, `org.youngmonkeys.masterserver.pagination`, `org.youngmonkeys.masterserver.admin.service` (+22).
- **Other library JARs:** `ezyfox-server-java-client-1.2.8.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiAuthenticatedInstanceController`, `AdminApiRoomInstanceController`, `AdminApiSettingController`, `AdminInstanceControllerService`, `AdminApiKeyValidator`, `AdminGameMasterServerSettingService`, `AdminInstanceControllerService`, `AdminInstanceRepository`, `AdminInstanceService`.
- **Configuration and permission classes (sample):** `GameMasterServerConfig`.
- **Potential extension points based on class names:** `AdminInstanceBuildPathSupplierRegistry`, `InstanceManager`.

### web-plugin

- **JARs inspected:** `game-master-server-sdk-0.0.7.jar`, `game-master-server-web-plugin-0.0.7.jar`; 36 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.masterserver.pagination`, `org.youngmonkeys.masterserver.entity`, `org.youngmonkeys.masterserver.web.converter` (+14).
- **Controllers, services, and repositories (sample):** `AuthenticationController`, `WebInstanceController`, `WebInstanceControllerService`, `InstanceRepository`, `InstanceService`, `PaginationInstanceRepository`, `PaginationInstanceService`, `WebInstanceControllerService`.
- **Potential extension points based on class names:** `AuthenticationInterceptor`.

### socket-plugin

- **JARs inspected:** `game-master-server-sdk-0.0.7.jar`, `game-master-server-socket-plugin-0.0.7.jar`; 32 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.masterserver.pagination`, `org.youngmonkeys.masterserver.entity`, `org.youngmonkeys.masterserver.converter` (+13).
- **Controllers, services, and repositories (sample):** `BrokerController`, `UserLoginController`, `InstanceRepository`, `InstanceService`, `PaginationInstanceRepository`, `PaginationInstanceService`, `SocketInstanceRepository`.
- **Configuration and permission classes (sample):** `EzyPluginContextConfig`.
- **Potential extension points based on class names:** `PluginEntryLoader`.
- **Zone / entry loader:** `game-master-server` / `org.youngmonkeys.masterserver.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `BrokerController`, `UserLoginController`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/game-master-server/game-master-server` returned 200; the Web instances API returned 401 without a login. No game instance was started.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Use this as an example of orchestrating an external service. A 401 for an anonymous caller does not prove instance provisioning or Socket login works.

[Back to the plugin index](README.md)
