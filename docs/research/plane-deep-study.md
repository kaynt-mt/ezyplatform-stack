# Nghiên cứu mã nguồn Plane cho plugin quản lý công việc

**Phạm vi:** mã nguồn Plane Community tại revision [`723bb178f97b87e80a23df9eed134eb1388d7465`][plane-readme].
Đây là đối chiếu tĩnh, không phải kiểm thử runtime, đo tải hoặc kiểm kê các gói trả phí.
**Work item** là tên sản phẩm; trong nội dung kỹ thuật bên dưới dùng `Issue` khi nói về model/API tương ứng. [Model][m-issue] · [URL v1][v1-issue]

**Đọc cùng:** [thiết kế MVP hiện hành](plane-plugin-design-notes.md) chốt ranh giới plugin;
[nghiên cứu EzyPlatform](ezyplatform-deep-research.md) và [kiểm kê plugin](../plugins/README.md) là nguồn cho nửa EzyPlatform.
Các đề xuất ở phần 7–9 không phải hành vi Plane hay cam kết về API EzyPlatform.

## 1. Kiến trúc tổng thể

| Thành phần | Trách nhiệm ở revision này | Nguồn |
| --- | --- | --- |
| `apps/api` | Python/Django + Django REST Framework; model/migration, HTTP, quyền, API token, Celery. | [Dependencies][api-py] · [URL gốc][url-root] · [Celery][celery] |
| `apps/web` | Giao diện làm việc: issue, danh sách/board, tài liệu, thiết lập workspace/project. **React + React Router**, không phải ứng dụng Next.js ở bản này. | [Package và script build][web-pkg] · [Root store][web-root] |
| `apps/admin` | Giao diện quản trị instance ở lane `/god-mode/`; build bằng React Router. Không phải workspace admin của Web. | [Admin package][admin-pkg] · [Proxy][proxy] · [Instance model][instance] |
| `apps/space` | Frontend riêng cho các bề mặt chia sẻ; proxy mount ở `/spaces/`, backend mount ở `/api/public/`. Cũng dùng React Router. | [Space package][space-pkg] · [Proxy][proxy] · [URL gốc][url-root] |
| `apps/live` | WebSocket/Hocuspocus xác thực kết nối tài liệu; đồng bộ phân tán và ghi tài liệu qua API. Không phải kênh realtime tổng quát của CRUD issue. | [Server][live-hocus] · [Auth][live-auth] · [Persistence][live-db] |
| `apps/proxy` | Caddy chuyển tiếp UI, API/auth/static, live và bucket object storage theo prefix; Web là fallback. | [Caddyfile CE][proxy] |

### Monorepo và deployment

- pnpm workspace thu nhận `apps/*` và `packages/*` nhưng loại API và proxy; tác vụ JS/TS điều phối bằng script ở root. [Workspace][workspace-js] · [Root package][root-pkg]
- Các package dùng chung có tầng hợp đồng và logic (`types`, `constants`, `utils`), HTTP (`services`), state (`shared-state`), UI/nội dung (`blocks`, `editor`, `i18n`). Đây là cách chia ranh giới để tham khảo, không phải yêu cầu kéo monorepo JS sang EzyPlatform. [Packages][pkg-types] · [Services][pkg-services] · [State][pkg-state] · [Blocks][pkg-blocks] · [Editor][editor] · [i18n][pkg-i18n]
- Compose tách API, worker, beat và migrator, dùng chung phần build backend với entrypoint khác nhau. Beat phát lịch; worker chạy tác vụ; RabbitMQ là broker AMQP. Postgres giữ dữ liệu nghiệp vụ. [Compose][compose] · [Settings][settings] · [Celery][celery]
- Tên service dễ gây hiểu nhầm: `plane-redis` chạy **Valkey**, tương thích Redis; `plane-minio` dùng **pgsty/silo** trong Compose ở revision này. Code storage có đầu nối S3 và hỗ trợ cấu hình endpoint tương thích MinIO. Đừng suy tên service là image thực. [Compose][compose] · [Settings][settings]
- Compose local tách API và dịch vụ phụ trợ khỏi dev server frontend; Compose test có các service test riêng. Self-host Community còn có CLI/Compose, AIO, Swarm và hướng dẫn Helm. Các lựa chọn này không phải bằng chứng triển khai đã chạy trong nghiên cứu. [Local][compose-local] · [Test][compose-test] · [CLI][deploy-cli] · [AIO][deploy-aio] · [Swarm][deploy-swarm] · [Kubernetes][deploy-k8s]

### Đường đi của một yêu cầu

```text
Web → Caddy → API nội bộ → policy + truy vấn/ghi PostgreSQL
                           └─ dispatch tác vụ → RabbitMQ → Celery worker
Space → Caddy → API public → projection giới hạn theo anchor
Editor → Caddy → Live → API cho quyền page và lưu nội dung
```

Sơ đồ mô tả các lane chính, không diễn tả thứ tự commit/dispatch của mọi endpoint.
Nếu plugin MVP thiếu broker hoặc WebSocket, lát cắt HTTP + database vẫn có thể triển khai độc lập; phải quyết định trước phần nào cho phép nhất quán cuối cùng.
[Proxy][proxy] · [URL gốc][url-root] · [Điểm gọi task][app-issue-view] · [Broker][settings] · [Live auth][live-auth] · [Live store][live-db]

## 2. Mô hình dữ liệu và bất biến

Ở các bảng dưới, **unique active** là điều kiện trên bản ghi chưa soft-delete (`deleted_at IS NULL`), không đồng nghĩa `is_active=True` trên membership.
Chỉ ghi các ràng buộc quan sát ở model; không suy ra mọi ràng buộc runtime đều có trong DB. [Audit mixins][m-mixins] · [Membership][m-workspace] · [Project][m-project]

### Nền dữ liệu và tenant

| Model | Trường và ràng buộc đáng chú ý | Nguồn |
| --- | --- | --- |
| `AuditModel`, `BaseModel` | Audit thời gian `created_at/updated_at`, actor `created_by/updated_by`; `BaseModel` thêm UUID PK và gán actor từ user hiện tại, có đường ghi actor rõ ràng/bỏ tự động. | [Audit][m-mixins] · [Base][m-base] |
| Soft delete | Model/queryset thường đánh dấu `deleted_at`, manager mặc định loại hàng đã đánh dấu; có đường hard delete riêng. `archived_at` là vòng đời nghiệp vụ, không phải soft delete. | [Mixins][m-mixins] · [Issue manager][m-issue] · [Beat][celery] |
| `ProjectBaseModel`, `WorkspaceBaseModel` | Con cấp project mang FK project và workspace; `save()` lấy workspace từ project. Base cấp workspace có FK project tùy chọn và cũng suy workspace khi có project. Đừng dựa vào `save()` để kiểm quyền hay bảo vệ bulk write. | [Project][m-project] · [Workspace][m-workspace] |
| `Workspace` | `name`, `slug` unique, owner, thuộc tính hiển thị; `WorkspaceMember` chứa user, role, cờ active và unique active workspace/user. Invitation có email, token, role và trạng thái; unique active email/workspace. | [Workspace][m-workspace] |
| `Project`, `ProjectIdentifier` | Project giữ workspace, tên/mã, network, timezone, default state, thiết lập guest, archive/close. Tên và identifier mỗi loại unique active trong workspace; registry `ProjectIdentifier` cũng unique active theo workspace/tên. | [Project][m-project] |
| `ProjectMember`, `ProjectUserProperty`, `ProjectMemberInvite` | Membership role/active unique active project/user; preference riêng project/user giữ filter, display và thứ tự. Invitation project giữ email/token/role riêng, không mặc nhiên là membership. | [Project][m-project] |

