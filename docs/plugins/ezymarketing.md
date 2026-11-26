# ezymarketing

Quảng cáo, chiến dịch và liên kết rút gọn.

- **Bản Marketplace trên core 1.5.9:** `0.3.7`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezymarketing` | `org.youngmonkeys.ezymarketing` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md), [ezymail](ezymail.md), [ezysupport](ezysupport.md) |
| `web-plugin` — `web/plugins/ezymarketing` | `org.youngmonkeys.ezymarketing` | [ecommerce](ecommerce.md), [ezyarticle](ezyarticle.md), [ezymail](ezymail.md), [ezysupport](ezysupport.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 116 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

**web-plugin** — 8 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezymarketing: /`, `advertisements: /advertisements`, `shorted_urls: /shorted-urls`, `shorted_urls_add: ~/shorted-urls/add`, `shorted_urls_edit: ~/shorted-urls/{id}/edit`, `campaigns: /campaigns` (+30).

- **admin-plugin – Template:** `ezymarketing/advertisement/add.html`, `ezymarketing/advertisement/cost.html`, `ezymarketing/advertisement/details.html`, `ezymarketing/advertisement/edit.html`, `ezymarketing/advertisement/list.html`, `ezymarketing/advertisement/platform-statistic.html`, `ezymarketing/advertisement/scripts.html` (+53).

- **admin-plugin – Tài nguyên tĩnh:** `ezymarketing/css/marketing-cost.css`, `ezymarketing/js/marketing-cost.js`.

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `participant-fetching-script/fetch_all_users.properties`, `participant-fetching-script/fetch_only_me.properties`, `participant-fetching-script/fetch_users_bought_any_product.properties`, `participant-fetching-script/fetch_users_bought_product_by_category_name.properties` (+17).

- **web-plugin – Template:** `ezymarketing/advertisement/embed.html`, `ezymarketing/personalized-feed/index.html`, `ezymarketing/shorted-url/redirection.html`.

- **web-plugin – Tài nguyên tĩnh:** `ezymarketing/css/ads-layout.css`, `ezymarketing/css/ads.css`, `ezymarketing/css/style.css`, `ezymarketing/js/embed.js` (+1).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (19):** `ezymarketing_advertisements`, `ezymarketing_campaign_participant_segments`, `ezymarketing_campaigns`, `ezymarketing_conversion_events`, `ezymarketing_conversion_types`, `ezymarketing_cost_rates`, `ezymarketing_daily_costs`, `ezymarketing_daily_statistics`, `ezymarketing_participant_segment_participants`, `ezymarketing_participant_segments`, `ezymarketing_shorted_urls`, `ezymarketing_workflow_participant_step_logs`, `ezymarketing_workflow_participants`, `ezymarketing_workflow_run_participant_segment_participants`, `ezymarketing_workflow_runs`, `ezymarketing_workflow_statistics`, `ezymarketing_workflow_steps`, `ezymarketing_workflow_triggers`, `ezymarketing_workflows`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (19):** `Advertisement`, `MarketingCampaign`, `MarketingCampaignParticipantSegment`, `MarketingConversionEvent`, `MarketingConversionType`, `MarketingCostRate`, `MarketingDailyCost`, `MarketingDailyStatistic`, `MarketingParticipantSegment`, `MarketingParticipantSegmentParticipant`, `MarketingWorkflow`, `MarketingWorkflowParticipant`, `MarketingWorkflowParticipantStepLog`, `MarketingWorkflowRun`, `MarketingWorkflowRunParticipantSegmentParticipant`, `MarketingWorkflowStatistic`, `MarketingWorkflowStep`, `MarketingWorkflowTrigger` (+1).
- **SQL admin-plugin (17 tệp):** `resources/scripts/follow-up-workflow.sql`, `resources/scripts/marketing-cost.sql`, `resources/scripts/scripts.sql`, `resources/scripts/shorted-url.sql`, `resources/scripts/workflow-run-participant-segment-participant.sql`, `resources/scripts/workflow.sql`, `resources/scripts/alter-advertisement-index.sql` (+10).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezymarketing-admin-plugin-0.3.7.jar`, `ezymarketing-sdk-0.3.7.jar`; 613 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezymarketing.pagination`, `org.youngmonkeys.ezymarketing.entity`, `org.youngmonkeys.ezymarketing.admin.repo` (+34).
- **Controller/service/repository (mẫu):** `AdminAdvertisementControllerService`, `AdminAdvertisementsController`, `AdminApiAdvertisementController`, `AdminApiAdvertisementCostController`, `AdminAdvertisementContractService`, `AdminAdvertisementControllerService`, `AdminAdvertisementCostValidator`, `AdminAdvertisementPlatformStatisticValidator`, `AdminAdvertisementRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyMarketingConversionTypeConfig`, `AdminEzyMarketingCustomerPortraitConfig`, `AdminEzyMarketingDataAppenderConfig`, `AdminEzyMarketingParticipantFetchingScriptTemplateConfig`, `AdminEzyMarketingPostTypeConfig`, `AdminEzyMarketingViewMetadataConfig`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `content`, `contentType`, `title`.
- **Điểm mở rộng tiềm năng theo tên class:** `AddConversionEventEventHandler`, `AdminAbandonedCartFollowUpTriggerProvider`, `AdminAbstractMarketingPersonalizedContentCandidateProvider`, `AdminAbstractMarketingProductPersonalizedContentCandidateProvider`, `AdminAbstractMarketingUpsellProductPersonalizedContentCandidateProvider`, `AdminAddConversionEventEventHandler`, `AdminCreateShortedUrlEventHandler`, `AdminErpContractChargeAddedEventHandler`, `AdminErpContractStatusChangedEventHandler` (+53).

### web-plugin

- **JAR kiểm tra:** `ezymarketing-sdk-0.3.7.jar`, `ezymarketing-web-plugin-0.3.7.jar`; 355 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezymarketing.pagination`, `org.youngmonkeys.ezymarketing.entity`, `org.youngmonkeys.ezymarketing.model` (+25).
- **Controller/service/repository (mẫu):** `WebAdvertisementController`, `WebAdvertisementControllerService`, `WebApiAdvertisementController`, `WebApiMarketingConversionEventController`, `AdvertisementRepository`, `AdvertisementService`, `EzyMarketingSettingService`, `MarketingCampaignParticipantSegmentRepository`, `MarketingCampaignParticipantSegmentService`.
- **Điểm mở rộng tiềm năng theo tên class:** `AddConversionEventEventHandler`, `CreateShortedUrlEventHandler`, `FollowUpEnrollPolicyManager`, `FollowUpExitConditionManager`, `FollowUpStepInputDecoratorManager`, `FollowUpTriggerEvent`, `FollowUpTriggerProvider`, `FollowUpTriggerProviderManager`, `MarketingCampaignParticipantSegmentStatusManager` (+16).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezymarketing/advertisements` và Web `/ezymarketing/api/v1/advertisements` → 200.

## Áp dụng cho plugin quản lý công việc

Nếu cần liên kết thông báo, học xử lý định danh và tracking nhưng không bật tracking mặc định với issue riêng tư. Mã nhúng và provider vẫn là giao diện ngoài phạm vi.

[Về chỉ mục plugin](README.md)
