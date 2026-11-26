# ezydelivery

Mã vận đơn, quét mã và giao nhận.

- **Bản Marketplace trên core 1.5.9:** `0.7.7`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezydelivery` | `org.youngmonkeys.ezydelivery` | [ecommerce](ecommerce.md), [accounting](accounting.md), [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezydelivery` | `org.youngmonkeys.ezydelivery` | [ecommerce](ecommerce.md), [accounting](accounting.md), [ezyarticle](ezyarticle.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 150 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /users` | `AdminEzyDeliveryUserController` |
| `GET /settings` | `AdminEzyDeliverySettingController` |
| `GET /collaborators` | `AdminShopCollaboratorController` |
| `GET /shop-agencies` | `AdminShopAgencyController` |
| `GET /shop-vehicles` | `AdminShopVehicleController` |
| `GET /product-packages` | `AdminEzyDeliveryProductPackageController` |
| `GET /delivery-services` | `AdminDeliveryServiceController` |
| `POST /api/v1/create-delivery-order` | `AdminApiEzyDeliveryDeliveryOrderController` |
| `POST /api/v1/collaborators/add` | `AdminApiShopCollaboratorController` |
| `POST /api/v1/shop-vehicles/add` | `AdminApiShopVehicleController` |
| `POST /api/v1/product-package/create` | `AdminApiEzyDeliveryProductPackageController` |
| `PUT /api/v1/users/vip` | `AdminApiEzyDeliveryUserController` |
| `PUT /api/v1/settings/vehicle` | `AdminApiEzyDeliverySettingController` |
| `PUT /api/v1/product-packages/status` | `AdminApiEzyDeliveryProductPackageController` |
| `PUT /api/v1/settings/order-code-allocation` | `AdminApiEzyDeliverySettingController` |
| `DELETE /api/v1/shop-vehicles` | `AdminApiShopVehicleController` |
| `DELETE /api/v1/product-packages` | `AdminApiEzyDeliveryProductPackageController` |
| `DELETE /api/v1/shop-vehicles/product-packages` | `AdminApiShopVehicleProductPackageController` |
| `DELETE /api/v1/shop-vehicles/{id}` | `AdminApiShopVehicleController` |

**web-plugin** — 14 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /track-shipment` | `WebApiTrackShipmentController` |
| `GET /shipping-requests` | `WebApiUserShippingRequestController` |
| `GET /user/delivery-order-codes` | `WebApiUserDeliveryOrderCodeController` |
| `GET /user/delivery-order-items` | `WebApiUserDeliveryOrderCodeController` |
| `GET /shipping-requests/{id}/details` | `WebApiUserShippingRequestController` |
| `GET /account/customer-commissions/{year}/{month}` | `WebApiAccountCustomerCommissionController` |
| `GET /user/delivery-order-items/{code}/mapped-from-delivery-order-codes` | `WebApiPublicUserDeliveryOrderCodeController` |
| `POST /shipping-requests/add` | `WebApiUserShippingRequestController` |
| `POST /shipping-requests/debt-payment-qr-code` | `WebApiUserShippingRequestController` |
| `PUT /customer/delivery-method` | `WebApiEzyDeliveryCustomerController` |
| `PUT /shipping-requests/{id}` | `WebApiUserShippingRequestController` |
| `PUT /user/delivery-order-codes/{deliveryOrderCode}` | `WebApiUserDeliveryOrderCodeController` |
| `DELETE /shipping-requests/{id}` | `WebApiUserShippingRequestController` |
| `DELETE /user/delivery-order-codes/{deliveryOrderCode}/not-at-input-warehouse` | `WebApiUserDeliveryOrderCodeController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezydelivery: /`, `scan_order_code: /scan-delivery-order-codes`, `declare_order_code: /delivery-order-codes`, `rejected_delivery_order_codes: /rejected-delivery-order-codes`, `photo_required_delivery_order_codes: /photo-required-delivery-order-codes`, `sensitive_delivery_order_codes: /sensitive-delivery-order-codes` (+32).

- **admin-plugin – Template:** `ezydelivery/accounting/overview/user-delivery-order-item.html`, `ezydelivery/all-delivery-order-code/delivery-order-history-list.html`, `ezydelivery/all-delivery-order-code/delivery-order-list.html`, `ezydelivery/all-delivery-order-code/details.html`, `ezydelivery/all-delivery-order-code/list.html`, `ezydelivery/allocate-delivery-order-code-customer/customer-details.html`, `ezydelivery/allocate-delivery-order-code-customer/customer-list.html` (+102).

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `administrative-type-prefix-mapping-templates/ghtk.json`, `administrative-type-prefix-mapping-templates/spx.json`, `administrative-type-prefix-mapping-templates/viettel_post.json`, `administrative-type-prefix-mapping-templates/viettel_post_small.json` (+10).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (8):** `ezydelivery_delivery_order_shipping_rate_histories`, `ezydelivery_delivery_order_shipping_rates`, `ezydelivery_shop_vehicle_histories`, `ezydelivery_shop_vehicle_product_packages`, `ezydelivery_shop_vehicles`, `ezydelivery_user_shipping_rate_histories`, `ezydelivery_user_shipping_rates`, `ezydelivery_user_shipping_requests`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (8):** `DeliveryOrderShippingRate`, `DeliveryOrderShippingRateHistory`, `ShopVehicle`, `ShopVehicleHistory`, `ShopVehicleProductPackage`, `UserShippingRate`, `UserShippingRateHistory`, `UserShippingRequest`.
- **SQL admin-plugin (13 tệp):** `resources/scripts/scripts.sql`, `resources/scripts/shop_vehicle_history.sql`, `resources/scripts/user_shipping_rates.sql`, `resources/scripts/user_shipping_requests.sql`, `resources/scripts/alter_add_detailed_status.sql`, `resources/scripts/alter_delivery_order_table_100.sql`, `resources/scripts/alter_ezyplatform_user_add_username_status_index.sql` (+6).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezydelivery-admin-plugin-0.7.7.jar`, `ezydelivery-sdk-0.7.7.jar`; 459 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezydelivery.admin.response`, `org.youngmonkeys.ezydelivery.admin.service`, `org.youngmonkeys.ezydelivery.service` (+34).
- **JAR thư viện khác:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controller/service/repository (mẫu):** `AdminApiCustomerDeliveryOrderCodeController`, `AdminApiDeliveryOrderCodeController`, `AdminApiDeliveryOrderShippingRateController`, `AdminApiEzyDeliveryCustomerController`, `AdminCustomerDeliveryOrderControllerService`, `AdminDeliveryOrderCodeValidator`, `AdminDeliveryOrderFixedCostService`, `AdminDeliveryOrderShippingRateControllerService`, `AdminDeliveryOrderShippingRateHistoryRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminAdministrativeTypeNameMappingTemplateConfig`, `AdminEzyDeliveryConfig`, `AdminEzyDeliveryDataAppenderConfig`, `AdminEzyDeliveryOAResponseMessageTemplateConfig`, `AdminEzyDeliveryOaConfig`, `AdminEzyDeliveryUserRoleConfig`, `AdminEzyDeliveryViewMetadataConfig` (+1).
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `content`, `contentType`, `title`.
- **Resource trong JAR (mẫu):** `ezydelivery/ezydelivery.properties`.
- **Điểm mở rộng tiềm năng theo tên class:** `AccountingUserFormulaBeforeUpdateEventHandler`, `AccountingUserFormulaUpdatedEventHandler`, `AdminAccountingUserFormulaBeforeUpdateEventHandler`, `AdminAccountingUserFormulaUpdatedEventHandler`, `AdminEzyDeliveryCargoTypeManager`, `AdminShopVehicleStatusManager`, `AdminShopVehicleTypeManager`, `AdminUserDeliveryOrderCodeMessageProcessor`, `AdminUserSearchDeliveryOrderCodeMessageProcessor` (+5).

### web-plugin

- **JAR kiểm tra:** `ezydelivery-sdk-0.7.7.jar`, `ezydelivery-web-plugin-0.7.7.jar`; 290 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezydelivery.service`, `org.youngmonkeys.ezydelivery.web.service`, `org.youngmonkeys.ezydelivery.pagination` (+27).
- **JAR thư viện khác:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controller/service/repository (mẫu):** `WebApiAccountCustomerCommissionController`, `WebApiEzyDeliveryCustomerController`, `WebApiPublicUserDeliveryOrderCodeController`, `WebApiTrackShipmentController`, `DeliveryOrderCodeValidator`, `DeliveryOrderFixedCostService`, `DeliveryOrderShippingRateHistoryRepository`, `DeliveryOrderShippingRateRepository`, `DeliveryOrderShippingRateService`.
- **Class cấu hình/quyền (mẫu):** `EzyDeliveryOaConfig`, `WebEzyDeliveryConfig`, `WebEzyDeliveryOaConfig`.
- **Resource trong JAR (mẫu):** `ezydelivery/ezydelivery.properties`.
- **Điểm mở rộng tiềm năng theo tên class:** `AccountingUserFormulaBeforeUpdateEventHandler`, `AccountingUserFormulaUpdatedEventHandler`, `UpdateDeliveryOrderItemEvent`, `UserDeliveryOrderCodeMessageProcessor`, `UserSearchDeliveryOrderCodeMessageProcessor`, `UserTrackShipmentMessageProcessor`, `WebAccountingUserFormulaBeforeUpdateEventHandler`, `WebAccountingUserFormulaUpdatedEventHandler`, `WebUserDeliveryOrderCodeMessageProcessor` (+2).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezydelivery/scan-delivery-order-codes` → 200; `/track-shipment` chưa có trong Freestyle. Không gọi đơn vị vận chuyển.

## Lưu ý khi tích hợp

Tách luồng chuyển trạng thái nội bộ khỏi callback của nhà cung cấp vận chuyển.

[Về chỉ mục plugin](README.md)
