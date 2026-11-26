# ezypayment

Dịch vụ thanh toán, gói và thuê bao.

- **Bản Marketplace trên core 1.5.9:** `0.2.5`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezypayment` | `org.youngmonkeys.ezypayment` | [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/ezypayment` | `org.youngmonkeys.ezypayment` | [ecommerce](ecommerce.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 28 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

**web-plugin** — 17 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezypayment: /`, `payment_services: /payment-services`, `payment_subscriptions_menu_item: /payment-subscriptions`, `payment_subscriptions_menu_item_add: ~/payment-subscriptions/add`, `payment_subscriptions_menu_item_details: ~/payment-subscriptions/{id}`, `payment_subscriptions_menu_item_edit: ~/payment-subscriptions/{id}/edit` (+7).

- **admin-plugin – Template:** `ezypayment/customers/fragments/subscription-list.html`, `ezypayment/payment-plan/add.html`, `ezypayment/payment-plan/details.html`, `ezypayment/payment-plan/edit.html`, `ezypayment/payment-plan/history-details.html`, `ezypayment/payment-plan/list.html`, `ezypayment/payment-plan/payment-plan-history-list.html` (+10).

- **admin-plugin – Tài nguyên tĩnh:** `ezypayment/css/style.css`.

- **web-plugin – Template:** `checkout/pay2s.html`, `checkout/payfs.html`, `checkout/paypal.html`, `checkout/sepay.html`, `ezypayment/payment-required.html`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (4):** `ezypayment_payment_plan_histories`, `ezypayment_payment_plans`, `ezypayment_payment_subscription_histories`, `ezypayment_payment_subscriptions`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (4):** `PaymentPlan`, `PaymentPlanHistory`, `PaymentSubscription`, `PaymentSubscriptionHistory`.
- **SQL admin-plugin (3 tệp):** `resources/scripts/scripts.sql`, `resources/scripts/alter_tables_1.sql`, `resources/scripts/alter_tables_indexes.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezypayment-admin-plugin-0.2.5.jar`, `ezypayment-sdk-0.2.5.jar`; 167 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezypayment.pagination`, `org.youngmonkeys.ezypayment.admin.service`, `org.youngmonkeys.ezypayment.service` (+25).
- **Controller/service/repository (mẫu):** `AdminApiEzyPaymentSettingController`, `AdminApiPaymentPlanController`, `AdminApiPaymentPlanHistoryController`, `AdminApiPaymentSubscriptionController`, `AdminEzyPaymentSettingService`, `AdminEzyPaymentSettingValidator`, `AdminPaginationPaymentPlanHistoryRepository`, `AdminPaginationPaymentPlanHistoryService`, `AdminPaginationPaymentPlanRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyPaymentPageFragmentConfig`, `AdminEzyPaymentProductTypeConfig`, `AdminEzyPaymentViewMetadataConfig`, `EzyPaymentPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminPaymentPlanCategoryNameManager`, `AdminPaymentPlanPeriodUnitManager`, `AdminPaymentPlanStatusManager`, `AdminPaymentPlanSubscriptionTypeManager`, `AdminPaymentPlanTypeManager`, `AdminPaymentSubscriptionPeriodUnitManager`, `AdminPaymentSubscriptionStatusManager`, `AdminPaymentSubscriptionSubscriptionTypeManager`.

### web-plugin

- **JAR kiểm tra:** `ezypayment-sdk-0.2.5.jar`, `ezypayment-web-plugin-0.2.5.jar`; 150 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezypayment.pagination`, `org.youngmonkeys.ezypayment.web.service`, `org.youngmonkeys.ezypayment.service` (+24).
- **Controller/service/repository (mẫu):** `WebApiEzyPaymentPay2sController`, `WebApiEzyPaymentPayFsController`, `WebApiEzyPaymentPaypalController`, `WebApiEzyPaymentSePayController`, `EzyPaymentSettingService`, `PaginationPaymentPlanHistoryRepository`, `PaginationPaymentPlanHistoryService`, `PaginationPaymentPlanRepository`, `PaginationPaymentPlanService`.
- **Class cấu hình/quyền (mẫu):** `EzyPaymentPageFragmentConfig`, `WebEzyPaymentPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `WebDefaultValidateUserPaymentRequiredEventHandler`, `WebEzyPaymentExceptionHandler`, `WebEzyPaymentUserAuthenticationRequiredApiEventHandler`, `WebPaymentInterceptor`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezypayment/payment-services` và Web `/api/v1/payment-plans` → 200; không gọi cổng thanh toán.

## Áp dụng cho plugin quản lý công việc

Để ngoài MVP. Nếu sau này cần billing, giữ webhook/trạng thái thanh toán tách khỏi schema issue và chỉ thử bằng nhà cung cấp sandbox.

[Về chỉ mục plugin](README.md)
