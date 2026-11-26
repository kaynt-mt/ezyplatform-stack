# ezymarketing

Advertising, campaigns, and shortened links.

- **Marketplace version on core 1.5.9:** `0.3.7`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezymarketing` | `org.youngmonkeys.ezymarketing` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md), [ezymail](ezymail.md), [ezysupport](ezysupport.md) |
| `web-plugin` — `web/plugins/ezymarketing` | `org.youngmonkeys.ezymarketing` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md), [ezymail](ezymail.md), [ezysupport](ezysupport.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 116 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingsController` |
| `GET /campaigns` | `AdminMarketingCampaignsController` |
| `GET /workflows` | `AdminMarketingWorkflowsController` |
| `GET /competitors` | `AdminDataCenterCompetitorsController` |
| `GET /shorted-urls` | `AdminShortedUrlController` |
| `GET /advertisements` | `AdminAdvertisementsController` |
| `GET /marketing-costs` | `AdminMarketingCostsController` |
| `POST /api/v1/campaigns/add` | `AdminApiMarketingCampaignController` |
| `POST /api/v1/workflows/add` | `AdminApiMarketingWorkflowController` |
| `POST /api/v1/shorted-urls/add` | `AdminApiShortedUrlController` |
| `POST /api/v1/workflow-runs/add` | `AdminApiMarketingWorkflowRunController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/marketing-costs` | `AdminApiMarketingCostController` |
| `PUT /api/v1/marketing-strategy` | `AdminApiMarketingStrategyController` |
| `PUT /api/v1/settings/marketing-workflow-executor/stop` | `AdminApiSettingController` |
| `DELETE /api/v1/campaigns/{id}` | `AdminApiMarketingCampaignController` |
| `DELETE /api/v1/workflows/{id}` | `AdminApiMarketingWorkflowController` |
| `DELETE /api/v1/shorted-urls/{id}` | `AdminApiShortedUrlController` |
| `DELETE /api/v1/advertisements/{id}` | `AdminApiAdvertisementController` |