Mã role là **Admin 20, Member 15, Guest 5**. Workspace owner là một FK riêng, không phải role số thứ tư.
Luôn tách người tạo/owner, vai trò tại workspace và vai trò tại project khi xây policy. [Workspace][m-workspace] · [Project][m-project] · [Decorator][perm-base]

### Issue, số hiển thị và thứ tự

- UUID là định danh nội bộ. `sequence_id` đi với project identifier để tra mã người đọc. `IssueSequence` là sổ cấp số, FK issue có thể về null để giữ số khi issue bị xóa. [Issue/IssueSequence][m-issue] · [Tra mã][v1-issue]
- Khi thêm issue bằng `save()`, Plane mở transaction, lấy advisory lock PostgreSQL theo project, đọc `MAX(sequence)` trong sổ rồi cấp số kế tiếp (khởi đầu 1), lưu issue và ghi sổ trong cùng transaction. Không diễn giải thành `MAX(issues)` hoặc unique trên `Issue.sequence_id`; model sổ có index trên sequence nhưng không khai báo unique cặp project/sequence ở đây. [Luồng cấp số][m-issue]
- `sort_order` là float; khi tạo, lấy max trong project/state rồi cộng 10.000 (mặc định 65.535 khi không có max). Đây là rank hiển thị, không phải sequence hay invariant duy nhất. Một issue đổi cột không nhất thiết đi lại nhánh cấp thứ tự lúc tạo. [Issue.save][m-issue]
- Issue giữ `parent` tự tham chiếu, state, priority (`urgent/high/medium/low/none`), start/target date, estimate, type, dữ liệu nhập ngoài và các dạng description (JSON, HTML, text đã bỏ tag, binary). Không xem stripping HTML là sanitize đầu ra. [Issue][m-issue]
- Nếu không có state, `save()` tìm default không-triage, rồi fallback state đầu tiên không-triage. Khi tạo hoặc đổi state, đồng bộ `completed_at` theo nhóm Completed. Đường bulk update không tự chạy hook này. [Issue][m-issue] · [Bulk automation][job-auto]
- Hai mặt truy vấn khác nhau: `Issue.objects` có soft-delete mặc định; `Issue.issue_objects` còn loại triage, draft, item đã archive và item trong project đã archive. Chọn manager theo ý nghĩa endpoint, không dùng như một kiểm tra quyền độc lập. [IssueManager][m-issue] · [Guest policy][perm-base]

### Các quan hệ và lịch sử của issue

| Thành phần | Trường, khóa và điểm cần phân biệt | Nguồn |
| --- | --- | --- |
| Giao việc, nhắc tên | `IssueAssignee` unique active issue/user; `IssueMention` unique active issue/user được nhắc. Mention không đồng nghĩa giao việc hay cấp quyền truy cập. | [Model][m-issue] · [Notification][job-notif] |
| Nhãn | `Label` có tên/màu và project tùy chọn; partial unique chỉ theo tên khi project null (không kèm workspace trong khóa đó), và theo tên/project khi có project. `IssueLabel` là bảng nối; model không khai báo partial unique cặp issue/label. | [Label][m-label] · [IssueLabel][m-issue] |
| Phụ thuộc, trùng lặp | `IssueRelation` giữ cặp có hướng `issue/related_issue` và loại quan hệ; unique active trên cặp, không kèm loại. Model còn có `IssueBlocker` với hai FK có vai trò chặn/bị chặn. | [Model][m-issue] · [Relation endpoint][issue-rel] |
| Link | `IssueLink` giữ issue, URL, title tùy chọn và metadata. Không phải attachment hay quyền truy cập đích. | [Model][m-issue] |
| File | `IssueAttachment` có issue, file, attributes và mã nguồn ngoài; đường dẫn tạo theo workspace và validator kích thước. Model `FileAsset` riêng chứa asset và scope; khi nghiên cứu tải file nên đọc endpoint thực tế thay vì chỉ dựa vào bảng attachment. | [Attachment model][m-issue] · [Asset][m-asset] · [Attachment endpoint][issue-asset] |
| Bình luận | `IssueComment` giữ actor, issue, parent, edited timestamp, visibility, HTML/JSON/text; có liên kết `Description`. Xem policy bề mặt public riêng, không suy comment nội bộ là public. | [Comment model][m-issue] · [Description][m-desc] · [Space issue][space-issue-view] |
| Theo dõi và tương tác | `IssueSubscriber` unique active issue/subscriber; phản ứng issue/comment unique active theo đối tượng, actor, mã phản ứng; `IssueVote` unique active issue/actor. Đây là các quan hệ có vòng đời riêng. | [Model][m-issue] |
| Activity | Issue có thể null; bản ghi chứa actor, verb, field, giá trị cũ/mới, identifier tương ứng, epoch và tham chiếu comment. Đây là timeline nghiệp vụ chứ không phải snapshot đầy đủ hay chứng cứ audit đồng bộ tuyệt đối. | [IssueActivity][m-issue] · [Worker][job-activity] |
| Version | `IssueVersion` snapshot các thuộc tính và mảng ID liên quan; `IssueDescriptionVersion` lưu riêng description JSON/HTML/binary/text, owner và mốc lưu. `DescriptionVersion` lại là model version của thực thể `Description`, không đồng nhất với hai bảng trên. | [Issue versions][m-issue] · [Description][m-desc] · [Sync][job-ver-sync] |

### Workflow và tổ chức công việc

