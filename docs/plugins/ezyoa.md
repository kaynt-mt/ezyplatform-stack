# ezyoa

Official Accounts, workflows, and notifications.

- **Marketplace version on core 1.5.9:** `0.4.2`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyoa` | `org.youngmonkeys.ezyoa` | [ezysupport](ezysupport.md), [ezychat](ezychat.md), [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezyoa` | `org.youngmonkeys.ezyoa` | [ezychat](ezychat.md), [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 36 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/message-response-scenarios/{scenarioName}/parameters-template` | `AdminApiOAMessageResponseScenarioController` |
| `GET /api/v1/oa-services/{code}/notification-templates/{id}` | `AdminApiOANotificationTemplateController` |
| `GET /oa-services` | `AdminOAServiceSettingController` |
| `GET /oa-services/add` | `AdminOAServiceSettingController` |
| `GET /settings` | `AdminSettingController` |
| `GET /templates` | `AdminEzyOaTemplateController` |
| `GET /templates/add` | `AdminEzyOaTemplateController` |
| `POST /api/v1/oa-services/{code}/users/{oaUserId}/send-fake-webhook-text-message` | `AdminApiOAUserController` |
| `POST /api/v1/oa-services/{code}/users/{oaUserId}/send-fake-webhook-scenario-message` | `AdminApiOAUserController` |
| `POST /api/v1/oa-services/add` | `AdminApiOAServiceController` |
| `POST /api/v1/oa-services/{code}/send-message` | `AdminApiOAServiceController` |
| `PUT /api/v1/oa-services/{code}/notification-templates/{id}` | `AdminApiOANotificationTemplateController` |
| `PUT /api/v1/oa-services/{code}` | `AdminApiOAServiceController` |
| `PUT /api/v1/oa-services/{code}/activate` | `AdminApiOAServiceController` |
| `PUT /api/v1/settings` | `AdminApiSettingsController` |
| `DELETE /api/v1/oa-services/{code}/customer-service-staffs/{oaUserId}` | `AdminApiOACustomerServiceStaffController` |
| `DELETE /api/v1/oa-services/{code}/users/{oaUserId}/remove-user` | `AdminApiOAUserController` |

**web-plugin** — 3 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/oa/{code}/webhook` | `WebApiOAWebhookController` |
| `GET /oa/{code}/auth-callback` | `WebOACallbackController` |
| `POST /api/v1/oa/{code}/webhook` | `WebApiOAWebhookController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyoa: /`, `oa_services: /oa-services`, `oa_services_add: ~/oa-services/add`, `oa_services_edit: ~/oa-services/{code}/edit`, `oa_services_details: ~/oa-services/{code}`, `oa_user_details: ~/oa-users/{id}` (+5).

- **admin-plugin – Template:** `ezyoa/customers/fragments/details.html`, `ezyoa/customers/fragments/link-oa-services.html`, `ezyoa/customers/fragments/search-oa-user-modal.html`, `ezyoa/customers/oa-message/list.html`, `ezyoa/fragments/oa-user.html`, `ezyoa/modals/search-oa-user.html`, `ezyoa/oa-service/add.html` (+10).

- **admin-plugin – Configuration and template resources:** `oa-response-message-templates/default_message.properties`, `oa-response-message-templates/new_customer_message.properties`, `oa-response-message-templates/oa_user_message_notification_for_staff.properties`, `oa-response-message-templates/payment_message.properties` (+3).

## Data and migrations

- **Table in the DDL packaging (5):** `ezyoa_oa_notification_templates`, `ezyoa_oa_service_settings`, `ezyoa_oa_user_message_channels`, `ezyoa_oa_user_messages`, `ezyoa_oa_users`.
- **Class with JPA Entity/MappedSuperclass (5):** `OANotificationTemplate`, `OAServiceSetting`, `OAUser`, `OAUserMessage`, `OAUserMessageChannel`.
- **SQL admin-plugin (8 files):** `resources/scripts/notification_templates.sql`, `resources/scripts/scripts.sql`, `resources/scripts/users.sql`, `resources/scripts/alter_oa_service_setting_add_handing_service.sql`, `resources/scripts/alter_oa_service_settings_to_add_notification_channel.sql`, `resources/scripts/alter_oa_users_to_add_admin_id.sql`, `resources/scripts/alter_tables_1.sql` (+1).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyoa-admin-plugin-0.4.2.jar`, `ezyoa-sdk-0.4.2.jar`; 261 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyoa.model`, `org.youngmonkeys.ezyoa.listener`, `org.youngmonkeys.ezyoa.service` (+38).
- **Controllers, services, and repositories (sample):** `AdminApiOAChatChannelController`, `AdminApiOACustomerServiceStaffController`, `AdminApiOAMessageResponseScenarioController`, `AdminApiOANotificationTemplateController`, `AbstractOAService`, `AdminCustomerFetcher`, `AdminCustomerPortraitChangesFetcher`, `AdminCustomerPortraitDataFetcher`, `AdminCustomerPortraitOAUserRepository`.
- **Configuration and permission classes (sample):** `AdminEzyOACustomerPortraitConfig`, `AdminOAComponentManagerConfig`, `AdminOAResponseMessageTemplateConfig`, `OAComponentManagerConfig`, `OAServiceSetting`.
- **Configuration and template keys from resources (values omitted):** `content`, `title`.
- **Potential extension points based on class names:** `AbstractOATemplatedMessageSender`, `AdminFetchLastOaMessageMetadataEventHandler`, `AdminFetchOaPayCommandsEventHandler`, `AdminMessengerOAUserSendMessageListener`, `AdminNewOrdersAppendEventHandler`, `AdminOAExtensionMessageSenderManager`, `AdminOAListenerManager`, `AdminOAServiceManager`, `AdminOATemplatedMessageSenderManager` (+58).

### web-plugin

- **JARs inspected:** `ezyoa-sdk-0.4.2.jar`, `ezyoa-web-plugin-0.4.2.jar`; 211 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyoa.model`, `org.youngmonkeys.ezyoa.listener`, `org.youngmonkeys.ezyoa.service` (+32).
- **Controllers, services, and repositories (sample):** `WebApiOAWebhookController`, `WebOACallbackController`, `WebOAUserAvatarStorageControllerService`, `AbstractOAService`, `CustomerFetcher`, `EzyOASettingService`, `MessengerService`, `OACustomerServiceStaffService`.
- **Configuration and permission classes (sample):** `OAComponentManagerConfig`, `OAServiceSetting`, `WebOAComponentManagerConfig`.
- **Potential extension points based on class names:** `AbstractOATemplatedMessageSender`, `FetchLastOaMessageMetadataEventHandler`, `FetchOaPayCommandsEventHandler`, `MessengerOAUserSendMessageListener`, `OAAbstractListener`, `OAAbstractTemplatedMessageSender`, `OAAbstractTemplatedNotificationSender`, `OAAbstractTemplatedSender`, `OAAdminSendMessageListener` (+63).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyoa/oa-services` and `/ezyoa/templates` returned 200. No Official Account was connected.

## Integration notes

Keep Official Account connections, templates, parameters, and workflows separate. Make the external connector optional.

[Back to the plugin index](README.md)
