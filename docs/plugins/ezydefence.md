# ezydefence

IP policies, allowlists and blocklists, and HTTP filtering.

- **Marketplace version on core 1.5.9:** `0.1.5`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezydefence` | `org.youngmonkeys.ezydefence` | Not declared |
| `web-plugin` — `web/plugins/ezydefence` | `org.youngmonkeys.ezydefence` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 33 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /requests` | `AdminRequestsController` |
| `GET /settings` | `AdminSettingController` |
| `GET /admin-ips` | `AdminAdminIpListController` |
| `GET /blacklist` | `AdminBlackListController` |
| `GET /whitelist` | `AdminWhiteListController` |
| `GET /monitored-services` | `AdminEMonitoredServiceController` |
| `GET /api/v1/settings` | `AdminApiSettingController` |
| `POST /api/v1/admin-ips/add` | `AdminApiAdminIpController` |
| `POST /api/v1/blacklist/add` | `AdminApiBlackListController` |
| `POST /api/v1/whitelist/add` | `AdminApiWhiteListController` |
| `POST /api/v1/monitored-services/add` | `AdminApiEMonitoredServiceController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/settings/admin` | `AdminApiSettingController` |
| `PUT /api/v1/ip-regions/selected` | `AdminApiIpRegionController` |
| `PUT /api/v1/whitelist/edit-item` | `AdminApiWhiteListController` |
| `DELETE /api/v1/whitelist/delete-item` | `AdminApiWhiteListController` |
| `DELETE /api/v1/admin-ips/{ip}` | `AdminApiAdminIpController` |
| `DELETE /api/v1/blacklist/{blockedIpId}` | `AdminApiBlackListController` |
| `DELETE /api/v1/monitored-services/{id}` | `AdminApiEMonitoredServiceController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezydefence: /`, `blacklist: /blacklist`, `whitelist: /whitelist`, `admin_ips: /admin-ips`, `requests: /requests`, `service_monitoring: /monitored-services` (+1).

- **admin-plugin – Template:** `ezydefence/admin-ip/list.html`, `ezydefence/blacklist/list.html`, `ezydefence/monitored-services/add-monitored-service-modal.html`, `ezydefence/monitored-services/edit-monitored-service-modal.html`, `ezydefence/monitored-services/list.html`, `ezydefence/monitored-services/scripts.html`, `ezydefence/requests/index.html` (+5).

- **admin-plugin – Static resources:** `css/ezydefence.css`.

## Data and migrations

- **Table in the DDL package (7):** `ezydefence_admin_ips`, `ezydefence_blocking_ips`, `ezydefence_monitored_services`, `ezydefence_requested_ip_uris`, `ezydefence_requested_ips`, `ezydefence_requested_uris`, `ezydefence_white_uri_ips`.
- **Class with JPA Entity/MappedSuperclass indication (7):** `AdminIp`, `BlockingIp`, `EMonitoredService`, `RequestedIp`, `RequestedIpUri`, `RequestedUri`, `WhiteUriIp`.
- **SQL admin-plugin (7 files):** `resources/scripts/admin_ips.sql`, `resources/scripts/monitored_service.sql`, `resources/scripts/requested_ip.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_to_add_domain_name.sql`, `resources/scripts/alter_truncate_uri.sql`, `resources/scripts/alter_varchar_25_to_50.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezydefence-admin-plugin-0.1.5.jar`, `ezydefence-sdk-0.1.5.jar`; 181 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezydefence.sdk.pagination`, `org.youngmonkeys.ezydefence.sdk.repo`, `org.youngmonkeys.ezydefence.sdk.model` (+32).
- **Controllers, services, and repositories (sample):** `AdminAdminIpListController`, `AdminApiAdminIpController`, `AdminApiBlackListController`, `AdminApiEMonitoredServiceController`, `AdminAdminIpRepository`, `AdminAdminIpService`, `AdminAdminIpValidator`, `AdminApnicIpRegionFetcher`, `AdminBlackListValidator`.
- **Configuration and permission classes (sample):** `AdminIpRegionScriptConfig`.
- **Potential extension points based on class names:** `AdminEzyDefenceExceptionHandler`, `AdminEzyDefenceInterceptor`, `AdminIpRegionFetcherManager`, `AdminJavascriptIpRegionFetcherProvider`, `IpRegionFetcherManager`, `IpRegionFetcherProvider`, `JavascriptIpRegionFetcherProvider`.

### web-plugin

- **JARs inspected:** `ezydefence-sdk-0.1.5.jar`, `ezydefence-web-plugin-0.1.5.jar`; 121 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezydefence.sdk.pagination`, `org.youngmonkeys.ezydefence.sdk.repo`, `org.youngmonkeys.ezydefence.sdk.model` (+22).
- **Controllers, services, and repositories (sample):** `AdminIpRepository`, `AdminIpService`, `ApnicIpRegionFetcher`, `BlockingIpRepository`, `BlockingIpService`.
- **Configuration and permission classes (sample):** `WebEzyDefenceWatcherConfig`.
- **Potential extension points based on class names:** `IpRegionFetcherManager`, `IpRegionFetcherProvider`, `JavascriptIpRegionFetcherProvider`, `WebEzyDefenceInterceptor`, `WebIpRegionFetcherManager`, `WebIpRegionManager`, `WebJavascriptIpRegionFetcherProvider`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezydefence/blacklist` and `/ezydefence/whitelist` returned 200. No policies were changed.

## Integration notes

Use this as an additional operational control. The application still authenticates users and enforces business permissions in every deployment.

[Back to the plugin index](README.md)
