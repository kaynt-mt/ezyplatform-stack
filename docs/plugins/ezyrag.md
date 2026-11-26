# ezyrag

RAG administration and integration with the AI layer.

- **Marketplace version on core 1.5.9:** `0.0.6`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** Get through Admin. See the environment and general limits in [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyrag` | `org.youngmonkeys.ezyrag` | Not declared |
| `web-plugin` — `web/plugins/ezyrag` | `org.youngmonkeys.ezyrag` | Not declared |
| `socket-plugin` — `socket/plugins/ezyrag` | `org.youngmonkeys.ezyrag` | [ezyai](ezyai.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 25 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyrag: /`, `data_chunks: /data-chunks`, `embedding_services: /embedding-services`, `embedding_services_details: ~/embedding-services/{serviceName}`, `vector_database_services: /vector-database-services`, `vector_database_services_details: ~/vector-database-services/{serviceName}` (+1).

- **admin-plugin – Template:** `ezyrag/chunk/chunk-data.html`, `ezyrag/chunk/chunk-list.html`, `ezyrag/chunk/list.html`, `ezyrag/chunk/scripts.html`, `ezyrag/collection/add.html`, `ezyrag/collection/collection-list.html`, `ezyrag/collection/details.html` (+8).

## Data and migrations

- **Table in the DDL package (2):** `ezyrag_data_chunks`, `ezyrag_vector_collections`.
- **Class with JPA Entity/MappedSuperclass (2):** `RagDataChunk`, `RagVectorCollection`.
- **SQL admin-plugin (3 files):** `resources/scripts/collection.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_data_chunk.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyrag-admin-plugin-0.0.6.jar`, `ezyrag-sdk-0.0.6.jar`; 170 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyrag.model`, `org.youngmonkeys.ezyrag.pagination`, `org.youngmonkeys.ezyrag.reader` (+38).
- **Other library JARs:** `SparseBitSet-1.3.jar`, `commons-codec-1.16.0.jar`, `commons-collections4-4.4.jar`, `commons-compress-1.25.0.jar` (+11).
- **Controllers, services, and repositories (sample):** `AdminApiDataChunkController`, `AdminApiEmbeddingServiceController`, `AdminApiEzyRagSettingController`, `AdminApiVectorCollectionController`, `AdminEzyRagSettingService`, `AdminPaginationRagDataChunkRepository`, `AdminPaginationRagDataChunkService`, `AdminPaginationRagVectorCollectionRepository`, `AdminPaginationRagVectorCollectionService`.
- **Potential extension points based on class names:** `AdminEzyRagClient`, `AdminNormalizeQueryProcessor`, `AdminRagDataChunkerManager`, `AdminRagDataLoaderManager`, `AdminRagDataRetrieverManager`, `AdminRagEmbeddingServiceManager`, `AdminRagKnowledgeDataBuilderManager`, `AdminRagMediaTextReaderManager`, `AdminRagQueryProcessorManager` (+14).

### web-plugin

- **JARs inspected:** `ezyrag-sdk-0.0.6.jar`, `ezyrag-web-plugin-0.0.6.jar`; 142 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyrag.model`, `org.youngmonkeys.ezyrag.pagination`, `org.youngmonkeys.ezyrag.reader` (+31).
- **Other library JARs:** `SparseBitSet-1.3.jar`, `commons-codec-1.16.0.jar`, `commons-collections4-4.4.jar`, `commons-compress-1.25.0.jar` (+11).
- **Controllers, services, and repositories (sample):** `EzyRagSettingService`, `PaginationRagDataChunkRepository`, `PaginationRagDataChunkService`, `PaginationRagVectorCollectionRepository`, `PaginationRagVectorCollectionService`.
- **Potential extension points based on class names:** `EzyRagClient`, `NormalizeQueryProcessor`, `RagDataChunkerManager`, `RagDataLoaderManager`, `RagDataRetrieverManager`, `RagEmbeddingServiceManager`, `RagKnowledgeDataBuilderManager`, `RagMediaTextReaderManager`, `RagQueryProcessor` (+14).

### socket-plugin

- **JARs inspected:** `ezyrag-sdk-0.0.6.jar`, `ezyrag-socket-plugin-0.0.6.jar`; 131 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyrag.model`, `org.youngmonkeys.ezyrag.pagination`, `org.youngmonkeys.ezyrag.reader` (+32).
- **Controllers, services, and repositories (sample):** `UserLoginController`, `EzyRagSettingService`, `PaginationRagDataChunkRepository`, `PaginationRagDataChunkService`, `PaginationRagVectorCollectionRepository`, `PaginationRagVectorCollectionService`.
- **Potential extension points based on class names:** `EzyRagClient`, `NormalizeQueryProcessor`, `PluginEntryLoader`, `RagDataChunkerManager`, `RagDataLoaderManager`, `RagDataRetrieverManager`, `RagEmbeddingServiceManager`, `RagKnowledgeDataBuilderManager`, `RagMediaTextReaderManager` (+14).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezyrag.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `UserLoginController`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyrag/settings` returned 200. The module depends on `ezyai`; no embedding or LLM provider was called.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Enforce access scope on retrieval results. Opening settings does not verify the embedding and query pipeline.

[Back to the plugin index](README.md)
