# ecommerce

Catalog, stores, shopping carts, orders, and checkout.

- **Marketplace version on core 1.5.9:** `1.5.8`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ecommerce` | `org.youngmonkeys.ecommerce` | Not declared |
| `web-plugin` — `web/plugins/ecommerce` | `org.youngmonkeys.ecommerce` | Not declared |
| `socket-plugin` — `socket/plugins/ecommerce` | `org.youngmonkeys.ecommerce` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 413 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /banks` | `AdminBankController` |
| `GET /shops` | `AdminShopController` |
| `GET /tools` | `AdminEcommerceToolsController` |
| `GET /orders` | `AdminOrderController` |
| `GET /sellers` | `AdminShopSellerController` |
| `GET /agencies` | `AdminShopAgencyController` |
| `GET /products` | `AdminProductController` |
| `POST /api/v1/qr-code` | `AdminApiQrCodeController` |
| `POST /api/v1/banks/add` | `AdminApiBankController` |
| `POST /api/v1/shops/add` | `AdminApiShopController` |
| `POST /api/v1/products/add` | `AdminApiProductController` |
| `PUT /api/v1/settings` | `AdminApiEcommerceSettingController` |
| `PUT /api/v1/products/draft` | `AdminApiProductController` |
| `PUT /api/v1/products/prices` | `AdminApiProductController` |
| `PUT /api/v1/products/archive` | `AdminApiProductController` |
| `DELETE /api/v1/products` | `AdminApiProductController` |
| `DELETE /api/v1/product-tags` | `AdminApiProductTagController` |
| `DELETE /api/v1/shop-agencies` | `AdminApiShopAgencyController` |
| `DELETE /api/v1/banks/{id}` | `AdminApiBankController` |

