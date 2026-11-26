# Chọn skill EzyPlatform

Repo commit đầy đủ **19 skill upstream** trong [`skills/upstream/`](upstream/) theo [`upstream.lock.json`](../upstream.lock.json): **7/7** từ [EzyPlatform Skill Library](https://ezyplatform.com/ezyai/skill-library?lang=vi) của Young Monkeys (ZIP và SHA-256), và **12/12** từ [CPPAI Agents Plugins](https://github.com/cppai-vn/agents-plugins/tree/b34ff7c7b4f1efa2a7a28fbf40e0f53565eb1b52/ezyplatform/skills) (commit đã khóa). `ezy-shared` chứa thư viện Python dùng chung, không có `SKILL.md` nên không tính là skill. Báo cáo [37 plugin runtime](../docs/plugins/test-report.md) là một danh mục khác; đồng bộ skill không cài các plugin đó.

## Đồng bộ và tìm skill

Nếu `.agents/skills/` chưa có trên **workspace chỉ dùng Ezy**, chạy từ repo core:

```bash
python3 scripts/sync-upstream.py --skip-agentkit
find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort
```

The current lock produces `19 skills in .agents/skills`. If the workspace uses AgentKit, follow the [stack README](../README.md#cli-plugins-and-skills-for-agents) rather than running `--skip-agentkit`: sync rebuilds the skill directory, and that option leaves out the `ak-*` skills. The tables below link to the copies tracked in Git. When using a coding agent, read the corresponding copy under `.agents/skills/` and its references rather than loading both copies.

Cập nhật bản trong Git bằng `python3 scripts/sync-upstream.py --refresh-ezy-skills` ở repo core. Lệnh này tạo lại riêng `skills/upstream/` từ các nguồn đã khóa, không cài AgentKit hoặc thay `.agents/skills/`. Bản CPPAI đọc trực tiếp từ Git, không phụ thuộc vào xuống dòng của bản checkout. Kiểm tra diff trước khi commit; không sửa trực tiếp bản snapshot.

Nguồn CPPAI dùng [giấy phép MIT (© 2026 CPPAI Co.,LTD)](upstream/LICENSE-CPPAI); giữ thông báo này nếu phân phối lại. Bảy gói từ Young Monkeys được giữ nguyên nội dung ZIP; không thấy tệp giấy phép riêng trong ZIP, nên không áp giấy phép MIT của CPPAI cho các gói đó.

## Tra cứu đủ 19 skill

### CPPAI: nhóm `ezy-*`

| Skill | Làm gì / dùng khi | Không dùng khi | Skill liên quan |
| --- | --- | --- | --- |
| [`ezy-guide`](upstream/ezy-guide/SKILL.md) | Điểm bắt đầu để phân loại yêu cầu, tìm project, kiểm tra vai trò và chọn thứ tự thao tác. | Cần trực tiếp sửa hoặc phát hành; nó chỉ dẫn đường. | `ezy-new`, `ezy-sync`, `ezy-develop` |
| [`ezy-new`](upstream/ezy-new/SKILL.md) | Khởi tạo thư mục nội dung EzyArticle hoặc cấu hình kết nối khi thiếu `environment.json`/token không hợp lệ. | Tạo project Maven/plugin Java. | `ezy-sync`, `ezy-develop` |
| [`ezy-sync`](upstream/ezy-sync/SKILL.md) | So sánh hoặc kéo trang và fragment từ server về trước khi sửa; chỉ đọc trên server. | Đẩy thay đổi lên server hoặc build Java. | `ezy-author`, `ezy-publish` |
| [`ezy-author`](upstream/ezy-author/SKILL.md) | Soạn hoặc sửa HTML/Thymeleaf/CSS/JS, trang, fragment và bản dịch nội dung trong project EzyArticle. | Viết theme Java có controller/API mới hoặc quản lý message bundle của plugin. | `ezy-sync`, `ezy-media`, `ezy-verify` |
| [`ezy-media`](upstream/ezy-media/SKILL.md) | Tra cứu, tải lên, thay thế hoặc quản lý chế độ public/private của media trên site. | Đóng gói asset tĩnh trong JAR hay biến tệp riêng tư thành public để né kiểm quyền. | `ezy-author`, `ezy-verify` |
| [`ezy-i18n`](upstream/ezy-i18n/SKILL.md) | So sánh và đồng bộ key giao diện EzySupport theo ngôn ngữ, cho Admin hoặc Web. | Dịch nội dung từng trang hoặc sửa `messages*.properties` trong source plugin. | `ezy-author`, `ezy-verify`, `ezy-develop` |
| [`ezy-mail`](upstream/ezy-mail/SKILL.md) | Kiểm sức khỏe gửi mail, xem luồng Contact Us hoặc quản lý mẫu EzyMail. | Đăng bài, cài hệ thống SMTP mới hoặc gửi thư thật khi chưa được duyệt. | `ezy-media`, `ezy-verify` |
| [`ezy-verify`](upstream/ezy-verify/SKILL.md) | Xem trước trang/fragment local và kiểm nội dung trên site sau khi thay đổi. | Thay test Java, test phân quyền API hoặc kiểm migration. | `ezy-author`, `ezy-publish` |
| [`ezy-publish`](upstream/ezy-publish/SKILL.md) | Lập kế hoạch, sao lưu và đẩy nội dung EzyArticle; chuyển nội dung vào Trash hoặc khôi phục. | Nộp ZIP plugin/theme hay đăng skill AI. | `ezy-sync`, `ezy-verify`, `ezy-market-submit` |
| [`ezy-develop`](upstream/ezy-develop/SKILL.md) | Dùng CLI `ezy dev` để chuẩn bị SDK native, tạo/build/export module plugin, theme hoặc Socket; dùng cho Admin page và API viết bằng Java. | Chỉ sửa trang nội dung hoặc chỉnh CSS chung của Admin. | `ezyplatform-develop`, `ezyplatform-install`, [skill tạo plugin](ezy-build-plugin/SKILL.md) |
| [`ezy-admin-customize`](upstream/ezy-admin-customize/SKILL.md) | Tùy biến Admin đang chạy qua EzySupport, như logo, CSS, bố cục hoặc nút. | Tạo mục menu, controller, view và quyền nghiệp vụ thuộc một plugin mới. | `ezyplatform-admin-customize`, `ezy-develop` |
| [`ezy-market-submit`](upstream/ezy-market-submit/SKILL.md) | Dùng nhóm lệnh `ezy market` để gửi plugin/theme đóng gói, theo dõi xét duyệt, phát hành bản đã được duyệt. | Cài ZIP nội bộ, đăng bài EzyArticle hoặc đăng skill AI. | `ezy-develop`, `ezyplatform-market-submit` |

### Young Monkeys: nhóm `ezyplatform-*`

| Skill | Làm gì / dùng khi | Không dùng khi | Skill liên quan |
| --- | --- | --- | --- |
| [`ezyplatform-install`](upstream/ezyplatform-install/SKILL.md) | Set up EzyPlatform on a new machine. Choose native for SDK development or Docker for runtime only. | To start this existing Compose stack, use the [README](../README.md#start-on-a-development-machine-or-cloud-vm). | `ezyplatform-develop`, `ezyplatform-reset-admin-password` |
| [`ezyplatform-develop`](upstream/ezyplatform-develop/SKILL.md) | Quy trình Young Monkeys để thiết lập JDK/Maven/SDK, phát triển và export theme/plugin từ source. | Đang theo cùng quy trình với `ezy-develop` hoặc chỉ sửa nội dung. | `ezy-develop`, `ezyplatform-install`, `ezyplatform-market-submit` |
| [`ezyplatform-admin-customize`](upstream/ezyplatform-admin-customize/SKILL.md) | Quy trình Young Monkeys để chỉnh diện mạo/hành vi Admin qua EzySupport mà không viết module Java mới. | Thêm màn nghiệp vụ, route và quyền riêng cho plugin. | `ezy-admin-customize`, `ezyplatform-develop` |
| [`ezyplatform-landing-page`](upstream/ezyplatform-landing-page/SKILL.md) | Tạo trang đích độc lập từ creative brief; có thể thêm form lead, nút mua, preview và tên miền nếu cần. | Xây theme Java cho cả site hoặc ứng dụng nhiều màn/API; không tự cài plugin, đổi theme, xuất bản hay đổi DNS khi chưa được duyệt. | `ezy-author`, `ezy-media`, `ezy-verify` |
| [`ezyplatform-market-submit`](upstream/ezyplatform-market-submit/SKILL.md) | Quy trình Young Monkeys để nộp ZIP plugin/theme và quản lý bản phát hành Marketplace. | Chỉ deploy sandbox hoặc đăng AI skill. | `ezy-market-submit`, `ezyplatform-develop` |
| [`ezyplatform-publish-skill`](upstream/ezyplatform-publish-skill/SKILL.md) | Đóng gói và nộp thư mục AI skill có `SKILL.md` lên Skill Library. | Phát hành plugin/theme Java hay cập nhật bản pin của repo này. | `ezyplatform-market-submit`, `ezy-guide` |
| [`ezyplatform-reset-admin-password`](upstream/ezyplatform-reset-admin-password/SKILL.md) | Khôi phục quyền truy cập bằng reset mật khẩu Admin trong DB khi chủ hệ thống đã cho phép và không thể đăng nhập. | Cấp quyền cho thành viên, khởi tạo tài khoản mới hoặc xử lý token project hết hạn. | `ezyplatform-install`, `ezy-new` |

## Chọn theo công việc

1. **Creating a Java plugin, Java theme, or Socket module?** Start with the [stack plugin build skill](ezy-build-plugin/SKILL.md), which documents the `scripts/ezy-plugin.py` scaffold helper. If you need a native runtime, read `ezyplatform-install`; then choose either `ezy-develop` (stack CLI) or `ezyplatform-develop` (Young Monkeys scripts) for development. Use only the modules you need. `ezy new` creates content projects, not Java modules.
2. **Thêm Admin page, API Web hoặc migration vào plugin có sẵn?** Theo skill phát triển Java ở trên, không scaffold lại. Với Admin page, thêm menu/controller/view và quyền; với API, kiểm auth và scope tài nguyên ở server; với migration, thêm SQL mới trong Admin module, test cả cài mới lẫn nâng cấp có dữ liệu. Xem [Guide về Admin, DB và API](../docs/research/ezyplatform-guide-inventory.md) và [bài học từ lần thử plugin runtime](../docs/plugins/test-report.md#thứ-tự-phụ-thuộc-đáng-lưu-ý): có ca thiếu bảng khi bật hàng loạt và Admin/Web khởi động song song; HTTP 200 không xác nhận migration đã chạy. Chỉ chỉnh logo/CSS chung của Admin thì dùng nhóm `*-admin-customize`.
3. **Sửa giao diện/nội dung site đang có?** Nếu chưa có project nội dung, chạy theo `ezy-new`; sau đó `ezy-sync` → `ezy-author` → thêm `ezy-media`, `ezy-i18n` hoặc `ezy-mail` tùy việc → `ezy-verify` preview → người dùng duyệt → `ezy-publish` → `ezy-verify` trên site. Nếu mục tiêu là trang đích độc lập, bắt đầu bằng `ezyplatform-landing-page`; giữ nháp trước khi xuất bản.
4. **Deploy hay phát hành?** Để nghiệm thu plugin nội bộ: build/đóng gói ở native → cài ZIP của mình ở Docker dev → kiểm module active, Admin/Web, log, quyền và migration theo [skill tạo plugin](ezy-build-plugin/SKILL.md). Để phân phối công khai: `ezy-market-submit` hoặc `ezyplatform-market-submit` cho plugin/theme; `ezyplatform-publish-skill` cho AI skill; `ezy-publish` cho nội dung site. Xin duyệt riêng trước thao tác ghi và không đưa thông tin xác thực vào Git.
