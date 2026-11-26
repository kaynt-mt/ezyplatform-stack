# semi-theme

Module Admin hỗ trợ giao diện; không có Web theme.

- **Bản Marketplace trên core 1.5.9:** `1.0.2`. Metadata module báo `1.0.1`.
- **Module đã xác minh:** `admin-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/semi-theme` | `org.ltl.semi_theme` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 1 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingsController` |

- **admin-plugin – Template:** `modules/list.html`, `semi-theme/dashboards/admin.html`, `semi-theme/dashboards/scripts.html`, `semi-theme/dashboards/socket.html`, `semi-theme/dashboards/web.html`, `semi-theme/settings.html`.

- **admin-plugin – Tài nguyên tĩnh:** `css/newsemiv4/index.css`, `css/newsemiv4/index.min.css`, `css/recursive.css`, `css/semi/index.css` (+6).

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `semi-theme-admin-plugin-1.0.1.jar`; 3 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.ltl.semi_theme.admin.controller.view`.
- **Controller/service/repository (mẫu):** `AdminSettingsController`, `IndexController`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/semi-theme/` → 200; ZIP `1.0.2` khai `version=1.0.1` trong `module.properties`; đây là module Admin chứ không có Web theme.

## Áp dụng cho plugin quản lý công việc

Phân biệt tên thương mại, bản ZIP và lane đã cài. Không chọn Semi Theme trong trình chạy theme Web, không suy ra tùy biến theme từ trang Admin có tiêu đề Unknown.

[Về chỉ mục plugin](README.md)
