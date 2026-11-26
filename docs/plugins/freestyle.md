# freestyle

Theme Web tổng quát và cấu hình giao diện.

- **Bản Marketplace trên core 1.5.9:** `0.2.9`.
- **Module đã xác minh:** `admin-plugin`, `theme`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/freestyle` | `org.youngmonkeys.freestyle` | [ezyarticle](ezyarticle.md) |
| `theme` — `web/themes/freestyle` | `org.youngmonkeys.freestyle` | [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 4 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminFreestyleSettingController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/pages/{pageId}/settings` | `AdminApiFreestylePageSettingController` |
| `PUT /api/v1/posts/{postId}/settings` | `AdminApiFreestylePostSettingController` |

**theme** — 5 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `FreestyleHomeController` |
| `GET /freestyle/api/v1/shorted-posts` | `FreestyleNewApiPostController` |
| `GET /freestyle/api/v1/shorted-posts-by-ids` | `FreestyleNewApiPostController` |
| `GET /freestyle/api/v1/posts/{slug}/children` | `FreestyleNewApiPostController` |
| `GET /freestyle/api/v1/users/{uuid}/shorted-posts` | `FreestyleNewApiPostController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `freestyle: /`, `settings: /settings`.

- **admin-plugin – Template:** `freestyle/settings/index.html`.

- **admin-plugin – Tài nguyên tĩnh:** `freestyle/js/post-settings.js`.

- **theme – Template:** `account/register-success.html`, `account/reset-password.html`, `fragments/comments.html`, `fragments/footer.html`, `fragments/header.html`, `fragments/post-menu.html`, `fragments/posts.html` (+8).

- **theme – Tài nguyên tĩnh:** `css/ezyarticle.css`, `css/styles.css`, `css/styles.rtl.css`, `js/main.js`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `freestyle-admin-plugin-0.2.9.jar`, `freestyle-sdk-0.2.9.jar`; 20 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.freestyle.admin.controller.api`, `org.youngmonkeys.freestyle.constant`, `org.youngmonkeys.freestyle.admin.controller.view` (+9).
- **Controller/service/repository (mẫu):** `AdminApiFreestylePageSettingController`, `AdminApiFreestylePostSettingController`, `AdminApiSettingController`, `AdminFreestylePostControllerService`, `AdminFreestylePostControllerService`, `AdminFreestylePostService`, `AdminFreestyleSettingService`, `FreestylePostService`, `FreestyleSettingService`.
- **Class cấu hình/quyền (mẫu):** `AdminPageFragmentConfig`, `PageFragmentConfig`.

### theme

- **JAR kiểm tra:** `freestyle-sdk-0.2.9.jar`, `freestyle-theme-0.2.9.jar`; 49 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.freestyle.theme.controller.view`, `org.youngmonkeys.freestyle.theme.event`, `org.youngmonkeys.freestyle.theme.service` (+16).
- **Controller/service/repository (mẫu):** `FreestyleApiCommentController`, `FreestyleApiPostController`, `FreestyleApiTermController`, `FreestyleErrorController`, `FreestylePostService`, `FreestyleSettingService`, `WebFreestylePostControllerService`, `WebFreestylePostRepository`, `WebFreestylePostService`.
- **Class cấu hình/quyền (mẫu):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `ArticleWebGlobalErrorHandler`, `ArticleWebGlobalExceptionHandler`, `WebGetChildrenListBySlugSortByPriorityAscIdAscEzyFunctionEventHandler`, `WebGetMostViewPostsByAuthorUserIdEzyFunctionEventHandler`, `WebGetMostViewPostsByAuthorUserUuidEzyFunctionEventHandler`, `WebGetPostTitleAndChildrenListByMenuNameEzyFunctionEventHandler`, `WebRandomSameTermsPostsByPostIdEzyFunctionEventHandler`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/freestyle/settings` → 200; theme render được bài EzyArticle ở Web.

## Áp dụng cho plugin quản lý công việc

Mẫu cho layout, fragment, template riêng từng khu vực. Dùng làm chứng thực Web renders đúng dữ liệu; task plugin nên có template UI của nó và test với một theme xác định.

[Về chỉ mục plugin](README.md)