| Model | Trường chính và bất biến | Nguồn |
| --- | --- | --- |
| `State` | Tên, color, slug, thứ tự, default, `is_triage`, group. Nhóm: backlog, unstarted, started, completed, cancelled, triage. Tên unique active theo project; manager thường không trả triage. Tên hiển thị không phải group nghiệp vụ. | [State][m-state] |
| `Cycle` | Project, tên, thời gian bắt đầu/kết thúc, timezone, owner, progress snapshot, archive, version; lúc thêm đặt rank trước min hiện tại. `CycleIssue` unique active cặp cycle/issue; chỉ cặp đó không đủ để ràng buộc mỗi issue một cycle. Preference unique active cycle/user. | [Cycle][m-cycle] · [API gán/chuyển cycle][api-cycle-view] |
| `Module` | Project, tên, lead, status, khoảng ngày và archive; tên unique active trong project, rank thêm trước min. `ModuleIssue` unique active issue/module (quan hệ nhiều-nhiều); membership và preference unique active theo module/user. Có `ModuleLink` riêng. | [Module][m-module] |
| `IssueView` | Saved view ở workspace hoặc project: owner, access private/public, query, filters/rich filters, display filters/properties, lock/archive, rank. Rank gắn với scope; không thấy unique tên view ở model. “Public” của saved view không tự bật board internet. | [View][m-view] · [Deploy board][m-deploy] |
| `Intake`, `IntakeIssue` | Intake có tên unique active/project và cờ default. Item intake nối tới Issue, có nguồn/email, extra, duplicate target và snooze; status pending/rejected/snoozed/accepted/duplicate. Snooze chuẩn hóa theo đầu ngày trong timezone project. Không dùng intake làm tên khác của state board. | [Intake][m-intake] · [Automation][job-auto] |
| `Estimate`, `EstimatePoint` | Estimate thuộc project, tên unique active/project, có loại và last-used. Point thuộc thang estimate, có `key` số không âm và `value` chuỗi. Issue có FK point; tách thang điểm khỏi field số tổng quát. | [Estimate][m-estimate] · [Issue][m-issue] |
| `IssueType`, `ProjectIssueType` | Type khai báo cấp workspace, tên, level và cờ epic/default/active; mapping project/type unique active, có level/default riêng. Không lẫn type với state group. | [Issue type][m-type] |
| `DraftIssue` | Có model riêng, actor qua audit, project có thể qua workspace base, nội dung và quan hệ nháp; model không có `sequence_id`. Có join assignee, label, module, cycle; assignee/module/cycle unique active theo cặp trong model. Đừng nhầm với cờ `Issue.is_draft`. | [Draft][m-draft] · [Issue][m-issue] |

### Tài liệu, phân phối và giao tiếp

| Model | Trường chính và ràng buộc | Nguồn |
| --- | --- | --- |
| `Page`, `ProjectPage`, `PageVersion` | Workspace, owner, content đa định dạng, parent, access/lock/archive. Mapping project/page unique active; `PageVersion` giữ chủ sở hữu, mốc lưu và nội dung con. `PageLog` unique page/transaction; tách lịch sử cấu trúc với snapshot nội dung. | [Page][m-page] · [Page version task][job-page] |
| `Notification`, `UserNotificationPreference`, `EmailNotificationLog` | Notification có receiver, sender/trigger, workspace/project, entity ID/type, payload, read/snooze/archive; có composite index phục vụ danh sách người nhận. Preference tách property/state/comment/mention/completed; email log có processed/sent, không tuyên bố exactly-once. | [Models][m-notif] |
| `Webhook`, `WebhookLog`, `ProjectWebhook` | Webhook chứa URL, trạng thái, khóa ký và cờ theo loại event; unique active workspace/URL. Mapping project/webhook unique active; log giữ metadata request/response, trạng thái và số retry. | [Webhook][m-hook] · [Delivery][job-hook] |
| `UserFavorite` | Entity type/ID, owner, folder/parent và sequence; unique active type/entity/user như model, không thêm workspace vào khóa khi mô tả. | [Favorite][m-fav] |
| `ExporterHistory`, `Importer` | Export cấp workspace có actor, loại/provider, filter, status, reason, key/URL/token; import cấp project có service, status, actor, metadata/config và dữ liệu kết quả. Model Importer không tự chứng minh mọi connector có UI hay chạy trong CE. | [Export model][m-export] · [Import model][m-import] · [Export task][job-export] |
| `DeployBoard`, `ProjectDeployBoard` | Board generic có entity type/ID unique active và anchor unique, cờ tắt cùng quyền comment/reaction/vote/activity/intake. `ProjectDeployBoard` riêng có anchor unique và cặp project/anchor; đối chiếu route Space và kiểm tra scope khi trả dữ liệu. | [Deploy model][m-deploy] · [Project board][m-project] · [Space project][space-prj-view] · [Space issue][space-issue-view] |

### Ba chi tiết schema dễ hiểu nhầm khi thiết kế lại

1. **Xóa instance khác xóa theo queryset.** Đường xoá mềm instance gán ngày, gọi `save()` rồi dispatch dọn entity liên quan; đường queryset đánh dấu hàng loạt qua `update()`. Model cũng có `all_objects` không dùng filter mặc định.
   Đề xuất plugin không trông chờ DB cascade cho soft delete; kiểm thử riêng xóa project, xóa item, quyền đọc child và restore. [Mixins][m-mixins]
2. **Gán nhiều issue vào cycle không phải nối nhiều-nhiều tự do.** Endpoint v1 lập tập issue chưa có ở cycle khác và các bản ghi cần chuyển, scope theo workspace/project và từ chối cycle đã kết thúc.
   Nếu nghiệp vụ plugin chọn “mỗi item một cycle hiện hành”, ghi rõ invariant ở write path và ràng buộc DB của plugin thay vì nghĩ unique cặp tự bảo đảm. [Cycle endpoint][api-cycle-view] · [Cycle join][m-cycle]
3. **Tách dữ liệu file khỏi đường đăng tải.** Attachment V2 dùng `FileAsset`, kiểm tra scope issue và MIME allowlist trước khi tạo bản ghi với metadata/key riêng; luồng đọc/cập nhật là các nhánh khác.
   Không lấy việc POST thành công làm bằng chứng download riêng tư hay upload đã hoàn tất. [Attachment V2][issue-asset] · [FileAsset][m-asset]

## 3. Phân quyền và ranh giới truy cập

1. **Danh tính không phải quyền.** Admin/Member/Guest là role trong membership. `allow_permission` ở level Workspace tra active workspace membership; ở level Project tra active project membership theo slug/project. Nhánh nâng quyền workspace admin vẫn yêu cầu membership project active; nhánh creator cũng kiểm tra membership trước khi xét người tạo. Đây là hành vi decorator, không nên biến thành mô tả đúng cho mọi endpoint. [Decorator][perm-base]
2. **DRF có policy riêng theo thao tác.** `ProjectBasePermission`, `ProjectArchiveUnarchivePermission` và `ProjectMemberPermission` không phải một check dùng chung; lớp workspace và `ProjectPagePermission` cũng có điều kiện riêng. Page xét visibility, thao tác, membership và guest flag. [Project permissions][perm-project] · [Workspace permissions][perm-ws] · [Page permissions][perm-page]
3. **Guest không đồng nghĩa anonymous hay viewer tuyệt đối.** Với project tắt `guest_view_all_features`, guest bị giới hạn thấy issue do mình tạo. Helper `issue_hidden_from_guest` dùng ở các tuyến dữ liệu con; cần đọc cùng detail và các contract test API v1 để hiểu ngoại lệ theo bề mặt. Bài học: lọc cả list, detail, related object, file, count và search, không chỉ ẩn nút. [Helper][perm-base] · [Issue app][app-issue-view] · [Guest contract][guest-test]
4. **API key là danh tính của user liên kết.** `X-Api-Key` được đối chiếu token active, chưa hết hạn (hoặc không có hạn) và user active; cập nhật `last_used`. Model có nullable workspace và user type human/bot, nhưng riêng hàm xác thực không kiểm membership theo URL; không coi có key là có quyền workspace/project. [Auth][api-auth] · [Token model][m-api] · [API base][v1-base] · [Permission contract][api-perm-test]
5. **Public board là projection khác.** Anchor và feature flags quyết định bề mặt chia sẻ; issue/comment phải thuộc scope board. Không dùng auth scheme của external API v1 thay thế chính sách publish. [Space routes][space-issue-url] · [Space queryset và thao tác][space-issue-view]

