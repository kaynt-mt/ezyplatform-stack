# ezydelivery

Shipment codes, barcode scanning, and delivery.

- **Marketplace version on core 1.5.9:** `0.7.7`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezydelivery` | `org.youngmonkeys.ezydelivery` | [ecommerce](ecommerce.md), [accounting](accounting.md), [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezydelivery` | `org.youngmonkeys.ezydelivery` | [ecommerce](ecommerce.md), [accounting](accounting.md), [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 150 method/URI combinations identified; representative sample:

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

**web-plugin** — 14 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezydelivery: /`, `scan_order_code: /scan-delivery-order-codes`, `declare_order_code: /delivery-order-codes`, `rejected_delivery_order_codes: /rejected-delivery-order-codes`, `photo_required_delivery_order_codes: /photo-required-delivery-order-codes`, `sensitive_delivery_order_codes: /sensitive-delivery-order-codes` (+32).

- **admin-plugin – Template:** `ezydelivery/accounting/overview/user-delivery-order-item.html`, `ezydelivery/all-delivery-order-code/delivery-order-history-list.html`, `ezydelivery/all-delivery-order-code/delivery-order-list.html`, `ezydelivery/all-delivery-order-code/details.html`, `ezydelivery/all-delivery-order-code/list.html`, `ezydelivery/allocate-delivery-order-code-customer/customer-details.html`, `ezydelivery/allocate-delivery-order-code-customer/customer-list.html` (+102).

- **admin-plugin – Configuration and template resources:** `administrative-type-prefix-mapping-templates/ghtk.json`, `administrative-type-prefix-mapping-templates/spx.json`, `administrative-type-prefix-mapping-templates/viettel_post.json`, `administrative-type-prefix-mapping-templates/viettel_post_small.json` (+10).

## Data and migrations

- **Table in the DDL packaging (8):** `ezydelivery_delivery_order_shipping_rate_histories`, `ezydelivery_delivery_order_shipping_rates`, `ezydelivery_shop_vehicle_histories`, `ezydelivery_shop_vehicle_product_packages`, `ezydelivery_shop_vehicles`, `ezydelivery_user_shipping_rate_histories`, `ezydelivery_user_shipping_rates`, `ezydelivery_user_shipping_requests`.
- **Class with JPA Entity/MappedSuperclass indication (8):** `DeliveryOrderShippingRate`, `DeliveryOrderShippingRateHistory`, `ShopVehicle`, `ShopVehicleHistory`, `ShopVehicleProductPackage`, `UserShippingRate`, `UserShippingRateHistory`, `UserShippingRequest`.
- **SQL admin-plugin (13 files):** `resources/scripts/scripts.sql`, `resources/scripts/shop_vehicle_history.sql`, `resources/scripts/user_shipping_rates.sql`, `resources/scripts/user_shipping_requests.sql`, `resources/scripts/alter_add_detailed_status.sql`, `resources/scripts/alter_delivery_order_table_100.sql`, `resources/scripts/alter_ezyplatform_user_add_username_status_index.sql` (+6).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezydelivery-admin-plugin-0.7.7.jar`, `ezydelivery-sdk-0.7.7.jar`; 459 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezydelivery.admin.response`, `org.youngmonkeys.ezydelivery.admin.service`, `org.youngmonkeys.ezydelivery.service` (+34).
- **Other library JARs:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiCustomerDeliveryOrderCodeController`, `AdminApiDeliveryOrderCodeController`, `AdminApiDeliveryOrderShippingRateController`, `AdminApiEzyDeliveryCustomerController`, `AdminCustomerDeliveryOrderControllerService`, `AdminDeliveryOrderCodeValidator`, `AdminDeliveryOrderFixedCostService`, `AdminDeliveryOrderShippingRateControllerService`, `AdminDeliveryOrderShippingRateHistoryRepository`.
- **Configuration and permission classes (sample):** `AdminAdministrativeTypeNameMappingTemplateConfig`, `AdminEzyDeliveryConfig`, `AdminEzyDeliveryDataAppenderConfig`, `AdminEzyDeliveryOAResponseMessageTemplateConfig`, `AdminEzyDeliveryOaConfig`, `AdminEzyDeliveryUserRoleConfig`, `AdminEzyDeliveryViewMetadataConfig` (+1).
- **Configuration and template keys from resources (values omitted):** `content`, `contentType`, `title`.
- **JAR resources (sample):** `ezydelivery/ezydelivery.properties`.
- **Potential extension points based on class names:** `AccountingUserFormulaBeforeUpdateEventHandler`, `AccountingUserFormulaUpdatedEventHandler`, `AdminAccountingUserFormulaBeforeUpdateEventHandler`, `AdminAccountingUserFormulaUpdatedEventHandler`, `AdminEzyDeliveryCargoTypeManager`, `AdminShopVehicleStatusManager`, `AdminShopVehicleTypeManager`, `AdminUserDeliveryOrderCodeMessageProcessor`, `AdminUserSearchDeliveryOrderCodeMessageProcessor` (+5).

### web-plugin

- **JARs inspected:** `ezydelivery-sdk-0.7.7.jar`, `ezydelivery-web-plugin-0.7.7.jar`; 290 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezydelivery.service`, `org.youngmonkeys.ezydelivery.web.service`, `org.youngmonkeys.ezydelivery.pagination` (+27).
- **Other library JARs:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controllers, services, and repositories (sample):** `WebApiAccountCustomerCommissionController`, `WebApiEzyDeliveryCustomerController`, `WebApiPublicUserDeliveryOrderCodeController`, `WebApiTrackShipmentController`, `DeliveryOrderCodeValidator`, `DeliveryOrderFixedCostService`, `DeliveryOrderShippingRateHistoryRepository`, `DeliveryOrderShippingRateRepository`, `DeliveryOrderShippingRateService`.
- **Configuration and permission classes (sample):** `EzyDeliveryOaConfig`, `WebEzyDeliveryConfig`, `WebEzyDeliveryOaConfig`.
- **JAR resources (sample):** `ezydelivery/ezydelivery.properties`.
- **Potential extension points based on class names:** `AccountingUserFormulaBeforeUpdateEventHandler`, `AccountingUserFormulaUpdatedEventHandler`, `UpdateDeliveryOrderItemEvent`, `UserDeliveryOrderCodeMessageProcessor`, `UserSearchDeliveryOrderCodeMessageProcessor`, `UserTrackShipmentMessageProcessor`, `WebAccountingUserFormulaBeforeUpdateEventHandler`, `WebAccountingUserFormulaUpdatedEventHandler`, `WebUserDeliveryOrderCodeMessageProcessor` (+2).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezydelivery/scan-delivery-order-codes` returned 200. `/track-shipment` was not available in Freestyle. No carrier was called.

## Integration notes

Keep internal state transitions separate from carrier callbacks.

[Back to the plugin index](README.md)
