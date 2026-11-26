# ezylogin

Đăng nhập, cấu hình nhà cung cấp và phiên.

- **Bản Marketplace trên core 1.5.9:** `0.4.7`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezylogin` | `org.youngmonkeys.ezylogin` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezylogin` | `org.youngmonkeys.ezylogin` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 75 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /user-sessions` | `AdminUserSessionController` |
| `GET /api/v1/user-sessions` | `AdminApiUserSessionController` |
| `GET /sso/admin/login` | `AdminLoginSsoController` |
| `GET /ezylogin/cli/authorize` | `AdminCliAuthorizationController` |
| `GET /oauth20-client-ids` | `AdminOauth20ClientIdController` |
| `GET /settings/oauth20` | `AdminEzyLoginSettingController` |
| `GET /api/v1/admins/me/2fa` | `AdminApiTwoFactorController` |
| `POST /api/v1/user-sessions/logout` | `AdminApiUserSessionController` |
| `POST /api/v1/user-sessions/{id}/logout` | `AdminApiUserSessionController` |
| `POST /ezylogin/cli/authorize/approve` | `AdminCliAuthorizationController` |
| `POST /ezylogin/sso/admin/oauth2/par` | `AdminApiSsoOpenIdConnectController` |
| `PUT /api/v1/settings/allow-login-by-fields` | `AdminApiSettingController` |
| `PUT /api/v1/settings/oauth20/save` | `AdminApiSettingController` |
| `PUT /api/v1/oauth20-client-ids/{id}` | `AdminApiOauth20ClientIdController` |
| `PUT /api/v1/settings/jwt` | `AdminApiSettingController` |
| `DELETE /api/v1/oauth20-client-ids/{id}` | `AdminApiOauth20ClientIdController` |
| `DELETE /api/v1/admins/me/2fa` | `AdminApiTwoFactorController` |
| `DELETE /api/v1/users/{username}/2fa` | `AdminApiUserTwoFactorController` |
| `DELETE /api/v1/settings/{providerName}` | `AdminApiSettingController` |

**web-plugin** — 65 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /sso/login` | `WebLoginSsoController` |
| `GET /oauth2/login` | `WebLoginOauth20Controller` |
| `GET /oauth2/auth` | `WebOauth20Controller` |
| `GET /v1/oauth2/user` | `WebApiOauth20Controller` |
| `GET /2fa` | `WebTwoFactorController` |
| `GET /ezylogin/api/v1/users/me/2fa` | `WebApiTwoFactorController` |
| `GET /register-success` | `WebRegisterController` |
| `POST /ezylogin/api/v1/login/user-sessions` | `WebApiUserSessionController` |
| `POST /ezylogin/api/v1/login/user-sessions/{userSessionId}/logout` | `WebApiUserSessionController` |
| `POST /ezylogin/api/v1/login` | `WebApiAuthenticationController` |
| `POST /ezylogin/api/v1/register` | `WebApiAuthenticationController` |
| `PUT /ezylogin/api/v1/access-token/renew` | `WebApiAuthenticationController` |
| `PUT /ezylogin/api/v1/sso/user/clients/{clientId}` | `WebApiAuth20ClientController` |
| `DELETE /ezylogin/api/v1/access-tokens` | `WebApiAuthenticationController` |
| `DELETE /ezylogin/api/v1/sso/user/clients/{clientId}` | `WebApiAuth20ClientController` |
| `DELETE /ezylogin/api/v1/sso/user/clients/{clientId}/redirect-uris/{redirectUri}` | `WebApiAuth20ClientController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezylogin: /`, `regular_settings: /settings/regular`, `ezyplatform_settings: /settings/ezyplatform`, `google_settings: /settings/google`, `facebook_settings: /settings/facebook`, `other_oauth20_settings: /settings/oauth20` (+11).

- **admin-plugin – Template:** `ezylogin/admin-sso/consent.html`, `ezylogin/admins/fragments/profile-2fa.html`, `ezylogin/admins/fragments/profile-add-admin-access-token.html`, `ezylogin/admins/fragments/profile-admin-access-tokens.html`, `ezylogin/admins/fragments/profile-auto-renew-access-token.html`, `ezylogin/admins/fragments/profile-edit-admin-access-token.html`, `ezylogin/admins/fragments/profile.html` (+14).

- **admin-plugin – Tài nguyên tĩnh:** `ezylogin/css/icon.css`, `ezylogin/css/style.css`, `ezylogin/js/qrcode.min.js`.