### Các lớp không thay thế nhau

| Kiểm tra | Câu hỏi khi đọc code hoặc review plugin |
| --- | --- |
| Instance admin, workspace owner và project admin | Tác nhân đang quản lý service, quản lý tenant hay quản lý một project? Có được đọc nội dung work item không? [Instance][instance] · [Workspace][m-workspace] · [Project policy][perm-project] |
| Network dự án và publish | Plane có network Secret/Public ở project, riêng với anchor/flags của deploy board. “Public” trong cấu hình không phải lý do dùng chung serializer cho board internet. [Project][m-project] · [Board][m-deploy] · [Space][space-issue-view] |
| Quyền board và quyền comment | Space kiểm scope theo issue hiển thị và comment EXTERNAL; field server-controlled của comment không nằm trong danh sách nội dung cho phép ghi. Đây là policy dữ liệu, không chỉ gate đăng nhập. [Space issue][space-issue-view] |
| Token được nhận và action được cấp | Key đã xác thực vẫn cần quyền thao tác đúng tài nguyên. Test song song guest key, member key, membership đã thu hồi và ID project ngoài scope. [Token auth][api-auth] · [API permission test][api-perm-test] |

## 4. API, bộ lọc và phân trang

| Lane | Prefix / ví dụ | Nguồn |
| --- | --- | --- |
| Web app | `/api/workspaces/{slug}/projects/{project_id}/`; có `issues/`, `issues/list/`, `v2/issues/` và tài nguyên con. Không đồng nhất v2 nội bộ với public v1. | [URL gốc][url-root] · [Issue app URLs][app-issue-url] |
| Cycle/module Web | Cùng prefix project: `cycles/`, `cycles/{id}/cycle-issues/`; `modules/`, `modules/{id}/issues/`, module links. | [Cycle app][app-cycle-url] · [Module app][app-module-url] |
| API tích hợp | `/api/v1/workspaces/{slug}/projects/{project_id}/work-items/` và detail qua UUID. `issues/` là nhóm URL cũ (deprecated trong source) vẫn được mount. Có search ở workspace và route tra mã project/issue; links, comments, activities là tài nguyên con. | [URL gốc][url-root] · [Work item v1][v1-issue] |
| Cycle/module v1 | `cycles/`, `cycles/{id}/cycle-issues/`, `transfer-issues/`, archive; `modules/`, `modules/{id}/module-issues/`, archive. Chú ý tên `module-issues` khác lane Web. | [Cycle v1][v1-cycle] · [Module v1][v1-module] |
| Space public | `/api/public/`; nhóm URL dùng board anchor cho issue, comment, reaction và các tài nguyên được công bố. | [URL gốc][url-root] · [Space project][space-prj-url] · [Space issue][space-issue-url] |
| Quản trị instance / phiên | `/api/instances/` riêng với workspace API; auth mount dưới `/auth/`. | [URL gốc][url-root] |

**Filter và presentation là hai trục.** `issue_filters` chuyển tham số như state/state group, priority, label, assignee, cycle/module, ngày và một số cờ ngữ cảnh thành điều kiện ORM; lọc UUID trước khi dùng.
Projection/nhóm và sort đi qua utility riêng. Không lấy bản ghi rồi mới lọc permission ở client. [Filters][filters] · [Issue queryset][app-issue-view] · [Ordering][ordering]

- `order_issue_queryset` xử lý thứ tự có quy tắc riêng cho một số trường thay vì chỉ truyền thẳng tên cột; `sanitize_order_by` có allowlist và fallback. `issue_queryset_grouper` chuẩn bị biểu thức/annotation theo group và subgroup, formatter tạo cấu trúc nhóm cho payload. [Ordering][ordering] · [Grouper][grouper]
- Xem thứ tự gọi trong `IssueViewSet`: áp filter, chuẩn bị order/group/subgroup, rồi chọn cách paginate cho ngữ cảnh. External v1 có view riêng, không mặc nhiên dùng cùng bộ lọc hay hình dạng payload ở mọi route. [App view][app-issue-view] · [API v1 view][v1-issue-view]
- `BasePaginator` có offset paginator thường, theo nhóm và subgroup; trả ví dụ `next_cursor`, `prev_cursor`, cờ còn kết quả và tổng. Cursor ở đây mang limit/page/hướng; **không** bảo đảm ổn định keyset khi dữ liệu thêm hoặc rank thay đổi. Đường `IssuePaginatedViewSet` còn dùng `global_paginator` riêng. [Paginator][paginator] · [Global paginator][global-paginator] · [Điểm gọi][app-issue-view]

### Ví dụ đọc hợp đồng v1 từ URL

- Collection `work-items/` nhận GET/POST; detail `work-items/{uuid}/` dùng GET/PATCH/DELETE. Route `work-items/{project_identifier}-{issue_identifier}/` ở cấp workspace dùng GET và là tra mã hiển thị, không phải đường ghi thay thế. [URL mapping][v1-issue]
- Links và comments tách list/create với detail/update/delete; activities là GET. Nhóm mới có `attachments/` và `relations/`; nhóm cũ đặt attachment dưới `issue-attachments/`. So sánh theo URL+method, không giả định đổi mỗi tên prefix là đủ. [URL mapping][v1-issue]
- Đối với MVP Ezy, định nghĩa một hợp đồng HTTP nhất quán và bảng action riêng: danh sách có thể thiếu `activity`/comment đầy đủ, detail lấy tài nguyên con theo nhu cầu. Giữ list/board dùng chung policy, đừng ràng buộc màn hình vào payload tương thích với Plane.

| Tình huống phân trang | Quyết định cần ghi vào hợp đồng MVP |
| --- | --- |
| Kanban có một cột rất lớn | Mỗi cột có cursor của nó; không ép tải toàn project để thấy số phần tử hoặc thao tác chuyển cột. |
| Một item thuộc nhiều giá trị group, ví dụ assignee | MVP ưu tiên nhóm theo state đơn trị; nếu thêm nhóm assignee, định nghĩa trùng giữa cột và số lượng theo item hay theo thẻ. |
| Board thay đổi khi người dùng đang tải trang tiếp | Chọn snapshot hoặc eventual consistency; mô tả refetch khi move và không cam kết chống bỏ sót chỉ vì tên trường là cursor. |

