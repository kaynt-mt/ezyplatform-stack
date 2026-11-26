# ezyvector

Vector collections and data management.

- **Marketplace version on core 1.5.9:** `0.0.5`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyvector` | `org.youngmonkeys.ezyvector` | Not declared |
| `web-plugin` — `web/plugins/ezyvector` | `org.youngmonkeys.ezyvector` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 7 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyVectorSettingController` |
| `GET /vector-collections` | `AdminVectorCollectionController` |
| `GET /api/v1/vector-collections` | `AdminApiVectorCollectionController` |
| `GET /vector-collections/{id}` | `AdminVectorCollectionController` |
| `GET /api/v1/vector-collections/{collectionId}/points` | `AdminApiVectorCollectionController` |
| `GET /api/v1/vector-collections/{collectionId}/segments` | `AdminApiVectorCollectionController` |
| `PUT /api/v1/settings/collections` | `AdminApiEzyVectorSettingController` |

**web-plugin** — 5 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /ezyvector/collections/{collectionName}` | `WebApiEzyVectorCollectionController` |
| `POST /ezyvector/collections/{collectionName}/points/delete` | `WebApiEzyVectorCollectionController` |
| `POST /ezyvector/collections/{collectionName}/points/search` | `WebApiEzyVectorCollectionController` |
| `PUT /ezyvector/collections/{collectionName}` | `WebApiEzyVectorCollectionController` |
| `PUT /ezyvector/collections/{collectionName}/points` | `WebApiEzyVectorCollectionController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyvector: /`, `vector_collections: /vector-collections`, `vector_collections_details: ~/vector-collections/{id}`, `settings: /settings`.

- **admin-plugin – Template:** `ezyvector/collection/collection-list.html`, `ezyvector/collection/collection-point-list.html`, `ezyvector/collection/collection-segment-list.html`, `ezyvector/collection/details.html`, `ezyvector/collection/list.html`, `ezyvector/collection/scripts.html`, `ezyvector/setting/index.html`.

## Data and migrations

- **Table in the DDL package (3):** `ezyvector_collection_points`, `ezyvector_collection_segments`, `ezyvector_collections`.
- **Class with JPA Entity/MappedSuperclass (3):** `EzyVectorCollection`, `EzyVectorCollectionPoint`, `EzyVectorCollectionSegment`.
- **SQL admin-plugin (1 file):** `resources/scripts/scripts.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyvector-admin-plugin-0.0.5.jar`, `ezyvector-sdk-0.0.5.jar`; 83 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyvector.pagination`, `org.youngmonkeys.ezyvector.entity`, `org.youngmonkeys.ezyvector.admin.repo` (+17).
- **Controllers, services, and repositories (sample):** `AdminApiEzyVectorSettingController`, `AdminApiVectorCollectionController`, `AdminEzyVectorCollectionControllerService`, `AdminEzyVectorSettingController`, `AdminEzyVectorCollectionControllerService`, `AdminEzyVectorCollectionPointRepository`, `AdminEzyVectorCollectionRepository`, `AdminEzyVectorCollectionSegmentRepository`, `AdminEzyVectorCollectionService`.

### web-plugin

- **JARs inspected:** `ezyvector-sdk-0.0.5.jar`, `ezyvector-web-plugin-0.0.5.jar`; 93 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyvector.pagination`, `org.youngmonkeys.ezyvector.entity`, `org.youngmonkeys.ezyvector.repo` (+17).
- **Controllers, services, and repositories (sample):** `WebApiEzyVectorCollectionController`, `WebEzyVectorCollectionControllerService`, `WebEzyVectorPointsControllerService`, `WebEzyVectorSearchControllerService`, `EzyVectorCollectionPointRepository`, `EzyVectorCollectionRepository`, `EzyVectorCollectionSegmentRepository`, `EzyVectorCollectionService`, `EzyVectorService`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyvector/vector-collections` returned 200. No dataset was loaded and no vector queries were benchmarked.

## Integration notes

Add vector search only when measurements show a need. Verify result quality and access scope for private data.

[Back to the plugin index](README.md)
