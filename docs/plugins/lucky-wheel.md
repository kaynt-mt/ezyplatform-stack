# lucky-wheel

Prize wheel with Admin, Web, theme, and Socket modules.

- **Marketplace version on core 1.5.9:** `0.0.1`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `theme`, `socket-plugin`, `socket-app`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/lucky-wheel` | `org.youngmonkeys.lucky_wheel` | Not declared |
| `web-plugin` — `web/plugins/lucky-wheel` | `org.youngmonkeys.lucky_wheel` | Not declared |
| `theme` — `web/themes/lucky-wheel` | `org.youngmonkeys.lucky_wheel` | Not declared |
| `socket-plugin` — `socket/plugins/lucky-wheel` | `org.youngmonkeys.lucky_wheel.plugin` | Not declared |
| `socket-app` — `socket/apps/lucky-wheel` | `org.youngmonkeys.lucky_wheel.app` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 1 method/URI combination identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `SettingsController` |

**web-plugin** — 1 method/URI combination identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/lucky-wheel` | `LuckyWheelController` |

**theme** — 1 method/URI combination identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `HomeController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `lucky_wheel: /lucky-wheel`, `settings: /lucky-wheel/settings`, `dashboard: /lucky-wheel/dashboard`.

- **admin-plugin – Template:** `lucky-wheel/settings.html`.

- **theme - Resources:** `index.html`, `js/ezyclient-1.0.3.min.js`, `js/game.js`, `js/phaser.min.js` (+1).

- **Socket-plugin – Configuration/Sample Resource:** `wheel.json`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `lucky-wheel-admin-plugin-0.0.1.jar`; 1 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.lucky_wheel.controller`.
- **Other library JARs:** `javassist-3.20.0-GA.jar`.
- **Controllers, services, and repositories (sample):** `SettingsController`.
- **JAR resources (sample):** `admin.properties`, `config.properties`, `dictionary.properties`, `languages.properties`, `logback.xml` (+62).

### web-plugin

- **JARs inspected:** `lucky-wheel-web-plugin-0.0.1.jar`; 1 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.lucky_wheel.controller`.
- **Other library JARs:** `javassist-3.20.0-GA.jar`.
- **Controllers, services, and repositories (sample):** `LuckyWheelController`.
- **JAR resources (sample):** `config.properties`, `logback.xml`, `messages/messages.properties`, `messages/messages_vi.properties`, `platform.properties` (+10).

### theme

- **JARs inspected:** `lucky-wheel-theme-0.0.1.jar`; 1 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.lucky_wheel.controller`.
- **Other library JARs:** `javassist-3.20.0-GA.jar`.
- **Controllers, services, and repositories (sample):** `HomeController`.
- **JAR resources (sample):** `config.properties`, `logback.xml`, `messages/messages.properties`, `messages/messages_vi.properties`, `platform.properties` (+11).

### socket-plugin

- **JARs inspected:** `lucky-wheel-socket-plugin-0.0.1.jar`; 2 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.lucky_wheel.plugin.controller`, `org.youngmonkeys.lucky_wheel.plugin`.
- **Controllers, services, and repositories (sample):** `UserLoginController`.
- **Potential extension points based on class names:** `PluginEntryLoader`.
- **Zone / entry loader:** `lucky-wheel` / `org.youngmonkeys.lucky_wheel.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `UserLoginController`.

### socket-app

- **JARs inspected:** `lucky-wheel-socket-app-0.0.1.jar`; 6 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.lucky_wheel.app.entity`, `org.youngmonkeys.lucky_wheel.app`, `org.youngmonkeys.lucky_wheel.app.controller` (+1).
- **Controllers, services, and repositories (sample):** `RequestController`, `WheelService`.
- **Potential extension points based on class names:** `AppEntryLoader`.
- **Zone / entry loader:** `lucky-wheel` / `org.youngmonkeys.lucky_wheel.app.AppEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `RequestController`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/lucky-wheel/settings` returned 200. The Lucky Wheel theme redirected `/` to `/index.html` (200). `/api/v1/lucky-wheel` returned JSON with status 200, but `/lucky-wheel` showed a “Not found” page. No prize-bearing spins were tested.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

This package illustrates all five module types. Verify the theme and routes separately from Socket. A JSON response does not prove the UI works.

[Back to the plugin index](README.md)