Đối chiếu cơ chế phân nhóm và cursor offset của Plane: [Grouper][grouper] · [Paginator][paginator] · [Issue view][app-issue-view].

## 5. Luồng nghiệp vụ và tác vụ nền

### Mutation → activity → thông báo

1. Endpoint app issue ghi mutation và chuyển dữ liệu cho `issue_activity` bằng Celery; ở các nhánh tạo/cập nhật còn dispatch version mô tả và `model_activity` cho webhook. Các luồng này là dispatch riêng, không phải một outbox nghiệp vụ nguyên tử. [Điểm gọi][app-issue-view]
2. Worker tra project/issue, có thể chạm `updated_at`, chọn handler theo loại event (issue/comment/cycle/module/link/attachment/relation/reaction…), xây diff rồi `bulk_create` activity. Có cờ riêng điều khiển subscriber/notification. [Issue activity][job-activity]
3. Notification task xử lý mention, subscriber và preference để xây thông báo; in-app notification và email log là hai lưu trữ khác nhau. Email task có bước gom email, khóa và gửi theo người nhận; đừng suy từ timeline rằng email chắc chắn đã gửi. [Notification task][job-notif] · [Email task][job-email] · [Models][m-notif]

### Webhook, automation và tác vụ dài

| Luồng | Plane làm gì ở đây | Bài học cho plugin |
| --- | --- | --- |
| Webhook | Chọn webhook theo workspace/project và loại event; delivery có ID/header event, ký HMAC-SHA256 vào `X-Plane-Signature` nếu có secret. Celery backoff + jitter, `max_retries=5` với lỗi request có thể retry; nhánh lỗi kết nối hết retry có thể vô hiệu hóa webhook và thông báo. Không phải tất cả lỗi đều retry. [Worker][job-hook] | Ký đúng bytes gửi, event ID ổn định qua retry; tự thiết kế timeout, redaction, policy egress và hàng lỗi. |
| Auto-archive/close | Beat gọi tác vụ định kỳ. Project bật rule bằng `archive_in`/`close_in`; code so `updated_at` với ngưỡng tính theo bội 30 ngày, bulk update trường archive hoặc state rồi phát activity. [Beat][celery] · [Automation][job-auto] | Chốt định nghĩa “không hoạt động”, timezone và quy tắc cho đóng/hồi phục. Bulk path phải giữ đúng invariant mà đường đơn lẻ bảo vệ. |
| Export | Worker chuẩn bị dữ liệu, đóng ZIP và lưu object storage, cập nhật lịch sử; beat dọn link/file export cũ theo task tương ứng. [Export][job-export] · [Cleanup][job-export-exp] · [Beat][celery] | Kiểm quyền tại lúc đặt job và download, đặt TTL, không bỏ scope ở truy vấn nền. |
| Invitation | Worker workspace/project dựng và gửi email lời mời theo thông tin đích và token; bản ghi lời mời khác membership. [Workspace mail][job-ws-invite] · [Project mail][job-prj-invite] · [Workspace model][m-workspace] · [Project model][m-project] | Token dùng một lần/hết hạn là yêu cầu đề xuất; xác minh, áp role và revoke trong domain plugin. |
| Description/version | Task so sánh HTML, bỏ qua nếu không đổi (trừ lúc tạo); nếu bản gần nhất cùng tác giả trong cửa sổ 600 giây thì cập nhật snapshot đó, nếu không tạo bản mới. Có tác vụ sync lịch sử riêng và page version task riêng. [Description task][job-desc] · [Description sync][job-desc-sync] · [Issue sync][job-ver-sync] · [Page version][job-page] | Không gọi snapshot gộp là audit log; chốt giới hạn kích thước/retention và chính sách khôi phục trước khi mở version UI. |

**Điểm kiểm tra vận hành khi mở rộng:**

- Email gom các log chưa xử lý theo receiver và issue; đánh dấu processed trước dispatch và dùng ID log theo issue để đánh dấu sent. Hai timestamp phản ánh hai ranh giới khác nhau.
  Nếu sản phẩm cần SLA gửi, thêm retry có dedupe và giám sát lag trong plugin thay vì coi processed là delivered. [Email task][job-email]
- Webhook ghi status HTTP và chỉ giữ phần đầu response body; timeout/giới hạn đọc và kiểm tra đích outbound là các chi tiết vận hành, không chỉ việc tạo chữ ký.
  Không suy một HTTP status bất kỳ đều đi vào retry transport. [Webhook task][job-hook]
- Export hỗ trợ CSV/JSON/XLSX, đóng ZIP và tạo URL ký có hạn 7 ngày trong task lưu file. Query task dùng actor của export, active project membership và áp chính sách guest ngay tại bước lấy dữ liệu.
  Với dữ liệu nội bộ, cân nhắc link ngắn hạn hơn và cơ chế cấp lại URL qua kiểm quyền. [Export task][job-export]
- Page version có luồng snapshot theo thay đổi HTML và gộp bản của cùng actor trong cửa sổ riêng; không đồng nhất chính sách version tài liệu với audit cập nhật trạng thái issue. [Page version][job-page] · [Issue description version][job-desc]

### Realtime tài liệu: Hocuspocus/Yjs

- Server Hocuspocus cấu hình auth, stateless handler, extension và debounce 10 giây. WebSocket người dùng chỉ chấp nhận loại `project_page` trong gate hiện tại. Đây không phải bằng chứng mô tả issue cùng được edit realtime. [Hocuspocus][live-hocus] · [Auth][live-auth] · [Editor packages][editor]
- Mỗi kết nối xác minh user qua phiên và kiểm quyền page qua API riêng; kết quả trả project thực và cờ read-only. Không dùng project do socket gửi làm căn cứ quyền. Cần check ở mỗi kết nối kể cả khi tài liệu đã có trong bộ nhớ server. [Connection policy][live-auth]
- Extension DB đọc binary, có thể chuyển từ HTML nếu chưa có binary; lúc lưu serialize binary/HTML/JSON rồi gọi HTTP API. Redis extension hỗ trợ phân tán giữa server và admin messaging. Lỗi fetch/store có đường báo lỗi, không coi lần sửa ở client là lần lưu thành công. [Database extension][live-db] · [Redis extension][live-redis]
- Với plugin mới, ưu tiên autosave bằng HTTP và xử lý conflict. Khi làm collaborative editor, tách quyền kết nối, quyền chỉnh sửa, lưu và đóng phiên sau thu hồi quyền; không dùng Socket chat để thay thế tài liệu CRDT.

## 6. Frontend và trải nghiệm

