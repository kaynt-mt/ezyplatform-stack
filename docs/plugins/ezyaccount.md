# ezyaccount

Giao diện và API tài khoản thành viên.

- **Bản Marketplace trên core 1.5.9:** `0.2.4`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyaccount` | `org.youngmonkeys.ezyaccount` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezyaccount` | `org.youngmonkeys.ezyaccount` | [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 2 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyAccountSettingController` |
| `PUT /api/v1/settings` | `AdminEzyAccountApiSettingController` |

**web-plugin** — 12 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /account` | `AccountController` |
| `GET /account/edit` | `AccountController` |
| `GET /account/members` | `AccountController` |
| `GET /ezyaccount/api/v1/account/members` | `WebApiAccountMemberController` |
| `GET /account/inbox` | `AccountController` |
| `GET /api/v1/media/settings` | `WebApiEzyAccountMediaController` |
| `GET /ezyaccount/api/v1/account` | `WebApiAccountController` |
| `POST /ezyaccount/api/v1/account/members/add` | `WebApiAccountMemberController` |
| `PUT /ezyaccount/api/v1/account/update` | `WebApiAccountController` |
| `DELETE /ezyaccount/api/v1/account/members/{id}` | `WebApiAccountMemberController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyaccount: /`, `settings: /settings`.

- **admin-plugin – Template:** `ezyaccount/setting/index.html`.

- **web-plugin – Template:** `ezyaccount/account-members.html`, `ezyaccount/common-profile.html`, `ezyaccount/edit-password-modal.html`, `ezyaccount/inbox-letter.html`, `ezyaccount/inbox.html`, `ezyaccount/media-modal.html`, `ezyaccount/notification.html` (+4).

- **web-plugin – Tài nguyên tĩnh:** `ezyaccount/css/style.css`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (3):** `ezyaccount_account_member_entities`, `ezyaccount_account_member_entity_activity_histories`, `ezyaccount_account_member_entity_roles`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (3):** `AccountMemberEntity`, `AccountMemberEntityActivityHistory`, `AccountMemberEntityRole`.
- **SQL admin-plugin (1 tệp):** `resources/scripts/scripts.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyaccount-admin-plugin-0.2.4.jar`, `ezyaccount-sdk-0.2.4.jar`; 61 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyaccount.pagination`, `org.youngmonkeys.ezyaccount.service`, `org.youngmonkeys.ezyaccount.model` (+16).
- **JAR thư viện khác:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controller/service/repository (mẫu):** `AdminEzyAccountApiSettingController`, `AdminEzyAccountSettingController`, `IndexController`, `AccountMemberEntityActivityHistoryService`, `AccountMemberEntityRepository`, `AccountMemberEntityRoleRepository`, `AccountMemberEntityService`, `AdminAccountMemberEntityActivityHistoryRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminPageFragmentConfig`, `PageFragmentConfig`.
- **Resource trong JAR (mẫu):** `ecommerce/ecommerce.properties`.
- **Điểm mở rộng tiềm năng theo tên class:** `AccountMemberEntityRoleManager`, `AdminAccountMemberEntityRoleManager`.

### web-plugin

- **JAR kiểm tra:** `ezyaccount-sdk-0.2.4.jar`, `ezyaccount-web-plugin-0.2.4.jar`; 88 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyaccount.pagination`, `org.youngmonkeys.ezyaccount.web.service`, `org.youngmonkeys.ezyaccount.web.controller.api` (+22).
- **JAR thư viện khác:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controller/service/repository (mẫu):** `AccountController`, `WebAccountControllerService`, `WebAccountMemberControllerService`, `WebAccountMemberEntityActivityHistoryControllerService`, `AccountMemberEntityActivityHistoryService`, `AccountMemberEntityRepository`, `AccountMemberEntityRoleRepository`, `AccountMemberEntityService`, `EzyAccountSettingService`.
- **Class cấu hình/quyền (mẫu):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Resource trong JAR (mẫu):** `ecommerce/ecommerce.properties`.
- **Điểm mở rộng tiềm năng theo tên class:** `AccountMemberEntityRoleManager`, `EzyAccountValidateUserUpdateEventHandler`, `WebAccountMemberEntityRoleManager`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyaccount/settings` → 200; Web `/ezyaccount/api/v1/account` → 401 khi chưa đăng nhập.

## Áp dụng cho plugin quản lý công việc

`AccountMemberEntity`, `AccountMemberEntityRole` và `AccountMemberEntityActivityHistory` cho thấy ba trách nhiệm có thể lưu riêng: quan hệ thành viên, role và hoạt động. `AccountMemberEntityRoleManager` là điểm đọc tiếp nếu muốn tái sử dụng cơ chế role, nhưng chưa xác minh contract của nó cho entity mới. Ưu tiên kiểm trên API với guest, người chưa tham gia và thành viên có role khác nhau.

Tái sử dụng định danh core và bề mặt tài khoản sẵn có nếu tương thích với theme. Thành viên workspace, lời mời và quyền xem issue vẫn là dữ liệu riêng của task plugin; HTTP 401 chỉ chứng minh cổng xác thực từ chối guest.

[Về chỉ mục plugin](README.md)
