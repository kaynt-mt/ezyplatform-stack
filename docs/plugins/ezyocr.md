# ezyocr

Kịch bản OCR và cấu hình nhận dạng.

- **Bản Marketplace trên core 1.5.9:** `0.0.3`.
- **Module đã xác minh:** `admin-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyocr` | `org.youngmonkeys.ezyocr` | [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 21 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingsController` |
| `GET /ocr-business-scripts` | `AdminOcrBusinessScriptController` |
| `GET /ocr-business-scripts/add` | `AdminOcrBusinessScriptController` |
| `GET /api/v1/ocr-operators` | `AdminApiOcrOperatorController` |
| `GET /api/v1/ocr-business-scripts` | `AdminApiOcrBusinessScriptController` |
| `GET /api/v1/app-releases/latest` | `AdminApiAppReleaseController` |
| `GET /api/v1/ocr-business-scripts/categories` | `AdminApiOcrBusinessScriptController` |
| `POST /api/v1/ocr-operators/add` | `AdminApiOcrOperatorController` |
| `POST /api/v1/ocr-business-scripts/add` | `AdminApiOcrBusinessScriptController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/ocr-business-scripts/{scriptId}` | `AdminApiOcrBusinessScriptController` |
| `PUT /api/v1/ocr-operators/{adminId}/settings` | `AdminApiOcrOperatorController` |
| `PUT /api/v1/ocr-business-scripts/{scriptId}/publish` | `AdminApiOcrBusinessScriptController` |
| `DELETE /api/v1/ocr-operators/{adminId}` | `AdminApiOcrOperatorController` |
| `DELETE /api/v1/ocr-business-scripts/{scriptId}` | `AdminApiOcrBusinessScriptController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyocr: /`, `ocr_business_scripts: /ocr-business-scripts`, `ocr_business_scripts_add: ~/ocr-business-scripts/add`, `ocr_business_scripts_edit: ~/ocr-business-scripts/{scriptId}/edit`, `ocr_business_scripts_details: ~/ocr-business-scripts/{scriptId}`, `settings: /settings`.

- **admin-plugin – Template:** `ezyocr/ocr-business-scripts/add.html`, `ezyocr/ocr-business-scripts/category-list.html`, `ezyocr/ocr-business-scripts/details.html`, `ezyocr/ocr-business-scripts/edit.html`, `ezyocr/ocr-business-scripts/form.html`, `ezyocr/ocr-business-scripts/list.html`, `ezyocr/ocr-business-scripts/script-list.html` (+3).

- **admin-plugin – Tài nguyên tĩnh:** `ezyocr/css/style.css`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyocr-admin-plugin-0.0.3.jar`; 52 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyocr.admin.response`, `org.youngmonkeys.ezyocr.admin.constant`, `org.youngmonkeys.ezyocr.admin.controller.api` (+12).
- **Controller/service/repository (mẫu):** `AdminApiAppReleaseController`, `AdminApiOcrBusinessScriptController`, `AdminApiOcrOperatorController`, `AdminApiOcrOperatorMeController`, `AdminAppReleaseControllerService`, `AdminAppReleaseService`, `AdminAppReleaseValidator`, `AdminEzyocrSettingService`, `AdminEzyocrSettingsValidator`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyocrAdminRoleConfig`, `AdminEzyocrBusinessScriptConfig`, `AdminEzyocrPostConfig`, `AdminEzyocrTermTypeConfig`, `OcrOperatorSetting`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyocr/ocr-business-scripts` → 200. Chưa cấu hình OCR bên ngoài.

## Lưu ý khi tích hợp

Nếu dùng OCR bất đồng bộ, kiểm retry, quyền tệp và giới hạn dữ liệu gửi ra ngoài. Màn hình cấu hình không chứng minh OCR chạy.

[Về chỉ mục plugin](README.md)
