# ezycrm

Customers, staff assignments, groups, and history.

- **Marketplace version on core 1.5.9:** `0.6.3`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezycrm` | `org.youngmonkeys.ezycrm` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezycrm` | `org.youngmonkeys.ezycrm` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 97 method/URI combinations identified; representative sample:

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

**web-plugin** — 9 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezycrm: /`, `customers: /customers`, `customers_histories_details: ~/customers/{username}/histories/{historyId}`, `customer_portraits: /customer-portraits`, `user_groups: /user-groups`, `user_groups_add: ~/user-groups/add` (+13).

- **admin-plugin – Template:** `ezycrm/customer-portraits/fragments/customer.html`, `ezycrm/customer-portraits/fragments/messages.html`, `ezycrm/customer-portraits/index.html`, `ezycrm/customers/assigned-staff/add.html`, `ezycrm/customers/assigned-staff/edit.html`, `ezycrm/customers/assigned-staff/list.html`, `ezycrm/customers/data/add-data.html` (+61).

- **admin-plugin – Static resources:** `ezycrm/css/customer-portrait-common.css`, `ezycrm/css/customer-portrait-customer.css`, `ezycrm/css/customer-portrait-overview.css`, `ezycrm/css/style.css` (+5).

- **Web-plugin – Configuration/Sample Resource:** `messages.properties`, `messages_ar.properties`, `messages_vi.properties`.

## Data and migrations

- **Table in the DDL packaging (19):** `ezycrm_customer_data`, `ezycrm_customer_histories`, `ezycrm_customer_portrait_counters`, `ezycrm_customer_portrait_interests`, `ezycrm_customer_portrait_statistics`, `ezycrm_customer_portraits`, `ezycrm_customers`, `ezycrm_event_location_sessions`, `ezycrm_event_locations`, `ezycrm_event_participant_histories`, `ezycrm_event_participants`, `ezycrm_event_user_groups`, `ezycrm_events`, `ezycrm_user_group_member_histories`, `ezycrm_user_group_member_role_histories`, `ezycrm_user_group_member_roles`, `ezycrm_user_group_members`, `ezycrm_user_group_roles`, `ezycrm_user_groups`.
- **Class with JPA Entity/MappedSuperclass):** `Customer`, `CustomerData`, `CustomerHistory`, `CustomerPortrait`, `CustomerPortraitCounter`, `CustomerPortraitInterest`, `CustomerPortraitStatistic`, `EzyCRMEvent`, `EzyCRMEventLocation`, `EzyCRMEventLocationSession`, `EzyCRMEventParticipant`, `EzyCRMEventParticipantHistory`, `EzyCRMEventUserGroup`, `UserGroup`, `UserGroupMember`, `UserGroupMemberHistory`, `UserGroupMemberRole`, `UserGroupMemberRoleHistory` (+1).
- **SQL admin-plugin (45 files):** `resources/scripts/customer_datas.sql`, `resources/scripts/customer_portraits.sql`, `resources/scripts/event.sql`, `resources/scripts/ezycrm_customer_history.sql`, `resources/scripts/scripts.sql`, `resources/scripts/user-group.sql`, `resources/scripts/alter-add-type-indexes.sql` (+38).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezycrm-admin-plugin-0.6.3.jar`, `ezycrm-sdk-0.6.3.jar`; 579 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezycrm.pagination`, `org.youngmonkeys.ezycrm.entity`, `org.youngmonkeys.ezycrm.admin.repo` (+33).
- **Controllers, services, and repositories (sample):** `AdminApiCustomerAssignedStaffController`, `AdminApiCustomerController`, `AdminApiCustomerDataController`, `AdminApiCustomerHistoryController`, `AdminCustomerAssignedStaffControllerService`, `AdminCustomerAssignedStaffValidator`, `AdminCustomerControllerService`, `AdminCustomerDataControllerService`, `AdminCustomerDataRepository`.
- **Configuration and permission classes (sample):** `AdminEzyCRMMailConfig`, `AdminEzyCRMUserRoleConfig`, `AdminEzyCRMViewMetadataConfig`.
- **Potential extension points based on class names:** `AdminCheckDelayedPaymentCustomerIdEventHandler`, `AdminCheckDelinquentCustomerIdEventHandler`, `AdminCheckVipCustomerIdEventHandler`, `AdminContainsCustomerDataByUserIdAndDataNameAndDataValueEventHandler`, `AdminCustomerPortraitDataFetcherManager`, `AdminEzyCRMEventLocationTypeManager`, `AdminEzyCRMEventParticipantTypeManager`, `AdminEzyCRMEventTypeManager`, `AdminEzyCRMEzyAccountUpdateUserEventHandler` (+63).

### web-plugin

- **JARs inspected:** `ezycrm-sdk-0.6.3.jar`, `ezycrm-web-plugin-0.6.3.jar`; 413 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezycrm.pagination`, `org.youngmonkeys.ezycrm.entity`, `org.youngmonkeys.ezycrm.event` (+24).
- **Controllers, services, and repositories (sample):** `WebEzyCRMApiCustomerController`, `WebEzyCRMApiEventController`, `WebEzyCRMApiEventParticipantController`, `WebEzyCRMApiSubscriberController`, `CustomerDataRepository`, `CustomerDataService`, `CustomerHistoryRepository`, `CustomerHistoryService`, `CustomerMediaService`.
- **Configuration and template keys from resources (values omitted):** `relationship_aunt_maternal`, `relationship_aunt_paternal`, `relationship_aunt_uncle_wife`, `relationship_cousin_female_older`, `relationship_cousin_female_younger` (+23).
- **Potential extension points based on class names:** `CheckDelayedPaymentCustomerIdEventHandler`, `CheckDelinquentCustomerIdEventHandler`, `CheckVipCustomerIdEventHandler`, `EzyCRMEvent`, `EzyCRMEzyAccountUpdateUserEventHandler`, `EzyCRMSetUserAddressEventHandler`, `FetchContainsCustomerDataByUserIdAndDataNameAndDataValueEventHandler`, `FetchCustomerAddressByIdEventHandler`, `FetchCustomerAddressMapByIdEventHandler` (+54).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezycrm/customers` and `/ezycrm/user-groups` returned 200. No notifications were sent and no customer data was imported.

## Integration notes

`AdminApiCustomerAssignedStaffController` demonstrates separate list, create, and update operations and associations between `userId/adminId`. See also the group and history screens.

[Back to the plugin index](README.md)
