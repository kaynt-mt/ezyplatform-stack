# graphql

GraphQL endpoint and schema configuration.

- **Marketplace version on core 1.5.9:** `0.3.1`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/graphql` | `org.youngmonkeys.graphql` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/graphql` | `org.youngmonkeys.graphql` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md) |
| `socket-plugin` — `socket/plugins/graphql` | `org.youngmonkeys.graphql.socket.plugin` | [ecommerce](ecommerce.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 52 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /mcp` | `AdminMcpServerController` |
| `GET /settings` | `AdminGraphQLSettingController` |
| `GET /api-types` | `AdminApiTypeController` |
| `GET /system-endpoints` | `AdminGraphQLSystemEndpointController` |
| `GET /api/v1/sql-scripts` | `AdminGraphQLApiSqlScriptsController` |
| `GET /api/v1/system-endpoints` | `AdminGraphQLApiSystemEndpointController` |
| `GET /api/v1/page-type-descriptions` | `AdminGraphQLApiPageTypeDescriptionController` |
| `POST /mcp` | `AdminMcpServerController` |
| `POST /api/v1/fetch-data` | `AdminGraphQLApiDataFetchingController` |
| `POST /api/v1/system-event` | `AdminGraphqlApiSystemEventController` |
| `POST /api/v1/event-handler/save` | `AdminGraphQLApiEventHandlerAuthoringController` |
| `PUT /api/v1/settings` | `AdminGraphQLApiSettingController` |
| `PUT /api/v1/system-endpoints/{id}` | `AdminGraphQLApiSystemEndpointController` |
| `DELETE /api/v1/system-endpoints/{id}` | `AdminGraphQLApiSystemEndpointController` |

**web-plugin** — 19 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /graphql/mcp` | `WebMcpServerController` |
| `GET /rest/swagger` | `WebGraphQLRestSwaggerController` |
| `GET /graphql/schema` | `WebGraphQLSchemaController` |
| `GET /management/rest/swagger` | `WebGraphQLRestSwaggerManagementController` |
| `GET /management/graphql/schema` | `WebGraphQLSchemaManagementController` |
| `GET /api/v1/rest/swagger.yaml` | `WebApiGraphQLRestSwaggerController` |
| `GET /api/v1/graphql/schema.graphql` | `WebApiGraphQLSchemaController` |
| `POST /graphql/mcp` | `WebMcpServerController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `graphql: /`, `system_endpoints: /system-endpoints`, `api_types: /api-types`, `settings: /settings`.

- **admin-plugin – Template:** `graphql/api-type/index.html`, `graphql/schema/index.html`, `graphql/setting/index.html`, `graphql/swagger/swagger.html`, `graphql/system-endpoint/index.html`.

- **admin-plugin – Static resources:** `graphql/css/swagger-ui.css`, `graphql/js/swagger-ui-bundle.js`.

- **admin-plugin – Configuration and template resources:** `graphql.properties`.

- **web-plugin – Template:** `graphql/schema.html`, `graphql/swagger.html`.

- **web-plugin – Static resources:** `graphql/css/swagger-ui.css`, `graphql/js/swagger-ui-bundle.js`.

- **Web-plugin – Configuration/Sample Resource:** `graphql.properties`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `graphql-admin-plugin-0.3.1.jar`, `graphql-sdk-0.3.1.jar`; 334 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.graphql.admin.event`, `org.youngmonkeys.graphql.admin.controller.api`, `org.youngmonkeys.graphql.event` (+26).
- **Other library JARs:** `ezyhttp-server-graphql-1.6.5.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiMcpToolsController`, `AdminApiTypeController`, `AdminGraphQLApiClassSchemaController`, `AdminGraphQLApiContentTypeDescriptionController`, `AdminEventHandlerAuthoringService`, `AdminGraphQLDataFetchingService`, `AdminGraphQLDataRepository`, `AdminGraphQLDataService`, `AdminGraphQLFetcherAuthoringService`.
- **Configuration and permission classes (sample):** `AdminGraphQLConfig`, `AdminGraphQLPostConfig`.
- **Configuration and template keys from resources (values omitted):** `graphql.authenticated`, `graphql.enable`.
- **Potential extension points based on class names:** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `AdminEzySystemEventHandler`, `AdminGraphQLConfigFileManager`, `AdminGraphQLFetchPostTypeDescriptionEventHandler`, `AdminGraphQLObjectMapperProvider`, `AdminGraphQLSqlScriptFilesInputStreamFactory`, `AdminMcpAdminDataFetchingGuideResourceEventHandler`, `AdminMcpAdminDataFetchingGuideResourceSchemaEventHandler`, `AdminMcpAdminGraphQLDataFetchingToolEventHandler` (+212).

### web-plugin

- **JARs inspected:** `graphql-sdk-0.3.1.jar`, `graphql-web-plugin-0.3.1.jar`; 129 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.graphql.event`, `org.youngmonkeys.graphql.web.event`, `org.youngmonkeys.graphql.web.controller.api` (+21).
- **Other library JARs:** `ezyhttp-server-graphql-1.6.5.jar`.
- **Controllers, services, and repositories (sample):** `WebApiGraphQLClassSchemaManagementController`, `WebApiGraphQLEventSchemaManagementController`, `WebApiGraphQLEzyFunctionSchemaManagementController`, `WebApiGraphQLRestSwaggerController`, `GraphQLDataRepository`, `GraphQLDataService`, `GraphQLPostRepository`, `GraphQLSettingService`, `GraphQLSkillLibraryToolService`.
- **Configuration and permission classes (sample):** `WebGraphQLConfig`, `WebGraphQLControllerConfig`.
- **Configuration and template keys from resources (values omitted):** `graphql.enable`.
- **Potential extension points based on class names:** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `GraphQLDataFetcherListingProvider`, `GraphQLMcpCompletionCompleteMethodEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolSchemaEventHandler`, `GraphQLMcpFetchProductPriceToolEventHandler`, `GraphQLMcpFetchProductPriceToolSchemaEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptSchemaEventHandler` (+45).

### socket-plugin

- **JARs inspected:** `graphql-sdk-0.3.1.jar`, `graphql-socket-plugin-0.3.1.jar`; 78 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.graphql.event`, `org.youngmonkeys.graphql.result`, `org.youngmonkeys.graphql.socket.plugin.event` (+11).
- **Other library JARs:** `ezyhttp-server-graphql-1.6.5.jar`.
- **Controllers, services, and repositories (sample):** `GraphQLDataRepository`, `GraphQLDataService`, `GraphQLPostRepository`, `GraphQLSettingService`, `GraphQLSkillLibraryToolService`.
- **Potential extension points based on class names:** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `GraphQLDataFetcherListingProvider`, `GraphQLMcpCompletionCompleteMethodEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolSchemaEventHandler`, `GraphQLMcpFetchProductPriceToolEventHandler`, `GraphQLMcpFetchProductPriceToolSchemaEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptSchemaEventHandler` (+28).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.graphql.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `GraphQLMcpCompletionCompleteMethodEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolSchemaEventHandler`, `GraphQLMcpFetchProductPriceToolEventHandler`, `GraphQLMcpFetchProductPriceToolSchemaEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptSchemaEventHandler`, `GraphQLMcpGetSkillToolEventHandler`, `GraphQLMcpGetSkillToolSchemaEventHandler` (+23).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/graphql/system-endpoints` returned 200; `/rest/swagger` and the schema URLs tested showed a “Not found” page in Freestyle. No GraphQL queries were run.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

See the schema and fetcher patterns. Check the Ecommerce dependency, resolver permissions, and query counts before enabling the module.

[Back to the plugin index](README.md)
