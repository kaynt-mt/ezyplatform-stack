# ezylogin

Sign-in, provider configuration, and sessions.

- **Marketplace version on core 1.5.9:** `0.4.7`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezylogin` | `org.youngmonkeys.ezylogin` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezylogin` | `org.youngmonkeys.ezylogin` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 75 method/URI combinations identified; representative sample:

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

**web-plugin** — 65 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezylogin: /`, `regular_settings: /settings/regular`, `ezyplatform_settings: /settings/ezyplatform`, `google_settings: /settings/google`, `facebook_settings: /settings/facebook`, `other_oauth20_settings: /settings/oauth20` (+11).

- **admin-plugin – Template:** `ezylogin/admin-sso/consent.html`, `ezylogin/admins/fragments/profile-2fa.html`, `ezylogin/admins/fragments/profile-add-admin-access-token.html`, `ezylogin/admins/fragments/profile-admin-access-tokens.html`, `ezylogin/admins/fragments/profile-auto-renew-access-token.html`, `ezylogin/admins/fragments/profile-edit-admin-access-token.html`, `ezylogin/admins/fragments/profile.html` (+14).

- **admin-plugin – Static resources:** `ezylogin/css/icon.css`, `ezylogin/css/style.css`, `ezylogin/js/qrcode.min.js`.

- **web-plugin – Template:** `ezylogin/activation.html`, `ezylogin/cli-consent.html`, `ezylogin/forgot-password.html`, `ezylogin/login.html`, `ezylogin/oauth20-approval.html`, `ezylogin/register-success.html`, `ezylogin/register.html` (+3).

- **web-plugin – Static resources:** `ezylogin/css/style.css`, `ezylogin/js/ezylogin.js`, `ezylogin/js/qrcode.min.js`.

## Data and migrations

- **Table in the DDL package (6):** `ezylogin_oauth20_client_id_redirect_uris`, `ezylogin_oauth20_client_ids`, `ezylogin_oauth20_user_access_tokens`, `ezylogin_oauth20_user_refresh_tokens`, `ezylogin_oauth20_users`, `ezylogin_user_sessions`.
- **Class with JPA Entity/MappedSuperclass (6):** `Oauth20ClientId`, `Oauth20ClientIdRedirectUri`, `Oauth20User`, `Oauth20UserAccessToken`, `Oauth20UserRefreshToken`, `UserSession`.
- **SQL admin-plugin (4 files):** `resources/scripts/scripts.sql`, `resources/scripts/user_session.sql`, `resources/scripts/alter_oath_tables.sql`, `resources/scripts/alter_user_sessions_add_user_id_created_at_index.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezylogin-admin-plugin-0.4.7.jar`, `ezylogin-sdk-0.4.7.jar`; 268 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezylogin.model`, `org.youngmonkeys.ezylogin.admin.service`, `org.youngmonkeys.ezylogin.entity` (+32).
- **Controllers, services, and repositories (sample):** `AdminAdminAccessTokenControllerService`, `AdminApiAdminAdminAccessTokenController`, `AdminApiAdminTwoFactorController`, `AdminApiCliAuthorizationController`, `AdminAdminAccessTokenControllerService`, `AdminCliAuthorizationCodeService`, `AdminCliAuthorizationControllerService`, `AdminCliAuthorizationValidator`, `AdminCustomerPortraitChangesFetcher`.
- **Configuration and permission classes (sample):** `AdminEzyLoginAdminSsoConfig`, `AdminEzyLoginCliConfig`, `AdminEzyLoginCustomerPortraitConfig`, `AdminEzyLoginPageFragmentConfig`, `AdminEzyLoginSettingConfig`, `AdminEzyLoginTwoFactorConfig`, `AdminEzyLoginUserRoleConfig` (+1).
- **Potential extension points based on class names:** `AdminAdminAccessTokenStatusManager`, `AdminAdminAccessTokenTypeManager`, `AdminOauth20ApplicationTypeManager`, `AdminOauth20ClientApprovalPromptManager`, `AdminOauth20ClientStatusManager`, `AdminOauth20ClientTargetManager`, `AdminOauth20ClientTypeManager`, `Oauth20ApplicationTypeManager`, `Oauth20ClientApprovalPromptManager` (+3).

### web-plugin

- **JARs inspected:** `ezylogin-sdk-0.4.7.jar`, `ezylogin-web-plugin-0.4.7.jar`; 260 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezylogin.web.service`, `org.youngmonkeys.ezylogin.model`, `org.youngmonkeys.ezylogin.entity` (+34).
- **Controllers, services, and repositories (sample):** `CliAuthorizationControllerService`, `SsoTokenControllerService`, `WebAccessTokenControllerService`, `WebApiAnonymousAuthenticationController`, `AbstractLoginOauth20Service`, `CliAuthorizationCodeService`, `CliAuthorizationControllerService`, `CliAuthorizationValidator`, `EzyLoginSettingService`.
- **Configuration and permission classes (sample):** `AdminEzyLoginPageFragmentConfig`, `EzyLoginPageFragmentConfig`.
- **Potential extension points based on class names:** `EzyLoginAuthenticationInterceptor`, `Oauth20ApplicationTypeManager`, `Oauth20ClientApprovalPromptManager`, `Oauth20ClientStatusManager`, `Oauth20ClientTargetManager`, `Oauth20ClientTypeManager`, `WebCreateAnonymousUserEventHandler`, `WebEzyLoginExceptionHandler`, `WebSetUserAccessTokenCookiesEventHandler`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezylogin/settings/regular` returned 200. External OAuth or SSO was not connected.

## Integration notes

Reuse core identity and sessions where appropriate, but keep resource authorization separate. Test sign-in, theme-specific redirects, OAuth, and 2FA in a sandbox.

Activation is transitive: both EzyLogin lanes depend on EzyArticle and EzyMail. Install and activate EzyMail before EzyLogin, or run `python3 scripts/install-plugins.py --only ezylogin` from the stack checkout to resolve the pinned closure. A custom plugin that only uses EzyLogin should declare `dependencies=ezylogin`; it does not need to repeat EzyMail.

EzyLogin 0.4.7 does not register browser routes for `GET /login` or `GET /register`; the templates and page fragments are theme-integration building blocks around the JSON APIs. For disposable browser QA in the local stack, run `python3 scripts/install-plugins.py --only ezylogin --theme freestyle --browser-auth`. This seeds `/login` and `/register` fixture pages on Freestyle, disables local email activation, restarts, and verifies that the forms are rendered. Product UI should integrate authentication in its own theme rather than depend on this QA fixture.

[Back to the plugin index](README.md)
