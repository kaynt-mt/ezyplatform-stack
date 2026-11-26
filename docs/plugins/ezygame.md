# ezygame

Chỉ số, sự kiện và thành tích.

- **Bản Marketplace trên core 1.5.9:** `0.0.8`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezygame` | `org.youngmonkeys.ezygame` | Không khai báo |
| `web-plugin` — `web/plugins/ezygame` | `org.youngmonkeys.ezygame` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 30 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /metrics` | `AdminMetricController` |
| `GET /achievements` | `AdminAchievementController` |
| `GET /event-metrics` | `AdminEventMetricController` |
| `GET /player-achievements` | `AdminPlayerAchievementController` |
| `GET /achievement-conditions` | `AdminAchievementConditionController` |
| `GET /metrics/add` | `AdminMetricController` |
| `GET /achievements/add` | `AdminAchievementController` |
| `POST /api/v1/metrics/add` | `AdminApiMetricController` |
| `POST /api/v1/achievements/add` | `AdminApiAchievementController` |
| `POST /api/v1/event-metrics/add` | `AdminApiEventMetricController` |
| `POST /api/v1/achievement-conditions/add` | `AdminApiAchievementConditionController` |
| `PUT /api/v1/metrics/{id}` | `AdminApiMetricController` |
| `PUT /api/v1/achievements/{id}` | `AdminApiAchievementController` |
| `PUT /api/v1/event-metrics/{id}` | `AdminApiEventMetricController` |
| `PUT /api/v1/achievement-conditions/{id}` | `AdminApiAchievementConditionController` |
| `DELETE /api/v1/metrics/{id}` | `AdminApiMetricController` |
| `DELETE /api/v1/achievements/{id}` | `AdminApiAchievementController` |
| `DELETE /api/v1/event-metrics/{id}` | `AdminApiEventMetricController` |
| `DELETE /api/v1/achievement-conditions/{id}` | `AdminApiAchievementConditionController` |

**web-plugin** — 1 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /metrics/{id}/leaderboard` | `WebApiMetricController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezygame: /`, `metrics: /metrics`, `metrics_add: ~/metrics/add`, `metrics_edit: ~/metrics/{id}/edit`, `event_metrics: /event-metrics`, `event_metrics_add: ~/event-metrics/add` (+8).

- **admin-plugin – Template:** `ezygame/achievement-condition/add.html`, `ezygame/achievement-condition/edit.html`, `ezygame/achievement-condition/list.html`, `ezygame/achievement-condition/scripts.html`, `ezygame/achievement/add.html`, `ezygame/achievement/edit.html`, `ezygame/achievement/list.html` (+10).

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `ezygame/metrics.properties`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (6):** `ezygame_achievement_conditions`, `ezygame_achievements`, `ezygame_event_metrics`, `ezygame_metrics`, `ezygame_player_achievements`, `ezygame_player_metrics`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (6):** `Achievement`, `AchievementCondition`, `EventMetric`, `Metric`, `PlayerAchievement`, `PlayerMetric`.
- **SQL admin-plugin (2 tệp):** `resources/scripts/event_metric.sql`, `resources/scripts/scripts.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezygame-admin-plugin-0.0.8.jar`, `ezygame-sdk-0.0.8.jar`; 180 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezygame.pagination`, `org.youngmonkeys.ezygame.repo`, `org.youngmonkeys.ezygame.service` (+25).
- **Controller/service/repository (mẫu):** `AchievementConditionControllerService`, `AchievementControllerService`, `AdminAchievementConditionController`, `AdminAchievementConditionControllerService`, `AchievementConditionControllerService`, `AchievementConditionRepository`, `AchievementConditionService`, `AchievementConditionValidator`, `AchievementControllerService`.
- **Class cấu hình/quyền (mẫu):** `AdminMetricConfig`, `EzyGameMessageClientConfig`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `ezygame_experience_point`.
- **Điểm mở rộng tiềm năng theo tên class:** `BrokerMessageEvent`, `EzyGameEvent`, `EzyGameEventManager`, `EzyGameMessageClient`, `GameEventUpdateMetricEvent`, `GameEventUpdateMetricEventHandler`.

### web-plugin

- **JAR kiểm tra:** `ezygame-sdk-0.0.8.jar`, `ezygame-web-plugin-0.0.8.jar`; 142 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezygame.pagination`, `org.youngmonkeys.ezygame.repo`, `org.youngmonkeys.ezygame.service` (+20).
- **Controller/service/repository (mẫu):** `AchievementConditionControllerService`, `AchievementControllerService`, `EventMetricControllerService`, `LeaderboardControllerService`, `AchievementConditionControllerService`, `AchievementConditionRepository`, `AchievementConditionService`, `AchievementConditionValidator`, `AchievementControllerService`.
- **Class cấu hình/quyền (mẫu):** `EzyGameMessageClientConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `BrokerMessageEvent`, `EzyGameEvent`, `EzyGameEventManager`, `EzyGameMessageClient`, `GameEventUpdateMetricEvent`, `GameEventUpdateMetricEventHandler`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezygame/metrics` → 200. Danh mục ghi S, G nhưng ZIP thực tế không chứa hai module này.

## Lưu ý khi tích hợp

Tách chỉ số dẫn xuất khỏi thao tác chính; đối chiếu lane với module thực tế, không chỉ nhãn Marketplace.

[Về chỉ mục plugin](README.md)
