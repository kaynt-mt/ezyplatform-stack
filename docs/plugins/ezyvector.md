# ezyvector

Collection và quản trị dữ liệu vector.

- **Bản Marketplace trên core 1.5.9:** `0.0.5`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyvector` | `org.youngmonkeys.ezyvector` | Không khai báo |
| `web-plugin` — `web/plugins/ezyvector` | `org.youngmonkeys.ezyvector` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 7 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminEzyVectorSettingController` |
| `GET /vector-collections` | `AdminVectorCollectionController` |
| `GET /api/v1/vector-collections` | `AdminApiVectorCollectionController` |
| `GET /vector-collections/{id}` | `AdminVectorCollectionController` |
| `GET /api/v1/vector-collections/{collectionId}/points` | `AdminApiVectorCollectionController` |
| `GET /api/v1/vector-collections/{collectionId}/segments` | `AdminApiVectorCollectionController` |
| `PUT /api/v1/settings/collections` | `AdminApiEzyVectorSettingController` |

**web-plugin** — 5 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /ezyvector/collections/{collectionName}` | `WebApiEzyVectorCollectionController` |
| `POST /ezyvector/collections/{collectionName}/points/delete` | `WebApiEzyVectorCollectionController` |
| `POST /ezyvector/collections/{collectionName}/points/search` | `WebApiEzyVectorCollectionController` |
| `PUT /ezyvector/collections/{collectionName}` | `WebApiEzyVectorCollectionController` |
| `PUT /ezyvector/collections/{collectionName}/points` | `WebApiEzyVectorCollectionController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyvector: /`, `vector_collections: /vector-collections`, `vector_collections_details: ~/vector-collections/{id}`, `settings: /settings`.

- **admin-plugin – Template:** `ezyvector/collection/collection-list.html`, `ezyvector/collection/collection-point-list.html`, `ezyvector/collection/collection-segment-list.html`, `ezyvector/collection/details.html`, `ezyvector/collection/list.html`, `ezyvector/collection/scripts.html`, `ezyvector/setting/index.html`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (3):** `ezyvector_collection_points`, `ezyvector_collection_segments`, `ezyvector_collections`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (3):** `EzyVectorCollection`, `EzyVectorCollectionPoint`, `EzyVectorCollectionSegment`.
- **SQL admin-plugin (1 tệp):** `resources/scripts/scripts.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyvector-admin-plugin-0.0.5.jar`, `ezyvector-sdk-0.0.5.jar`; 83 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyvector.pagination`, `org.youngmonkeys.ezyvector.entity`, `org.youngmonkeys.ezyvector.admin.repo` (+17).
- **Controller/service/repository (mẫu):** `AdminApiEzyVectorSettingController`, `AdminApiVectorCollectionController`, `AdminEzyVectorCollectionControllerService`, `AdminEzyVectorSettingController`, `AdminEzyVectorCollectionControllerService`, `AdminEzyVectorCollectionPointRepository`, `AdminEzyVectorCollectionRepository`, `AdminEzyVectorCollectionSegmentRepository`, `AdminEzyVectorCollectionService`.

### web-plugin

- **JAR kiểm tra:** `ezyvector-sdk-0.0.5.jar`, `ezyvector-web-plugin-0.0.5.jar`; 93 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyvector.pagination`, `org.youngmonkeys.ezyvector.entity`, `org.youngmonkeys.ezyvector.repo` (+17).
- **Controller/service/repository (mẫu):** `WebApiEzyVectorCollectionController`, `WebEzyVectorCollectionControllerService`, `WebEzyVectorPointsControllerService`, `WebEzyVectorSearchControllerService`, `EzyVectorCollectionPointRepository`, `EzyVectorCollectionRepository`, `EzyVectorCollectionSegmentRepository`, `EzyVectorCollectionService`, `EzyVectorService`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyvector/vector-collections` → 200; chưa nạp bộ dữ liệu/đo truy vấn vector.

## Lưu ý khi tích hợp

Chỉ thêm vector khi có nhu cầu đã đo được; kiểm chất lượng kết quả và phạm vi truy cập của dữ liệu riêng tư.

[Về chỉ mục plugin](README.md)
