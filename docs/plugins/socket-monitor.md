# socket-monitor

Module Socket giám sát và entry loader.

- **Bản Marketplace trên core 1.5.9:** `0.0.3`.
- **Module đã xác minh:** `socket-plugin`.
- **Cài đặt:** Có sẵn. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `socket-plugin` — `socket/plugins/socket-monitor` | `com.ezyplatform.socket.monitor` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

Không tìm thấy annotation HTTP thuộc các lane Admin/Web/theme đã đọc.

Không thấy template HTML hay JS/CSS đi kèm trong các thư mục module.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### socket-plugin

- **JAR kiểm tra:** `socket-monitor-0.0.3.jar`; 24 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `com.ezyplatform.socket.monitor.plugin.data`, `com.ezyplatform.socket.monitor.plugin.controller`, `com.ezyplatform.socket.monitor.plugin.service` (+7).
- **Controller/service/repository (mẫu):** `AbstractController`, `AdminLoginController`, `ModuleRequestController`, `SettingsRequestController`, `SocketMonitorAdminPermissionService`, `SocketMonitorAdminRoleRepository`, `SocketMonitorAdminRoleService`.
- **Class cấu hình/quyền (mẫu):** `SocketMonitorPostConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `EntryLoader`, `SocketMonitorAdminRequestInterceptor`.
- **Zone / entry loader:** `admin` / `com.ezyplatform.socket.monitor.plugin.EntryLoader`.
- **Class controller/handler/event/request (mẫu):** `AbstractController`, `AdminLoginController`, `ModuleRequestController`, `SettingsRequestController`, `StatisticsRequestController`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Đã thấy entry loader đăng ký `AdminLoginController` khi Socket khởi động; không có trang Web riêng.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Lưu ý khi tích hợp

Ví dụ package, zone và loader đăng ký handler. Kiểm handshake/quyền app và xử lý payload riêng; log startup không đủ.

[Về chỉ mục plugin](README.md)
