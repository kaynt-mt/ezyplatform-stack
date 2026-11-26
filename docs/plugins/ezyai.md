# ezyai

Cấu hình dịch vụ AI, skill và thư viện kỹ năng.

- **Bản Marketplace trên core 1.5.9:** `0.1.8`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyai` | `org.youngmonkeys.ezyai` | [graphql](graphql.md), [ezychat](ezychat.md) |
| `web-plugin` — `web/plugins/ezyai` | `org.youngmonkeys.ezyai` | [graphql](graphql.md), [ezychat](ezychat.md) |
| `socket-plugin` — `socket/plugins/ezyai` | `org.youngmonkeys.ezyai.socket.plugin` | [graphql](graphql.md), [ezychat](ezychat.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 52 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyAISettingController` |
| `GET /ai-skills` | `AdminAISkillController` |
| `GET /skill-library` | `AdminSkillLibraryController` |
| `GET /ai-chat-services` | `AdminAIChatServiceController` |
| `GET /ai-skills/add` | `AdminAISkillController` |
| `GET /skill-library/add` | `AdminSkillLibraryController` |
| `GET /api/v1/ai-skills` | `AdminApiAISkillController` |
| `POST /api/v1/ai-skills/add` | `AdminApiAISkillController` |
| `POST /api/v1/skill-library/add` | `AdminApiSkillLibraryController` |
| `POST /api/v1/skill-library/add-package` | `AdminApiSkillLibraryController` |
| `POST /api/v1/skill-library/{skillId}/package` | `AdminApiSkillLibraryController` |
| `PUT /api/v1/settings` | `AdminApiEzyAISettingController` |
| `PUT /api/v1/ai-skills/{skillId}` | `AdminApiAISkillController` |
| `PUT /api/v1/skill-library/{skillId}` | `AdminApiSkillLibraryController` |
| `PUT /api/v1/skill-library/{skillId}/publish` | `AdminApiSkillLibraryController` |
| `DELETE /api/v1/ai-skills/{skillId}` | `AdminApiAISkillController` |
| `DELETE /api/v1/skill-library/{skillId}` | `AdminApiSkillLibraryController` |
| `DELETE /api/v1/skill-library/{skillId}/languages/{languageCode}` | `AdminApiSkillLibraryController` |
| `DELETE /api/v1/ai-chat-services/{serviceName}/profiles/{profileId}` | `AdminApiAIProfileServiceController` |

**web-plugin** — 16 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /ezyai/skill-library` | `WebSkillLibraryController` |
| `GET /account/ai-skill-library` | `WebAccountSkillLibraryController` |
| `GET /api/v1/skill-library/skills` | `WebApiSkillLibraryController` |
| `GET /api/v1/account/ai-skill-library` | `WebApiAccountSkillLibraryController` |
| `GET /api/v1/skill-library/categories` | `WebApiSkillLibraryController` |
| `GET /ezyai/skill-library/{slug}` | `WebSkillLibraryController` |
| `GET /api/v1/account/ai-skill-library/{skillId}` | `WebApiAccountSkillLibraryController` |
| `POST /api/v1/account/ai-skill-library/add` | `WebApiAccountSkillLibraryController` |
| `POST /api/v1/account/ai-skill-library/add-package` | `WebApiAccountSkillLibraryController` |
| `POST /api/v1/account/ai-skill-library/{skillId}/package` | `WebApiAccountSkillLibraryController` |
| `PUT /api/v1/account/ai-skill-library/{skillId}` | `WebApiAccountSkillLibraryController` |
| `DELETE /api/v1/account/ai-skill-library/{skillId}` | `WebApiAccountSkillLibraryController` |
| `DELETE /api/v1/account/ai-skill-library/{skillId}/revision` | `WebApiAccountSkillLibraryController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyai: /`, `ai_chat_services: /ai-chat-services`, `ai_chat_services_details: ~/ai-chat-services/{serviceName}`, `ai_chat_services_profile_add: ~/ai-chat-services/{serviceName}/profiles/add`, `ai_chat_services_profile_details: ~/ai-chat-services/{serviceName}/profiles/{profileName}`, `ai_chat_services_profile_edit: ~/ai-chat-services/{serviceName}/profiles/{profileName}/edit` (+10).

- **admin-plugin – Template:** `ezyai/ai-chat-services/chat.html`, `ezyai/ai-chat-services/list.html`, `ezyai/ai-chat-services/profile/add.html`, `ezyai/ai-chat-services/profile/details.html`, `ezyai/ai-chat-services/profile/edit.html`, `ezyai/ai-chat-services/profile/scripts.html`, `ezyai/ai-chat-services/profiles.html` (+17).

- **admin-plugin – Tài nguyên tĩnh:** `ezyai/js/skill-package-reader.js`.

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `ezyai/letter_template_skill_library_approved.properties`, `ezyai/letter_template_skill_library_update_approved.properties`, `ezyai/letter_template_skill_library_update_rejected.properties`, `ezyai/notification_template_skill_library_approved.properties` (+2).

- **web-plugin – Template:** `ezyai/fragments/my-skill-library.html`, `ezyai/my-skill-library.html`, `ezyai/skill-library-detail.html`, `ezyai/skill-library.html`.

- **web-plugin – Tài nguyên tĩnh:** `ezyai/css/skill-library.css`, `ezyai/js/skill-library.js`, `ezyai/js/skill-package-reader.js`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyai-admin-plugin-0.1.8.jar`, `ezyai-sdk-0.1.8.jar`; 172 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyai.service`, `org.youngmonkeys.ezyai.admin.service`, `org.youngmonkeys.ezyai.model` (+30).
- **Controller/service/repository (mẫu):** `AdminAIChatControllerService`, `AdminAIChatProfileController`, `AdminAIChatProfileControllerService`, `AdminAIChatServiceController`, `AIChatBotService`, `AISkillService`, `AbstractAIChatService`, `AdminAIChatControllerService`, `AdminAIChatProfileControllerService`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyAIPageFragmentConfig`, `AdminEzyAIPostTypeConfig`, `AdminEzyAIProductTypeConfig`, `AdminEzyAITemplateConfig`, `AdminEzyAITermTypeConfig`, `AdminEzyAIUserRoleConfig`, `AdminEzyAIViewMetadataConfig` (+1).
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `content`, `title`.
- **Điểm mở rộng tiềm năng theo tên class:** `AIChatToolProvider`, `AdminKnowledgeDataSourceManager`, `AdminMcpAIChatToolProvider`, `AdminSearchKnowledgeDataListToolEventHandler`, `AdminSearchKnowledgeDataListToolSchemaEventHandler`, `AdminSearchKnowledgeDataToolEventHandler`, `AdminSearchKnowledgeDataToolSchemaEventHandler`, `ChatBotStreamEventHandler`, `KnowledgeDataSourceManager` (+6).

