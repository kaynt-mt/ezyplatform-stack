# sites

Quản lý máy chủ và cấu hình site.

- **Bản Marketplace trên core 1.5.9:** `0.0.3`.
- **Module đã xác minh:** `admin-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/sites` | `org.youngmonkeys.sites` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 17 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `sites: /`, `servers: /servers`, `settings: /settings`.

- **admin-plugin – Template:** `sites/servers/list.html`, `sites/settings/index.html`.

- **admin-plugin – Tài nguyên tĩnh:** `sites/css/style.css`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (1):** `sites_servers`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (1):** `SiteServer`.
- **SQL admin-plugin (2 tệp):** `resources/scripts/scripts.sql`, `resources/scripts/alter_servers_node_statuses.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `sites-admin-plugin-0.0.3.jar`, `sites-sdk-0.0.3.jar`; 71 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.sites.pagination`, `org.youngmonkeys.sites.admin.service`, `org.youngmonkeys.sites.admin.controller.api` (+26).
- **JAR thư viện khác:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controller/service/repository (mẫu):** `AdminApiSettingController`, `AdminApiSiteServerController`, `AdminApiSiteServerProxyController`, `AdminApiSocketProxyController`, `AdminPaginationSiteServerRepository`, `AdminPaginationSiteServerService`, `AdminSiteServerControllerService`, `AdminSiteServerProxyControllerService`, `AdminSiteServerProxyValidator`.
- **Class cấu hình/quyền (mẫu):** `AdminSitesSettings`, `AdminSocketProxyPermissionSettings`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminServerPropertiesUpdatedEventHandler`, `AdminSiteServerNodeManager`, `AdminSocketConnector`, `AdminSocketConnectorManager`, `AdminSocketProxyPermissionManager`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/sites/servers` và `/sites/settings` → 200; chưa tạo site/host mới.

## Áp dụng cho plugin quản lý công việc

Nghiên cứu ở cấp vận hành nhiều site, không dùng một site thay ACL workspace. Tách cấu hình host/deployment khỏi mô hình workspace để vẫn chạy single-host trong development.

[Về chỉ mục plugin](README.md)