**web-plugin** — 85 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /orders` | `WebApiOrderController` |
| `GET /products` | `WebApiProductController` |
| `GET /referral` | `WebAffiliateController` |
| `GET /affiliate` | `WebAffiliateController` |
| `GET /countries` | `WebApiCountryController` |
| `GET /commission` | `WebCommissionController` |
| `GET /shopping-cart` | `WebApiShoppingCartController` |
| `POST /qr-code` | `WebApiQrCodeController` |
| `POST /checkout` | `WebApiCheckoutController` |
| `POST /orders/create` | `WebApiOrderController` |
| `POST /products/checkout` | `WebApiProductCheckoutController` |
| `PUT /orders/{id}/waiting-to-confirm` | `WebApiOrderController` |
| `PUT /checkout/shopping-cart-products/{id}` | `WebApiCheckoutController` |
| `PUT /orders/{id}/waiting-to-confirm-in-duration` | `WebApiOrderController` |
| `DELETE /checkout/shopping-cart-products/{id}` | `WebApiCheckoutController` |
| `DELETE /checkout/shopping-carts/{shoppingCartId}/products/{productId}` | `WebApiCheckoutController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ecommerce: /`, `orders: /orders`, `orders_create: ~/orders/create`, `orders_details: ~/orders/{id}`, `orders_edit: ~/orders/{id}/edit`, `orders_history_details: ~/orders/{id}/histories/{historyId}` (+76).

- **admin-plugin – Template:** `ecommerce/affiliate-token/add-target.html`, `ecommerce/affiliate-token/add.html`, `ecommerce/affiliate-token/details.html`, `ecommerce/affiliate-token/edit.html`, `ecommerce/affiliate-token/list.html`, `ecommerce/affiliate-token/scripts.html`, `ecommerce/affiliate-token/target-list.html` (+197).

- **admin-plugin – Static resources:** `ecommerce/css/style.css`, `ecommerce/editors/text.js`, `ecommerce/js/JsBarcode.all.min.js`, `ecommerce/js/html2canvas.min.js` (+3).

- **admin-plugin – Configuration and template resources:** `ecommerce/currencies.properties`, `ecommerce/letter_template_new_orders_for_managers.properties`, `ecommerce/letter_template_order_approved.properties`, `ecommerce/letter_template_order_created.properties` (+19).

- **web-plugin – Template:** `checkout/shopping-cart-empty.html`, `checkout/shopping-cart.html`, `ecommerce/address/scripts.html`, `ecommerce/affiliate/affiliate-token-details.html`, `ecommerce/affiliate/affiliate-token-list.html`, `ecommerce/affiliate/affiliate.html`, `ecommerce/affiliate/voucher-details.html` (+13).

- **web-plugin – Static resources:** `ecommerce/css/style.css`, `ecommerce/js/main.js`, `ecommerce/js/qrcode.min.js`.

## Data and migrations

- **Table in DDL packaging (98):** `ecommerce_administrative_units`, `ecommerce_affiliate_token_targets`, `ecommerce_affiliate_token_usage_histories`, `ecommerce_affiliate_token_usages`, `ecommerce_affiliate_token_user_usages`, `ecommerce_affiliate_tokens`, `ecommerce_banks`, `ecommerce_countries`, `ecommerce_deliverable_products`, `ecommerce_delivery_order_histories`, `ecommerce_delivery_order_products`, `ecommerce_delivery_orders`, `ecommerce_delivery_service_settings`, `ecommerce_districts`, `ecommerce_exchange_rates`, `ecommerce_invoice_orders`, `ecommerce_invoice_products`, `ecommerce_nearby_districts`, `ecommerce_order_histories`, `ecommerce_order_product_children`, `ecommerce_order_products`, `ecommerce_order_recipients`, `ecommerce_orders`, `ecommerce_payment_histories`, `ecommerce_payment_service_settings`, `ecommerce_process_delivery_orders`, `ecommerce_product_bonuses`, `ecommerce_product_books`, `ecommerce_product_categories`, `ecommerce_product_categories_i18n`, `ecommerce_product_category_medias`, `ecommerce_product_category_parents`, `ecommerce_product_category_product_medias`, `ecommerce_product_category_products`, `ecommerce_product_color_medias`, `ecommerce_product_colors`, `ecommerce_product_currencies`, `ecommerce_product_descriptions`, `ecommerce_product_descriptions_i18n`, `ecommerce_product_histories`, `ecommerce_product_import_price_histories`, `ecommerce_product_material_medias`, `ecommerce_product_materials`, `ecommerce_product_medias`, `ecommerce_product_meta`, `ecommerce_product_package_histories`, `ecommerce_product_package_products`, `ecommerce_product_packages`, `ecommerce_product_price_histories`, `ecommerce_product_prices`, `ecommerce_product_size_color_price_histories`, `ecommerce_product_size_color_prices`, `ecommerce_product_size_color_quantities`, `ecommerce_product_sizes`, `ecommerce_product_tag_products`, `ecommerce_product_tags`, `ecommerce_products`, `ecommerce_provinces`, `ecommerce_set_products`, `ecommerce_shop_agencies`, `ecommerce_shop_agency_members`, `ecommerce_shop_agency_products`, `ecommerce_shop_bank_accounts`, `ecommerce_shop_branch_details`, `ecommerce_shop_branches`, `ecommerce_shop_commission_rate_histories`, `ecommerce_shop_commission_rates`, `ecommerce_shop_details`, `ecommerce_shop_product_colors`, `ecommerce_shop_product_materials`, `ecommerce_shop_product_price_list_histories`, `ecommerce_shop_product_price_list_product_prices`, `ecommerce_shop_product_price_list_products`, `ecommerce_shop_product_price_list_targets`, `ecommerce_shop_product_price_lists`, `ecommerce_shop_seller_commission_histories`, `ecommerce_shop_seller_customer_commissions`, `ecommerce_shop_seller_customers`, `ecommerce_shop_seller_monthly_commissions`, `ecommerce_shop_sellers`, `ecommerce_shop_tax_setting_histories`, `ecommerce_shop_tax_settings`, `ecommerce_shop_warehouse_products`, `ecommerce_shop_warehouses`, `ecommerce_shopping_cart_products`, `ecommerce_shopping_carts`, `ecommerce_shops`, `ecommerce_upsell_products`, `ecommerce_user_balance_histories`, `ecommerce_user_balances`, `ecommerce_user_order_statuses`, `ecommerce_voucher_targets`, `ecommerce_voucher_usage_histories`, `ecommerce_voucher_usages`, `ecommerce_voucher_user_usages`, `ecommerce_vouchers`, `ecommerce_wards`, `ecommerce_warehouse_product_operation_histories`.
- **Class with JPA Entity/MappedSuperclass (98 ):** `AdministrativeUnit`, `AffiliateToken`, `AffiliateTokenTarget`, `AffiliateTokenUsage`, `AffiliateTokenUsageHistory`, `AffiliateTokenUserUsage`, `Bank`, `Country`, `DeliverableProduct`, `DeliveryOrder`, `DeliveryOrderHistory`, `DeliveryOrderProduct`, `DeliveryServiceSetting`, `District`, `ExchangeRate`, `InvoiceOrder`, `InvoiceProduct`, `NearbyDistrict` (+80).
- **SQL admin-plugin (141 files):** `resources/scripts/administrative.sql`, `resources/scripts/affiliate.sql`, `resources/scripts/delivery.sql`, `resources/scripts/description.sql`, `resources/scripts/invoice_order.sql`, `resources/scripts/invoice_product.sql`, `resources/scripts/product-categories-i18n.sql` (+134).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ecommerce-admin-plugin-1.5.8.jar`, `ecommerce-sdk-1.5.8.jar`; 2166 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ecommerce.pagination`, `org.youngmonkeys.ecommerce.entity`, `org.youngmonkeys.ecommerce.model` (+39).
- **Other library JARs:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controllers, services, and repositories (sample):** `AdminAdministrativeUnitControllerService`, `AdminAffiliateTokenController`, `AdminAffiliateTokenControllerService`, `AdminAffiliateTokenTargetControllerService`, `AddressService`, `AdminAbstractViettelPostCountryFetcher`, `AdminAddressService`, `AdminAdministrativeUnitControllerService`, `AdminAdministrativeUnitRepository`.
- **Configuration and permission classes (sample):** `AdminEcommerceAdminRoleConfig`, `AdminEcommerceConfig`, `AdminEcommerceDataAppenderConfig`, `AdminEcommerceInvoiceGenerationScriptConfig`, `AdminEcommerceLetterConfig`, `AdminEcommerceMailConfig`, `AdminEcommerceNotificationConfig` (+10).
- **Configuration and template keys from resources (values omitted):** `CNY`, `EUR`, `INR`, `JPY`, `KRW` (+4).
- **JAR resources (sample):** `ecommerce/ecommerce.properties`.
- **Potential extension points based on class names:** `AdminAdministrativeUnitTypeManager`, `AdminAffiliateTokenTypeManager`, `AdminBanksFetcherManager`, `AdminCountryFetcherManager`, `AdminCreateProductEventHandler`, `AdminDeliveryOptionManager`, `AdminDeliveryOrderProcessor`, `AdminDeliveryOrderStatusManager`, `AdminDeliveryOrderTypeManager` (+86).

### web-plugin

- **JARs inspected:** `ecommerce-sdk-1.5.8.jar`, `ecommerce-web-plugin-1.5.8.jar`; 1846 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ecommerce.pagination`, `org.youngmonkeys.ecommerce.entity`, `org.youngmonkeys.ecommerce.model` (+36).
- **Other library JARs:** `core-3.5.3.jar`, `jai-imageio-core-1.4.0.jar`, `javase-3.5.3.jar`, `jcommander-1.82.jar`.
- **Controllers, services, and repositories (sample):** `AffiliateTokenControllerService`, `ApiInvoiceController`, `ApiQrCodeController`, `InvoiceControllerService`, `AddressService`, `AdministrativeUnitRepository`, `AdministrativeUnitService`, `AffiliateTokenControllerService`, `AffiliateTokenRepository`.
- **Configuration and permission classes (sample):** `DeliveryOption`, `DeliveryServiceSetting`, `EcommercePageFragmentConfig`, `PaymentServiceSetting`, `ShopTaxSetting`, `WebEcommerceConfig`, `WebEcommercePageFragmentConfig`.
- **JAR resources (sample):** `ecommerce/ecommerce.properties`.
- **Potential extension points based on class names:** `AdministrativeUnitTypeManager`, `AffiliateTokenTypeManager`, `BanksFetcherManager`, `CountryFetcherManager`, `CreateProductEventHandler`, `DeliveryOptionManager`, `DeliveryOrderStatusManager`, `DeliveryOrderTypeManager`, `DeliveryServiceManager` (+59).