| Bề mặt | Hành vi cần học, không chép UI | Nguồn |
| --- | --- | --- |
| List | Nhóm item theo cấu hình, hiển thị hàng và thao tác nhanh; tái dùng query thay vì nhân bản resource. | [List root][ui-list] |
| Kanban | Có group/subgroup và các root theo ngữ cảnh; hiển thị cột, thẻ và thao tác trên board. | [Kanban root][ui-kanban] |
| Calendar | Bề mặt theo ngày, cùng nguồn issue nhưng phụ thuộc ngữ nghĩa ngày của item. | [Calendar root][ui-calendar] |
| Spreadsheet | Bề mặt dạng bảng cho dữ liệu issue, không phải type mới của work item. | [Spreadsheet root][ui-sheet] |
| Gantt | Timeline dùng mốc thời gian và thao tác cập nhật từ layout riêng; không cần có scheduler đồ thị để làm list/board MVP. | [Gantt root][ui-gantt] |
| Display options | Khác với filter dữ liệu: chọn group, subgroup, sort và property hiển thị. State của từng ngữ cảnh không nhất thiết giống nhau. | [Display options][ui-display] · [Properties][ui-props] · [Issue view model][m-view] |

- Root store MobX gom store theo domain, còn issue root tập hợp các store theo ngữ cảnh (project/cycle/module/view và chi tiết issue); tránh để mỗi layout tự sở hữu một bản khác nhau của cùng item. [App store][web-root] · [Issue root store][web-issue-root] · [Issue detail store][web-detail-root]
- Editor dùng Tiptap cùng các extension và phần đồng bộ tài liệu. Đối với MVP, Markdown hoặc text được sanitize là đủ nếu cùng đáp ứng yêu cầu render và phân quyền file. [Editor package][editor] · [Page editor root][ui-page]
- Power K có global shortcut handler và modal lệnh. MVP nên dùng nút đổi trạng thái truy cập được bằng bàn phím và shortcut có thể học, không bắt buộc command palette đầy đủ. [Global shortcuts][ui-keys] · [Shortcut handler][ui-key-handler]

**Thứ tự xây UI đề xuất:** form tạo/sửa có phản hồi validation → list theo project → board theo state → thao tác move không phụ thuộc kéo-thả.
Ưu tiên dùng chung cache/item ID và cập nhật lại list/board khi ghi thất bại; thêm ngày, bảng nhiều cột và timeline khi đã có dữ liệu/nhu cầu.
Điều đáng lấy từ Plane là việc tách layout và display options khỏi entity, không phải số lượng layout ở bản đầu. [List][ui-list] · [Kanban][ui-kanban] · [Display options][ui-display] · [Issue root][web-issue-root]

## 7. Đối chiếu với EzyPlatform và phạm vi edition

Cột Ezy là **đề xuất có điều kiện** theo [kiểm kê runtime](../plugins/README.md) và [bằng chứng sandbox](../plugins/test-report.md).
“Dùng” nghĩa là dùng đường tích hợp được kiểm chứng; nếu plugin tham chiếu chỉ có giao diện hoặc API không công khai thì học mẫu, không thêm phụ thuộc.

| Năng lực Plane và nguồn | Tái sử dụng Ezy / sở hữu trong plugin | Mốc |
| --- | --- | --- |
| Danh tính, workspace/project membership [Policy][perm-base] | [EzyAccount](../plugins/ezyaccount.md)/[EzyLogin](../plugins/ezylogin.md) cho danh tính/phiên; membership, lời mời, role theo scope do plugin sở hữu. | MVP |
| Assignment, label, workflow [Issue][m-issue] · [State][m-state] | Học [EzyCRM](../plugins/ezycrm.md) cách organize phụ trách, lọc, lịch sử; tự xây entity issue và DB constraints. | MVP |
| List, board, search [List][ui-list] · [Board][ui-kanban] · [Filters][filters] | Web UI trong phiên/core theme đã chứng minh mount được; query và policy riêng, không dùng content listing làm task board. | MVP |
| Comment/activity/version [Issue][m-issue] · [Versions worker][job-desc] | Audit/timeline riêng; [Markdown](../plugins/markdown.md) là tham chiếu render, không thay thế ACL. Version và rich editing tách khỏi CRUD. | MVP comment/activity; version sau |
| Attachment [Assets][m-asset] · [Endpoint][issue-asset] | Adapter media core nếu chứng minh private read/revoke; không dùng URL công khai làm đường mặc định. | Có điều kiện sau lát cắt MVP |
| Inbox, email, realtime edge [Notification][m-notif] · [Email][job-email] | Outbox domain; [EzyMail](../plugins/ezymail.md) cho template/kênh mail, [EzyChat](../plugins/ezychat.md) làm mẫu lifecycle HTTP/Socket, không sở hữu task. | Outbox contract MVP; delivery sau |
| Cycle/module/estimate/type/relation/saved view [Cycle][m-cycle] · [Module][m-module] · [Estimate][m-estimate] · [Type][m-type] · [Issue][m-issue] · [View][m-view] | Mô hình và filter trong plugin; không lấy CRM/contact/taxonomy làm bảng nối nghiệp vụ. | Sau MVP, chọn theo nhu cầu |
| Intake [Intake][m-intake] | Học form/triage từ [EzySupport](../plugins/ezysupport.md); record intake, chống trùng và transaction chuyển issue riêng. | Sau MVP |
| Wiki/page/Yjs [Page][m-page] · [Live][live-hocus] | [EzyArticle](../plugins/ezyarticle.md)/Markdown cho tài liệu liên kết nếu ACL phù hợp; editor cộng tác riêng, không đổi issue thành bài viết. | Sau MVP |
| Public board [Space][space-issue-view] | Tự xây public projection có quyền explicit và revoke; không chia sẻ nguyên JSON nội bộ. | Sau MVP, opt-in |
| Token API và truy vấn [Auth][api-auth] · [v1 routes][v1-issue] | REST nội bộ plugin trước; [GraphQL](../plugins/graphql.md) là lựa chọn nếu cần, mọi resolver phải giữ scope. | API Web MVP; tích hợp ngoài sau |
| Export/import/webhook/automation [Export][job-export] · [Import model][m-import] · [Webhook][job-hook] · [Automation][job-auto] | Jobs do plugin sở hữu; [EzyOA](../plugins/ezyoa.md)/[Omnichannel](../plugins/omnichannel.md) chỉ là adapter kênh khi có nhu cầu, không là engine task. | Sau MVP |
| Trợ lý và tìm kiếm ngữ nghĩa | Cơ hội Ezy riêng: [EzyAI](../plugins/ezyai.md)/[EzyRAG](../plugins/ezyrag.md)/[EzyVector](../plugins/ezyvector.md) sau khi có filter ACL trong retrieval. Không đưa provider vào luồng ghi issue. | Sau MVP |

