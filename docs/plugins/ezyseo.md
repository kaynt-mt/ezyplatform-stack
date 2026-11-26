# ezyseo

Sitemap, liên kết và robots.

- **Bản Marketplace trên core 1.5.9:** `0.1.2`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyseo` | `org.youngmonkeys.ezyseo` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezyseo` | `org.youngmonkeys.ezyseo` | [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 13 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /links` | `AdminLinkController` |
| `GET /settings` | `AdminSettingController` |
| `GET /sitemaps` | `AdminSitemapController` |
| `GET /links/add` | `AdminLinkController` |
| `GET /api/v1/links` | `AdminApiLinkController` |
| `GET /api/v1/sitemaps` | `AdminApiSitemapController` |
| `GET /links/{linkId}/edit` | `AdminLinkController` |
| `POST /api/v1/links/add` | `AdminApiLinkController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/sitemaps` | `AdminApiSitemapController` |
| `PUT /api/v1/links/{linkId}` | `AdminApiLinkController` |
| `DELETE /api/v1/links/{linkId}` | `AdminApiLinkController` |

**web-plugin** — 3 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /robots.txt` | `ApiRobotsController` |
| `GET /api/v1/sitemaps` | `ApiSitemapController` |
| `GET /api/v1/sitemaps/{linkType}` | `ApiSitemapController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyseo: /`, `sitemaps: /sitemaps`, `links: /links`, `links_add: ~/links/add`, `links_edit: ~/links/{linkId}/edit`, `settings: /settings`.

- **admin-plugin – Template:** `ezyseo/links/add-new-type.html`, `ezyseo/links/add.html`, `ezyseo/links/edit.html`, `ezyseo/links/list.html`, `ezyseo/links/scripts.html`, `ezyseo/setting/index.html`, `ezyseo/sitemaps/list.html`.

- **admin-plugin – Tài nguyên tĩnh:** `css/ezyseo.css`.

- **web-plugin – Tài nguyên tĩnh:** `css/ezyseo/style.css`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyseo-admin-plugin-0.1.2.jar`, `ezyseo-sdk-0.1.2.jar`; 41 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyseo.admin.response`, `org.youngmonkeys.ezyseo.admin.serializer`, `org.youngmonkeys.ezyseo.admin.controller.view` (+15).
- **Controller/service/repository (mẫu):** `AdminApiLinkController`, `AdminApiSettingController`, `AdminApiSitemapController`, `AdminIndexController`, `AdminEzySeoLinkService`, `AdminEzySeoLinkValidator`, `AdminEzySeoSettingService`, `AdminEzySeoSettingValidator`, `AdminLinkControllerService`.
- **Class cấu hình/quyền (mẫu):** `AdminScheduledSitemapConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminEzySeoFileSystemManager`, `EzySeoFileSystemManager`.

### web-plugin

- **JAR kiểm tra:** `ezyseo-sdk-0.1.2.jar`, `ezyseo-web-plugin-0.1.2.jar`; 9 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyseo.common.constant`, `org.youngmonkeys.ezyseo.web.controller.api`, `org.youngmonkeys.ezyseo.common.service` (+4).
- **Controller/service/repository (mẫu):** `ApiRobotsController`, `ApiSitemapController`, `EzySeoSettingService`, `WebEzySeoSettingService`.
- **Điểm mở rộng tiềm năng theo tên class:** `EzySeoFileSystemManager`, `WebEzySeoFileSystemManager`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyseo/sitemaps`, Web `/robots.txt` và `/api/v1/sitemaps` → 200.

## Áp dụng cho plugin quản lý công việc

Mẫu xuất XML/text và nội dung Web công khai; không để URL workspace, issue hay attachment riêng vào sitemap, và không dùng robots.txt làm ACL.

[Về chỉ mục plugin](README.md)
