# ezyiot

Devices, configuration, and a Socket module.

- **Marketplace version on core 1.5.9:** `0.0.3`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyiot` | `org.youngmonkeys.ezyiot` | [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/ezyiot` | `org.youngmonkeys.ezyiot` | Not declared |
| `socket-plugin` — `socket/plugins/ezyiot` | `org.youngmonkeys.ezyiot` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 7 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /devices` | `AdminEzyIoTDeviceController` |
| `GET /settings` | `AdminSettingsController` |
| `GET /api/v1/devices` | `AdminApiEzyIoTDeviceController` |
| `POST /api/v1/devices/add` | `AdminApiEzyIoTDeviceController` |
| `PUT /api/v1/devices/status` | `AdminApiEzyIoTDeviceController` |
| `PUT /api/v1/devices/{id}` | `AdminApiEzyIoTDeviceController` |
| `DELETE /api/v1/devices` | `AdminApiEzyIoTDeviceController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyiot: /`, `dashboard: /dashboard`, `devices: /devices`, `settings: /settings`.

- **admin-plugin – Template:** `ezyiot/device/list.html`, `ezyiot/device/save-modal.html`, `ezyiot/settings.html`.

- **admin-plugin – Static resources:** `ezyiot/css/style.css`.

## Data and migrations

- **Table in the DDL package (1):** `ezyiot_devices`.
- **Class with JPA Entity/MappedSuperclass indication (1):** `EzyIoTDevice`.
- **SQL admin-plugin (1 file):** `resources/scripts/scripts.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyiot-admin-plugin-0.0.3.jar`, `ezyiot-sdk-0.0.3.jar`; 50 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyiot.pagination`, `org.youngmonkeys.ezyiot.mqtt`, `org.youngmonkeys.ezyiot.admin.converter` (+19).
- **Other library JARs:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiEzyIoTDeviceController`, `AdminApiSettingController`, `AdminEzyIoTDeviceController`, `AdminEzyIoTDeviceControllerService`, `AdminEzyIoTDeviceControllerService`, `AdminEzyIoTDeviceRepository`, `AdminEzyIoTDeviceService`, `AdminEzyIoTDeviceValidator`, `AdminPaginationEzyIoTDeviceRepository`.
- **Potential extension points based on class names:** `AdminEzyIoTSocketConnectorManager`, `EzyIoTMqttMessageListener`.

### web-plugin

- **JARs inspected:** `ezyiot-sdk-0.0.3.jar`, `ezyiot-web-plugin-0.0.3.jar`; 28 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyiot.pagination`, `org.youngmonkeys.ezyiot.mqtt`, `org.youngmonkeys.ezyiot.entity` (+6).
- **Controllers, services, and repositories (sample):** `EzyIoTDeviceRepository`, `EzyIoTDeviceService`, `PaginationEzyIoTDeviceRepository`, `PaginationEzyIoTDeviceService`.
- **Potential extension points based on class names:** `EzyIoTMqttMessageListener`.

### socket-plugin

- **JARs inspected:** `ezyiot-sdk-0.0.3.jar`, `ezyiot-socket-plugin-0.0.3.jar`; 74 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyiot.socket.plugin.mqtt`, `org.youngmonkeys.ezyiot.pagination`, `org.youngmonkeys.ezyiot.mqtt` (+16).
- **Controllers, services, and repositories (sample):** `SessionRemovedController`, `SocketEzyIoTConnectorController`, `SocketMqttController`, `UserAddedController`, `EzyIoTDeviceRepository`, `EzyIoTDeviceService`, `PaginationEzyIoTDeviceRepository`, `PaginationEzyIoTDeviceService`, `SocketEzyIoTConnectorValidator`.
- **Configuration and permission classes (sample):** `MqttProperties`, `SocketEzyIoTDeviceConfig`.
- **Potential extension points based on class names:** `EzyIoTMqttMessageListener`, `PluginEntryLoader`, `SocketMqttClient`.
- **Zone / entry loader:** `iot` / `org.youngmonkeys.ezyiot.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `SessionRemovedController`, `SocketEzyIoTConnectorController`, `SocketMqttController`, `UserAddedController`, `UserLoginController`, `UserRemovedController`, `SocketDisconnectDevicesRequest`, `SocketMqttConnectRequest`, `SocketMqttPublishRequest`, `SocketMqttSubscribeRequest` (+3).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyiot/devices` returned 200. No physical device was tested.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

See how Admin configures devices and handles events. The Admin list alone does not prove the device protocol works.

[Back to the plugin index](README.md)
