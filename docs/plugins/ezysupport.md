# ezysupport

Liên hệ, FAQ, tuyển dụng và nội dung hỗ trợ.

- **Bản Marketplace trên core 1.5.9:** `0.6.2`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezysupport` | `org.youngmonkeys.ezysupport` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezysupport` | `org.youngmonkeys.ezysupport` | [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 135 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

**web-plugin** — 23 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezysupport: /`, `contact_us: /contact-us`, `contact_us_details: ~/contact-us/{mailId}`, `recruitment: /recruitment`, `recruitment_add: ~/recruitment/add`, `recruitment_details: ~/recruitment/{id}` (+36).

- **admin-plugin – Template:** `ezysupport/contact-method/add.html`, `ezysupport/contact-method/details.html`, `ezysupport/contact-method/edit.html`, `ezysupport/contact-method/list.html`, `ezysupport/contact-method/scripts.html`, `ezysupport/contact-us/details.html`, `ezysupport/contact-us/list.html` (+50).

- **admin-plugin – Tài nguyên tĩnh:** `ezysupport/css/style.css`, `ezysupport/html/help.html`, `ezysupport/html/help_vi.html`, `ezysupport/js/post-settings.js`.

- **web-plugin – Template:** `ezysupport/about-us.html`, `ezysupport/contact-us.html`, `ezysupport/cookie-policy.html`, `ezysupport/faq.html`, `ezysupport/license.html`, `ezysupport/privacy-policy.html`, `ezysupport/purchase-guide.html` (+5).

- **web-plugin – Tài nguyên tĩnh:** `ezysupport/css/style.css`, `ezysupport/js/captcha.js`, `ezysupport/js/cookie-consent.js`, `ezysupport/js/proof-of-work-captcha.js` (+1).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (3):** `ezysupport_contact_methods`, `ezysupport_domain_settings`, `ezysupport_social_networks`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (3):** `ContactMethod`, `DomainSetting`, `SocialNetwork`.
- **SQL admin-plugin (8 tệp):** `resources/scripts/contact-methods.sql`, `resources/scripts/domain-setting.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter-remove-status.sql`, `resources/scripts/alter-social-networks-1.sql`, `resources/scripts/alter-social-networks.sql`, `resources/scripts/alter-tables-1.sql` (+1).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezysupport-admin-plugin-0.6.2.jar`, `ezysupport-sdk-0.6.2.jar`; 261 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezysupport.admin.request`, `org.youngmonkeys.ezysupport.pagination`, `org.youngmonkeys.ezysupport.admin.service` (+30).
- **Controller/service/repository (mẫu):** `AdminCaptchaControllerService`, `AdminContactMethodControllerService`, `AdminContactUsControllerService`, `AdminContentTemplateControllerService`, `AdminAutoRestartEzyPlatformService`, `AdminCaptchaControllerService`, `AdminCertbotService`, `AdminCertbotValidator`, `AdminConfigurationValidator`.
- **Class cấu hình/quyền (mẫu):** `AdminEzySupportConfig`, `AdminEzySupportMailConfig`, `AdminEzySupportNginxConfig`, `AdminEzySupportViewMetadataConfig`, `AdminPageFragmentConfig`, `CaptchaConfigs`, `DomainSetting` (+1).
- **Điểm mở rộng tiềm năng theo tên class:** `AdminCaptchaServiceManager`, `AdminContactMethodTypeManager`, `AdminContactUsMailTypeManager`, `AdminDomainSettingEventHandler`, `AdminEditableDomainSettingMetadataManager`, `AdminShellCommandManager`, `AdminSocialNetworkStatusManager`, `AdminSocialNetworkTypeManager`, `AdminSocketSslReloadManager` (+3).

### web-plugin

- **JAR kiểm tra:** `ezysupport-sdk-0.6.2.jar`, `ezysupport-web-plugin-0.6.2.jar`; 162 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezysupport.pagination`, `org.youngmonkeys.ezysupport.web.service`, `org.youngmonkeys.ezysupport.service` (+29).
- **Controller/service/repository (mẫu):** `ApiCaptchaController`, `ApiEzySupportMessageController`, `ApiFaqController`, `ApiManagementUriController`, `CaptchaService`, `ContactMethodRepository`, `ContactMethodService`, `DomainSettingMetaService`, `DomainSettingRepository`.
- **Class cấu hình/quyền (mẫu):** `CaptchaConfigs`, `DomainSetting`, `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `CaptchaServiceManager`, `RecruitmentViewFactory`, `SupportViewFactory`, `WebApiUriManager`, `WebCaptchaInterceptor`, `WebCaptchaServiceManager`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezysupport/contact-us` và Web `/contact-us`, `/faq` → 200; không gửi yêu cầu ra ngoài.

## Lưu ý khi tích hợp

`ApiContactUsController` tách đánh dấu/bỏ spam khỏi đọc và xóa, là mẫu quản lý vòng đời yêu cầu tiếp nhận.

[Về chỉ mục plugin](README.md)
