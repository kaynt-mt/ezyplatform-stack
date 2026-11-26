# markdown

Giao diện Markdown và module Web.

- **Bản Marketplace trên core 1.5.9:** `0.2.6`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/markdown` | `org.youngmonkeys.markdown` | Không khai báo |
| `web-plugin` — `web/plugins/markdown` | `org.youngmonkeys.markdown` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 2 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `IndexController` |
| `POST /api/v1/convert-to-html` | `AdminApiMarkdownController` |

**web-plugin** — 2 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `POST /api/v1/markdown/convert-to-html` | `WebApiMarkdownController` |
| `POST /markdown/api/v1/convert-to-html` | `WebApiMarkdownController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `markdown: /`.

- **admin-plugin – Template:** `markdown/index.html`.

- **admin-plugin – Tài nguyên tĩnh:** `markdown/css/editor.css`, `markdown/css/syntax.css`, `markdown/js/editor.js`.

- **web-plugin – Tài nguyên tĩnh:** `markdown/css/editor.css`, `markdown/css/style.css`, `markdown/js/editor.js`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `markdown-admin-plugin-0.2.6.jar`, `markdown-sdk-0.2.6.jar`; 45 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.markdown.block`, `org.youngmonkeys.markdown.event`, `org.youngmonkeys.markdown.admin.event` (+17).
- **Controller/service/repository (mẫu):** `AdminApiMarkdownController`, `IndexController`, `AdminConvertMarkdownToHtmlEventSchemaFetcher`, `AdminMarkdownSettingService`, `ConvertMarkdownToHtmlEventSchemaFetcher`, `MarkdownSettingService`.
- **Class cấu hình/quyền (mẫu):** `AdminMarkdownEditorConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminConvertMarkdownToHtmlEventHandler`, `AdminProgrammingKeywordManager`, `ConvertMarkdownToHtmlEventHandler`, `ProgrammingKeywordManager`.

### web-plugin

- **JAR kiểm tra:** `markdown-sdk-0.2.6.jar`, `markdown-web-plugin-0.2.6.jar`; 46 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.markdown.block`, `org.youngmonkeys.markdown.event`, `org.youngmonkeys.markdown.web.view` (+17).
- **Controller/service/repository (mẫu):** `WebApiMarkdownController`, `WebMarkdownControllerService`, `ConvertMarkdownToHtmlEventSchemaFetcher`, `MarkdownSettingService`, `WebConvertMarkdownToHtmlEventSchemaFetcher`, `WebMarkdownControllerService`, `WebMarkdownSettingService`.
- **Điểm mở rộng tiềm năng theo tên class:** `ConvertMarkdownToHtmlEventHandler`, `ProgrammingKeywordManager`, `WebConvertMarkdownToHtmlEventHandler`, `WebProgrammingKeywordManager`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/markdown/` hiển thị trang Markdown (200).

## Lưu ý khi tích hợp

Dùng sanitizer, chặn nội dung chủ động và kiểm quyền tệp/ảnh. Trang soạn thảo mở được không chứng minh render an toàn.

[Về chỉ mục plugin](README.md)
