# consulting

Tư vấn: khách hàng, nhân sự, tài liệu và theme riêng.

- **Bản Marketplace trên core 1.5.9:** `0.1.6`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `theme`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/consulting` | `org.youngmonkeys.consulting` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezylogin](ezylogin.md), [ezyoa](ezyoa.md) |
| `web-plugin` — `web/plugins/consulting` | `org.youngmonkeys.consulting` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezylogin](ezylogin.md), [ezyoa](ezyoa.md), [ecommerce](ecommerce.md), [ezycrm](ezycrm.md) |
| `theme` — `web/themes/consulting` | `org.youngmonkeys.consulting` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezylogin](ezylogin.md), [ezyaccount](ezyaccount.md), [ezyoa](ezyoa.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 4 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /branches` | `AdminBranchController` |
| `GET /customers` | `AdminCustomerController` |
| `GET /employees` | `AdminEmployeeController` |
| `GET /team-members` | `AdminTeamMembersController` |

**web-plugin** — 11 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `HomeController` |
| `GET /history` | `ServiceController` |
| `GET /services` | `ServiceController` |
| `GET /documents` | `DocumentController` |
| `GET /api/v1/documents` | `WebApiDocumentController` |
| `GET /api/v1/consultations/history` | `WebApiConsultationController` |
| `GET /faqs/{slug}` | `FaqController` |
| `POST /api/v1/services/{id}/consultation/register` | `WebApiConsultationController` |

**theme** — 11 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `HomeController` |
| `GET /history` | `ServiceController` |
| `GET /services` | `ServiceController` |
| `GET /documents` | `DocumentController` |
| `GET /api/v1/documents` | `WebApiDocumentController` |
| `GET /api/v1/consultations/history` | `WebApiConsultationController` |
| `GET /faqs/{slug}` | `FaqController` |
| `POST /api/v1/services/{id}/consultation/register` | `WebApiConsultationController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `consulting: /`, `customers: /customers`, `employees: /employees`, `members: /team-members`, `branches: /branches`, `page_fragments: /pages/fragments` (+1).

- **theme – Template:** `about-us.html`, `consultations/history.html`, `contact-us.html`, `documents/details.html`, `documents/index.html`, `faqs/details.html`, `faqs/index.html` (+27).

- **theme – Tài nguyên tĩnh:** `css/main.css`, `js/jquery.hoverdir.js`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `consulting-admin-plugin-0.1.6.jar`, `consulting-sdk-0.1.6.jar`; 12 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.consulting.admin.controller.view`, `org.youngmonkeys.consulting.admin.config`, `org.youngmonkeys.consulting.constant` (+1).
- **Controller/service/repository (mẫu):** `AdminBranchController`, `AdminConsultingHelpController`, `AdminConsultingPageFragmentController`, `AdminCustomerController`.
- **Class cấu hình/quyền (mẫu):** `AdminConsultingPostConfig`, `AdminDocumentProductConfig`, `AdminPageFragmentConfig`, `PageFragmentConfig`.

### web-plugin

- **JAR kiểm tra:** `consulting-sdk-0.1.6.jar`, `consulting-web-plugin-0.1.6.jar`; 24 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.consulting.web.controller.view`, `org.youngmonkeys.consulting.web.controller.api`, `org.youngmonkeys.consulting.web.view` (+11).
- **Controller/service/repository (mẫu):** `ApiConsultingNewsController`, `ConsultationController`, `DocumentController`, `FaqController`, `WebConsultationHistoryControllerService`, `WebConsultationValidator`, `WebDocumentService`.
- **Class cấu hình/quyền (mẫu):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `ConsultingGlobalErrorHandler`, `ConsultingGlobalExceptionHandler`, `WebConsultationViewFactory`.

### theme

- **JAR kiểm tra:** `consulting-sdk-0.1.6.jar`, `consulting-theme-0.1.6.jar`, `consulting-web-plugin-0.1.6.jar`; 35 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.consulting.web.controller.view`, `org.youngmonkeys.consulting.web.controller.api`, `org.youngmonkeys.consulting.web.view` (+11).
- **Controller/service/repository (mẫu):** `ApiConsultingNewsController`, `ConsultationController`, `DocumentController`, `FaqController`, `WebConsultationHistoryControllerService`, `WebConsultationValidator`, `WebDocumentService`.
- **Class cấu hình/quyền (mẫu):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `ConsultingGlobalErrorHandler`, `ConsultingGlobalExceptionHandler`, `WebConsultationViewFactory`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/consulting/customers` → danh sách người dùng; Web `/api/v1/documents` → 200; theme Consulting render được `/services`, `/documents`.

## Lưu ý khi tích hợp

Tách module nghiệp vụ khỏi template của theme. Redirect HTTP 200 sang CRUD của core không chứng minh plugin có màn hình riêng.

[Về chỉ mục plugin](README.md)
