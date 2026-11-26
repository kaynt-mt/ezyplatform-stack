# Quy trình làm việc với AgentKit cho Đội ngũ Bot & Devin Sessions

Tài liệu này tổng hợp kết quả nghiên cứu trực tiếp bộ **AgentKit 3.2.0** (`engineer` + `marketing`, xuất dạng `portable`) đã tích hợp trong `ezyplatform-stack`, đồng thời chuẩn hóa quy trình áp dụng cho đội ngũ thực tế gồm **`chanht_tt`**, các **Bot** (`Chief of Staff`, `Upstream Watcher`) và các **Devin session** triển khai dự án trên nền tảng EzyPlatform.

---

## 1. Cấu trúc thực tế của bộ AgentKit trên stack

Khi chạy `python3 scripts/sync-upstream.py` (với `AGENTKIT_API_KEY` hoặc đã đăng nhập `./scripts/ak login`), `.agents/skills/` chứa tổng cộng **167 skill**:

| Nhóm | Số lượng | Tiền tố | Vai trò chính |
|---|---:|---|---|
| **AgentKit Shared** (`engineer` ∩ `marketing`) | 40 | `ak-*` | Khung làm việc lõi: `ak-agentkit`, `ak-brainstorm`, `ak-plan`, `ak-cook`, `ak-debug`, `ak-fix`, `ak-test`, `ak-scout`, `ak-git`, `ak-docs`, `ak-journal`, `ak-handoff`, `ak-worktree`, `ak-frontend-design`, `ak-ui-ux-pro-max`, `ak-copywriting`, `ak-design`, `ak-preview`... |
| **AgentKit Engineer-only** | 65 | `ak-*` | Kỹ thuật chuyên sâu: `ak-review-pr`, `ak-code-review`, `ak-security`, `ak-ship`, `ak-scenario`, `ak-databases`, `ak-web-testing`, `ak-devops`, `ak-deploy`, `ak-github`, `ak-research`, `ak-xia`, `ak-predict`, `ak-retro`, `ak-advise`, `ak-vibe`, `ak-mcp-builder`, `ak-payment-integration`... |
| **AgentKit Marketing-only** | 43 | `ak-*` | Khám phá sản phẩm & GTM: `ak-play`, `ak-marketing-research`, `ak-competitor`, `ak-marketing-planning`, `ak-brand`, `ak-launch-strategy`, `ak-pricing-strategy`, `ak-seo`, `ak-onboarding-cro`, `ak-form-cro`, `ak-analytics`, `ak-ab-test-setup`, `ak-campaign`, `ak-email`, `ak-social`... |
| **EzyPlatform Stack** | 19 | `ezy-*`, `ezyplatform-*` | Nghiệp vụ & công cụ riêng của EzyPlatform (`ezy-guide`, `ezy-new`, `ezy-sync`, `ezy-develop`, `ezyplatform-develop`, `ezy-i18n`, `ezy-media`...) + skill nội bộ `skills/ezy-build-plugin/SKILL.md` |

---

## 2. Điều chỉnh quan trọng so với bản mẫu tham khảo

Bản quy trình mẫu ban đầu là ví dụ từ một team truyền thống và chứa một số điểm **không khớp** với AgentKit 3.2.0 hoặc với hạ tầng Devin. Các điểm đã hiệu chỉnh:

1. **Đúng tên skill thực tế**:
   - Không có skill tên `ak-security-scan` trong bản 3.2.0 (`ak-security-scan` chỉ còn là legacy alias). Tên chính thức là **`ak-security`** (hỗ trợ `--secrets-only`, `--deps-only`, `--red-team`, `--fix`, `--iterations N`).
2. **Đúng cơ cấu đội ngũ (không dùng tên nhân sự ví dụ)**:
   - **Owner (`chanht_tt`)**: duyệt production, xóa DB/volume, thay đổi `.env`/secret, kiến trúc rủi ro cao, publish diện rộng và quyết định sản phẩm.
   - **Chief of Staff (Bot điều phối)**: quản lý Devin Boards, tách và giao ticket theo nguyên tắc 1 writer cho mỗi repo/nhánh, theo dõi tiến độ, kiểm tra bằng chứng và tự merge PR cho các repo Bot sở hữu (như `kaynt-mt/ezyplatform-stack`) sau khi CI và Devin Review pass.
   - **Upstream Watcher (Bot theo dõi upstream)**: theo dõi phiên bản mới của EzyPlatform, CPPAI và AgentKit.
   - **Devin sessions (Writer / Researcher / Reviewer)**: thực thi ticket end-to-end, tự chạy kiểm thử thật, mở PR, không tự merge trừ khi repo thuộc quyền sở hữu của Bot và đã được ủy quyền.