**CE so với trả phí:** model edition trong revision này chỉ khai báo `PLANE_COMMUNITY`, UI có badge Community mở upgrade modal, và deployment tách `community`.
Các nguồn dẫn trên chứng minh *có mã trong checkout CE*, không phải quyền sử dụng của mọi edition, mọi feature flag hoặc cam kết parity với Cloud.
Không lấy nút upgrade, model hoặc enum đơn lẻ làm bằng chứng cho một tính năng trả phí đã triển khai; cần bảng tính năng theo phiên bản và kiểm thử riêng nếu edition trở thành tiêu chí mua. [Instance][instance] · [Badge][edition-ui] · [CE deployment][deploy-cli]

## 8. Rủi ro và giấy phép

- **AGPL-3.0:** đọc [LICENSE][license] và [manifest][root-pkg]. Nghiên cứu chỉ lấy ý tưởng, vocabulary và invariant; tự viết code, migration/schema, contract API, test và UI/tài sản đồ họa.
  Nếu sau này có đề xuất dùng lại code, thư viện nội bộ hoặc triển khai bản sửa đổi cho người dùng qua mạng, rà riêng nghĩa vụ AGPL (đặc biệt điều 13), tương thích giấy phép và yêu cầu cung cấp source; không suy tích hợp qua mạng là tự động miễn trừ hoặc tự động kéo mọi repo. Đây không phải tư vấn pháp lý.
- **MySQL không phải PostgreSQL.** Advisory lock theo project, partial unique và array field trong Plane không phải migration có thể bê nguyên sang MySQL. Dùng counter khóa theo project, unique thích hợp để giữ bản ghi active và kiểm nghiệm migration bằng DB mục tiêu. [Issue][m-issue] · [Project constraints][m-project] · [Compose DB][compose]
- **Rank float và cạnh tranh.** Khoảng trống ban đầu không bảo đảm luôn chèn được giữa hai hàng; retry đồng thời có thể đặt trùng rank nếu chỉ nhìn hàng xóm ở client. Đề xuất rank có thứ tự phụ ổn định, kiểm version, khóa nhóm khi rebalance, và thử hai lần kéo cùng vị trí. [Issue rank][m-issue] · [Module rank][m-module]
- **Activity và snapshot tăng nhanh.** Plane ghi app activity bất đồng bộ và có nhiều biến thể snapshot; query group/count có chi phí riêng. Không suy P95 từ code. Đo với dữ liệu có nhiều issue/comment; tách retention timeline nghiệp vụ, payload phiên bản và delivery log. [Activity task][job-activity] · [Version model][m-issue] · [Paginator][paginator] · [Cleanup lịch][celery]
- **Mất nhất quán giữa đường đơn và bulk/job.** Hook của `save()` không đại diện bulk update; retry có thể trễ hoặc lặp, `updated_at` không nhất thiết chỉ là lần người dùng sửa. Đặt invariant trong domain mutation chung và dùng event ID/dedupe. [Issue save][m-issue] · [Automation][job-auto] · [Activity worker][job-activity]
- **Rò dữ liệu qua đường phụ.** App, v1, Space và Live là các bề mặt riêng; attachment, search/count, public projection, websocket đã mở và bản export cần kiểm tra vòng đời quyền riêng. [URL gốc][url-root] · [Guest policy][perm-base] · [Space scope][space-issue-view] · [Live auth][live-auth]
- **Nhiều bản biểu diễn nội dung.** HTML, JSON, binary và text tìm kiếm có thể lệch nhau; định nghĩa bản nào là chuẩn và giới hạn đầu vào trước khi thêm editor cộng tác. [Model][m-issue] · [Live persistence][live-db]

## 9. Đề xuất cập nhật thiết kế MVP

Các delta dưới đây bổ sung cho [thiết kế hiện hành](plane-plugin-design-notes.md), không mở rộng MVP đến mức clone Plane.
Giữ mặc định project riêng, policy domain, audit trong transaction và HTTP làm nguồn chuẩn.

| Bổ sung so với thiết kế hiện tại | Tiêu chí chấp nhận đề xuất | Động cơ từ Plane |
| --- | --- | --- |
| Ghi rõ vòng đời `active/archived/deleted` và phân biệt state/group/default; chốt khi nào ghi/xóa mốc hoàn tất. Trì hoãn triage và nháp riêng. | Test default lúc tạo, reopen, archive không làm tái sử dụng mã, và list/detail theo từng vòng đời. | [Issue manager/save][m-issue] · [State][m-state] |
| Làm rõ counter project được khóa trong transaction tạo item **cùng** unique `(project_id, sequence_no)`; không yêu cầu mã liên tiếp tuyệt đối khi có rollback/import. | Tạo đồng thời ở một và hai project; lỗi, retry và archive không tạo trùng mã; rollback không để item nửa vời. | [Sequence ledger][m-issue] |
| Chốt contract move: state đích, hai hàng xóm theo scope, version item, thứ tự phụ ổn định; phân biệt xung đột và input không hợp lệ. | Hai người kéo cùng cột/vị trí; hết khoảng rank; hàng xóm nằm ngoài scope bị từ chối; UI refetch/rollback được. | [Issue rank][m-issue] · [Kanban][ui-kanban] |
| Viết policy matrix trước khi mở endpoint: role × action × resource lifecycle, tách 401/403/404, không mở creator shortcut hay guest mode ngoài quy tắc MVP. | Fixture hai workspace và hai project khác quyền; negative test cho detail, comment, activity, media, filter/count lẫn ẩn sự tồn tại qua mã item. | [Permission][perm-base] · [Guest contract][guest-test] |
| Chốt API list và board trước saved views: filter nghiệp vụ allowlist; display options riêng; cursor cột bind vào scope/filter/sort; count tùy chi phí. | Test snapshot tĩnh, bộ lọc không có kết quả, cursor sai/khác cột, tie-break rank và quyền sau thay đổi membership. | [Filters][filters] · [Grouper][grouper] · [Paginator][paginator] |
| Định nghĩa một update gồm issue + activity tối thiểu trong transaction, và hợp đồng outbox cho các sink sau này (không ship email/Socket mặc định). | Rollback không có activity/event mồ côi; event replay không nhân thông báo; activity vẫn đọc được sau archive theo policy. | [Dispatch Plane][app-issue-view] · [Activity worker][job-activity] · [Email][job-email] |
| Viết spike ACL cho attachment và boundary cho description: một định dạng chuẩn MVP, URL download qua policy, giới hạn input. | Dữ liệu rỗng/nội dung không hợp lệ, upload/download qua hai user, revoke, render sanitize; nếu adapter không đáp ứng thì hoãn file. | [Asset][m-asset] · [Attachment endpoint][issue-asset] · [Description versions][job-desc] |
| Tách backlog mở rộng theo phụ thuộc: cycle/module/saved views → intake → export/automation và nội dung cộng tác theo nhu cầu. Đừng gộp “realtime” với “giao việc”. | Mỗi phase có fixture scope, migration, đo hiệu năng và quyết định opt-in trước khi ra mắt. | [Cycle][m-cycle] · [Intake][m-intake] · [Export][job-export] · [Live][live-hocus] |

