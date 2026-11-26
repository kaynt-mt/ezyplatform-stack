# ezysupport

Contact forms, FAQs, recruitment, and support content.

- **Marketplace version on core 1.5.9:** `0.6.2`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezysupport` | `org.youngmonkeys.ezysupport` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezysupport` | `org.youngmonkeys.ezysupport` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 135 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /contact-us` | `ContactUsController` |
| `GET /api/v1/contact-us` | `ApiContactUsController` |
| `GET /faqs` | `FaqsController` |
| `GET /faqs/add` | `FaqsController` |
| `GET /recruitment` | `RecruitmentController` |
| `GET /recruitment/add` | `RecruitmentController` |
| `GET /help` | `HelpController` |
| `POST /api/v1/faqs/add` | `ApiFaqsController` |
| `POST /api/v1/recruitment/add` | `ApiRecruitmentController` |
| `POST /api/v1/nginx/reload` | `ApiNginxController` |
| `POST /api/v1/nginx/install` | `ApiNginxController` |
| `PUT /api/v1/contact-us/mark-as-spam` | `ApiContactUsController` |
| `PUT /api/v1/contact-us/unmark-as-spam` | `ApiContactUsController` |
| `PUT /api/v1/faqs/{faqId}` | `ApiFaqsController` |
| `PUT /api/v1/faqs/{faqId}/publish` | `ApiFaqsController` |
| `DELETE /api/v1/contact-us/{mailId}` | `ApiContactUsController` |
| `DELETE /api/v1/faqs/{faqId}` | `ApiFaqsController` |
| `DELETE /api/v1/recruitment/{id}` | `ApiRecruitmentController` |
| `DELETE /api/v1/indexed-data` | `ApiIndexedDataController` |

**web-plugin** — 23 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /contact-us` | `SupportController` |
| `GET /faq` | `SupportController` |
| `GET /faqs` | `SupportController` |
| `GET /recruitment` | `RecruitmentController` |
| `GET /api/v1/recruitments` | `ApiRecruitmentController` |
| `GET /license` | `SupportController` |
| `GET /about-us` | `SupportController` |
| `POST /api/v1/contact-us` | `ApiSupportController` |
| `POST /api/v1/recruitments/{id}/apply` | `ApiRecruitmentController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezysupport: /`, `contact_us: /contact-us`, `contact_us_details: ~/contact-us/{mailId}`, `recruitment: /recruitment`, `recruitment_add: ~/recruitment/add`, `recruitment_details: ~/recruitment/{id}` (+36).

- **admin-plugin – Template:** `ezysupport/contact-method/add.html`, `ezysupport/contact-method/details.html`, `ezysupport/contact-method/edit.html`, `ezysupport/contact-method/list.html`, `ezysupport/contact-method/scripts.html`, `ezysupport/contact-us/details.html`, `ezysupport/contact-us/list.html` (+50).

- **admin-plugin – Static resources:** `ezysupport/css/style.css`, `ezysupport/html/help.html`, `ezysupport/html/help_vi.html`, `ezysupport/js/post-settings.js`.

- **web-plugin – Template:** `ezysupport/about-us.html`, `ezysupport/contact-us.html`, `ezysupport/cookie-policy.html`, `ezysupport/faq.html`, `ezysupport/license.html`, `ezysupport/privacy-policy.html`, `ezysupport/purchase-guide.html` (+5).

- **web-plugin – Static resources:** `ezysupport/css/style.css`, `ezysupport/js/captcha.js`, `ezysupport/js/cookie-consent.js`, `ezysupport/js/proof-of-work-captcha.js` (+1).

## Data and migrations

- **Table in the DDL package (3):** `ezysupport_contact_methods`, `ezysupport_domain_settings`, `ezysupport_social_networks`.
- **Class with JPA Entity/MappedSuperclass (3):** `ContactMethod`, `DomainSetting`, `SocialNetwork`.
- **SQL admin-plugin (8 files):** `resources/scripts/contact-methods.sql`, `resources/scripts/domain-setting.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter-remove-status.sql`, `resources/scripts/alter-social-networks-1.sql`, `resources/scripts/alter-social-networks.sql`, `resources/scripts/alter-tables-1.sql` (+1).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezysupport-admin-plugin-0.6.2.jar`, `ezysupport-sdk-0.6.2.jar`; 261 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezysupport.admin.request`, `org.youngmonkeys.ezysupport.pagination`, `org.youngmonkeys.ezysupport.admin.service` (+30).
- **Controllers, services, and repositories (sample):** `AdminCaptchaControllerService`, `AdminContactMethodControllerService`, `AdminContactUsControllerService`, `AdminContentTemplateControllerService`, `AdminAutoRestartEzyPlatformService`, `AdminCaptchaControllerService`, `AdminCertbotService`, `AdminCertbotValidator`, `AdminConfigurationValidator`.
- **Configuration and permission classes (sample):** `AdminEzySupportConfig`, `AdminEzySupportMailConfig`, `AdminEzySupportNginxConfig`, `AdminEzySupportViewMetadataConfig`, `AdminPageFragmentConfig`, `CaptchaConfigs`, `DomainSetting` (+1).
- **Potential extension points based on class names:** `AdminCaptchaServiceManager`, `AdminContactMethodTypeManager`, `AdminContactUsMailTypeManager`, `AdminDomainSettingEventHandler`, `AdminEditableDomainSettingMetadataManager`, `AdminShellCommandManager`, `AdminSocialNetworkStatusManager`, `AdminSocialNetworkTypeManager`, `AdminSocketSslReloadManager` (+3).

### web-plugin

- **JARs inspected:** `ezysupport-sdk-0.6.2.jar`, `ezysupport-web-plugin-0.6.2.jar`; 162 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezysupport.pagination`, `org.youngmonkeys.ezysupport.web.service`, `org.youngmonkeys.ezysupport.service` (+29).
- **Controllers, services, and repositories (sample):** `ApiCaptchaController`, `ApiEzySupportMessageController`, `ApiFaqController`, `ApiManagementUriController`, `CaptchaService`, `ContactMethodRepository`, `ContactMethodService`, `DomainSettingMetaService`, `DomainSettingRepository`.
- **Configuration and permission classes (sample):** `CaptchaConfigs`, `DomainSetting`, `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Potential extension points based on class names:** `CaptchaServiceManager`, `RecruitmentViewFactory`, `SupportViewFactory`, `WebApiUriManager`, `WebCaptchaInterceptor`, `WebCaptchaServiceManager`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezysupport/contact-us` and Web `/contact-us` and `/faq` returned 200. No requests were sent externally.

## Integration notes

`ApiContactUsController` separates marking or unmarking spam from reading and deleting submissions, illustrating how to manage their lifecycle.

[Back to the plugin index](README.md)
