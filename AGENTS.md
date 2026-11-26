# Làm việc với EzyPlatform Core

- Chạy `./scripts/up.sh` để khởi động Admin/Web/MySQL. Chạy `python3 scripts/sync-upstream.py` để lấy toàn bộ plugin/skill đã khóa; CLI của stack là `./scripts/ezy`.
- Bắt đầu tại `.agents/skills/ezy-guide/SKILL.md`. Dùng `ezy-new` và `ezy-sync` cho project nội dung; dùng `ezy-develop` và `ezyplatform-develop` cho theme/plugin. Skill chính thức có tiền tố `ezyplatform-`; có thể thay đổi quy trình nên đọc `SKILL.md` trước khi chạy script kèm theo.
- Đặt ứng dụng mới ở repo riêng. Dùng `ezy new --mode live --admin-url URL` để nối vào core có sẵn hoặc `--mode local` để tạo sandbox độc lập. Dùng quyền tối thiểu, không commit `.env` hay `environment.json`, không chạy tác vụ ghi lên production khi chưa được phép.
- Không chỉnh file được sinh dưới `.upstream/` hay `.agents/skills/`. Cập nhật pin theo README và kiểm tra Admin/Web trên môi trường dev.
