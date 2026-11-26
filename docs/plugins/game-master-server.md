# game-master-server

Quản lý game master và các instance.

- **Bản Marketplace trên core 1.5.9:** `0.0.7`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/game-master-server` | `org.youngmonkeys.masterserver` | Không khai báo |
| `web-plugin` — `web/plugins/game-master-server` | `org.youngmonkeys.masterserver` | Không khai báo |
| `socket-plugin` — `socket/plugins/game-master-server` | `org.youngmonkeys.masterserver.socket.plugin` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 14 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

**web-plugin** — 3 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/game-master-server/instances` | `WebInstanceController` |
| `GET /api/v1/game-master-server/validate-token` | `AuthenticationController` |
| `GET /api/v1/game-master-server/instances/allocation` | `WebInstanceController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `game_master_server: /game-master-server`, `instances: /game-master-server/instances`, `settings: /game-master-server/settings`.

- **admin-plugin – Template:** `game-master-server/instances/index.html`, `game-master-server/settings/index.html`.

- **admin-plugin – Tài nguyên tĩnh:** `game-master-server/js/main.js`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (1):** `game_master_server_instances`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (1):** `Instance`.
- **SQL admin-plugin (2 tệp):** `resources/scripts/scripts.sql`, `resources/scripts/alter_instances.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `game-master-server-admin-plugin-0.0.7.jar`, `game-master-server-sdk-0.0.7.jar`; 64 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.masterserver.admin.request`, `org.youngmonkeys.masterserver.pagination`, `org.youngmonkeys.masterserver.admin.service` (+22).
- **JAR thư viện khác:** `ezyfox-server-java-client-1.2.8.jar`.
- **Controller/service/repository (mẫu):** `AdminApiAuthenticatedInstanceController`, `AdminApiRoomInstanceController`, `AdminApiSettingController`, `AdminInstanceControllerService`, `AdminApiKeyValidator`, `AdminGameMasterServerSettingService`, `AdminInstanceControllerService`, `AdminInstanceRepository`, `AdminInstanceService`.
- **Class cấu hình/quyền (mẫu):** `GameMasterServerConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminInstanceBuildPathSupplierRegistry`, `InstanceManager`.

### web-plugin

- **JAR kiểm tra:** `game-master-server-sdk-0.0.7.jar`, `game-master-server-web-plugin-0.0.7.jar`; 36 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.masterserver.pagination`, `org.youngmonkeys.masterserver.entity`, `org.youngmonkeys.masterserver.web.converter` (+14).
- **Controller/service/repository (mẫu):** `AuthenticationController`, `WebInstanceController`, `WebInstanceControllerService`, `InstanceRepository`, `InstanceService`, `PaginationInstanceRepository`, `PaginationInstanceService`, `WebInstanceControllerService`.
- **Điểm mở rộng tiềm năng theo tên class:** `AuthenticationInterceptor`.

### socket-plugin

- **JAR kiểm tra:** `game-master-server-sdk-0.0.7.jar`, `game-master-server-socket-plugin-0.0.7.jar`; 32 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.masterserver.pagination`, `org.youngmonkeys.masterserver.entity`, `org.youngmonkeys.masterserver.converter` (+13).
- **Controller/service/repository (mẫu):** `BrokerController`, `UserLoginController`, `InstanceRepository`, `InstanceService`, `PaginationInstanceRepository`, `PaginationInstanceService`, `SocketInstanceRepository`.
- **Class cấu hình/quyền (mẫu):** `EzyPluginContextConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `PluginEntryLoader`.
- **Zone / entry loader:** `game-master-server` / `org.youngmonkeys.masterserver.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `BrokerController`, `UserLoginController`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/game-master-server/game-master-server` → 200; Web API instances → 401 khi chưa đăng nhập. Chưa chạy game instance.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Áp dụng cho plugin quản lý công việc

Mẫu quan sát điều phối service ngoài; không cần cho MVP. HTTP 401 với guest không chứng minh cấp phát instance hoặc đăng nhập Socket hoạt động.

[Về chỉ mục plugin](README.md)