- **web-plugin – Template:** `ezylogin/activation.html`, `ezylogin/cli-consent.html`, `ezylogin/forgot-password.html`, `ezylogin/login.html`, `ezylogin/oauth20-approval.html`, `ezylogin/register-success.html`, `ezylogin/register.html` (+3).

- **web-plugin – Tài nguyên tĩnh:** `ezylogin/css/style.css`, `ezylogin/js/ezylogin.js`, `ezylogin/js/qrcode.min.js`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (6):** `ezylogin_oauth20_client_id_redirect_uris`, `ezylogin_oauth20_client_ids`, `ezylogin_oauth20_user_access_tokens`, `ezylogin_oauth20_user_refresh_tokens`, `ezylogin_oauth20_users`, `ezylogin_user_sessions`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (6):** `Oauth20ClientId`, `Oauth20ClientIdRedirectUri`, `Oauth20User`, `Oauth20UserAccessToken`, `Oauth20UserRefreshToken`, `UserSession`.
- **SQL admin-plugin (4 tệp):** `resources/scripts/scripts.sql`, `resources/scripts/user_session.sql`, `resources/scripts/alter_oath_tables.sql`, `resources/scripts/alter_user_sessions_add_user_id_created_at_index.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezylogin-admin-plugin-0.4.7.jar`, `ezylogin-sdk-0.4.7.jar`; 268 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezylogin.model`, `org.youngmonkeys.ezylogin.admin.service`, `org.youngmonkeys.ezylogin.entity` (+32).
- **Controller/service/repository (mẫu):** `AdminAdminAccessTokenControllerService`, `AdminApiAdminAdminAccessTokenController`, `AdminApiAdminTwoFactorController`, `AdminApiCliAuthorizationController`, `AdminAdminAccessTokenControllerService`, `AdminCliAuthorizationCodeService`, `AdminCliAuthorizationControllerService`, `AdminCliAuthorizationValidator`, `AdminCustomerPortraitChangesFetcher`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyLoginAdminSsoConfig`, `AdminEzyLoginCliConfig`, `AdminEzyLoginCustomerPortraitConfig`, `AdminEzyLoginPageFragmentConfig`, `AdminEzyLoginSettingConfig`, `AdminEzyLoginTwoFactorConfig`, `AdminEzyLoginUserRoleConfig` (+1).
- **Điểm mở rộng tiềm năng theo tên class:** `AdminAdminAccessTokenStatusManager`, `AdminAdminAccessTokenTypeManager`, `AdminOauth20ApplicationTypeManager`, `AdminOauth20ClientApprovalPromptManager`, `AdminOauth20ClientStatusManager`, `AdminOauth20ClientTargetManager`, `AdminOauth20ClientTypeManager`, `Oauth20ApplicationTypeManager`, `Oauth20ClientApprovalPromptManager` (+3).

### web-plugin

- **JAR kiểm tra:** `ezylogin-sdk-0.4.7.jar`, `ezylogin-web-plugin-0.4.7.jar`; 260 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezylogin.web.service`, `org.youngmonkeys.ezylogin.model`, `org.youngmonkeys.ezylogin.entity` (+34).
- **Controller/service/repository (mẫu):** `CliAuthorizationControllerService`, `SsoTokenControllerService`, `WebAccessTokenControllerService`, `WebApiAnonymousAuthenticationController`, `AbstractLoginOauth20Service`, `CliAuthorizationCodeService`, `CliAuthorizationControllerService`, `CliAuthorizationValidator`, `EzyLoginSettingService`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyLoginPageFragmentConfig`, `EzyLoginPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `EzyLoginAuthenticationInterceptor`, `Oauth20ApplicationTypeManager`, `Oauth20ClientApprovalPromptManager`, `Oauth20ClientStatusManager`, `Oauth20ClientTargetManager`, `Oauth20ClientTypeManager`, `WebCreateAnonymousUserEventHandler`, `WebEzyLoginExceptionHandler`, `WebSetUserAccessTokenCookiesEventHandler`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezylogin/settings/regular` → 200; chưa kết nối OAuth/SSO bên ngoài.

## Lưu ý khi tích hợp

Tận dụng danh tính/phiên core nếu phù hợp; quyền tài nguyên vẫn độc lập. Kiểm login, redirect theo theme và OAuth/2FA trong sandbox.

[Về chỉ mục plugin](README.md)
