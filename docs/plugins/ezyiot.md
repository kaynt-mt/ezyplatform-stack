# ezyiot

Thiết bị, cấu hình và lane Socket.

- **Bản Marketplace trên core 1.5.9:** `0.0.3`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyiot` | `org.youngmonkeys.ezyiot` | [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/ezyiot` | `org.youngmonkeys.ezyiot` | Không khai báo |
| `socket-plugin` — `socket/plugins/ezyiot` | `org.youngmonkeys.ezyiot` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 7 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /devices` | `AdminEzyIoTDeviceController` |
| `GET /settings` | `AdminSettingsController` |
| `GET /api/v1/devices` | `AdminApiEzyIoTDeviceController` |
| `POST /api/v1/devices/add` | `AdminApiEzyIoTDeviceController` |
| `PUT /api/v1/devices/status` | `AdminApiEzyIoTDeviceController` |
| `PUT /api/v1/devices/{id}` | `AdminApiEzyIoTDeviceController` |
| `DELETE /api/v1/devices` | `AdminApiEzyIoTDeviceController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyiot: /`, `dashboard: /dashboard`, `devices: /devices`, `settings: /settings`.

- **admin-plugin – Template:** `ezyiot/device/list.html`, `ezyiot/device/save-modal.html`, `ezyiot/settings.html`.

- **admin-plugin – Tài nguyên tĩnh:** `ezyiot/css/style.css`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (1):** `ezyiot_devices`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (1):** `EzyIoTDevice`.
- **SQL admin-plugin (1 tệp):** `resources/scripts/scripts.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyiot-admin-plugin-0.0.3.jar`, `ezyiot-sdk-0.0.3.jar`; 50 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyiot.pagination`, `org.youngmonkeys.ezyiot.mqtt`, `org.youngmonkeys.ezyiot.admin.converter` (+19).
- **JAR thư viện khác:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controller/service/repository (mẫu):** `AdminApiEzyIoTDeviceController`, `AdminApiSettingController`, `AdminEzyIoTDeviceController`, `AdminEzyIoTDeviceControllerService`, `AdminEzyIoTDeviceControllerService`, `AdminEzyIoTDeviceRepository`, `AdminEzyIoTDeviceService`, `AdminEzyIoTDeviceValidator`, `AdminPaginationEzyIoTDeviceRepository`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminEzyIoTSocketConnectorManager`, `EzyIoTMqttMessageListener`.

### web-plugin

- **JAR kiểm tra:** `ezyiot-sdk-0.0.3.jar`, `ezyiot-web-plugin-0.0.3.jar`; 28 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyiot.pagination`, `org.youngmonkeys.ezyiot.mqtt`, `org.youngmonkeys.ezyiot.entity` (+6).
- **Controller/service/repository (mẫu):** `EzyIoTDeviceRepository`, `EzyIoTDeviceService`, `PaginationEzyIoTDeviceRepository`, `PaginationEzyIoTDeviceService`.
- **Điểm mở rộng tiềm năng theo tên class:** `EzyIoTMqttMessageListener`.

### socket-plugin

- **JAR kiểm tra:** `ezyiot-sdk-0.0.3.jar`, `ezyiot-socket-plugin-0.0.3.jar`; 74 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyiot.socket.plugin.mqtt`, `org.youngmonkeys.ezyiot.pagination`, `org.youngmonkeys.ezyiot.mqtt` (+16).
- **Controller/service/repository (mẫu):** `SessionRemovedController`, `SocketEzyIoTConnectorController`, `SocketMqttController`, `UserAddedController`, `EzyIoTDeviceRepository`, `EzyIoTDeviceService`, `PaginationEzyIoTDeviceRepository`, `PaginationEzyIoTDeviceService`, `SocketEzyIoTConnectorValidator`.
- **Class cấu hình/quyền (mẫu):** `MqttProperties`, `SocketEzyIoTDeviceConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `EzyIoTMqttMessageListener`, `PluginEntryLoader`, `SocketMqttClient`.
- **Zone / entry loader:** `iot` / `org.youngmonkeys.ezyiot.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `SessionRemovedController`, `SocketEzyIoTConnectorController`, `SocketMqttController`, `UserAddedController`, `UserLoginController`, `UserRemovedController`, `SocketDisconnectDevicesRequest`, `SocketMqttConnectRequest`, `SocketMqttPublishRequest`, `SocketMqttSubscribeRequest` (+3).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyiot/devices` → 200; chưa thử thiết bị vật lý.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Lưu ý khi tích hợp

Ví dụ Admin cấu hình thiết bị và xử lý sự kiện. Không suy giao thức thiết bị hoạt động chỉ từ danh sách Admin.

[Về chỉ mục plugin](README.md)
