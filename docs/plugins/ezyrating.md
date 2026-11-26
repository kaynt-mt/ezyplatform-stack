# ezyrating

Đánh giá người dùng, mục và hành trình khách hàng.

- **Bản Marketplace trên core 1.5.9:** `0.4.5`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyrating` | `org.youngmonkeys.ezyrating` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezyrating` | `org.youngmonkeys.ezyrating` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 48 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyRatingSettingController` |
| `GET /dashboard` | `AdminEzyRatingDashboardController` |
| `GET /all-ratings` | `AdminUserItemRatingController` |
| `GET /item-actions` | `AdminItemActionController` |
| `GET /summary-ratings` | `AdminItemRatingController` |
| `GET /customer-journeys` | `AdminCustomerJourneyController` |
| `GET /user-item-actions` | `AdminUserItemActionController` |
| `POST /api/v1/user-item-ratings/add` | `AdminApiUserItemRatingController` |
| `PUT /api/v1/settings` | `AdminApiEzyRatingSettingController` |
| `PUT /api/v1/customer-journeys/shopping-seasons/settings` | `AdminApiShoppingSeasonController` |
| `PUT /api/v1/user-item-ratings/{id}` | `AdminApiUserItemRatingController` |
| `DELETE /api/v1/user-item-ratings` | `AdminApiUserItemRatingController` |
| `DELETE /api/v1/user-item-ratings/{userItemRatingId}` | `AdminApiUserItemRatingController` |

**web-plugin** — 10 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /ezyrating/user-ratings` | `WebUserItemRatingController` |
| `GET /api/v1/user-item-actions` | `WebApiUserItemActionController` |
| `GET /api/v1/user-item-ratings` | `WebApiUserItemRatingController` |
| `GET /ezyrating/user-ratings/products/{productCode}` | `WebUserItemRatingController` |
| `GET /api/v1/user-item-ratings/{itemType}/{itemId}/{ratingType}/rated-point` | `WebApiUserItemRatingController` |
| `POST /api/v1/user-item-ratings/add` | `WebApiUserItemRatingController` |
| `POST /api/v1/user-item-ratings/save` | `WebApiUserItemRatingController` |
| `POST /api/v1/user-item-ratings/toggle` | `WebApiUserItemRatingController` |
| `POST /ezyrating/api/v1/user-item-actions/add` | `WebApiUserItemActionHistoryController` |
| `DELETE /api/v1/user-item-ratings` | `WebApiUserItemRatingController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyrating: /`, `dashboard: /dashboard`, `customer_journeys: /customer-journeys`, `all_ratings: /all-ratings`, `all_ratings_add: ~/all-ratings/add`, `all_ratings_details: ~/all-ratings/{id}` (+8).

- **admin-plugin – Template:** `ezyrating/all-ratings/add.html`, `ezyrating/all-ratings/details.html`, `ezyrating/all-ratings/edit.html`, `ezyrating/all-ratings/import-user-item-ratings-from-excel.html`, `ezyrating/all-ratings/list.html`, `ezyrating/all-ratings/scripts.html`, `ezyrating/customer-journeys/fragments/customer.html` (+17).

- **admin-plugin – Tài nguyên tĩnh:** `ezyrating/css/customer-journey-common.css`, `ezyrating/css/customer-journey-customer.css`, `ezyrating/css/customer-journey-funnel.css`, `ezyrating/css/customer-journey-overview.css` (+15).

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `ezyrating/user-item-rating-importable-fields.json`.

- **web-plugin – Template:** `ezyrating/stars.html`, `ezyrating/user-item-ratings.html`, `ezyrating/user-product-rating.html`.