**Quyết định đầu tiên khi viết plugin:** chứng minh Web user/route/migration trên sandbox EzyPlatform, rồi làm lát cắt có hai tenant đi từ tạo issue đến chuyển cột, comment và đọc activity.
Chỉ sau khi vượt qua test scope và concurrent mutation mới mở các đường đọc phụ như attachment, API tích hợp hoặc export. Đây là đề xuất triển khai, chưa có bằng chứng runtime từ tài liệu này.

### Bằng chứng cần lưu ở mỗi mốc

| Mốc | Bằng chứng để người khác kiểm chứng lại |
| --- | --- |
| Spike core Ezy | Phiên bản core/artifact, route thực tế, auth anonymous/user, migration trên DB trống và vị trí UI mount; ghi rõ adapter nào chưa xác minh. |
| Lát cắt MVP | Request/response đã che dữ liệu nhạy cảm, test hai tenant, kết quả thử concurrent create/move và tình trạng rollback audit. |
| Kiểm tra hiệu năng | Dataset giả lập có cột lệch kích thước, nhiều comment/assignment; kế hoạch query và P95 cho list/board trước và sau thêm index. |
| Chức năng sau MVP | Bằng chứng policy còn đúng khi thu hồi quyền, job chạy lại và có lỗi adapter; chưa đạt thì để sau feature gate hoặc hoãn. |

### Cách đọc nguồn

Các liên kết tài liệu Plane bên dưới cùng trỏ vào revision đã chốt, không trỏ nhánh đang thay đổi.
Khi nâng revision tham chiếu, ưu tiên kiểm lại API/permission, service images và điều kiện page socket trước khi cập nhật thiết kế.

[plane-readme]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/README.md
[api-py]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/pyproject.toml
[root-pkg]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/package.json
[web-pkg]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/package.json
[admin-pkg]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/admin/package.json
[space-pkg]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/space/package.json
[workspace-js]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/pnpm-workspace.yaml
[pkg-types]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/packages/types/package.json
[pkg-services]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/packages/services/package.json
[pkg-state]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/packages/shared-state/package.json
[pkg-blocks]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/packages/blocks/package.json
[pkg-i18n]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/packages/i18n/package.json
[editor]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/packages/editor/package.json
[proxy]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/proxy/Caddyfile.ce
[compose]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/docker-compose.yml
[compose-local]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/docker-compose-local.yml
[compose-test]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/docker-compose-test.yml
[deploy-cli]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/deployments/cli/community/README.md
[deploy-aio]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/deployments/aio/community/README.md
[deploy-swarm]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/deployments/swarm/community/swarm.sh
[deploy-k8s]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/deployments/kubernetes/community/README.md
[license]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/LICENSE.txt
[url-root]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/urls.py
[settings]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/settings/common.py
[celery]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/celery.py
[instance]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/license/models/instance.py
[m-mixins]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/mixins.py
[perm-base]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/permissions/base.py
[perm-project]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/permissions/project.py
[perm-ws]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/permissions/workspace.py
[perm-page]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/permissions/page.py
[issue-rel]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/views/issue/relation.py
[issue-asset]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/views/issue/attachment.py
[app-issue-view]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/views/issue/base.py
[api-cycle-view]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/views/cycle.py
[v1-issue-view]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/views/issue.py
[v1-base]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/views/base.py
[api-auth]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/middleware/api_authentication.py
[guest-test]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/tests/contract/api/test_external_api_guest_issue_visibility.py
[api-perm-test]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/tests/contract/api/test_api_permission_parity.py
[app-issue-url]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/urls/issue.py
[app-cycle-url]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/urls/cycle.py
[app-module-url]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/app/urls/module.py
[v1-issue]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/urls/work_item.py
[v1-cycle]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/urls/cycle.py
[v1-module]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/api/urls/module.py
[space-prj-url]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/space/urls/project.py
[space-issue-url]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/space/urls/issue.py
[space-prj-view]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/space/views/project.py
[space-issue-view]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/space/views/issue.py
[live-auth]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/live/src/lib/auth.ts
[live-hocus]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/live/src/hocuspocus.ts
[live-db]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/live/src/extensions/database.ts
[live-redis]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/live/src/extensions/redis.ts
[web-root]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/store/root.store.ts
[web-issue-root]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/store/issue/root.store.ts
[web-detail-root]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/store/issue/issue-details/root.store.ts
[ui-page]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/pages/editor/page-root.tsx
[ui-keys]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/power-k/global-shortcuts.tsx
[ui-key-handler]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/power-k/core/shortcut-handler.ts
[edition-ui]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/workspace/edition-badge.tsx
[m-base]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/base.py
[m-workspace]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/workspace.py
[m-project]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/project.py
[m-issue]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/issue.py
[m-label]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/label.py
[m-asset]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/asset.py
[m-desc]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/description.py
[m-state]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/state.py
[m-cycle]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/cycle.py
[m-module]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/module.py
[m-view]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/view.py
[m-intake]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/intake.py
[m-estimate]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/estimate.py
[m-type]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/issue_type.py
[m-draft]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/draft.py
[m-page]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/page.py
[m-notif]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/notification.py
[m-hook]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/webhook.py
[m-fav]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/favorite.py
[m-export]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/exporter.py
[m-import]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/importer.py
[m-deploy]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/deploy_board.py
[m-api]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/db/models/api.py
[job-activity]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/issue_activities_task.py
[job-notif]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/notification_task.py
[job-email]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/email_notification_task.py
[job-hook]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/webhook_task.py
[job-auto]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/issue_automation_task.py
[job-export]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/export_task.py
[job-export-exp]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/exporter_expired_task.py
[job-ws-invite]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/workspace_invitation_task.py
[job-prj-invite]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/project_invitation_task.py
[job-desc]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/issue_description_version_task.py
[job-desc-sync]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/issue_description_version_sync.py
[job-ver-sync]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/issue_version_sync.py
[job-page]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/bgtasks/page_version_task.py
[filters]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/utils/issue_filters.py
[ordering]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/utils/order_queryset.py
[grouper]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/utils/grouper.py
[paginator]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/utils/paginator.py
[global-paginator]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/api/plane/utils/global_paginator.py
[ui-list]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/list/base-list-root.tsx
[ui-kanban]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/kanban/base-kanban-root.tsx
[ui-calendar]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/calendar/base-calendar-root.tsx
[ui-sheet]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/spreadsheet/base-spreadsheet-root.tsx
[ui-gantt]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/gantt/base-gantt-root.tsx
[ui-display]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/filters/header/display-filters/display-filters-selection.tsx
[ui-props]: https://github.com/makeplane/plane/blob/723bb178f97b87e80a23df9eed134eb1388d7465/apps/web/components/issues/issue-layouts/filters/header/display-filters/display-properties.tsx
