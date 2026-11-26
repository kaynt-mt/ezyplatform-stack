# lucky-wheel

Trò quay thưởng có Admin, Web, theme và Socket.

- **Bản Marketplace trên core 1.5.9:** `0.0.1`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `theme`, `socket-plugin`, `socket-app`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/lucky-wheel` | `org.youngmonkeys.lucky_wheel` | Không khai báo |
| `web-plugin` — `web/plugins/lucky-wheel` | `org.youngmonkeys.lucky_wheel` | Không khai báo |
| `theme` — `web/themes/lucky-wheel` | `org.youngmonkeys.lucky_wheel` | Không khai báo |
| `socket-plugin` — `socket/plugins/lucky-wheel` | `org.youngmonkeys.lucky_wheel.plugin` | Không khai báo |
| `socket-app` — `socket/apps/lucky-wheel` | `org.youngmonkeys.lucky_wheel.app` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 1 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `SettingsController` |

**web-plugin** — 1 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /api/v1/lucky-wheel` | `LuckyWheelController` |

**theme** — 1 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `HomeController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `lucky_wheel: /lucky-wheel`, `settings: /lucky-wheel/settings`, `dashboard: /lucky-wheel/dashboard`.

- **admin-plugin – Template:** `lucky-wheel/settings.html`.

- **theme – Tài nguyên tĩnh:** `index.html`, `js/ezyclient-1.0.3.min.js`, `js/game.js`, `js/phaser.min.js` (+1).

- **socket-plugin – Tài nguyên cấu hình/mẫu:** `wheel.json`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `lucky-wheel-admin-plugin-0.0.1.jar`; 1 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.lucky_wheel.controller`.
- **JAR thư viện khác:** `javassist-3.20.0-GA.jar`.
- **Controller/service/repository (mẫu):** `SettingsController`.
- **Resource trong JAR (mẫu):** `admin.properties`, `config.properties`, `dictionary.properties`, `languages.properties`, `logback.xml` (+62).

### web-plugin

- **JAR kiểm tra:** `lucky-wheel-web-plugin-0.0.1.jar`; 1 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.lucky_wheel.controller`.
- **JAR thư viện khác:** `javassist-3.20.0-GA.jar`.
- **Controller/service/repository (mẫu):** `LuckyWheelController`.
- **Resource trong JAR (mẫu):** `config.properties`, `logback.xml`, `messages/messages.properties`, `messages/messages_vi.properties`, `platform.properties` (+10).

### theme

- **JAR kiểm tra:** `lucky-wheel-theme-0.0.1.jar`; 1 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.lucky_wheel.controller`.
- **JAR thư viện khác:** `javassist-3.20.0-GA.jar`.
- **Controller/service/repository (mẫu):** `HomeController`.
- **Resource trong JAR (mẫu):** `config.properties`, `logback.xml`, `messages/messages.properties`, `messages/messages_vi.properties`, `platform.properties` (+11).

### socket-plugin

- **JAR kiểm tra:** `lucky-wheel-socket-plugin-0.0.1.jar`; 2 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.lucky_wheel.plugin.controller`, `org.youngmonkeys.lucky_wheel.plugin`.
- **Controller/service/repository (mẫu):** `UserLoginController`.
- **Điểm mở rộng tiềm năng theo tên class:** `PluginEntryLoader`.
- **Zone / entry loader:** `lucky-wheel` / `org.youngmonkeys.lucky_wheel.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `UserLoginController`.

### socket-app

- **JAR kiểm tra:** `lucky-wheel-socket-app-0.0.1.jar`; 6 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.lucky_wheel.app.entity`, `org.youngmonkeys.lucky_wheel.app`, `org.youngmonkeys.lucky_wheel.app.controller` (+1).
- **Controller/service/repository (mẫu):** `RequestController`, `WheelService`.
- **Điểm mở rộng tiềm năng theo tên class:** `AppEntryLoader`.
- **Zone / entry loader:** `lucky-wheel` / `org.youngmonkeys.lucky_wheel.app.AppEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `RequestController`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/lucky-wheel/settings` → 200. Theme Lucky Wheel đưa `/` đến `/index.html` (200); `/api/v1/lucky-wheel` → JSON 200, nhưng `/lucky-wheel` là trang “Not found”. Chưa thử lượt quay có giải thưởng.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Lưu ý khi tích hợp

Ví dụ cả năm loại module trong một gói; kiểm theme/route và Socket riêng, JSON không chứng minh UI chạy.

[Về chỉ mục plugin](README.md)
