# ezyai

AI service configuration, skills, and the skill library.

- **Marketplace version on core 1.5.9:** `0.1.8`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyai` | `org.youngmonkeys.ezyai` | [graphql](graphql.md), [ezychat](ezychat.md) |
| `web-plugin` — `web/plugins/ezyai` | `org.youngmonkeys.ezyai` | [graphql](graphql.md), [ezychat](ezychat.md) |
| `socket-plugin` — `socket/plugins/ezyai` | `org.youngmonkeys.ezyai.socket.plugin` | [graphql](graphql.md), [ezychat](ezychat.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 52 method/URI combinations identified; representative sample:

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

**web-plugin** — 16 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyai: /`, `ai_chat_services: /ai-chat-services`, `ai_chat_services_details: ~/ai-chat-services/{serviceName}`, `ai_chat_services_profile_add: ~/ai-chat-services/{serviceName}/profiles/add`, `ai_chat_services_profile_details: ~/ai-chat-services/{serviceName}/profiles/{profileName}`, `ai_chat_services_profile_edit: ~/ai-chat-services/{serviceName}/profiles/{profileName}/edit` (+10).

- **admin-plugin – Template:** `ezyai/ai-chat-services/chat.html`, `ezyai/ai-chat-services/list.html`, `ezyai/ai-chat-services/profile/add.html`, `ezyai/ai-chat-services/profile/details.html`, `ezyai/ai-chat-services/profile/edit.html`, `ezyai/ai-chat-services/profile/scripts.html`, `ezyai/ai-chat-services/profiles.html` (+17).

- **admin-plugin – Static resources:** `ezyai/js/skill-package-reader.js`.

- **admin-plugin – Configuration and template resources:** `ezyai/letter_template_skill_library_approved.properties`, `ezyai/letter_template_skill_library_update_approved.properties`, `ezyai/letter_template_skill_library_update_rejected.properties`, `ezyai/notification_template_skill_library_approved.properties` (+2).

- **web-plugin – Template:** `ezyai/fragments/my-skill-library.html`, `ezyai/my-skill-library.html`, `ezyai/skill-library-detail.html`, `ezyai/skill-library.html`.

- **web-plugin – Static resources:** `ezyai/css/skill-library.css`, `ezyai/js/skill-library.js`, `ezyai/js/skill-package-reader.js`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyai-admin-plugin-0.1.8.jar`, `ezyai-sdk-0.1.8.jar`; 172 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyai.service`, `org.youngmonkeys.ezyai.admin.service`, `org.youngmonkeys.ezyai.model` (+30).
- **Controllers, services, and repositories (sample):** `AdminAIChatControllerService`, `AdminAIChatProfileController`, `AdminAIChatProfileControllerService`, `AdminAIChatServiceController`, `AIChatBotService`, `AISkillService`, `AbstractAIChatService`, `AdminAIChatControllerService`, `AdminAIChatProfileControllerService`.
- **Configuration and permission classes (sample):** `AdminEzyAIPageFragmentConfig`, `AdminEzyAIPostTypeConfig`, `AdminEzyAIProductTypeConfig`, `AdminEzyAITemplateConfig`, `AdminEzyAITermTypeConfig`, `AdminEzyAIUserRoleConfig`, `AdminEzyAIViewMetadataConfig` (+1).
- **Configuration and template keys from resources (values omitted):** `content`, `title`.
- **Potential extension points based on class names:** `AIChatToolProvider`, `AdminKnowledgeDataSourceManager`, `AdminMcpAIChatToolProvider`, `AdminSearchKnowledgeDataListToolEventHandler`, `AdminSearchKnowledgeDataListToolSchemaEventHandler`, `AdminSearchKnowledgeDataToolEventHandler`, `AdminSearchKnowledgeDataToolSchemaEventHandler`, `ChatBotStreamEventHandler`, `KnowledgeDataSourceManager` (+6).

### web-plugin

- **JARs inspected:** `ezyai-sdk-0.1.8.jar`, `ezyai-web-plugin-0.1.8.jar`; 144 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyai.service`, `org.youngmonkeys.ezyai.web.service`, `org.youngmonkeys.ezyai.model` (+27).
- **Controllers, services, and repositories (sample):** `WebAccountSkillLibraryController`, `WebApiAccountSkillLibraryController`, `WebApiSkillLibraryController`, `WebSkillLibraryController`, `AIChatBotService`, `AISkillService`, `AbstractAIChatService`, `AbstractWebSkillLibrarySaveEventSchemaFetcher`, `ChatGptChatService`.
- **Configuration and permission classes (sample):** `EzyAIPageFragmentConfig`, `WebEzyAIPageFragmentConfig`.
- **Potential extension points based on class names:** `AIChatToolProvider`, `ChatBotStreamEventHandler`, `KnowledgeDataSourceManager`, `KnowledgeDataSourceProvider`, `McpAIChatToolProvider`, `SearchKnowledgeDataListToolEventHandler`, `SearchKnowledgeDataListToolSchemaEventHandler`, `SearchKnowledgeDataToolEventHandler`, `SearchKnowledgeDataToolSchemaEventHandler` (+6).

### socket-plugin

- **JARs inspected:** `ezyai-sdk-0.1.8.jar`, `ezyai-socket-plugin-0.1.8.jar`; 118 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyai.service`, `org.youngmonkeys.ezyai.model`, `org.youngmonkeys.ezyai.knowledge` (+22).
- **Other library JARs:** `jsoup-1.18.3.jar`.
- **Controllers, services, and repositories (sample):** `McpToolsRequestController`, `SocketPluginEzyAIServerReadyController`, `AIChatBotService`, `AISkillService`, `AbstractAIChatService`, `ChatGptChatService`, `ClaudeChatService`.
- **Configuration and permission classes (sample):** `EzyAIPageFragmentConfig`.
- **Potential extension points based on class names:** `AIChatToolProvider`, `ChatBotStreamEventHandler`, `KnowledgeDataSourceManager`, `KnowledgeDataSourceProvider`, `McpAIChatToolProvider`, `PluginEntryLoader`, `SearchKnowledgeDataListToolEventHandler`, `SearchKnowledgeDataListToolSchemaEventHandler`, `SearchKnowledgeDataToolEventHandler` (+8).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezyai.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `KnowledgeDataFetcherEventSchemaFetcher`, `KnowledgeDataListFetcherEventSchemaFetcher`, `SearchKnowledgeDataListToolEventHandler`, `SearchKnowledgeDataListToolSchemaEventHandler`, `SearchKnowledgeDataToolEventHandler`, `SearchKnowledgeDataToolSchemaEventHandler`, `ChatBotStreamEventHandler`, `SocketPluginEzyAIServerReadyController`, `SocketEzyAIMcpEventHandlerProvider`, `SocketSearchKnowledgeDataListToolEventHandler` (+3).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyai/ai-chat-services` and Web `/ezyai/skill-library` returned 200. No AI provider was called.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Keep provider adapters separate from application logic. A 200 from the catalog page does not prove that a model call works.

[Back to the plugin index](README.md)