3. **Bản chất `portable` export trên Devin (tránh gọi tính năng chỉ chạy trên Claude Code)**:
   - **`ak-team` và `ak-orchestrate`**: được thiết kế cho Claude Code Agent Teams / CLI headless runtimes. Trên hệ thống này, điều phối đa session song song đi qua **Chief of Staff + Devin Boards** (hoặc **Dynamic Workflows** khi có ≥ 5 nhánh độc lập). Chỉ dùng **`ak-worktree`** khi cần cô lập nhiều nhánh ngay trong cùng một VM.
   - **Cờ `--advice` (gọi subagent `kongming`) và `--ultra` (wave best-of-5 verifier)**: là cơ chế mở rộng của Claude Code; trên Devin không có subagent `kongming`. Khi gặp bài toán khó cần phản biện, thay bằng **`ak-brainstorm`** (so sánh 2–3 phương án, chỉ rõ giả định dễ gãy nhất), **`ak-predict`** (5 góc nhìn chuyên gia: architecture, security, performance, UX, ops) hoặc **`ak-plan red-team`** (4 persona phản biện).
   - **Bước journal tự động**: `ak-plan`, `ak-cook`, `ak-fix`, `ak-ship` mặc định gợi ý chạy `ak-journal` (ghi vào `plans/journals/YYYY-MM-DD-<slug>.md` qua `./scripts/ak journal create`). Với task nhỏ/nhanh, dùng `--skip-journal` hoặc bỏ qua để tránh sinh file thừa trong repo.
   - **Đường dẫn kế hoạch & báo cáo**: AgentKit quy ước lưu plan tại `plans/<timestamp>-<slug>/` (`plan.md`, `phase-NN-<name>.md`, `plans/reports/`, `plans/journals/`). Không commit file nháp/báo cáo tạm lên git trừ khi là tài liệu chính thức cần lưu trong `docs/`.

---

## 3. Quy tắc chung (áp dụng cho mọi quy trình)

Follow the [model routing rule](model-routing.md) for every Bot and Devin session.

1. **Mặc định chỉ LOCAL / DEV**: Mọi thao tác chạm **production**, xóa DB/volume (`docker compose down -v`), sửa `.env`/secret thật, hoặc gửi/publish công khai diện rộng đều cần **`chanht_tt` duyệt riêng**.
2. **Một writer tại một thời điểm**: Mỗi nhánh/repo chỉ có một session ghi tại một thời điểm; các session khác chỉ đọc, nghiên cứu hoặc review. Khi chia việc song song, các ticket phải có ranh giới file không chồng chéo.
3. **Bảo mật & Backup**: Backup/restore point trước mọi thao tác publish hoặc migration dữ liệu. Không bao giờ ghi hay để lộ token, API key, mật khẩu trong log, báo cáo, PR hoặc chat (nếu phát hiện lộ secret, ẩn dạng `<REDACTED_...>` và yêu cầu xoay khóa ngay).
4. **Cổng tương xứng (Proportionality Gate — từ `ak-agentkit`)**: Phân loại công việc trước khi chọn quy trình dựa trên **3 tiêu chí**:
   - **Size**: `trivial` (1–2 file, ≤ 30 phút, không ẩn số → làm thẳng, bỏ plan) · `standard` (1 deliverable, vài file) · `epic` (nhiều module/phase → bắt buộc `ak-plan` + tách file ownership).
   - **Risk**: `low` (nội bộ, dễ hoàn tác) · `elevated` (ảnh hưởng người dùng hoặc nhiều module → bắt buộc `ak-test` + review) · `high` (auth, bảo mật, thanh toán, migration DB, public contract, thao tác phá hủy, publish diện rộng → bắt buộc `ak-test` + `ak-security` + review độc lập/Devin Review + duyệt của `chanht_tt` trước bước không thể hoàn tác).
   - **Collapse Rule**: Bỏ mọi bước trung gian không sinh ra artifact cho bước sau dùng và không làm giảm mức kiểm chứng mà Risk yêu cầu.
