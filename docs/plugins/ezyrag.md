# ezyrag

Quản trị RAG và tích hợp lớp AI.

- **Bản Marketplace trên core 1.5.9:** `0.0.6`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Đạt qua Admin. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyrag` | `org.youngmonkeys.ezyrag` | Không khai báo |
| `web-plugin` — `web/plugins/ezyrag` | `org.youngmonkeys.ezyrag` | Không khai báo |
| `socket-plugin` — `socket/plugins/ezyrag` | `org.youngmonkeys.ezyrag` | [ezyai](ezyai.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 25 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyRagSettingController` |
| `GET /data-chunks` | `AdminDataChunkController` |
| `GET /embedding-services` | `AdminEmbeddingServiceController` |
| `GET /vector-database-services` | `AdminVectorDatabaseServiceController` |
| `GET /api/v1/data-chunks` | `AdminApiDataChunkController` |
| `GET /api/v1/vector-collections` | `AdminApiVectorCollectionController` |
| `GET /embedding-services/{serviceName}` | `AdminEmbeddingServiceController` |
| `POST /api/v1/chunk-data` | `AdminApiDataChunkController` |
| `POST /api/v1/chunk-data/search` | `AdminApiDataChunkController` |
| `POST /api/v1/vector-collections/add` | `AdminApiVectorCollectionController` |
| `PUT /api/v1/settings` | `AdminApiEzyRagSettingController` |
| `PUT /api/v1/vector-database-services/QDRANT/connection-properties` | `AdminApiVectorDatabaseServiceController` |
| `PUT /api/v1/vector-database-services/EZYVECTOR/connection-properties` | `AdminApiVectorDatabaseServiceController` |
| `PUT /api/v1/vector-collections/{id}` | `AdminApiVectorCollectionController` |
| `DELETE /api/v1/data-chunks/{id}` | `AdminApiDataChunkController` |
| `DELETE /api/v1/vector-collections/{id}` | `AdminApiVectorCollectionController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyrag: /`, `data_chunks: /data-chunks`, `embedding_services: /embedding-services`, `embedding_services_details: ~/embedding-services/{serviceName}`, `vector_database_services: /vector-database-services`, `vector_database_services_details: ~/vector-database-services/{serviceName}` (+1).

- **admin-plugin – Template:** `ezyrag/chunk/chunk-data.html`, `ezyrag/chunk/chunk-list.html`, `ezyrag/chunk/list.html`, `ezyrag/chunk/scripts.html`, `ezyrag/collection/add.html`, `ezyrag/collection/collection-list.html`, `ezyrag/collection/details.html` (+8).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (2):** `ezyrag_data_chunks`, `ezyrag_vector_collections`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (2):** `RagDataChunk`, `RagVectorCollection`.
- **SQL admin-plugin (3 tệp):** `resources/scripts/collection.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_data_chunk.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyrag-admin-plugin-0.0.6.jar`, `ezyrag-sdk-0.0.6.jar`; 170 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyrag.model`, `org.youngmonkeys.ezyrag.pagination`, `org.youngmonkeys.ezyrag.reader` (+38).
- **JAR thư viện khác:** `SparseBitSet-1.3.jar`, `commons-codec-1.16.0.jar`, `commons-collections4-4.4.jar`, `commons-compress-1.25.0.jar` (+11).
- **Controller/service/repository (mẫu):** `AdminApiDataChunkController`, `AdminApiEmbeddingServiceController`, `AdminApiEzyRagSettingController`, `AdminApiVectorCollectionController`, `AdminEzyRagSettingService`, `AdminPaginationRagDataChunkRepository`, `AdminPaginationRagDataChunkService`, `AdminPaginationRagVectorCollectionRepository`, `AdminPaginationRagVectorCollectionService`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminEzyRagClient`, `AdminNormalizeQueryProcessor`, `AdminRagDataChunkerManager`, `AdminRagDataLoaderManager`, `AdminRagDataRetrieverManager`, `AdminRagEmbeddingServiceManager`, `AdminRagKnowledgeDataBuilderManager`, `AdminRagMediaTextReaderManager`, `AdminRagQueryProcessorManager` (+14).

### web-plugin

- **JAR kiểm tra:** `ezyrag-sdk-0.0.6.jar`, `ezyrag-web-plugin-0.0.6.jar`; 142 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyrag.model`, `org.youngmonkeys.ezyrag.pagination`, `org.youngmonkeys.ezyrag.reader` (+31).
- **JAR thư viện khác:** `SparseBitSet-1.3.jar`, `commons-codec-1.16.0.jar`, `commons-collections4-4.4.jar`, `commons-compress-1.25.0.jar` (+11).
- **Controller/service/repository (mẫu):** `EzyRagSettingService`, `PaginationRagDataChunkRepository`, `PaginationRagDataChunkService`, `PaginationRagVectorCollectionRepository`, `PaginationRagVectorCollectionService`.
- **Điểm mở rộng tiềm năng theo tên class:** `EzyRagClient`, `NormalizeQueryProcessor`, `RagDataChunkerManager`, `RagDataLoaderManager`, `RagDataRetrieverManager`, `RagEmbeddingServiceManager`, `RagKnowledgeDataBuilderManager`, `RagMediaTextReaderManager`, `RagQueryProcessor` (+14).

### socket-plugin

- **JAR kiểm tra:** `ezyrag-sdk-0.0.6.jar`, `ezyrag-socket-plugin-0.0.6.jar`; 131 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyrag.model`, `org.youngmonkeys.ezyrag.pagination`, `org.youngmonkeys.ezyrag.reader` (+32).
- **Controller/service/repository (mẫu):** `UserLoginController`, `EzyRagSettingService`, `PaginationRagDataChunkRepository`, `PaginationRagDataChunkService`, `PaginationRagVectorCollectionRepository`, `PaginationRagVectorCollectionService`.
- **Điểm mở rộng tiềm năng theo tên class:** `EzyRagClient`, `NormalizeQueryProcessor`, `PluginEntryLoader`, `RagDataChunkerManager`, `RagDataLoaderManager`, `RagDataRetrieverManager`, `RagEmbeddingServiceManager`, `RagKnowledgeDataBuilderManager`, `RagMediaTextReaderManager` (+14).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezyrag.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `UserLoginController`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyrag/settings` → 200; phụ thuộc `ezyai`; chưa gọi nhà cung cấp embedding/LLM.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Áp dụng cho plugin quản lý công việc

Chỉ cân nhắc cho tìm kiếm tri thức giai đoạn sau. Các kết quả truy xuất phải lọc đúng workspace; cài plugin và mở settings không chứng minh chuỗi embedding/truy vấn.

[Về chỉ mục plugin](README.md)