- **web-plugin – Tài nguyên tĩnh:** `ezyrating/css/style.css`, `ezyrating/js/embed.js`, `ezyrating/js/main.js`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (23):** `ezyrating_active_visitors`, `ezyrating_daily_funnel_visitors`, `ezyrating_daily_hourly_searches`, `ezyrating_daily_hourly_touchpoints`, `ezyrating_daily_hourly_visits`, `ezyrating_daily_item_statistics`, `ezyrating_daily_journey_links`, `ezyrating_daily_journey_paths`, `ezyrating_daily_journey_touchpoint_nodes`, `ezyrating_daily_journey_touchpoints`, `ezyrating_daily_statistics`, `ezyrating_daily_visitors`, `ezyrating_item_actions`, `ezyrating_item_ratings`, `ezyrating_monthly_journey_touchpoints`, `ezyrating_realtime_snapshots`, `ezyrating_user_item_action_histories`, `ezyrating_user_item_actions`, `ezyrating_user_item_rating_histories`, `ezyrating_user_item_ratings`, `ezyrating_visitor_session_steps`, `ezyrating_visitor_sessions`, `ezyrating_visitors`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (23):** `ActiveVisitor`, `DailyFunnelVisitor`, `DailyHourlySearch`, `DailyHourlyTouchpoint`, `DailyHourlyVisit`, `DailyItemStatistic`, `DailyJourneyLink`, `DailyJourneyPath`, `DailyJourneyTouchpoint`, `DailyJourneyTouchpointNode`, `DailyStatistic`, `DailyVisitor`, `ItemAction`, `ItemRating`, `MonthlyJourneyTouchpoint`, `RealtimeSnapshot`, `UserItemAction`, `UserItemActionHistory` (+5).
- **SQL admin-plugin (20 tệp):** `resources/scripts/action.sql`, `resources/scripts/daily_item_statistics.sql`, `resources/scripts/daily_journey_hourly.sql`, `resources/scripts/daily_journey_touchpoint.sql`, `resources/scripts/journey.sql`, `resources/scripts/rating.sql`, `resources/scripts/scripts.sql` (+13).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyrating-admin-plugin-0.4.5.jar`, `ezyrating-sdk-0.4.5.jar`; 401 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyrating.admin.response`, `org.youngmonkeys.ezyrating.model`, `org.youngmonkeys.ezyrating.admin.repo` (+30).
- **Controller/service/repository (mẫu):** `AdminApiCustomerJourneyController`, `AdminApiEzyRatingSettingController`, `AdminApiEzyRatingStatisticsController`, `AdminApiItemActionController`, `ActionStatisticsService`, `ActiveVisitorRepository`, `ActiveVisitorService`, `AdminActionStatisticsService`, `AdminActiveVisitorRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyRatingCustomerPortraitConfig`, `AdminEzyRatingMailConfig`, `AdminEzyRatingPageFragmentConfig`, `AdminEzyRatingPostTypeConfig`, `AdminEzyRatingTemplateConfig`, `AdminEzyRatingUserRoleConfig`, `AdminEzyRatingViewMetadataConfig` (+1).
- **Điểm mở rộng tiềm năng theo tên class:** `AddUserItemActionEventHandler`, `AdminAddUserItemActionEventHandler`, `AdminDataIndexSearchResultCountEventHandler`, `AdminFetchTotalActionCountMapByItemIdsEventHandler`, `AdminGetLastUserActionEventHandler`, `AdminRatingTypeManager`, `BuiltInShoppingEvent`, `GetLastUserActionEventHandler`.

### web-plugin

- **JAR kiểm tra:** `ezyrating-sdk-0.4.5.jar`, `ezyrating-web-plugin-0.4.5.jar`; 239 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyrating.model`, `org.youngmonkeys.ezyrating.pagination`, `org.youngmonkeys.ezyrating.entity` (+23).
- **Controller/service/repository (mẫu):** `WebApiUserItemActionController`, `WebApiUserItemActionHistoryController`, `WebApiUserItemRatingController`, `WebEzyRatingRequestControllerService`, `ActionStatisticsService`, `ActiveVisitorRepository`, `ActiveVisitorService`, `ConversionStatisticsService`, `DailyItemStatisticRepository`.
- **Class cấu hình/quyền (mẫu):** `EzyRatingPageFragmentConfig`, `WebEzyRatingPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AddUserItemActionEventHandler`, `BuiltInShoppingEvent`, `GetLastUserActionEventHandler`, `WebAddUserItemActionEventHandler`, `WebGetLastUserActionEventHandler`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyrating/dashboard` và Web `/ezyrating/user-ratings` → 200.

## Lưu ý khi tích hợp

Mẫu endpoint tổng hợp và hiển thị công khai; không áp nguyên quyền của trang đánh giá cho dữ liệu riêng tư.

[Về chỉ mục plugin](README.md)