5. **Luật thép (Iron Laws)**:
   - Mọi task nhiều bước đều mở đầu bằng **Brainstorm Contract** gồm 4 mục: *Outcome, Constraints, Non-goals, Acceptance criteria* (3–4 dòng cho task nhỏ; đầy đủ cho task lớn).
   - **Không sửa bug khi chưa chứng minh nguyên nhân gốc** (`ak-debug` trước `ak-fix`). Nếu sửa thất bại 3 lần liên tiếp → dừng lại, đánh giá lại kiến trúc và báo Chief of Staff / `chanht_tt`.
   - **Không báo xong khi chưa có bằng chứng chạy thật trên đúng revision cuối** (output test, build, HTTP/Docker hoặc kiểm tra thực tế). Tuyệt đối không làm yếu test/assertion để lấy màu xanh.

---

## 4. Năm quy trình chuẩn hóa

### Quy trình 1: Task dễ / nhanh (`trivial`, `low` risk, ≤ ~1 giờ, ít file)

- **Chuỗi skill**: `ak-scout` *(nếu chưa rõ vị trí file)* → `ak-cook --fast --skip-journal` → `ak-test` → `ak-code-review --pending` *(nhẹ)*
- **Cách chạy**:
  1. Chốt nhanh 4 dòng: Outcome, Constraints, Non-goals, Acceptance criteria.
  2. Triển khai tối giản, đúng phạm vi; giữ nguyên hành vi ngoài scope.
  3. Chạy bộ test hẹp nhất bao phủ phần sửa; kiểm tra nhanh diff bằng `ak-code-review --pending`.
  4. Mở PR, chờ CI + Devin Review pass (tự merge nếu repo do Bot sở hữu).

### Quy trình 2: Task khó / nhiều phase / tính năng lớn (`epic`, `elevated`–`high` risk)

*Ví dụ tiêu biểu: xây dựng plugin quản lý công việc kiểu `makeplane/plane` trên nền EzyPlatform.*

- **Chuỗi skill**: `ak-brainstorm` *(kèm `ak-research` / `ak-xia` nếu đối chiếu repo mẫu)* → `ak-plan --hard` *(+ `ak-plan validate` / `ak-plan red-team`)* → **Chief of Staff chia ticket Devin Boards theo phase** → Mỗi phase: **Skill domain EzyPlatform** + `ak-cook <plan-path>` → `ak-test` → `ak-security` *(nếu đụng auth/API/DB/input)* → `ak-code-review` → PR + Devin Review → `ak-journal` *(khi có quyết định kiến trúc đáng lưu)*
- **Cách chạy**:
  1. Khóa Outcome, Constraints, Non-goals, Acceptance criteria; so sánh phương án (tối đa 3 phương án, nêu rõ giả định dễ gãy nhất). Nếu bài toán kiến trúc có rủi ro cao → dùng `ak-predict` hoặc `ak-plan red-team`, trình `chanht_tt` duyệt trước khi code.
  2. `ak-plan` xuất kế hoạch theo phase (`plans/<ts>-<slug>/plan.md` và `phase-NN-<name>.md`), mỗi phase ghi rõ danh sách file sở hữu và tiêu chí kiểm chứng.
  3. Chief of Staff giao từng phase thành ticket độc lập trên Devin Boards; chỉ chạy song song các phase không sửa chung file (dùng `ak-worktree` nếu cần tách nhánh trong 1 VM).
  4. Mỗi phase phải qua kiểm thử thật (unit/integration + chạy kiểm tra Admin/Web trên Docker dev với plugin EzyPlatform) và qua Devin Review trước khi sang phase phụ thuộc.

### Quy trình 3: Fix bug / sự cố CI (`fix-defect`)

- **Chuỗi skill**: `ak-scout` → `ak-debug` → `ak-fix` → `ak-test` → `ak-security` *(nếu là lỗi bảo mật)* → `ak-code-review --pending`
- **Cách chạy**:
  1. Ghi rõ hiện tượng, kỳ vọng và cách tái hiện (lệnh/log/request cụ thể).
  2. Chạy `ak-debug` để **chứng minh nguyên nhân gốc bằng log/test trước khi sửa** — không đoán mò.
  3. Chạy `ak-fix`: viết hoặc bổ sung test tái hiện lỗi (đỏ → xanh), sửa đúng nguyên nhân gốc, không làm yếu test.
  4. Chạy `ak-test` kiểm tra đúng lỗi và hồi quy lân cận. Nếu là lỗi bảo mật/auth/injection/secret → chạy thêm `ak-security`.
  5. Báo cáo rõ: nguyên nhân gốc, thay đổi, bằng chứng trước/sau. Với sự cố lặp lại hoặc sau một đợt sửa lớn → dùng `ak-retro` để rút kinh nghiệm từ git history.

### Quy trình 4: Review PR (`review-audit`)

