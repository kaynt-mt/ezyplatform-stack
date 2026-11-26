# ezyaccount

Member account UI and API.

- **Marketplace version on core 1.5.9:** `0.2.4`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyaccount` | `org.youngmonkeys.ezyaccount` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezyaccount` | `org.youngmonkeys.ezyaccount` | [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 2 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyAccountSettingController` |
| `PUT /api/v1/settings` | `AdminEzyAccountApiSettingController` |

**web-plugin** — 12 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyaccount: /`, `settings: /settings`.

- **admin-plugin – Template:** `ezyaccount/setting/index.html`.

- **web-plugin – Template:** `ezyaccount/account-members.html`, `ezyaccount/common-profile.html`, `ezyaccount/edit-password-modal.html`, `ezyaccount/inbox-letter.html`, `ezyaccount/inbox.html`, `ezyaccount/media-modal.html`, `ezyaccount/notification.html` (+4).

- **web-plugin – Static resources:** `ezyaccount/css/style.css`.

## Data and migrations

- **Table in the DDL package (3):** `ezyaccount_account_member_entities`, `ezyaccount_account_member_entity_activity_histories`, `ezyaccount_account_member_entity_roles`.
- **Class with JPA Entity/MappedSuperclass (3):** `AccountMemberEntity`, `AccountMemberEntityActivityHistory`, `AccountMemberEntityRole`.
- **SQL admin-plugin (1 file):** `resources/scripts/scripts.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyaccount-admin-plugin-0.2.4.jar`, `ezyaccount-sdk-0.2.4.jar`; 61 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyaccount.pagination`, `org.youngmonkeys.ezyaccount.service`, `org.youngmonkeys.ezyaccount.model` (+16).
- **Other library JARs:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controllers, services, and repositories (sample):** `AdminEzyAccountApiSettingController`, `AdminEzyAccountSettingController`, `IndexController`, `AccountMemberEntityActivityHistoryService`, `AccountMemberEntityRepository`, `AccountMemberEntityRoleRepository`, `AccountMemberEntityService`, `AdminAccountMemberEntityActivityHistoryRepository`.
- **Configuration and permission classes (sample):** `AdminPageFragmentConfig`, `PageFragmentConfig`.
- **JAR resources (sample):** `ecommerce/ecommerce.properties`.
- **Potential extension points based on class names:** `AccountMemberEntityRoleManager`, `AdminAccountMemberEntityRoleManager`.

### web-plugin

- **JARs inspected:** `ezyaccount-sdk-0.2.4.jar`, `ezyaccount-web-plugin-0.2.4.jar`; 88 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyaccount.pagination`, `org.youngmonkeys.ezyaccount.web.service`, `org.youngmonkeys.ezyaccount.web.controller.api` (+22).
- **Other library JARs:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controllers, services, and repositories (sample):** `AccountController`, `WebAccountControllerService`, `WebAccountMemberControllerService`, `WebAccountMemberEntityActivityHistoryControllerService`, `AccountMemberEntityActivityHistoryService`, `AccountMemberEntityRepository`, `AccountMemberEntityRoleRepository`, `AccountMemberEntityService`, `EzyAccountSettingService`.
- **Configuration and permission classes (sample):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **JAR resources (sample):** `ecommerce/ecommerce.properties`.
- **Potential extension points based on class names:** `AccountMemberEntityRoleManager`, `EzyAccountValidateUserUpdateEventHandler`, `WebAccountMemberEntityRoleManager`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyaccount/settings` returned 200. Web `/ezyaccount/api/v1/account` returned 401 without a login.

## Integration notes

The membership entities, roles, and activity history show how to separate these responsibilities. System account permissions do not replace plugin ACLs.

[Back to the plugin index](README.md)
