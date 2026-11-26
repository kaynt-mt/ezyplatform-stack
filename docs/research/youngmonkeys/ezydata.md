# EzyData: scope truy vấn, transaction và projection

Nguồn: [Overview](https://youngmonkeys.org/projects/ezydata?lang=vi), [EzyJPA hoạt động](https://youngmonkeys.org/ezydata/guides/how-ezyjpa-works?lang=vi), [Query Data](https://youngmonkeys.org/ezydata/guides/ezyjpa-query-data?lang=vi), [Repository và Transactions](https://youngmonkeys.org/ezydata/guides/guide-to-ezydatabaserepository-ezyjparepository-and-transactions?lang=vi). MVP dùng MySQL của runtime và schema riêng; EzyMongo/EzyRedis là adapter khác, không phải yêu cầu của repository JPA.

## Quyết định truy vấn

1. Dùng `@EzyRepository` và `EzyDatabaseRepository` cho CRUD đơn giản có đủ scope, chẳng hạn ID cùng project sau khi policy đã xác định workspace; phương thức gốc như `findById`, `deleteByIds` không mang ACL. Giá trị người dùng là tham số, không ghép chuỗi query/sort.
2. Tài liệu cho thấy truy vấn theo tên dựa trên prefix/điều kiện được hỗ trợ, **không** suy ra sort từ `OrderBy...`. Dùng `@EzyQuery` viết rõ điều kiện, join và `order by`; đặc biệt không để nhánh OR lọt ra ngoài predicate workspace/project. Quy ước bind/index phải đối chiếu với artifact chạy thật, không đoán theo Spring Data.
3. `Next` là đối số cuối và được chuyển thành skip/limit, không phải cursor/keyset. Cho board và activity, định nghĩa thứ tự ổn định có tie-break ID; nếu cần keyset, tự cài điều kiện after-cursor trên cặp sort/ID và kiểm scope/filter trước khi dùng token. Scope cả count, search, autocomplete và export.
4. [Custom Query Result](https://youngmonkeys.org/ezydata/guides/ezyjpa-custom-query-result?lang=vi) phân biệt projection JPQL, scalar, aggregate và mapping result class của native query. Trả DTO cho list/board, không serialize entity có quan hệ lazy. Native SQL cần thử alias, kiểu dữ liệu `COUNT` và kết quả rỗng trên MySQL đích; index theo query thật và đo bằng `EXPLAIN` trên dev.

## Không nhầm transaction từng câu với transaction nghiệp vụ

Theo hướng dẫn repository, các write query tự sinh như `update...`/`delete...` có transaction riêng; read không mở write transaction. **Không suy ra** ba repository calls liên tiếp cùng commit. Với tạo work item (cấp sequence + item + activity) và move (so version + state/rank + activity), spike một phương thức `EzyJpaRepository` dùng chung `EntityManager` và một transaction, hoặc API transaction do core cung cấp nếu xác nhận được trên SDK đang pin. Khi quản lý tay: begin → ghi và flush khi cần → commit; khi lỗi rollback và luôn close. Không gọi side effect bên ngoài trong transaction, đặt outbox cùng transaction nếu sau này cần gửi tin. Kiểm bằng ca lỗi có chủ đích sau khi ghi một phần: item, counter, activity/outbox phải nhất quán theo hợp đồng.

## Cấu hình, migration và loại dữ liệu khác

- [EzyJPA configuration](https://youngmonkeys.org/ezydata/guides/ezyjpa-configuration?lang=vi) và [multi-datasource](https://youngmonkeys.org/ezydata/guides/ezyjpa-connect-multi-datasources?lang=vi) mô tả khởi tạo factory/context riêng và nhóm repository theo datasource. Plugin chỉ dùng context được nền tảng cấp cho core DB; không tạo pool hay bật tự tạo schema production từ ví dụ framework.
- Lưu script versioned ở Admin theo hướng dẫn EzyPlatform; không sửa script đã phát hành hoặc coi restart là kiểm migration. Test fresh install và upgrade trên bản sao dữ liệu; smoke Web không đủ. Xem [ghi nhận thiếu bảng lúc khởi động](../../plugins/test-report.md#thứ-tự-phụ-thuộc-đáng-lưu-ý).
- [EzyRedis](https://youngmonkeys.org/ezydata/guides/introduce-ezy-redis?lang=vi) có cấu trúc dùng cache/counter và channel; không phải nguồn chuẩn quyền hay độ bền outbox. [EzyMongo](https://youngmonkeys.org/ezydata/guides/introduce-ezymongo?lang=vi) là đường document với config, query và result riêng. Không thêm datastore chỉ vì có adapter.
