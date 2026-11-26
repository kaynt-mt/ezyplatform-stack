# data-backup

Sao lưu dữ liệu và lập lịch snapshot.

- **Bản Marketplace trên core 1.5.9:** `0.0.9`.
- **Module đã xác minh:** `admin-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/data-backup` | `org.youngmonkeys.databackup` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 25 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingController` |
| `GET /backup-clients` | `AdminBackupClientController` |
| `GET /api/v1/realtime-backup/status` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/clients` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/database/tool-logs` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/database/privileges` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/platform-files/deletion-setting` | `AdminApiRealtimeBackupController` |
| `POST /api/v1/realtime-backup/database/snapshots` | `AdminApiRealtimeBackupController` |
| `POST /api/v1/realtime-backup/database/privileges` | `AdminApiRealtimeBackupController` |
| `POST /api/v1/realtime-backup/platform-files/delete` | `AdminApiRealtimeBackupController` |
| `POST /data-backup/api/v1/realtime-backup/client/ping` | `AdminApiRealtimeBackupClientController` |
| `PUT /api/v1/settings/s3` | `AdminApiDataBackSettingController` |
| `PUT /api/v1/settings/scheduler` | `AdminApiDataBackSettingController` |
| `PUT /api/v1/settings/ezyplatform-backup` | `AdminApiDataBackSettingController` |
| `PUT /api/v1/settings/platform-file-deletion` | `AdminApiDataBackSettingController` |
| `DELETE /api/v1/realtime-backup/clients/{clientId}` | `AdminApiRealtimeBackupController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `data_backup: /`, `backup_clients: /data-backup/backup-clients`, `settings: /data-backup/settings`.

- **admin-plugin – Template:** `data-backup/backup-clients.html`, `data-backup/settings.html`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `data-backup-admin-plugin-0.0.9.jar`; 90 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.databackup.admin.model`, `org.youngmonkeys.databackup.admin.response`, `org.youngmonkeys.databackup.admin.manager` (+14).
- **Controller/service/repository (mẫu):** `AdminApiDataBackSettingController`, `AdminApiRealtimeBackupClientController`, `AdminApiRealtimeBackupController`, `AdminBackupClientController`, `AdminDataBackSettingValidator`, `AdminDataBackupSettingService`, `AdminPlatformFileDeletionValidator`, `AdminRealtimeBackupClientControllerService`, `AdminRealtimeBackupClientService`.
- **Class cấu hình/quyền (mẫu):** `AdminAwsS3ClientConfig`, `AdminEzyPlatformBackupDeletionSchedulerConfig`, `AdminRealtimeBackupConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminAwsS3ClientManager`, `AdminDatabaseSnapshotS3Manager`, `AdminDatabaseToolLogManager`, `AdminDatabaseToolManager`, `AdminEzyPlatformBackupDeletionScheduler`, `AdminRealtimeAsyncResponseManager`, `AdminRealtimeBackupClientFileManager`, `AdminRealtimeBackupClientManager`, `AdminRealtimeBackupScheduler` (+8).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/data-backup/backup-clients` → 200; backup tự động lỗi vì container ứng dụng thiếu MySQL/MariaDB CLI; chưa thử restore.

## Áp dụng cho plugin quản lý công việc

Mẫu hữu ích là tách scheduler, client đích và cấu hình vận hành khỏi giao diện quản trị. Kế hoạch sao lưu task plugin phải thử restore trên DB khác; mở được trang Backup Clients không chứng minh có bản sao.

[Về chỉ mục plugin](README.md)