### socket-plugin

- **JARs inspected:** `ecommerce-sdk-1.5.8.jar`, `ecommerce-socket-plugin-1.5.8.jar`; 1304 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ecommerce.pagination`, `org.youngmonkeys.ecommerce.entity`, `org.youngmonkeys.ecommerce.model` (+19).
- **Controllers, services, and repositories (sample):** `AffiliateTokenControllerService`, `ApiInvoiceController`, `ApiQrCodeController`, `InvoiceControllerService`, `AddressService`, `AdministrativeUnitRepository`, `AdministrativeUnitService`, `AffiliateTokenControllerService`, `AffiliateTokenRepository`.
- **Configuration and permission classes (sample):** `DeliveryOption`, `DeliveryServiceSetting`, `EcommercePageFragmentConfig`, `PaymentServiceSetting`, `ShopTaxSetting`.
- **JAR resources (sample):** `ecommerce/ecommerce.properties`.
- **Potential extension points based on class names:** `AdministrativeUnitTypeManager`, `AffiliateTokenTypeManager`, `BanksFetcherManager`, `CountryFetcherManager`, `CreateProductEventHandler`, `DeliveryOptionManager`, `DeliveryOrderStatusManager`, `DeliveryOrderTypeManager`, `DeliveryServiceManager` (+33).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ecommerce.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `ApiInvoiceController`, `ApiQrCodeController`, `InvoiceModelDecorator`, `ProductModelDecorator`, `ShopBankAccountModelDecorator`, `ShopBranchModelDecorator`, `ShopSellerMonthlyCommissionDecorator`, `UserBalanceModelDecorator`, `AffiliateTokenControllerService`, `InvoiceControllerService` (+97).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ecommerce/orders`, `/ecommerce/products` → 200; the Web page `/products` is not available in Freestyle. No real orders or payments were tested.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Orders illustrate business identifiers, filtering and pagination, and state transitions. Add the Ecommerce dependency only if the application needs this module's behavior.

[Back to the plugin index](README.md)
