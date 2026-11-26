# ezycrm

Khách hàng, phụ trách, nhóm và lịch sử.

- **Bản Marketplace trên core 1.5.9:** `0.6.3`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezycrm` | `org.youngmonkeys.ezycrm` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezycrm` | `org.youngmonkeys.ezycrm` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 97 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/customers/{userId}/all-assigned-staff` | `AdminApiCustomerAssignedStaffController` |
| `GET /api/v1/customers/{userId}/assigned-staff/{adminId}/commission` | `AdminApiCustomerAssignedStaffController` |
| `GET /customers` | `AdminCustomerController` |
| `GET /api/v1/customers` | `AdminApiCustomerController` |
| `GET /user-groups` | `AdminUserGroupController` |
| `GET /user-groups/add` | `AdminUserGroupController` |
| `GET /customers/{username}/histories/{historyId}` | `AdminCustomerHistoryController` |
| `POST /api/v1/customers/{userId}/assigned-staff/add` | `AdminApiCustomerAssignedStaffController` |
| `POST /api/v1/customers/{userId}/data/add` | `AdminApiCustomerDataController` |
| `POST /api/v1/customers/{userId}/meta/add` | `AdminApiCustomerMetaController` |
| `POST /api/v1/user-groups/add` | `AdminApiUserGroupController` |
| `PUT /api/v1/customers/{userId}/assigned-staff/{adminId}` | `AdminApiCustomerAssignedStaffController` |
| `PUT /api/v1/customers/{userId}/assigned-staff/{adminId}/link` | `AdminApiCustomerAssignedStaffController` |
| `PUT /api/v1/customers/{username}` | `AdminApiCustomerController` |
| `PUT /api/v1/customers/{customerId}/medias` | `AdminApiEzyCRMCustomerMediaController` |
| `DELETE /api/v1/customers/{userId}/tags/{tag}` | `AdminApiCustomerTagController` |
| `DELETE /api/v1/customers/{customerId}/medias/{mediaId}` | `AdminApiEzyCRMCustomerMediaController` |
| `DELETE /api/v1/user-groups/{id}` | `AdminApiUserGroupController` |
| `DELETE /api/v1/event-user-groups/{id}` | `AdminApiEzyCRMEventUserGroupController` |

**web-plugin** — 9 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/ezycrm/customers/{customerUserId}/meta/{metaKey}` | `WebEzyCRMApiCustomerController` |
| `GET /events` | `WebEzyCRMApiEventController` |
| `GET /events-participants` | `WebEzyCRMApiEventParticipantController` |
| `GET /events/{id}/check-in` | `WebEzyCRMEventParticipantCheckInController` |
| `GET /events/{id}/event-participant-ids` | `WebEzyCRMApiEventParticipantController` |
| `POST /api/v1/ezycrm/subscribe` | `WebEzyCRMApiSubscriberController` |
| `POST /api/v1/ezycrm/customer/meta/{metaKey}/increase` | `WebEzyCRMApiCustomerController` |
| `PUT /event-participants/{eventParticipantId}/check-in` | `WebEzyCRMApiEventParticipantController` |
| `PUT /events/{eventId}/participants/{participantId}/check-in` | `WebEzyCRMApiEventParticipantController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezycrm: /`, `customers: /customers`, `customers_histories_details: ~/customers/{username}/histories/{historyId}`, `customer_portraits: /customer-portraits`, `user_groups: /user-groups`, `user_groups_add: ~/user-groups/add` (+13).

- **admin-plugin – Template:** `ezycrm/customer-portraits/fragments/customer.html`, `ezycrm/customer-portraits/fragments/messages.html`, `ezycrm/customer-portraits/index.html`, `ezycrm/customers/assigned-staff/add.html`, `ezycrm/customers/assigned-staff/edit.html`, `ezycrm/customers/assigned-staff/list.html`, `ezycrm/customers/data/add-data.html` (+61).

- **admin-plugin – Tài nguyên tĩnh:** `ezycrm/css/customer-portrait-common.css`, `ezycrm/css/customer-portrait-customer.css`, `ezycrm/css/customer-portrait-overview.css`, `ezycrm/css/style.css` (+5).

