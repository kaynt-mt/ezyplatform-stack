# ezymail

Email templates, drafts, and delivery tracking.

- **Marketplace version on core 1.5.9:** `0.3.3`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Get the next test again. see the environment and the general boundaries in [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezymail` | `org.youngmonkeys.ezymail` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezymail` | `org.youngmonkeys.ezymail` | [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 42 method/URI combinations identified; representative sample:

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

**web-plugin** — 6 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /ezymail/mail/unsubscribe` | `WebMailUnsubscribeController` |
| `GET /ezymail/api/v1/mail/read` | `WebApiMailController` |
| `GET /ezymail/api/v1/mail/click` | `WebApiMailController` |
| `GET /ezymail/api/v1/mail/unsubscribe` | `WebApiMailController` |
| `POST /ezymail/api/v1/mail/resubscribe` | `WebApiMailController` |
| `POST /ezymail/api/v1/mail/unsubscribe` | `WebApiMailController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezymail: /`, `mail_templates: /templates`, `mail_templates_add: ~/templates/add`, `mail_templates_details: ~/templates/{id}`, `mail_templates_edit: ~/templates/{id}/edit`, `mail_templates_preview: ~/templates/preview` (+7).

- **admin-plugin – Template:** `ezymail/composes/compose.html`, `ezymail/fragments/mail-links-generator.html`, `ezymail/mails/details.html`, `ezymail/mails/fragments/actions.html`, `ezymail/mails/fragments/histories.html`, `ezymail/mails/list.html`, `ezymail/mails/scripts.html` (+18).

- **admin-plugin – Static resources:** `ezymail/css/style.css`.

- **admin-plugin – Configuration and template resources:** `skill-library/ezymail_compose_email.md`, `skill-library/ezymail_create_mail_template.md`.

- **web-plugin – Template:** `ezymail/mail-unsubscribe.html`.

## Data and migrations

- **Table in the DDL package (6):** `ezymail_mail_actions`, `ezymail_mail_click_tracks`, `ezymail_mail_histories`, `ezymail_mail_participants`, `ezymail_mails`, `ezymail_unsubscribed_emails`.
- **Class with JPA Entity/MappedSuperclass (6):** `Mail`, `MailAction`, `MailClickTrack`, `MailHistory`, `MailParticipant`, `UnsubscribedEmail`.
- **SQL admin-plugin (13 files):** `resources/scripts/ezymail_mail_participants.sql`, `resources/scripts/mail_action.sql`, `resources/scripts/mail_history.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_mail_add_content_id_index.sql`, `resources/scripts/alter_mail_add_template_index.sql`, `resources/scripts/alter_mail_and_participant.sql` (+6).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezymail-admin-plugin-0.3.3.jar`, `ezymail-sdk-0.3.3.jar`; 202 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezymail.pagination`, `org.youngmonkeys.ezymail.admin.service`, `org.youngmonkeys.ezymail.admin.repo` (+29).
- **Other library JARs:** `activation-1.1.jar`, `javax.mail-1.6.2.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiMailController`, `AdminApiSettingController`, `AdminApiSettingGmailApiController`, `AdminApiTemplateController`, `AdminDuplicatedMailTemplateControllerService`, `AdminEzyMailAdminRepository`, `AdminEzyMailSettingsService`, `AdminEzyMailTemplateRepository`, `AdminEzyMailTemplateService`.
- **Configuration and permission classes (sample):** `AdminEzyMailPageFragmentConfig`, `AdminEzyMailPostTypeConfig`, `AdminEzyMailSkillLibraryConfig`, `AdminEzyMailTermTypeConfig`, `EzyMailPageFragmentConfig`, `MailchimpSettings`, `MailgunSettings` (+3).
- **Potential extension points based on class names:** `AdminEzyMailAdminSender`, `AdminMailDeliveryServiceManager`, `AdminSendTemplatedMailEventHandler`, `MailDeliveryServiceManager`, `SendTemplatedMailEventHandler`.

### web-plugin

- **JARs inspected:** `ezymail-sdk-0.3.3.jar`, `ezymail-web-plugin-0.3.3.jar`; 142 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezymail.pagination`, `org.youngmonkeys.ezymail.web.service`, `org.youngmonkeys.ezymail.service` (+23).
- **Other library JARs:** `activation-1.1.jar`, `javax.mail-1.6.2.jar`.
- **Controllers, services, and repositories (sample):** `WebApiMailController`, `WebMailUnsubscribeController`, `WebMailUnsubscribeControllerService`, `EzyMailSettingsService`, `EzyMailUserRepository`, `EzyMailUserService`, `GmailApiMailDeliveryService`, `MailActionRepository`.
- **Configuration and permission classes (sample):** `EzyMailPageFragmentConfig`, `MailchimpSettings`, `MailgunSettings`, `MicrosoftGraphApiSettings`, `SimpleEmailServiceSettings`, `SmtpSettings`, `WebEzyMailPageFragmentConfig`.
- **Potential extension points based on class names:** `MailDeliveryServiceManager`, `SendTemplatedMailEventHandler`, `WebMailDeliveryServiceManager`, `WebSendTemplatedMailEventHandler`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezymail/templates` and `/ezymail/sent-mails` returned 200. No real email was sent.

## Integration notes

See `AdminSendTemplatedMailEventHandler` and `MailDeliveryServiceManager`. Send only the data the template needs, deduplicate sends, and test with simulated SMTP.

[Back to the plugin index](README.md)
