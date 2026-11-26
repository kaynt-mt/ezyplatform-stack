# ezyoa

Tài khoản Official Account, kịch bản và thông báo.

- **Bản Marketplace trên core 1.5.9:** `0.4.2`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyoa` | `org.youngmonkeys.ezyoa` | [ezysupport](ezysupport.md), [ezychat](ezychat.md), [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezyoa` | `org.youngmonkeys.ezyoa` | [ezychat](ezychat.md), [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 36 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

**web-plugin** — 3 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/oa/{code}/webhook` | `WebApiOAWebhookController` |
| `GET /oa/{code}/auth-callback` | `WebOACallbackController` |
| `POST /api/v1/oa/{code}/webhook` | `WebApiOAWebhookController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyoa: /`, `oa_services: /oa-services`, `oa_services_add: ~/oa-services/add`, `oa_services_edit: ~/oa-services/{code}/edit`, `oa_services_details: ~/oa-services/{code}`, `oa_user_details: ~/oa-users/{id}` (+5).

- **admin-plugin – Template:** `ezyoa/customers/fragments/details.html`, `ezyoa/customers/fragments/link-oa-services.html`, `ezyoa/customers/fragments/search-oa-user-modal.html`, `ezyoa/customers/oa-message/list.html`, `ezyoa/fragments/oa-user.html`, `ezyoa/modals/search-oa-user.html`, `ezyoa/oa-service/add.html` (+10).

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `oa-response-message-templates/default_message.properties`, `oa-response-message-templates/new_customer_message.properties`, `oa-response-message-templates/oa_user_message_notification_for_staff.properties`, `oa-response-message-templates/payment_message.properties` (+3).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (5):** `ezyoa_oa_notification_templates`, `ezyoa_oa_service_settings`, `ezyoa_oa_user_message_channels`, `ezyoa_oa_user_messages`, `ezyoa_oa_users`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (5):** `OANotificationTemplate`, `OAServiceSetting`, `OAUser`, `OAUserMessage`, `OAUserMessageChannel`.
- **SQL admin-plugin (8 tệp):** `resources/scripts/notification_templates.sql`, `resources/scripts/scripts.sql`, `resources/scripts/users.sql`, `resources/scripts/alter_oa_service_setting_add_handing_service.sql`, `resources/scripts/alter_oa_service_settings_to_add_notification_channel.sql`, `resources/scripts/alter_oa_users_to_add_admin_id.sql`, `resources/scripts/alter_tables_1.sql` (+1).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyoa-admin-plugin-0.4.2.jar`, `ezyoa-sdk-0.4.2.jar`; 261 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyoa.model`, `org.youngmonkeys.ezyoa.listener`, `org.youngmonkeys.ezyoa.service` (+38).
- **Controller/service/repository (mẫu):** `AdminApiOAChatChannelController`, `AdminApiOACustomerServiceStaffController`, `AdminApiOAMessageResponseScenarioController`, `AdminApiOANotificationTemplateController`, `AbstractOAService`, `AdminCustomerFetcher`, `AdminCustomerPortraitChangesFetcher`, `AdminCustomerPortraitDataFetcher`, `AdminCustomerPortraitOAUserRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyOACustomerPortraitConfig`, `AdminOAComponentManagerConfig`, `AdminOAResponseMessageTemplateConfig`, `OAComponentManagerConfig`, `OAServiceSetting`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `content`, `title`.
- **Điểm mở rộng tiềm năng theo tên class:** `AbstractOATemplatedMessageSender`, `AdminFetchLastOaMessageMetadataEventHandler`, `AdminFetchOaPayCommandsEventHandler`, `AdminMessengerOAUserSendMessageListener`, `AdminNewOrdersAppendEventHandler`, `AdminOAExtensionMessageSenderManager`, `AdminOAListenerManager`, `AdminOAServiceManager`, `AdminOATemplatedMessageSenderManager` (+58).

### web-plugin

- **JAR kiểm tra:** `ezyoa-sdk-0.4.2.jar`, `ezyoa-web-plugin-0.4.2.jar`; 211 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyoa.model`, `org.youngmonkeys.ezyoa.listener`, `org.youngmonkeys.ezyoa.service` (+32).
- **Controller/service/repository (mẫu):** `WebApiOAWebhookController`, `WebOACallbackController`, `WebOAUserAvatarStorageControllerService`, `AbstractOAService`, `CustomerFetcher`, `EzyOASettingService`, `MessengerService`, `OACustomerServiceStaffService`.
- **Class cấu hình/quyền (mẫu):** `OAComponentManagerConfig`, `OAServiceSetting`, `WebOAComponentManagerConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AbstractOATemplatedMessageSender`, `FetchLastOaMessageMetadataEventHandler`, `FetchOaPayCommandsEventHandler`, `MessengerOAUserSendMessageListener`, `OAAbstractListener`, `OAAbstractTemplatedMessageSender`, `OAAbstractTemplatedNotificationSender`, `OAAbstractTemplatedSender`, `OAAdminSendMessageListener` (+63).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyoa/oa-services`, `/ezyoa/templates` → 200. Chưa tích hợp tài khoản Official Account.

## Áp dụng cho plugin quản lý công việc

Mẫu cho automation: template, parameter, kịch bản và connector tách nhau. File task_list_message.properties là template phản hồi OA, không phải engine quản lý task. Để OA là kênh tùy chọn, không phụ thuộc lúc triển khai MVP.

[Về chỉ mục plugin](README.md)
