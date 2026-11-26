# ezygame

Metrics, events, and achievements.

- **Marketplace version on core 1.5.9:** `0.0.8`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezygame` | `org.youngmonkeys.ezygame` | Not declared |
| `web-plugin` — `web/plugins/ezygame` | `org.youngmonkeys.ezygame` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 30 method/URI combinations identified; representative sample:

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

**web-plugin** — 1 method/URI combination identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /metrics/{id}/leaderboard` | `WebApiMetricController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezygame: /`, `metrics: /metrics`, `metrics_add: ~/metrics/add`, `metrics_edit: ~/metrics/{id}/edit`, `event_metrics: /event-metrics`, `event_metrics_add: ~/event-metrics/add` (+8).

- **admin-plugin – Template:** `ezygame/achievement-condition/add.html`, `ezygame/achievement-condition/edit.html`, `ezygame/achievement-condition/list.html`, `ezygame/achievement-condition/scripts.html`, `ezygame/achievement/add.html`, `ezygame/achievement/edit.html`, `ezygame/achievement/list.html` (+10).

- **admin-plugin – Configuration and template resources:** `ezygame/metrics.properties`.

## Data and migrations

- **Table in the DDL package (6):** `ezygame_achievement_conditions`, `ezygame_achievements`, `ezygame_event_metrics`, `ezygame_metrics`, `ezygame_player_achievements`, `ezygame_player_metrics`.
- **Class with JPA Entity/MappedSuperclass (6):** `Achievement`, `AchievementCondition`, `EventMetric`, `Metric`, `PlayerAchievement`, `PlayerMetric`.
- **SQL admin-plugin (2 files):** `resources/scripts/event_metric.sql`, `resources/scripts/scripts.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezygame-admin-plugin-0.0.8.jar`, `ezygame-sdk-0.0.8.jar`; 180 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezygame.pagination`, `org.youngmonkeys.ezygame.repo`, `org.youngmonkeys.ezygame.service` (+25).
- **Controllers, services, and repositories (sample):** `AchievementConditionControllerService`, `AchievementControllerService`, `AdminAchievementConditionController`, `AdminAchievementConditionControllerService`, `AchievementConditionControllerService`, `AchievementConditionRepository`, `AchievementConditionService`, `AchievementConditionValidator`, `AchievementControllerService`.
- **Configuration and permission classes (sample):** `AdminMetricConfig`, `EzyGameMessageClientConfig`.
- **Configuration and template keys from resources (values omitted):** `ezygame_experience_point`.
- **Potential extension points based on class names:** `BrokerMessageEvent`, `EzyGameEvent`, `EzyGameEventManager`, `EzyGameMessageClient`, `GameEventUpdateMetricEvent`, `GameEventUpdateMetricEventHandler`.

### web-plugin

- **JARs inspected:** `ezygame-sdk-0.0.8.jar`, `ezygame-web-plugin-0.0.8.jar`; 142 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezygame.pagination`, `org.youngmonkeys.ezygame.repo`, `org.youngmonkeys.ezygame.service` (+20).
- **Controllers, services, and repositories (sample):** `AchievementConditionControllerService`, `AchievementControllerService`, `EventMetricControllerService`, `LeaderboardControllerService`, `AchievementConditionControllerService`, `AchievementConditionRepository`, `AchievementConditionService`, `AchievementConditionValidator`, `AchievementControllerService`.
- **Configuration and permission classes (sample):** `EzyGameMessageClientConfig`.
- **Potential extension points based on class names:** `BrokerMessageEvent`, `EzyGameEvent`, `EzyGameEventManager`, `EzyGameMessageClient`, `GameEventUpdateMetricEvent`, `GameEventUpdateMetricEventHandler`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezygame/metrics` returned 200. The catalog lists S and G, but the ZIP contains neither module.

## Integration notes

Keep derived metrics separate from the primary operation. Check the actual module types, not just the Marketplace labels.

[Back to the plugin index](README.md)
