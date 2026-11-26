# Thiết kế đề xuất: plugin quản lý công việc kiểu Plane

Tài liệu này mô tả một plugin mới, không phải tính năng EzyPlatform đã có. Nhắm tới trải nghiệm cốt lõi của Plane: tạo workspace/project, phân việc, cập nhật trạng thái, tìm việc, theo dõi tiến độ. Không sao chép mã, UI, database schema hay API Plane; đối chiếu giấy phép nếu sau này muốn dùng lại bất kỳ tài sản/mã nguồn nào.

Đọc cùng [kiểm kê dự án Young Monkeys](youngmonkeys/index.md) để tra tài liệu framework và phân biệt cơ chế trong guide với hành vi của runtime 1.5.9.

## 1. Bài học từ Plane và ranh giới triển khai

Đối chiếu [Plane](https://github.com/makeplane/plane) ở commit [723bb17](https://github.com/makeplane/plane/tree/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models) và các trang sản phẩm bên dưới. Tên **work item** trên UI tương ứng `Issue` trong model. Các tính năng trong tài liệu Plane không mặc nhiên thuộc cùng edition, và không phải tiêu chí tương thích cho plugin.

| Plane | Dữ liệu/luồng tham chiếu | Trên EzyPlatform |
| --- | --- | --- |
| [Workspace](https://docs.plane.so/core-concepts/workspaces/overview), [project](https://docs.plane.so/core-concepts/projects/overview) | `WorkspaceMember` và `ProjectMember` riêng; `ProjectBaseModel` mang project và workspace; dự án có identifier. | Core User là danh tính; `wm_workspace`, `wm_workspace_member`, `wm_project`, `wm_project_member` là ranh giới riêng của plugin. Khi quản lý một workspace, không cần tài khoản hệ thống Admin. |
| [Work item](https://docs.plane.so/work-items/overview), [properties](https://docs.plane.so/work-items/work-item-properties) | `Issue` có parent, state, priority, ngày, sequence, thứ tự; bảng nối cho nhiều assignee/label; models riêng cho comment, activity, attachment, relation. `State` có group ở cấp project. | MVP: tạo/sửa item, list/board theo state, assignee, label, priority, due date, comment và activity. Dùng schema plugin; dùng media sau spike quyền. Parent/relations bổ sung sau khi có phép kiểm tra chu trình và cross-project. |
| [Cycles](https://docs.plane.so/core-concepts/cycles), [Modules](https://docs.plane.so/core-concepts/modules) | Hai chiều khác nhau: đợt làm việc có thời gian và nhóm chức năng; Plane có `CycleIssue`, `ModuleIssue`. | Sau MVP: cycle theo project và membership; module nghiệp vụ không phải module EzyPlatform. Nếu thiết kế chỉ cho một cycle hiện tại, ghi rõ đây là lựa chọn plugin, không suy từ unique của bảng nối Plane. |
| [Views](https://docs.plane.so/core-concepts/views) | `IssueView` lưu query/filter, chủ sở hữu, access và thiết lập hiển thị. | Lưu JSON filter đã validate và scope chia sẻ, không lưu bản sao kết quả hay cho tự viết SQL. View được chia sẻ không cấp thêm quyền xem item. |
| [Intake](https://docs.plane.so/intake/overview) | `IntakeIssue` có pending/rejected/snoozed/accepted/duplicate và nguồn, trỏ đến `Issue`. | Sau MVP: hộp triage và API nhận yêu cầu riêng; idempotency theo nguồn + external ID, kiểm tra quyền khi accept/merge/mark duplicate. Chưa làm public intake hoặc email intake mặc định. |
| [Pages](https://docs.plane.so/pages/overview) | `Page` có workspace, access, parent; `ProjectPage` nối nhiều project. | Giai đoạn sau: xem EzyArticle như adapter nội dung; chỉ dùng nếu mọi route đọc, search, revision, media và preview tuân workspace ACL. Nếu không, giữ tài liệu riêng hoặc hoãn. Work item không phụ thuộc EzyArticle. |

## 2. Cấu trúc repo plugin

| Module | Trách nhiệm |
| --- | --- |
| `work-management-sdk` | Domain, entity, repository/scoped queries, policy, services/transaction, DTO không phụ thuộc UI. Shared SDK được link vào module runtime, không cài như một plugin riêng. |
| `work-management-web-plugin` | Controller API và Web authentication, validate input, ánh xạ current user → domain actor, UI entry/assets nếu theme cho phép, lỗi JSON và download được bảo vệ. |
| `work-management-admin-plugin` | Nếu cần: cấu hình cấp hệ thống, trạng thái job và quyền vận hành bằng `@EzyFeature` riêng. Không đặc cách cho Admin xem dữ liệu workspace; nếu có support access về sau phải thiết kế quyền và audit rõ ràng. |
| Theme hoặc Socket App/Plugin | Tuỳ chọn sau spike. Không bắt người dùng thay theme nếu Web plugin có thể gắn app tốt; không cài Socket cho MVP HTTP. |

Repo core không chứa app. Theo [README stack](../../README.md), dùng sandbox dev và artifact được pin; không thử trên DB chia sẻ hay production.

Dùng [EzyFox Bean](youngmonkeys/ezyfox-library.md) cho wiring: constructor injection cho service không mang state request, module scan đúng package và kiểm startup từng lane. Chỉ chạy logic cần các bean khác sau khi bean cần thiết được tạo; không mở context riêng để vá discovery.

## 3. Schema và tính nhất quán

Đây là mô hình logic; kiểu cột, khả năng transaction/migration và index phải được chứng minh ở MySQL 8.0 của core mục tiêu.

| Bảng đề xuất | Invariant cần có |
| --- | --- |
| `wm_workspace`, `wm_workspace_member` | Workspace slug unique; membership unique `(workspace_id,user_id)`, có trạng thái và role. Owner cuối không bị xoá/hạ quyền. |
| `wm_project`, `wm_project_member` | Unique `(workspace_id,project_key)`; membership chỉ dành cho thành viên workspace. Trong MVP project riêng mặc định; người không phải thành viên project không thấy dữ liệu. |
| `wm_state`, `wm_work_item` | State thuộc project, có group, thứ tự và default. Số `sequence_no` unique trong project; cấp số bằng counter có transaction, không dùng `max()+1`. Tách ID nội bộ với mã hiển thị `PROJECT-42`. Item có `version`, rank, lifecycle timestamps; không tái dùng code khi archive. |
| `wm_label`, `wm_item_label`, `wm_item_assignee` | Không nối khác project; assignee phải có membership hợp lệ lúc gán. Dùng unique ở bảng nối và kiểm tra scope ở service kể cả khi request gửi ID trực tiếp. |
| `wm_comment`, `wm_activity` | Comment chứa tác giả và item; nội dung render an toàn. Activity append-only lưu actor, action, time, thay đổi tối thiểu trong transaction của mutation; không sao chép bí mật/nguyên văn attachment vào log. |
| `wm_attachment`, `wm_outbox` | Attachment tham chiếu media ID/private storage, luôn đọc qua quyền item. Outbox có event ID, dedupe key, trạng thái retry; sink notification không được tạo trùng nếu gửi lại. |

Giữ chung một quy tắc scope: `workspace → project → item → child`. Truy vấn child phải kiểm tra scope của parent qua khóa phù hợp; không tải bằng ID rồi giả định route đã xác thực. Ràng buộc DB (FK/unique/composite nếu phù hợp) bổ sung cho kiểm tra service. Đừng chép partial unique index có điều kiện của Django/PostgreSQL: chọn thiết kế unique phù hợp MySQL với dữ liệu archived, xác minh bằng migration thực tế.

Theo [EzyData](youngmonkeys/ezydata.md), dùng `EzyDatabaseRepository` cho CRUD/điều kiện đơn giản và `@EzyQuery` cho scope/join/sort/projection của board và list. `Next` (đối số cuối) là offset/limit; cursor trên sort + ID phải tự thiết kế nếu API chọn keyset. Transaction từng write query không bao quát nhiều repository calls: spike `EzyJpaRepository` với một `EntityManager` cho cấp số + insert + activity, và move + activity; kiểm rollback khi lỗi chen giữa các bước trước khi chốt API.

Tạo index từ workload: board `(project_id,state_id,rank,id)`, work item theo ngày/ID, activity/comment `(item_id,created_at,id)`, tra membership/assignee theo cả hai chiều cần dùng. Sau đo `EXPLAIN` mới bổ sung index cho filter phối hợp; không index mọi thuộc tính. Với drag-and-drop, gửi state đích và hàng xóm hoặc vị trí mong muốn, server xác minh cùng project/filter thích hợp, ghi state/rank/history nguyên tử với kiểm tra version. Khi hết khoảng rank, rebalance theo strategy có khóa và snapshot nhất quán.

## 4. Quyền, API và trải nghiệm

- **Hai tầng quyền:** kiểm tra Web user và feature ở adapter; ở domain, kiểm tra workspace membership active, project membership, quyền thao tác. Giữ ma trận rõ: workspace owner quản lý thành viên/cấu hình workspace; project manager quản lý trạng thái/project; member cập nhật work item theo chính sách; viewer chỉ đọc. Đừng suy role workspace tự động có quyền mọi project. Ẩn nút chỉ phục vụ UX.
- **Biên EzyHTTP và i18n:** kiểm interceptor auth chạy trên route thật; bind path/query/body vào DTO và dùng danh tính từ session. View/JSON trả theo hợp đồng riêng, dùng `ResponseEntity` khi cần status/header tùy chỉnh. Đưa nhãn mặc định/lỗi UI vào bundle, giữ state key và giá trị filter ổn định giữa locale. Xem [EzyHTTP](youngmonkeys/ezyhttp.md) và [quy ước core](youngmonkeys/ezyplatform.md).
- **API đề xuất**, không phải route core: `/api/v1/work-management/workspaces/{workspace}/projects/{project}/work-items`; `GET/POST` cho collection, `GET/PATCH` cho item, `POST …/{item}/move`, `GET/POST …/{item}/comments`, `GET …/{item}/activity`. Attachment tách bước upload/link/download; chưa chứng minh quyền private thì chưa phát hành. Giới hạn request/file/page size, chỉ nhận field nghiệp vụ allowlisted, lấy actor từ phiên xác thực. Giữ quy ước 401 khi chưa login, 403 khi actor không có quyền thao tác trên tài nguyên thấy được, 404 khi không nên để lộ sự tồn tại, 409 cho version xung đột (hoặc 412 nếu dùng `If-Match`).
- **List/board** dùng chung query/policy nhưng pagination theo cột cho board; trả `nextPageToken` và số lượng chỉ khi count đủ nhanh và đúng scope. Search/export/saved views phải thừa hưởng policy; count/label gợi ý không lộ dữ liệu chéo workspace. Cung cấp thao tác đổi state không kéo-thả cho bàn phím, xử lý UI optimistic có rollback khi server từ chối.
- **Bình luận/mô tả:** bắt đầu bằng text/Markdown được sanitize khi render, không thực thi JS template do user cung cấp. Kiểm tra lại scope trên URL media khi render/link, không nhúng dữ liệu nhạy cảm vào preview hoặc link public. Tách activity nghiệp vụ khỏi notification gửi ra.
- **Realtime sau MVP:** [EzyFox Server](youngmonkeys/ezyfox-server.md) có login/app access và reconnect, không tự cấp policy project hay replay. Dùng topic theo project, từ chối dùng token Admin như token Web. Kiểm tra quyền khi subscribe, reconnect và fan-out, nhất là sau thu hồi membership; phát sau commit, gửi ID/version tối thiểu và cho client refetch nếu bỏ lỡ event. HTTP là nguồn chuẩn.

## 5. Các mốc và tiêu chí chấp nhận

1. **Spike tương thích:** artifact đang pin, startup test, đóng gói/cài module trên dev, route được prefix như thế nào, lớp auth nào thực sự chạy, có render plugin trong theme đang dùng không, script SQL được áp dụng ở bước nào, Web/User ID và Admin ID có phân tách; test một Web route anonymous/member và một Admin route riêng. Chốt cách rollback build & migration trước khi có dữ liệu.
2. **MVP lát cắt dọc:** workspace và project có member/viewer, tạo item và hiển thị list/board, chuyển trạng thái, bình luận, activity. Thử hai workspace và hai user; kiểm tra không đọc/ghi/count/autocomplete bằng ID chéo scope, và thu hồi membership có hiệu lực với API kế tiếp. Song song tạo item không trùng mã; hai phiên di chuyển item xử lý xung đột không mất update; phân trang không trùng/bỏ item trên snapshot tĩnh.
3. **Tái sử dụng có điều kiện:** private attachment + download, Core notification/letter, giao diện Admin nếu cần. Test URL gốc, upload/download dưới hai user, đổi quyền sau upload, event bị retry, không gửi thông báo khi giao dịch rollback. Nếu tích hợp lõi không đạt, hoãn feature hoặc dùng adapter tự sở hữu phù hợp, không hạ quyền kiểm tra.
4. **Mở rộng:** cycles/modules, saved views, intake, docs và analytics theo nhu cầu thực; sau đó mới realtime, tự động hoá và import. Job có checkpoint, xử lý UTC + timezone hiển thị; đo P95 list/board/search và kiểm tra kế hoạch truy vấn trên dữ liệu thử.

**Chưa xác nhận bằng runtime:** cơ chế mount UI trong theme hiện hành, adapter login đang dùng, mức ACL của media/notification và EzyArticle, giao dịch và vòng đời migration của plugin, khả năng realtime trong stack. Xem [nghiên cứu nền tảng](ezyplatform-deep-research.md) để biết chứng cứ và phạm vi.
