# omnichannel

External channel management and social network connections.

- **Marketplace version on core 1.5.9:** `0.0.4`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/omnichannel` | `org.youngmonkeys.omnichannel` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezyrating](ezyrating.md), [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/omnichannel` | `org.youngmonkeys.omnichannel` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezyrating](ezyrating.md), [ecommerce](ecommerce.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 22 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `omnichannel: /`, `social_networks: /social-networks`, `social_networks_details: ~/social-networks/{name}`, `social_networks_developer_app_details: ~/social-networks/{name}/developer-apps/{appId}`, `settings: /settings`.

- **admin-plugin – Template:** `omnichannel/setting/index.html`, `omnichannel/social-network/facebook/add-developer-app-modal.html`, `omnichannel/social-network/facebook/add-page-modal.html`, `omnichannel/social-network/facebook/developer-app.html`, `omnichannel/social-network/facebook/developer-apps.html`, `omnichannel/social-network/facebook/edit-developer-app-modal.html`, `omnichannel/social-network/facebook/edit-page-modal.html` (+6).

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `omnichannel-admin-plugin-0.0.4.jar`, `omnichannel-sdk-0.0.4.jar`; 94 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.omnichannel.request`, `org.youngmonkeys.omnichannel.admin.service`, `org.youngmonkeys.omnichannel.facebook` (+24).
- **Controllers, services, and repositories (sample):** `AdminOmnichannelApiDeveloperAppController`, `AdminOmnichannelApiSettingController`, `AdminOmnichannelApiSocialNetworkController`, `AdminOmnichannelFacebookOauthController`, `AdminOmnichannelClientIdService`, `AdminOmnichannelDeveloperAppService`, `AdminOmnichannelFacebookPagePostService`, `AdminOmnichannelFacebookService`, `AdminOmnichannelFacebookSocialNetworkService`.
- **Configuration and permission classes (sample):** `AdminOmnichannelDataAppenderConfig`, `AdminOmnichannelDomainSettingMetaConfig`, `AdminOmnichannelSocialNetworkConfig`, `AdminOmnichannelViewMetadataConfig`.
- **Potential extension points based on class names:** `AdminAutoPublishPostToSocialPageScheduler`, `AdminFacebookClient`, `AdminFacebookPixelSendUserActionToChannelEventHandler`, `AdminFacebookPixelSendUserOrderStatusToChannelEventHandler`, `AdminGa4Client`, `AdminGa4SendUserActionToChannelEventHandler`, `AdminGa4SendUserOrderStatusToChannelEventHandler`, `AdminOmnichannelFacebookOauthStateManager`, `AdminOmnichannelSocialNetworkServiceManager` (+6).

### web-plugin

- **JARs inspected:** `omnichannel-sdk-0.0.4.jar`, `omnichannel-web-plugin-0.0.4.jar`; 49 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.omnichannel.request`, `org.youngmonkeys.omnichannel.facebook`, `org.youngmonkeys.omnichannel.web.service` (+9).
- **Controllers, services, and repositories (sample):** `OmnichannelClientIdService`, `OmnichannelFacebookService`, `OmnichannelGa4Service`, `OmnichannelSettingService`, `OmnichannelTikTokService`.
- **Potential extension points based on class names:** `FacebookClient`, `Ga4Client`, `TikTokClient`, `WebFacebookClient`, `WebGa4Client`, `WebTikTokClient`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/omnichannel/social-networks` returned 200. No external channel was connected.

## Integration notes

If multiple channels are needed, keep adapters independent, test each external connector, and account for dependency costs.

[Back to the plugin index](README.md)
