# wordpress

Cấu hình và luồng nhập dữ liệu WordPress.

- **Bản Marketplace trên core 1.5.9:** `0.1.4`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/wordpress` | `org.youngmonkeys.wordpress` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/wordpress` | `org.youngmonkeys.wordpress` | [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 16 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `WordpressSettingController` |
| `GET /migration` | `MigrationController` |
| `GET /public/media/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{month}/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{fileName}` | `AdminWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{fileName}` | `AdminWpMediaController` |
| `POST /api/v1/connect-database` | `ApiMigrationController` |
| `POST /api/v1/start-data-migration` | `ApiMigrationController` |
| `PUT /api/v1/settings` | `ApiWordpressSettingController` |
| `PUT /api/v1/disconnect-database` | `ApiMigrationController` |
| `PUT /api/v1/stop-data-migration` | `ApiMigrationController` |
| `PUT /api/v1/restart-data-migration` | `ApiMigrationController` |
| `DELETE /api/v1/clear-database-information` | `ApiMigrationController` |

**web-plugin** — 7 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /public/media/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{minute}/{fileName}` | `WebWpMediaController` |
| `GET /public/media/{year}/{month}/{day}/{hour}/{minute}/{second}/{fileName}` | `WebWpMediaController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `wordpress: /`, `migrate_data: /migration`, `settings: /settings`.

- **admin-plugin – Template:** `wordpress/migration/index.html`, `wordpress/setting/index.html`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `wordpress-admin-plugin-0.1.4.jar`, `wordpress-sdk-0.1.4.jar`; 36 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.wordpress.admin.migrator`, `org.youngmonkeys.wordpress.admin.event`, `org.youngmonkeys.wordpress.admin.request` (+10).
- **JAR thư viện khác:** `jwordpress-1.0.5.jar`.
- **Controller/service/repository (mẫu):** `AdminWpMediaController`, `ApiMigrationController`, `ApiWordpressSettingController`, `IndexController`, `AdminWordpressSettingService`, `MigrationValidator`, `WordpressSettingService`.
- **Điểm mở rộng tiềm năng theo tên class:** `WpGetMediaFilePathEventHandler`, `WpMigrationFinishedEventHandler`, `WpMigrationFinshedEvent`, `WpMigrationRestartEvent`, `WpMigrationRestartEventHandler`, `WpMigratorManager`.

### web-plugin

- **JAR kiểm tra:** `wordpress-sdk-0.1.4.jar`, `wordpress-web-plugin-0.1.4.jar`; 4 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.wordpress.web.service`, `org.youngmonkeys.wordpress.web.controller.api`, `org.youngmonkeys.wordpress.service` (+1).
- **JAR thư viện khác:** `jwordpress-1.0.5.jar`.
- **Controller/service/repository (mẫu):** `WebWpMediaController`, `WebWordpressSettingService`, `WordpressSettingService`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/wordpress/migration` → 200; chưa nhập dữ liệu từ WordPress.

## Áp dụng cho plugin quản lý công việc

Mẫu cho màn hình migration. Import issue sau này nên có dry-run, mapping ID và báo cáo lỗi từng dòng; chưa có bằng chứng kết nối WordPress trên sandbox.

[Về chỉ mục plugin](README.md)
