# graphql

Cấu hình endpoint và schema GraphQL.

- **Bản Marketplace trên core 1.5.9:** `0.3.1`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/graphql` | `org.youngmonkeys.graphql` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/graphql` | `org.youngmonkeys.graphql` | [ezyarticle](ezyarticle.md), [ecommerce](ecommerce.md) |
| `socket-plugin` — `socket/plugins/graphql` | `org.youngmonkeys.graphql.socket.plugin` | [ecommerce](ecommerce.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 52 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

**web-plugin** — 19 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `graphql: /`, `system_endpoints: /system-endpoints`, `api_types: /api-types`, `settings: /settings`.

- **admin-plugin – Template:** `graphql/api-type/index.html`, `graphql/schema/index.html`, `graphql/setting/index.html`, `graphql/swagger/swagger.html`, `graphql/system-endpoint/index.html`.

- **admin-plugin – Tài nguyên tĩnh:** `graphql/css/swagger-ui.css`, `graphql/js/swagger-ui-bundle.js`.

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `graphql.properties`.

- **web-plugin – Template:** `graphql/schema.html`, `graphql/swagger.html`.

- **web-plugin – Tài nguyên tĩnh:** `graphql/css/swagger-ui.css`, `graphql/js/swagger-ui-bundle.js`.

- **web-plugin – Tài nguyên cấu hình/mẫu:** `graphql.properties`.

## Dữ liệu và migration

- Không tìm thấy `CREATE TABLE` trong các tệp SQL rời của gói; không suy ra module không lưu dữ liệu hoặc không dùng schema của core.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `graphql-admin-plugin-0.3.1.jar`, `graphql-sdk-0.3.1.jar`; 334 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.graphql.admin.event`, `org.youngmonkeys.graphql.admin.controller.api`, `org.youngmonkeys.graphql.event` (+26).
- **JAR thư viện khác:** `ezyhttp-server-graphql-1.6.5.jar`.
- **Controller/service/repository (mẫu):** `AdminApiMcpToolsController`, `AdminApiTypeController`, `AdminGraphQLApiClassSchemaController`, `AdminGraphQLApiContentTypeDescriptionController`, `AdminEventHandlerAuthoringService`, `AdminGraphQLDataFetchingService`, `AdminGraphQLDataRepository`, `AdminGraphQLDataService`, `AdminGraphQLFetcherAuthoringService`.
- **Class cấu hình/quyền (mẫu):** `AdminGraphQLConfig`, `AdminGraphQLPostConfig`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `graphql.authenticated`, `graphql.enable`.
- **Điểm mở rộng tiềm năng theo tên class:** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `AdminEzySystemEventHandler`, `AdminGraphQLConfigFileManager`, `AdminGraphQLFetchPostTypeDescriptionEventHandler`, `AdminGraphQLObjectMapperProvider`, `AdminGraphQLSqlScriptFilesInputStreamFactory`, `AdminMcpAdminDataFetchingGuideResourceEventHandler`, `AdminMcpAdminDataFetchingGuideResourceSchemaEventHandler`, `AdminMcpAdminGraphQLDataFetchingToolEventHandler` (+212).

### web-plugin

- **JAR kiểm tra:** `graphql-sdk-0.3.1.jar`, `graphql-web-plugin-0.3.1.jar`; 129 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.graphql.event`, `org.youngmonkeys.graphql.web.event`, `org.youngmonkeys.graphql.web.controller.api` (+21).
- **JAR thư viện khác:** `ezyhttp-server-graphql-1.6.5.jar`.
- **Controller/service/repository (mẫu):** `WebApiGraphQLClassSchemaManagementController`, `WebApiGraphQLEventSchemaManagementController`, `WebApiGraphQLEzyFunctionSchemaManagementController`, `WebApiGraphQLRestSwaggerController`, `GraphQLDataRepository`, `GraphQLDataService`, `GraphQLPostRepository`, `GraphQLSettingService`, `GraphQLSkillLibraryToolService`.
- **Class cấu hình/quyền (mẫu):** `WebGraphQLConfig`, `WebGraphQLControllerConfig`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `graphql.enable`.
- **Điểm mở rộng tiềm năng theo tên class:** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `GraphQLDataFetcherListingProvider`, `GraphQLMcpCompletionCompleteMethodEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolSchemaEventHandler`, `GraphQLMcpFetchProductPriceToolEventHandler`, `GraphQLMcpFetchProductPriceToolSchemaEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptSchemaEventHandler` (+45).

### socket-plugin

- **JAR kiểm tra:** `graphql-sdk-0.3.1.jar`, `graphql-socket-plugin-0.3.1.jar`; 78 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.graphql.event`, `org.youngmonkeys.graphql.result`, `org.youngmonkeys.graphql.socket.plugin.event` (+11).
- **JAR thư viện khác:** `ezyhttp-server-graphql-1.6.5.jar`.
- **Controller/service/repository (mẫu):** `GraphQLDataRepository`, `GraphQLDataService`, `GraphQLPostRepository`, `GraphQLSettingService`, `GraphQLSkillLibraryToolService`.
- **Điểm mở rộng tiềm năng theo tên class:** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `GraphQLDataFetcherListingProvider`, `GraphQLMcpCompletionCompleteMethodEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolSchemaEventHandler`, `GraphQLMcpFetchProductPriceToolEventHandler`, `GraphQLMcpFetchProductPriceToolSchemaEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptSchemaEventHandler` (+28).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.graphql.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `AbstractGraphQLMcpSkillLibraryToolEventHandler`, `GraphQLMcpCompletionCompleteMethodEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolEventHandler`, `GraphQLMcpCreateProductCheckoutLinkToolSchemaEventHandler`, `GraphQLMcpFetchProductPriceToolEventHandler`, `GraphQLMcpFetchProductPriceToolSchemaEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptEventHandler`, `GraphQLMcpGenerateCheckoutLinkPromptSchemaEventHandler`, `GraphQLMcpGetSkillToolEventHandler`, `GraphQLMcpGetSkillToolSchemaEventHandler` (+23).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/graphql/system-endpoints` → 200; `/rest/swagger` và URL schema đã thử trả trang “Not found” trên Freestyle. Chưa chạy truy vấn GraphQL.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Áp dụng cho plugin quản lý công việc

Tham khảo cách tổ chức schema/fetcher nếu thật sự cần GraphQL. Lõi task nên đi từ API HTTP dễ thử; cân nhắc chi phí phụ thuộc Ecommerce và ACL ở resolver trước khi bật.

[Về chỉ mục plugin](README.md)
