# Làm việc với EzyPlatform Core

- Chạy `./scripts/up.sh` để khởi động Admin/Web/MySQL. Chạy `python3 scripts/sync-upstream.py` để lấy toàn bộ plugin/skill đã khóa (gồm cả bộ AgentKit `engineer` và `marketing` khi có `AGENTKIT_API_KEY` hoặc đã đăng nhập `ak`); CLI của stack là `./scripts/ezy` và `./scripts/ak`.
- Bắt đầu tại `.agents/skills/ezy-guide/SKILL.md` cho tác vụ EzyPlatform và `.agents/skills/ak-agentkit/SKILL.md` (hoặc `ak-help`) cho bộ skill AgentKit (`ak-*`). Dùng `ezy-new` và `ezy-sync` cho project nội dung; dùng `ezy-develop` và `ezyplatform-develop` cho theme/plugin. Skill chính thức có tiền tố `ezyplatform-`; có thể thay đổi quy trình nên đọc `SKILL.md` trước khi chạy script kèm theo.
- Đọc [kiến thức nền và chỉ mục blog EzyPlatform](docs/research/ezyplatform-blogs/README.md), rồi mở ghi chú theo chủ đề và bài gốc liên quan trước khi đề xuất cách vận hành, triển khai hoặc xây tính năng. Dùng skill, Guide và phiên bản stack hiện hành để xác minh các bước thực hiện.
- Tra [danh mục đầy đủ các skill Ezy](skills/README.md) và đọc bản commit trong [`skills/upstream/`](skills/upstream/) để chọn theo tác vụ. Khi tạo plugin Java mới, theo [skill xây dựng plugin của stack](skills/ezy-build-plugin/SKILL.md) để build trên native và kiểm tra artifact trên Docker dev.
- Đặt ứng dụng mới ở repo riêng. Dùng `ezy new --mode live --admin-url URL` để nối vào core có sẵn hoặc `--mode local` để tạo sandbox độc lập. Dùng quyền tối thiểu, không commit `.env` hay `environment.json`, không chạy tác vụ ghi lên production khi chưa được phép.
- Không chỉnh tay file sinh dưới `.upstream/`, `.agents/skills/` hay `skills/upstream/`. Cập nhật pin theo README và kiểm tra Admin/Web trên môi trường dev. Chạy `python3 scripts/sync-upstream.py --refresh-ezy-skills` để cập nhật bản Ezy được commit.

## Quy trình áp dụng AgentKit (cho Bot và Devin sessions)

Đọc chi tiết tại [quy trình làm việc với AgentKit](docs/agentkit-workflow.md). Các quy tắc bắt buộc cho mọi session:

- **Cổng tương xứng & Luật thép**: Trước mọi task nhiều bước, chốt 4 mục *Outcome, Constraints, Non-goals, Acceptance criteria*. Không sửa bug khi chưa chứng minh nguyên nhân gốc (`ak-debug` trước `ak-fix`; dừng và báo lại sau 3 lần sửa thất bại). Không báo xong khi chưa có bằng chứng chạy thật trên revision cuối; không làm yếu test.
- **Mặc định chỉ LOCAL / DEV**: Production, xóa DB/volume (`docker compose down -v`), sửa `.env`/secret thật hoặc publish công khai cần `chanht_tt` duyệt riêng. Mỗi nhánh/repo chỉ 1 writer tại một thời điểm; che mọi token/secret trong log, báo cáo và chat.
- **Chọn đúng chuỗi skill thực tế (AgentKit 3.2.0)**:
  - Task nhanh (`trivial`, `low` risk): `ak-scout` (nếu cần) → `ak-cook --fast --skip-journal` → `ak-test` → `ak-code-review --pending`.
  - Task lớn / nhiều phase (`epic`): `ak-brainstorm` → `ak-plan --hard` (`validate`/`red-team` khi rủi ro cao) → tách ticket không chồng chéo file qua Chief of Staff + Devin Boards → từng phase dùng skill domain EzyPlatform + `ak-cook` → `ak-test` → `ak-security` (nếu đụng auth/API/DB/input) → `ak-code-review`.
  - Fix bug / CI: `ak-scout` → `ak-debug` → `ak-fix` (test tái hiện đỏ → xanh) → `ak-test` → `ak-security` (nếu là lỗi bảo mật) → `ak-code-review --pending`.
  - Review PR: `ak-review-pr <PR>` (mặc định chỉ đọc; không `--fix`/`--reply`/`--merge` khi chưa được giao) hoặc `ak-code-review --pending`; thêm `ak-security` khi chạm auth/payment/input/secret. Phân loại `Blocker / Nên sửa / Gợi ý` kèm `file:dòng`.
- **Khác biệt bản `portable` trên Devin**: Dùng `ak-security` (không dùng tên cũ `ak-security-scan`). Điều phối đa session qua **Chief of Staff + Devin Boards** (không dùng `ak-team`/`ak-orchestrate` vốn dành cho Claude Code; chỉ dùng `ak-worktree` khi tách nhánh trong 1 VM). Không có subagent `kongming` (`--advice`) — dùng `ak-brainstorm`, `ak-predict` hoặc `ak-plan red-team` để phản biện.
- **Báo cáo kết thúc**: Luôn nêu rõ `Status` (`DONE` | `DONE_WITH_CONCERNS` | `BLOCKED`), link PR/artifact, bằng chứng chạy thật và phần chưa kiểm chứng/tồn đọng.