**web-plugin** — 8 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /ezymarketing/advertisements/embed` | `WebAdvertisementController` |
| `GET /ezymarketing/api/v1/advertisements` | `WebApiAdvertisementController` |
| `GET /ezymarketing/api/v1/advertisements/popup` | `WebApiAdvertisementController` |
| `GET /ezymarketing/api/v1/advertisements/settings` | `WebApiAdvertisementController` |
| `GET /shorted/{uri}` | `WebShortedUrlController` |
| `GET /advertisements/{id}/click` | `WebAdvertisementController` |
| `GET /ezymarketing/api/v1/advertisements/positions/{position}` | `WebApiAdvertisementController` |
| `POST /ezymarketing/api/v1/conversion-events/add` | `WebApiMarketingConversionEventController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezymarketing: /`, `advertisements: /advertisements`, `shorted_urls: /shorted-urls`, `shorted_urls_add: ~/shorted-urls/add`, `shorted_urls_edit: ~/shorted-urls/{id}/edit`, `campaigns: /campaigns` (+30).

- **admin-plugin – Template:** `ezymarketing/advertisement/add.html`, `ezymarketing/advertisement/cost.html`, `ezymarketing/advertisement/details.html`, `ezymarketing/advertisement/edit.html`, `ezymarketing/advertisement/list.html`, `ezymarketing/advertisement/platform-statistic.html`, `ezymarketing/advertisement/scripts.html` (+53).

- **admin-plugin – Static resources:** `ezymarketing/css/marketing-cost.css`, `ezymarketing/js/marketing-cost.js`.

- **admin-plugin – Configuration and template resources:** `participant-fetching-script/fetch_all_users.properties`, `participant-fetching-script/fetch_only_me.properties`, `participant-fetching-script/fetch_users_bought_any_product.properties`, `participant-fetching-script/fetch_users_bought_product_by_category_name.properties` (+17).

- **web-plugin – Template:** `ezymarketing/advertisement/embed.html`, `ezymarketing/personalized-feed/index.html`, `ezymarketing/shorted-url/redirection.html`.

- **web-plugin – Static resources:** `ezymarketing/css/ads-layout.css`, `ezymarketing/css/ads.css`, `ezymarketing/css/style.css`, `ezymarketing/js/embed.js` (+1).

## Data and migrations

- **Table in the DDL packaging (19):** `ezymarketing_advertisements`, `ezymarketing_campaign_participant_segments`, `ezymarketing_campaigns`, `ezymarketing_conversion_events`, `ezymarketing_conversion_types`, `ezymarketing_cost_rates`, `ezymarketing_daily_costs`, `ezymarketing_daily_statistics`, `ezymarketing_participant_segment_participants`, `ezymarketing_participant_segments`, `ezymarketing_shorted_urls`, `ezymarketing_workflow_participant_step_logs`, `ezymarketing_workflow_participants`, `ezymarketing_workflow_run_participant_segment_participants`, `ezymarketing_workflow_runs`, `ezymarketing_workflow_statistics`, `ezymarketing_workflow_steps`, `ezymarketing_workflow_triggers`, `ezymarketing_workflows`.
- **Class with JPA Entity/MappedSuperclass):** `Advertisement`, `MarketingCampaign`, `MarketingCampaignParticipantSegment`, `MarketingConversionEvent`, `MarketingConversionType`, `MarketingCostRate`, `MarketingDailyCost`, `MarketingDailyStatistic`, `MarketingParticipantSegment`, `MarketingParticipantSegmentParticipant`, `MarketingWorkflow`, `MarketingWorkflowParticipant`, `MarketingWorkflowParticipantStepLog`, `MarketingWorkflowRun`, `MarketingWorkflowRunParticipantSegmentParticipant`, `MarketingWorkflowStatistic`, `MarketingWorkflowStep`, `MarketingWorkflowTrigger` (+1).
- **SQL admin-plugin (17 files):** `resources/scripts/follow-up-workflow.sql`, `resources/scripts/marketing-cost.sql`, `resources/scripts/scripts.sql`, `resources/scripts/shorted-url.sql`, `resources/scripts/workflow-run-participant-segment-participant.sql`, `resources/scripts/workflow.sql`, `resources/scripts/alter-advertisement-index.sql` (+10).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezymarketing-admin-plugin-0.3.7.jar`, `ezymarketing-sdk-0.3.7.jar`; 613 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezymarketing.pagination`, `org.youngmonkeys.ezymarketing.entity`, `org.youngmonkeys.ezymarketing.admin.repo` (+34).
- **Controllers, services, and repositories (sample):** `AdminAdvertisementControllerService`, `AdminAdvertisementsController`, `AdminApiAdvertisementController`, `AdminApiAdvertisementCostController`, `AdminAdvertisementContractService`, `AdminAdvertisementControllerService`, `AdminAdvertisementCostValidator`, `AdminAdvertisementPlatformStatisticValidator`, `AdminAdvertisementRepository`.
- **Configuration and permission classes (sample):** `AdminEzyMarketingConversionTypeConfig`, `AdminEzyMarketingCustomerPortraitConfig`, `AdminEzyMarketingDataAppenderConfig`, `AdminEzyMarketingParticipantFetchingScriptTemplateConfig`, `AdminEzyMarketingPostTypeConfig`, `AdminEzyMarketingViewMetadataConfig`.
- **Configuration and template keys from resources (values omitted):** `content`, `contentType`, `title`.
- **Potential extension points based on class names:** `AddConversionEventEventHandler`, `AdminAbandonedCartFollowUpTriggerProvider`, `AdminAbstractMarketingPersonalizedContentCandidateProvider`, `AdminAbstractMarketingProductPersonalizedContentCandidateProvider`, `AdminAbstractMarketingUpsellProductPersonalizedContentCandidateProvider`, `AdminAddConversionEventEventHandler`, `AdminCreateShortedUrlEventHandler`, `AdminErpContractChargeAddedEventHandler`, `AdminErpContractStatusChangedEventHandler` (+53).

### web-plugin

- **JARs inspected:** `ezymarketing-sdk-0.3.7.jar`, `ezymarketing-web-plugin-0.3.7.jar`; 355 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezymarketing.pagination`, `org.youngmonkeys.ezymarketing.entity`, `org.youngmonkeys.ezymarketing.model` (+25).
- **Controllers, services, and repositories (sample):** `WebAdvertisementController`, `WebAdvertisementControllerService`, `WebApiAdvertisementController`, `WebApiMarketingConversionEventController`, `AdvertisementRepository`, `AdvertisementService`, `EzyMarketingSettingService`, `MarketingCampaignParticipantSegmentRepository`, `MarketingCampaignParticipantSegmentService`.
- **Potential extension points based on class names:** `AddConversionEventEventHandler`, `CreateShortedUrlEventHandler`, `FollowUpEnrollPolicyManager`, `FollowUpExitConditionManager`, `FollowUpStepInputDecoratorManager`, `FollowUpTriggerEvent`, `FollowUpTriggerProvider`, `FollowUpTriggerProviderManager`, `MarketingCampaignParticipantSegmentStatusManager` (+16).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezymarketing/advertisements` and Web `/ezymarketing/api/v1/advertisements` returned 200.

## Integration notes

See how links are identified and tracked. Do not add tracking codes to private URLs by default.

[Back to the plugin index](README.md)
