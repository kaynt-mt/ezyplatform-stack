# omnichannel

Quản trị kênh ngoài và kết nối mạng xã hội.

- **Bản Marketplace trên core 1.5.9:** `0.0.4`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/omnichannel` | `org.youngmonkeys.omnichannel` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezyrating](ezyrating.md), [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/omnichannel` | `org.youngmonkeys.omnichannel` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezyrating](ezyrating.md), [ecommerce](ecommerce.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 22 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminOmnichannelSettingsController` |
| `GET /social-networks` | `AdminOmnichannelSocialNetworkController` |
| `GET /facebook/oauth/callback` | `AdminOmnichannelFacebookOauthController` |
| `GET /social-networks/{name}` | `AdminOmnichannelSocialNetworkController` |
| `GET /facebook/oauth/connect/{id}` | `AdminOmnichannelFacebookOauthController` |
| `GET /social-networks/{name}/developer-apps/{appId}` | `AdminOmnichannelSocialNetworkController` |
| `GET /api/v1/developer-apps/{id}/pages` | `AdminOmnichannelApiDeveloperAppController` |
| `POST /api/v1/social-networks/post-to-pages` | `AdminOmnichannelApiSocialNetworkController` |
| `POST /api/v1/social-networks/{id}/post-to-pages` | `AdminOmnichannelApiDeveloperAppController` |
| `POST /api/v1/developer-apps/{appId}/post-to-pages` | `AdminOmnichannelApiDeveloperAppController` |
| `PUT /api/v1/settings/ga4` | `AdminOmnichannelApiSettingController` |
| `PUT /api/v1/settings/tiktok` | `AdminOmnichannelApiSettingController` |
| `PUT /api/v1/settings/facebook-ads` | `AdminOmnichannelApiSettingController` |
| `PUT /api/v1/settings/auto-publish-to-social-page-posts` | `AdminOmnichannelApiSettingController` |
| `DELETE /api/v1/developer-apps/{id}` | `AdminOmnichannelApiDeveloperAppController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `omnichannel: /`, `social_networks: /social-networks`, `social_networks_details: ~/social-networks/{name}`, `social_networks_developer_app_details: ~/social-networks/{name}/developer-apps/{appId}`, `settings: /settings`.

- **admin-plugin – Template:** `omnichannel/setting/index.html`, `omnichannel/social-network/facebook/add-developer-app-modal.html`, `omnichannel/social-network/facebook/add-page-modal.html`, `omnichannel/social-network/facebook/developer-app.html`, `omnichannel/social-network/facebook/developer-apps.html`, `omnichannel/social-network/facebook/edit-developer-app-modal.html`, `omnichannel/social-network/facebook/edit-page-modal.html` (+6).

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `omnichannel-admin-plugin-0.0.4.jar`, `omnichannel-sdk-0.0.4.jar`; 94 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.omnichannel.request`, `org.youngmonkeys.omnichannel.admin.service`, `org.youngmonkeys.omnichannel.facebook` (+24).
- **Controller/service/repository (mẫu):** `AdminOmnichannelApiDeveloperAppController`, `AdminOmnichannelApiSettingController`, `AdminOmnichannelApiSocialNetworkController`, `AdminOmnichannelFacebookOauthController`, `AdminOmnichannelClientIdService`, `AdminOmnichannelDeveloperAppService`, `AdminOmnichannelFacebookPagePostService`, `AdminOmnichannelFacebookService`, `AdminOmnichannelFacebookSocialNetworkService`.
- **Class cấu hình/quyền (mẫu):** `AdminOmnichannelDataAppenderConfig`, `AdminOmnichannelDomainSettingMetaConfig`, `AdminOmnichannelSocialNetworkConfig`, `AdminOmnichannelViewMetadataConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminAutoPublishPostToSocialPageScheduler`, `AdminFacebookClient`, `AdminFacebookPixelSendUserActionToChannelEventHandler`, `AdminFacebookPixelSendUserOrderStatusToChannelEventHandler`, `AdminGa4Client`, `AdminGa4SendUserActionToChannelEventHandler`, `AdminGa4SendUserOrderStatusToChannelEventHandler`, `AdminOmnichannelFacebookOauthStateManager`, `AdminOmnichannelSocialNetworkServiceManager` (+6).

### web-plugin

- **JAR kiểm tra:** `omnichannel-sdk-0.0.4.jar`, `omnichannel-web-plugin-0.0.4.jar`; 49 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.omnichannel.request`, `org.youngmonkeys.omnichannel.facebook`, `org.youngmonkeys.omnichannel.web.service` (+9).
- **Controller/service/repository (mẫu):** `OmnichannelClientIdService`, `OmnichannelFacebookService`, `OmnichannelGa4Service`, `OmnichannelSettingService`, `OmnichannelTikTokService`.
- **Điểm mở rộng tiềm năng theo tên class:** `FacebookClient`, `Ga4Client`, `TikTokClient`, `WebFacebookClient`, `WebGa4Client`, `WebTikTokClient`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/omnichannel/social-networks` → 200; chưa nối kênh bên ngoài.

## Lưu ý khi tích hợp

Nếu cần nhiều kênh, giữ adapter độc lập và thử từng connector ngoài; lưu ý chi phí dependency.

[Về chỉ mục plugin](README.md)
