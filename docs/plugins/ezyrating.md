# ezyrating

User reviews, items, and customer journeys.

- **Marketplace version on core 1.5.9:** `0.4.5`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyrating` | `org.youngmonkeys.ezyrating` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md), [ezymail](ezymail.md) |
| `web-plugin` — `web/plugins/ezyrating` | `org.youngmonkeys.ezyrating` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 48 method/URI combinations identified; representative sample:

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

**web-plugin** — 10 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyrating: /`, `dashboard: /dashboard`, `customer_journeys: /customer-journeys`, `all_ratings: /all-ratings`, `all_ratings_add: ~/all-ratings/add`, `all_ratings_details: ~/all-ratings/{id}` (+8).

- **admin-plugin – Template:** `ezyrating/all-ratings/add.html`, `ezyrating/all-ratings/details.html`, `ezyrating/all-ratings/edit.html`, `ezyrating/all-ratings/import-user-item-ratings-from-excel.html`, `ezyrating/all-ratings/list.html`, `ezyrating/all-ratings/scripts.html`, `ezyrating/customer-journeys/fragments/customer.html` (+17).

- **admin-plugin – Static resources:** `ezyrating/css/customer-journey-common.css`, `ezyrating/css/customer-journey-customer.css`, `ezyrating/css/customer-journey-funnel.css`, `ezyrating/css/customer-journey-overview.css` (+15).

- **admin-plugin – Configuration and template resources:** `ezyrating/user-item-rating-importable-fields.json`.

- **web-plugin – Template:** `ezyrating/stars.html`, `ezyrating/user-item-ratings.html`, `ezyrating/user-product-rating.html`.

- **web-plugin – Static resources:** `ezyrating/css/style.css`, `ezyrating/js/embed.js`, `ezyrating/js/main.js`.

## Data and migrations

- **Table in the DDL packaging (23):** `ezyrating_active_visitors`, `ezyrating_daily_funnel_visitors`, `ezyrating_daily_hourly_searches`, `ezyrating_daily_hourly_touchpoints`, `ezyrating_daily_hourly_visits`, `ezyrating_daily_item_statistics`, `ezyrating_daily_journey_links`, `ezyrating_daily_journey_paths`, `ezyrating_daily_journey_touchpoint_nodes`, `ezyrating_daily_journey_touchpoints`, `ezyrating_daily_statistics`, `ezyrating_daily_visitors`, `ezyrating_item_actions`, `ezyrating_item_ratings`, `ezyrating_monthly_journey_touchpoints`, `ezyrating_realtime_snapshots`, `ezyrating_user_item_action_histories`, `ezyrating_user_item_actions`, `ezyrating_user_item_rating_histories`, `ezyrating_user_item_ratings`, `ezyrating_visitor_session_steps`, `ezyrating_visitor_sessions`, `ezyrating_visitors`.
- **Class with JPA Entity/MappedSuperclass):** `ActiveVisitor`, `DailyFunnelVisitor`, `DailyHourlySearch`, `DailyHourlyTouchpoint`, `DailyHourlyVisit`, `DailyItemStatistic`, `DailyJourneyLink`, `DailyJourneyPath`, `DailyJourneyTouchpoint`, `DailyJourneyTouchpointNode`, `DailyStatistic`, `DailyVisitor`, `ItemAction`, `ItemRating`, `MonthlyJourneyTouchpoint`, `RealtimeSnapshot`, `UserItemAction`, `UserItemActionHistory` (+5).
- **SQL admin-plugin (20 files):** `resources/scripts/action.sql`, `resources/scripts/daily_item_statistics.sql`, `resources/scripts/daily_journey_hourly.sql`, `resources/scripts/daily_journey_touchpoint.sql`, `resources/scripts/journey.sql`, `resources/scripts/rating.sql`, `resources/scripts/scripts.sql` (+13).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyrating-admin-plugin-0.4.5.jar`, `ezyrating-sdk-0.4.5.jar`; 401 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyrating.admin.response`, `org.youngmonkeys.ezyrating.model`, `org.youngmonkeys.ezyrating.admin.repo` (+30).
- **Controllers, services, and repositories (sample):** `AdminApiCustomerJourneyController`, `AdminApiEzyRatingSettingController`, `AdminApiEzyRatingStatisticsController`, `AdminApiItemActionController`, `ActionStatisticsService`, `ActiveVisitorRepository`, `ActiveVisitorService`, `AdminActionStatisticsService`, `AdminActiveVisitorRepository`.
- **Configuration and permission classes (sample):** `AdminEzyRatingCustomerPortraitConfig`, `AdminEzyRatingMailConfig`, `AdminEzyRatingPageFragmentConfig`, `AdminEzyRatingPostTypeConfig`, `AdminEzyRatingTemplateConfig`, `AdminEzyRatingUserRoleConfig`, `AdminEzyRatingViewMetadataConfig` (+1).
- **Potential extension points based on class names:** `AddUserItemActionEventHandler`, `AdminAddUserItemActionEventHandler`, `AdminDataIndexSearchResultCountEventHandler`, `AdminFetchTotalActionCountMapByItemIdsEventHandler`, `AdminGetLastUserActionEventHandler`, `AdminRatingTypeManager`, `BuiltInShoppingEvent`, `GetLastUserActionEventHandler`.

### web-plugin

- **JARs inspected:** `ezyrating-sdk-0.4.5.jar`, `ezyrating-web-plugin-0.4.5.jar`; 239 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyrating.model`, `org.youngmonkeys.ezyrating.pagination`, `org.youngmonkeys.ezyrating.entity` (+23).
- **Controllers, services, and repositories (sample):** `WebApiUserItemActionController`, `WebApiUserItemActionHistoryController`, `WebApiUserItemRatingController`, `WebEzyRatingRequestControllerService`, `ActionStatisticsService`, `ActiveVisitorRepository`, `ActiveVisitorService`, `ConversionStatisticsService`, `DailyItemStatisticRepository`.
- **Configuration and permission classes (sample):** `EzyRatingPageFragmentConfig`, `WebEzyRatingPageFragmentConfig`.
- **Potential extension points based on class names:** `AddUserItemActionEventHandler`, `BuiltInShoppingEvent`, `GetLastUserActionEventHandler`, `WebAddUserItemActionEventHandler`, `WebGetLastUserActionEventHandler`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyrating/dashboard` and Web `/ezyrating/user-ratings` returned 200.

## Integration notes

See the aggregate endpoint and public display patterns. Do not reuse public review permissions for private data.

[Back to the plugin index](README.md)