- **web-plugin – Tài nguyên cấu hình/mẫu:** `messages.properties`, `messages_ar.properties`, `messages_vi.properties`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (19):** `ezycrm_customer_data`, `ezycrm_customer_histories`, `ezycrm_customer_portrait_counters`, `ezycrm_customer_portrait_interests`, `ezycrm_customer_portrait_statistics`, `ezycrm_customer_portraits`, `ezycrm_customers`, `ezycrm_event_location_sessions`, `ezycrm_event_locations`, `ezycrm_event_participant_histories`, `ezycrm_event_participants`, `ezycrm_event_user_groups`, `ezycrm_events`, `ezycrm_user_group_member_histories`, `ezycrm_user_group_member_role_histories`, `ezycrm_user_group_member_roles`, `ezycrm_user_group_members`, `ezycrm_user_group_roles`, `ezycrm_user_groups`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (19):** `Customer`, `CustomerData`, `CustomerHistory`, `CustomerPortrait`, `CustomerPortraitCounter`, `CustomerPortraitInterest`, `CustomerPortraitStatistic`, `EzyCRMEvent`, `EzyCRMEventLocation`, `EzyCRMEventLocationSession`, `EzyCRMEventParticipant`, `EzyCRMEventParticipantHistory`, `EzyCRMEventUserGroup`, `UserGroup`, `UserGroupMember`, `UserGroupMemberHistory`, `UserGroupMemberRole`, `UserGroupMemberRoleHistory` (+1).
- **SQL admin-plugin (45 tệp):** `resources/scripts/customer_datas.sql`, `resources/scripts/customer_portraits.sql`, `resources/scripts/event.sql`, `resources/scripts/ezycrm_customer_history.sql`, `resources/scripts/scripts.sql`, `resources/scripts/user-group.sql`, `resources/scripts/alter-add-type-indexes.sql` (+38).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezycrm-admin-plugin-0.6.3.jar`, `ezycrm-sdk-0.6.3.jar`; 579 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezycrm.pagination`, `org.youngmonkeys.ezycrm.entity`, `org.youngmonkeys.ezycrm.admin.repo` (+33).
- **Controller/service/repository (mẫu):** `AdminApiCustomerAssignedStaffController`, `AdminApiCustomerController`, `AdminApiCustomerDataController`, `AdminApiCustomerHistoryController`, `AdminCustomerAssignedStaffControllerService`, `AdminCustomerAssignedStaffValidator`, `AdminCustomerControllerService`, `AdminCustomerDataControllerService`, `AdminCustomerDataRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyCRMMailConfig`, `AdminEzyCRMUserRoleConfig`, `AdminEzyCRMViewMetadataConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminCheckDelayedPaymentCustomerIdEventHandler`, `AdminCheckDelinquentCustomerIdEventHandler`, `AdminCheckVipCustomerIdEventHandler`, `AdminContainsCustomerDataByUserIdAndDataNameAndDataValueEventHandler`, `AdminCustomerPortraitDataFetcherManager`, `AdminEzyCRMEventLocationTypeManager`, `AdminEzyCRMEventParticipantTypeManager`, `AdminEzyCRMEventTypeManager`, `AdminEzyCRMEzyAccountUpdateUserEventHandler` (+63).

### web-plugin

- **JAR kiểm tra:** `ezycrm-sdk-0.6.3.jar`, `ezycrm-web-plugin-0.6.3.jar`; 413 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezycrm.pagination`, `org.youngmonkeys.ezycrm.entity`, `org.youngmonkeys.ezycrm.event` (+24).
- **Controller/service/repository (mẫu):** `WebEzyCRMApiCustomerController`, `WebEzyCRMApiEventController`, `WebEzyCRMApiEventParticipantController`, `WebEzyCRMApiSubscriberController`, `CustomerDataRepository`, `CustomerDataService`, `CustomerHistoryRepository`, `CustomerHistoryService`, `CustomerMediaService`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `relationship_aunt_maternal`, `relationship_aunt_paternal`, `relationship_aunt_uncle_wife`, `relationship_cousin_female_older`, `relationship_cousin_female_younger` (+23).
- **Điểm mở rộng tiềm năng theo tên class:** `CheckDelayedPaymentCustomerIdEventHandler`, `CheckDelinquentCustomerIdEventHandler`, `CheckVipCustomerIdEventHandler`, `EzyCRMEvent`, `EzyCRMEzyAccountUpdateUserEventHandler`, `EzyCRMSetUserAddressEventHandler`, `FetchContainsCustomerDataByUserIdAndDataNameAndDataValueEventHandler`, `FetchCustomerAddressByIdEventHandler`, `FetchCustomerAddressMapByIdEventHandler` (+54).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezycrm/customers`, `/ezycrm/user-groups` → 200. Chưa bắn thông báo hoặc nhập dữ liệu khách hàng.

## Lưu ý khi tích hợp

`AdminApiCustomerAssignedStaffController` là mẫu tách danh sách, thêm/sửa và liên kết `userId/adminId`; xem thêm màn hình nhóm và lịch sử.

[Về chỉ mục plugin](README.md)