- **Chuỗi skill**: `ak-review-pr <PR>` *(cho PR GitHub)* hoặc `ak-code-review --pending` *(cho local diff/commit)*; thêm `ak-security` nếu PR chạm auth, thanh toán, input người dùng, secret hoặc dependency.
- **Cách chạy**:
  1. Đọc mô tả PR, ticket/issue, plan liên quan và lấy diff bằng `gh` / git tools.
  2. Rà soát theo thứ tự ưu tiên: đúng nghiệp vụ/contract, bug & hồi quy, bảo mật (threat model: PR lưu/truyền/lộ gì), breaking change, kiểm thử và khả năng bảo trì.
  3. Phân loại góp ý rõ ràng: **Blocker / Nên sửa / Gợi ý**, mỗi mục kèm `file:dòng`, bằng chứng và lý do.
  4. Chạy test/build local nếu rủi ro cao hoặc chạm public contract.
  5. Kết luận: **Approve / Request changes / Comment**. Mặc định chỉ đọc: **không** chạy `--fix`, `--reply` hay `--merge` nếu không được giao rõ trong ticket/lệnh.

### Quy trình 5: Khám phá sản phẩm & Marketing / GTM (`discover-validate`, `plan-campaign`, `create-content`)

Tận dụng 43 skill `marketing` + 40 skill `shared` khi chuẩn bị sản phẩm, định vị hoặc tài liệu ra mắt:

- **Khám phá & kiểm chứng ý tưởng**: `ak-play create <name> --template product-discovery` (hoặc chuỗi `ak-marketing-research` → `ak-competitor` → `ak-brainstorm` → `ak-marketing-planning`).
- **Nội dung, SEO & Ra mắt**: `ak-brand` → `ak-copywriting` / `ak-seo` / `ak-launch-strategy` / `ak-onboarding-cro` / `ak-pricing-strategy`.
- **Cổng an toàn**: Mọi bước publish ra ngoài (mạng xã hội, email hàng loạt, chạy ads trả phí) là **high risk** → mặc định dừng ở bản nháp / dry-run và cần `chanht_tt` duyệt.

---

## 5. Khung báo cáo kết thúc chuẩn

Mọi Devin session khi bàn giao cho Chief of Staff hoặc `chanht_tt` đều giữ gọn, bám 4 phần:

- **Status**: `DONE` | `DONE_WITH_CONCERNS` | `BLOCKED`
- **Kết quả & link**: PR/commit/file đã tạo hoặc cập nhật.
- **Bằng chứng chạy thật**: lệnh kiểm thử/build/kiểm tra thực tế và kết quả trên revision cuối.
- **Chưa kiểm chứng / Tồn đọng**: nêu thẳng phần chưa test được hoặc bước tiếp theo (nếu có).

---

## 6. Ghép skill AgentKit + EzyPlatform cho dự án sắp tới (Plugin quản lý công việc kiểu Plane)

Khi bắt đầu dự án plugin quản lý công việc trên core EzyPlatform (tham khảo `makeplane/plane`), các session kết hợp đúng skill sở hữu của cả hai bộ thay vì dùng một bộ đơn lẻ:

| Giai đoạn / Hạng mục | Skill EzyPlatform | Skill AgentKit |
|---|---|---|
| Nghiên cứu & đối chiếu `makeplane/plane` | `docs/research/plane-plugin-design-notes.md`, `docs/plugins/` | `ak-research`, `ak-xia`, `ak-brainstorm`, `ak-predict` |
| Thiết kế kiến trúc & chia phase | `ezy-guide`, `docs/research/ezyplatform-deep-research.md` | `ak-plan --hard`, `ak-plan red-team`, `ak-databases` |
| Xây dựng plugin Java & build/deploy dev | `skills/ezy-build-plugin/SKILL.md`, `ezy-develop`, `ezyplatform-develop` | `ak-cook`, `ak-debug`, `ak-fix`, `ak-worktree` |
| UI/UX Admin & Web + i18n/Media | `ezy-i18n`, `ezy-media`, `ezy-sync` | `ak-frontend-design`, `ak-ui-ux-pro-max`, `ak-enhance-ux-ax` |
| Kiểm thử, Edge cases & Bảo mật | Docker dev (`./scripts/up.sh`), Admin/Web smoke check | `ak-scenario`, `ak-test`, `ak-web-testing`, `ak-security` |
| Review, Tài liệu & Ra mắt | `AGENTS.md`, `README.md` | `ak-review-pr`, `ak-code-review`, `ak-docs`, `ak-launch-strategy` |
