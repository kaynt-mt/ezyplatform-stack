# ezymail

Template email, thư nháp và theo dõi gửi.

- **Bản Marketplace trên core 1.5.9:** `0.3.3`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt sau thử lại. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezymail` | `org.youngmonkeys.ezymail` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezymail` | `org.youngmonkeys.ezymail` | [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 42 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /templates` | `AdminTemplateController` |
| `GET /templates/add` | `AdminTemplateController` |
| `GET /sent-mails` | `AdminMailController` |
| `GET /draft-mails` | `AdminMailController` |
| `GET /compose` | `AdminComposeController` |
| `GET /settings` | `AdminSettingController` |
| `GET /templates/preview` | `AdminTemplateController` |
| `POST /api/v1/templates/add` | `AdminApiTemplateController` |
| `POST /api/v1/templates/add-or-update` | `AdminApiTemplateController` |
| `POST /api/v1/save` | `AdminApiMailController` |
| `POST /api/v1/send` | `AdminApiMailController` |
| `PUT /api/v1/templates/{id}` | `AdminApiTemplateController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/settings/mail-delivery-services/smtp` | `AdminApiSettingController` |
| `PUT /api/v1/settings/mail-delivery-services/mailgun` | `AdminApiSettingController` |
| `DELETE /api/v1/templates/delete-by-name` | `AdminApiTemplateController` |
| `DELETE /api/v1/templates/{id}` | `AdminApiTemplateController` |
| `DELETE /api/v1/mails/{id}` | `AdminApiMailController` |

**web-plugin** — 6 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /ezymail/mail/unsubscribe` | `WebMailUnsubscribeController` |
| `GET /ezymail/api/v1/mail/read` | `WebApiMailController` |
| `GET /ezymail/api/v1/mail/click` | `WebApiMailController` |
| `GET /ezymail/api/v1/mail/unsubscribe` | `WebApiMailController` |
| `POST /ezymail/api/v1/mail/resubscribe` | `WebApiMailController` |
| `POST /ezymail/api/v1/mail/unsubscribe` | `WebApiMailController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezymail: /`, `mail_templates: /templates`, `mail_templates_add: ~/templates/add`, `mail_templates_details: ~/templates/{id}`, `mail_templates_edit: ~/templates/{id}/edit`, `mail_templates_preview: ~/templates/preview` (+7).

- **admin-plugin – Template:** `ezymail/composes/compose.html`, `ezymail/fragments/mail-links-generator.html`, `ezymail/mails/details.html`, `ezymail/mails/fragments/actions.html`, `ezymail/mails/fragments/histories.html`, `ezymail/mails/list.html`, `ezymail/mails/scripts.html` (+18).

- **admin-plugin – Tài nguyên tĩnh:** `ezymail/css/style.css`.

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `skill-library/ezymail_compose_email.md`, `skill-library/ezymail_create_mail_template.md`.

- **web-plugin – Template:** `ezymail/mail-unsubscribe.html`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (6):** `ezymail_mail_actions`, `ezymail_mail_click_tracks`, `ezymail_mail_histories`, `ezymail_mail_participants`, `ezymail_mails`, `ezymail_unsubscribed_emails`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (6):** `Mail`, `MailAction`, `MailClickTrack`, `MailHistory`, `MailParticipant`, `UnsubscribedEmail`.
- **SQL admin-plugin (13 tệp):** `resources/scripts/ezymail_mail_participants.sql`, `resources/scripts/mail_action.sql`, `resources/scripts/mail_history.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_mail_add_content_id_index.sql`, `resources/scripts/alter_mail_add_template_index.sql`, `resources/scripts/alter_mail_and_participant.sql` (+6).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezymail-admin-plugin-0.3.3.jar`, `ezymail-sdk-0.3.3.jar`; 202 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezymail.pagination`, `org.youngmonkeys.ezymail.admin.service`, `org.youngmonkeys.ezymail.admin.repo` (+29).
- **JAR thư viện khác:** `activation-1.1.jar`, `javax.mail-1.6.2.jar`.
- **Controller/service/repository (mẫu):** `AdminApiMailController`, `AdminApiSettingController`, `AdminApiSettingGmailApiController`, `AdminApiTemplateController`, `AdminDuplicatedMailTemplateControllerService`, `AdminEzyMailAdminRepository`, `AdminEzyMailSettingsService`, `AdminEzyMailTemplateRepository`, `AdminEzyMailTemplateService`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyMailPageFragmentConfig`, `AdminEzyMailPostTypeConfig`, `AdminEzyMailSkillLibraryConfig`, `AdminEzyMailTermTypeConfig`, `EzyMailPageFragmentConfig`, `MailchimpSettings`, `MailgunSettings` (+3).
- **Điểm mở rộng tiềm năng theo tên class:** `AdminEzyMailAdminSender`, `AdminMailDeliveryServiceManager`, `AdminSendTemplatedMailEventHandler`, `MailDeliveryServiceManager`, `SendTemplatedMailEventHandler`.

### web-plugin

- **JAR kiểm tra:** `ezymail-sdk-0.3.3.jar`, `ezymail-web-plugin-0.3.3.jar`; 142 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezymail.pagination`, `org.youngmonkeys.ezymail.web.service`, `org.youngmonkeys.ezymail.service` (+23).
- **JAR thư viện khác:** `activation-1.1.jar`, `javax.mail-1.6.2.jar`.
- **Controller/service/repository (mẫu):** `WebApiMailController`, `WebMailUnsubscribeController`, `WebMailUnsubscribeControllerService`, `EzyMailSettingsService`, `EzyMailUserRepository`, `EzyMailUserService`, `GmailApiMailDeliveryService`, `MailActionRepository`.
- **Class cấu hình/quyền (mẫu):** `EzyMailPageFragmentConfig`, `MailchimpSettings`, `MailgunSettings`, `MicrosoftGraphApiSettings`, `SimpleEmailServiceSettings`, `SmtpSettings`, `WebEzyMailPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `MailDeliveryServiceManager`, `SendTemplatedMailEventHandler`, `WebMailDeliveryServiceManager`, `WebSendTemplatedMailEventHandler`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezymail/templates`, `/ezymail/sent-mails` → 200. Không gửi email thật.

## Áp dụng cho plugin quản lý công việc

Đọc tiếp từ `AdminSendTemplatedMailEventHandler` và `MailDeliveryServiceManager`: schema thông báo issue nên chỉ truyền dữ liệu template cần dùng, có khóa chống gửi trùng theo sự kiện/người nhận. Tách test chọn template khỏi test kích hoạt việc gửi.

Dùng template cho lời mời, nhắc hạn và thông báo. Đưa gửi mail vào job/outbox sau giao dịch, có idempotency; trên local dùng SMTP giả lập trước khi kiểm nhánh gửi.

[Về chỉ mục plugin](README.md)
