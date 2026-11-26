# ezydefence

Chính sách IP, danh sách cho phép/chặn và filter HTTP.

- **Bản Marketplace trên core 1.5.9:** `0.1.5`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezydefence` | `org.youngmonkeys.ezydefence` | Không khai báo |
| `web-plugin` — `web/plugins/ezydefence` | `org.youngmonkeys.ezydefence` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 33 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezydefence: /`, `blacklist: /blacklist`, `whitelist: /whitelist`, `admin_ips: /admin-ips`, `requests: /requests`, `service_monitoring: /monitored-services` (+1).

- **admin-plugin – Template:** `ezydefence/admin-ip/list.html`, `ezydefence/blacklist/list.html`, `ezydefence/monitored-services/add-monitored-service-modal.html`, `ezydefence/monitored-services/edit-monitored-service-modal.html`, `ezydefence/monitored-services/list.html`, `ezydefence/monitored-services/scripts.html`, `ezydefence/requests/index.html` (+5).

- **admin-plugin – Tài nguyên tĩnh:** `css/ezydefence.css`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (7):** `ezydefence_admin_ips`, `ezydefence_blocking_ips`, `ezydefence_monitored_services`, `ezydefence_requested_ip_uris`, `ezydefence_requested_ips`, `ezydefence_requested_uris`, `ezydefence_white_uri_ips`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (7):** `AdminIp`, `BlockingIp`, `EMonitoredService`, `RequestedIp`, `RequestedIpUri`, `RequestedUri`, `WhiteUriIp`.
- **SQL admin-plugin (7 tệp):** `resources/scripts/admin_ips.sql`, `resources/scripts/monitored_service.sql`, `resources/scripts/requested_ip.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_to_add_domain_name.sql`, `resources/scripts/alter_truncate_uri.sql`, `resources/scripts/alter_varchar_25_to_50.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezydefence-admin-plugin-0.1.5.jar`, `ezydefence-sdk-0.1.5.jar`; 181 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezydefence.sdk.pagination`, `org.youngmonkeys.ezydefence.sdk.repo`, `org.youngmonkeys.ezydefence.sdk.model` (+32).
- **Controller/service/repository (mẫu):** `AdminAdminIpListController`, `AdminApiAdminIpController`, `AdminApiBlackListController`, `AdminApiEMonitoredServiceController`, `AdminAdminIpRepository`, `AdminAdminIpService`, `AdminAdminIpValidator`, `AdminApnicIpRegionFetcher`, `AdminBlackListValidator`.
- **Class cấu hình/quyền (mẫu):** `AdminIpRegionScriptConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminEzyDefenceExceptionHandler`, `AdminEzyDefenceInterceptor`, `AdminIpRegionFetcherManager`, `AdminJavascriptIpRegionFetcherProvider`, `IpRegionFetcherManager`, `IpRegionFetcherProvider`, `JavascriptIpRegionFetcherProvider`.

### web-plugin

- **JAR kiểm tra:** `ezydefence-sdk-0.1.5.jar`, `ezydefence-web-plugin-0.1.5.jar`; 121 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezydefence.sdk.pagination`, `org.youngmonkeys.ezydefence.sdk.repo`, `org.youngmonkeys.ezydefence.sdk.model` (+22).
- **Controller/service/repository (mẫu):** `AdminIpRepository`, `AdminIpService`, `ApnicIpRegionFetcher`, `BlockingIpRepository`, `BlockingIpService`.
- **Class cấu hình/quyền (mẫu):** `WebEzyDefenceWatcherConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `IpRegionFetcherManager`, `IpRegionFetcherProvider`, `JavascriptIpRegionFetcherProvider`, `WebEzyDefenceInterceptor`, `WebIpRegionFetcherManager`, `WebIpRegionManager`, `WebJavascriptIpRegionFetcherProvider`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezydefence/blacklist`, `/ezydefence/whitelist` → 200; không thay chính sách.

## Lưu ý khi tích hợp

Dùng như lớp vận hành bổ sung; ứng dụng vẫn tự xác thực và kiểm quyền nghiệp vụ ở mọi deployment.

[Về chỉ mục plugin](README.md)
