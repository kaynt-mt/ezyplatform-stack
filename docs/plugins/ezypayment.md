# ezypayment

Payment services, plans, and subscriptions.

- **Marketplace version on core 1.5.9:** `0.2.5`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezypayment` | `org.youngmonkeys.ezypayment` | [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/ezypayment` | `org.youngmonkeys.ezypayment` | [ecommerce](ecommerce.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 28 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyPaymentSettingController` |
| `GET /payment-plans` | `AdminPaymentPlanController` |
| `GET /payment-services` | `AdminPaymentServiceController` |
| `GET /payment-subscriptions` | `AdminPaymentSubscriptionController` |
| `GET /payment-plans/add` | `AdminPaymentPlanController` |
| `GET /payment-subscriptions/add` | `AdminPaymentSubscriptionController` |
| `GET /api/v1/payment-plans` | `AdminApiPaymentPlanController` |
| `POST /api/v1/payment-plans/add` | `AdminApiPaymentPlanController` |
| `POST /api/v1/payment-subscriptions/add` | `AdminApiPaymentSubscriptionController` |
| `POST /api/v1/payment-plans/{id}/make-a-copy` | `AdminApiPaymentPlanController` |
| `PUT /api/v1/settings` | `AdminApiEzyPaymentSettingController` |
| `PUT /api/v1/payment-plans/{id}` | `AdminApiPaymentPlanController` |
| `PUT /api/v1/payment-subscriptions/{id}` | `AdminApiPaymentSubscriptionController` |
| `PUT /api/v1/payment-plans/{id}/activate` | `AdminApiPaymentPlanController` |
| `DELETE /api/v1/payment-plans/{id}` | `AdminApiPaymentPlanController` |

**web-plugin** — 17 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /checkout/pay2s` | `WebEzyPaymentPay2sController` |
| `GET /checkout/payfs` | `WebEzyPaymentPayFsController` |
| `GET /checkout/sepay` | `WebEzyPaymentSePayController` |
| `GET /checkout/paypal` | `WebEzyPaymentPaypalController` |
| `GET /ezypayment/payment-required` | `WebPaymentRequiredController` |
| `GET /api/v1/payment-plans` | `WebApiPaymentPlanController` |
| `GET /api/v1/ezypayment/subscriptions` | `WebApiPaymentSubscriptionController` |
| `POST /api/v1/ezypayment/subscriptions/create-from-product` | `WebApiPaymentSubscriptionController` |
| `POST /api/v1/paypal/orders/{orderId}/create` | `WebApiEzyPaymentPaypalController` |
| `PUT /api/v1/pay2s/orders/{orderId}/bank-transferred` | `WebApiEzyPaymentPay2sController` |
| `PUT /api/v1/payfs/orders/{orderId}/bank-transferred` | `WebApiEzyPaymentPayFsController` |
| `PUT /api/v1/sepay/orders/{orderId}/bank-transferred` | `WebApiEzyPaymentSePayController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezypayment: /`, `payment_services: /payment-services`, `payment_subscriptions_menu_item: /payment-subscriptions`, `payment_subscriptions_menu_item_add: ~/payment-subscriptions/add`, `payment_subscriptions_menu_item_details: ~/payment-subscriptions/{id}`, `payment_subscriptions_menu_item_edit: ~/payment-subscriptions/{id}/edit` (+7).

- **admin-plugin – Template:** `ezypayment/customers/fragments/subscription-list.html`, `ezypayment/payment-plan/add.html`, `ezypayment/payment-plan/details.html`, `ezypayment/payment-plan/edit.html`, `ezypayment/payment-plan/history-details.html`, `ezypayment/payment-plan/list.html`, `ezypayment/payment-plan/payment-plan-history-list.html` (+10).

- **admin-plugin – Static resources:** `ezypayment/css/style.css`.

- **web-plugin – Template:** `checkout/pay2s.html`, `checkout/payfs.html`, `checkout/paypal.html`, `checkout/sepay.html`, `ezypayment/payment-required.html`.

## Data and migrations

- **Table in the DDL package (4):** `ezypayment_payment_plan_histories`, `ezypayment_payment_plans`, `ezypayment_payment_subscription_histories`, `ezypayment_payment_subscriptions`.
- **Class with JPA Entity/MappedSuperclass):** `PaymentPlan`, `PaymentPlanHistory`, `PaymentSubscription`, `PaymentSubscriptionHistory`.
- **SQL admin-plugin (3 files):** `resources/scripts/scripts.sql`, `resources/scripts/alter_tables_1.sql`, `resources/scripts/alter_tables_indexes.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezypayment-admin-plugin-0.2.5.jar`, `ezypayment-sdk-0.2.5.jar`; 167 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezypayment.pagination`, `org.youngmonkeys.ezypayment.admin.service`, `org.youngmonkeys.ezypayment.service` (+25).
- **Controllers, services, and repositories (sample):** `AdminApiEzyPaymentSettingController`, `AdminApiPaymentPlanController`, `AdminApiPaymentPlanHistoryController`, `AdminApiPaymentSubscriptionController`, `AdminEzyPaymentSettingService`, `AdminEzyPaymentSettingValidator`, `AdminPaginationPaymentPlanHistoryRepository`, `AdminPaginationPaymentPlanHistoryService`, `AdminPaginationPaymentPlanRepository`.
- **Configuration and permission classes (sample):** `AdminEzyPaymentPageFragmentConfig`, `AdminEzyPaymentProductTypeConfig`, `AdminEzyPaymentViewMetadataConfig`, `EzyPaymentPageFragmentConfig`.
- **Potential extension points based on class names:** `AdminPaymentPlanCategoryNameManager`, `AdminPaymentPlanPeriodUnitManager`, `AdminPaymentPlanStatusManager`, `AdminPaymentPlanSubscriptionTypeManager`, `AdminPaymentPlanTypeManager`, `AdminPaymentSubscriptionPeriodUnitManager`, `AdminPaymentSubscriptionStatusManager`, `AdminPaymentSubscriptionSubscriptionTypeManager`.

### web-plugin

- **JARs inspected:** `ezypayment-sdk-0.2.5.jar`, `ezypayment-web-plugin-0.2.5.jar`; 150 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezypayment.pagination`, `org.youngmonkeys.ezypayment.web.service`, `org.youngmonkeys.ezypayment.service` (+24).
- **Controllers, services, and repositories (sample):** `WebApiEzyPaymentPay2sController`, `WebApiEzyPaymentPayFsController`, `WebApiEzyPaymentPaypalController`, `WebApiEzyPaymentSePayController`, `EzyPaymentSettingService`, `PaginationPaymentPlanHistoryRepository`, `PaginationPaymentPlanHistoryService`, `PaginationPaymentPlanRepository`, `PaginationPaymentPlanService`.
- **Configuration and permission classes (sample):** `EzyPaymentPageFragmentConfig`, `WebEzyPaymentPageFragmentConfig`.
- **Potential extension points based on class names:** `WebDefaultValidateUserPaymentRequiredEventHandler`, `WebEzyPaymentExceptionHandler`, `WebEzyPaymentUserAuthenticationRequiredApiEventHandler`, `WebPaymentInterceptor`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezypayment/payment-services` and Web `/api/v1/payment-plans` returned 200. No payment gateway was called.

## Integration notes

Keep webhooks and payment state separate from business data writes. Test only against the provider's sandbox.

[Back to the plugin index](README.md)