### web-plugin

- **JAR kiểm tra:** `ezyai-sdk-0.1.8.jar`, `ezyai-web-plugin-0.1.8.jar`; 144 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyai.service`, `org.youngmonkeys.ezyai.web.service`, `org.youngmonkeys.ezyai.model` (+27).
- **Controller/service/repository (mẫu):** `WebAccountSkillLibraryController`, `WebApiAccountSkillLibraryController`, `WebApiSkillLibraryController`, `WebSkillLibraryController`, `AIChatBotService`, `AISkillService`, `AbstractAIChatService`, `AbstractWebSkillLibrarySaveEventSchemaFetcher`, `ChatGptChatService`.
- **Class cấu hình/quyền (mẫu):** `EzyAIPageFragmentConfig`, `WebEzyAIPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AIChatToolProvider`, `ChatBotStreamEventHandler`, `KnowledgeDataSourceManager`, `KnowledgeDataSourceProvider`, `McpAIChatToolProvider`, `SearchKnowledgeDataListToolEventHandler`, `SearchKnowledgeDataListToolSchemaEventHandler`, `SearchKnowledgeDataToolEventHandler`, `SearchKnowledgeDataToolSchemaEventHandler` (+6).

### socket-plugin

- **JAR kiểm tra:** `ezyai-sdk-0.1.8.jar`, `ezyai-socket-plugin-0.1.8.jar`; 118 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyai.service`, `org.youngmonkeys.ezyai.model`, `org.youngmonkeys.ezyai.knowledge` (+22).
- **JAR thư viện khác:** `jsoup-1.18.3.jar`.
- **Controller/service/repository (mẫu):** `McpToolsRequestController`, `SocketPluginEzyAIServerReadyController`, `AIChatBotService`, `AISkillService`, `AbstractAIChatService`, `ChatGptChatService`, `ClaudeChatService`.
- **Class cấu hình/quyền (mẫu):** `EzyAIPageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AIChatToolProvider`, `ChatBotStreamEventHandler`, `KnowledgeDataSourceManager`, `KnowledgeDataSourceProvider`, `McpAIChatToolProvider`, `PluginEntryLoader`, `SearchKnowledgeDataListToolEventHandler`, `SearchKnowledgeDataListToolSchemaEventHandler`, `SearchKnowledgeDataToolEventHandler` (+8).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezyai.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `KnowledgeDataFetcherEventSchemaFetcher`, `KnowledgeDataListFetcherEventSchemaFetcher`, `SearchKnowledgeDataListToolEventHandler`, `SearchKnowledgeDataListToolSchemaEventHandler`, `SearchKnowledgeDataToolEventHandler`, `SearchKnowledgeDataToolSchemaEventHandler`, `ChatBotStreamEventHandler`, `SocketPluginEzyAIServerReadyController`, `SocketEzyAIMcpEventHandlerProvider`, `SocketSearchKnowledgeDataListToolEventHandler` (+3).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyai/ai-chat-services` và Web `/ezyai/skill-library` → 200; không gọi nhà cung cấp AI.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Lưu ý khi tích hợp

Tách adapter nhà cung cấp khỏi logic ứng dụng. HTTP 200 trên trang danh mục không chứng minh gọi model thành công.

[Về chỉ mục plugin](README.md)
