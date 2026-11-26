# logs-monitor

Console, thư mục log và lane Socket.

- **Bản Marketplace trên core 1.5.9:** `0.0.5`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/logs-monitor` | `org.youngmonkeys.logsmonitor` | Không khai báo |
| `web-plugin` — `web/plugins/logs-monitor` | `org.youngmonkeys.logsmonitor` | Không khai báo |
| `socket-plugin` — `socket/plugins/logs-monitor` | `org.youngmonkeys.logsmonitor` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 12 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `logs_monitor: /`, `console: /console`, `log_folder: /log-folder`, `settings: /logs-monitor/settings`.

- **admin-plugin – Template:** `logs-monitor/console/index.html`, `logs-monitor/folder/index.html`, `logs-monitor/settings/index.html`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `logs-monitor-admin-plugin-0.0.5.jar`, `logs-monitor-sdk-0.0.5.jar`; 22 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.logsmonitor.admin.controller.view`, `org.youngmonkeys.logsmonitor.admin.controller.api`, `org.youngmonkeys.logsmonitor.admin.response` (+9).
- **Controller/service/repository (mẫu):** `AdminApiLogFilesController`, `AdminApiLogsController`, `AdminApiLogsMonitorSettingController`, `AdminApiSlackLogsController`, `AdminLogFileService`, `AdminLogsMonitorSettingValidator`.
- **Class cấu hình/quyền (mẫu):** `AdminLogFilesDeletionScheduleConfig`, `AdminSlackLogbackAppenderConfig`, `SlackLogbackAppenderConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminLogFileManager`.

### web-plugin

- **JAR kiểm tra:** `logs-monitor-sdk-0.0.5.jar`, `logs-monitor-web-plugin-0.0.5.jar`; 4 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.logsmonitor.web.config`, `org.youngmonkeys.logsmonitor.config`, `org.youngmonkeys.logsmonitor.constant` (+1).
- **Class cấu hình/quyền (mẫu):** `SlackLogbackAppenderConfig`, `WebSlackLogbackAppenderConfig`.

### socket-plugin

- **JAR kiểm tra:** `logs-monitor-sdk-0.0.5.jar`, `logs-monitor-socket-plugin-0.0.5.jar`; 5 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.logsmonitor.config`, `org.youngmonkeys.logsmonitor.socket.plugin.config`, `org.youngmonkeys.logsmonitor.constant` (+2).
- **Class cấu hình/quyền (mẫu):** `SlackLogbackAppenderConfig`, `SocketSlackLogbackAppenderConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `PluginEntryLoader`.
- **Zone / entry loader:** `admin` / `org.youngmonkeys.logsmonitor.socket.plugin.PluginEntryLoader`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/logs-monitor/console` và `/logs-monitor/log-folder` → 200.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Áp dụng cho plugin quản lý công việc

Tham khảo quan sát runtime để chẩn đoán module/job. Không ghi nội dung issue riêng, token hoặc cookie vào log; chỉ log correlation ID, loại sự kiện và kết quả có kiểm soát.

[Về chỉ mục plugin](README.md)
