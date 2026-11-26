# postgresql

Bề mặt quản trị PostgreSQL.

- **Bản Marketplace trên core 1.5.9:** `0.0.1`.
- **Module đã xác minh:** `admin-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/postgresql` | `org.youngmonkeys.postgresql` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 6 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /dashboard` | `AdminDashboardController` |
| `GET /api/v1/dashboard/tables` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/overview` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/datasource` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/active-queries` | `AdminApiDashboardController` |
| `GET /api/v1/dashboard/connection-states` | `AdminApiDashboardController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `postgresql: /`, `dashboard: /dashboard`.

- **admin-plugin – Template:** `postgresql/dashboard.html`.

- **admin-plugin – Tài nguyên tĩnh:** `postgresql/css/dashboard.css`, `postgresql/css/style.css`, `postgresql/js/dashboard.js`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `postgresql-42.7.4.jar`, `postgresql-admin-plugin-0.0.1.jar`; 361 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.postgresql.core`, `org.postgresql.util`, `org.postgresql.jdbc` (+46).
- **JAR thư viện khác:** `checker-qual-3.42.0.jar`.
- **Controller/service/repository (mẫu):** `AdminApiDashboardController`, `AdminDashboardController`, `AdminPostgresqlDashboardControllerService`, `IndexController`, `AdminPostgresqlDashboardControllerService`, `AdminPostgresqlStatisticService`.
- **Class cấu hình/quyền (mẫu):** `AdminPostgresqlSqlScriptsConverterConfig`, `ChannelBindingOption`, `CommonOptions`, `ExpressionProperties`, `LogicalReplicationOptions`, `Option`, `PhysicalReplicationOptions`.
- **Điểm mở rộng tiềm năng theo tên class:** `ArrayAssistantRegistry`, `AuthenticationPluginManager`, `BatchResultHandler`, `CallableBatchResultHandler`, `ClientFinalProcessor`, `ConnectionFactory`, `CopyManager`, `DbKeyStoreSocketFactory`, `DefaultJavaSSLFactory` (+27).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/postgresql/dashboard` → 200 trên stack MySQL; chưa đổi datasource hay thử PostgreSQL thật.

## Lưu ý khi tích hợp

Nếu đổi engine DB, chạy lại migration, phân trang và truy vấn. Dashboard Admin không chứng minh tích hợp datasource hoạt động.

[Về chỉ mục plugin](README.md)
