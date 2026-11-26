# EzyPlatform Core Stack

Nền tảng dùng chung để phát triển nhiều ứng dụng EzyPlatform, không phải một app landing page. Stack gồm EzyPlatform **1.5.9**, EzyArticle **1.5.6** đã kích hoạt, Java 11 trong container và MySQL 8.0. Runtime build từ Dockerfile của CPPAI; ezy CLI, kho plugin agent CPPAI và các gói skill công khai của Young Monkeys được khóa phiên bản trong `upstream.lock.json`.

## Khởi chạy trên máy phát triển hoặc VM cloud

Cần Git, Bash, curl, Python 3.9+ và Docker Engine/Desktop với Docker Compose V2. Không cần Java hay MySQL trên máy host. Image EzyPlatform chạy trên `linux/amd64`; máy ARM cần hỗ trợ giả lập amd64. Lần đầu cần Internet để tải mã nguồn, các bản phát hành và base image.

```bash
./scripts/up.sh
```

| Dịch vụ | Địa chỉ mặc định |
|---|---|
| Admin | <http://127.0.0.1:9090/login> |
| Tạo super admin lần đầu | <http://127.0.0.1:9090/setup-admin> |
| Web | <http://127.0.0.1:8080/> |
| MySQL | `mysql:3306` trong mạng Compose, không mở port ra host |

**Không có tài khoản hay mật khẩu Admin mặc định.** Mở `/setup-admin`, tạo super admin của bạn, rồi dùng tài khoản đó tại `/login`. Lệnh khởi động sinh mật khẩu DB ngẫu nhiên trong `.env`; không commit, chia sẻ hoặc thay file này giữa chừng với volume MySQL cũ.

Trên VM, port chỉ bind loopback. Từ máy của bạn, mở tunnel (thay `user@vm` bằng địa chỉ SSH của VM), rồi truy cập các URL ở trên:

```bash
ssh -N -L 9090:127.0.0.1:9090 -L 8080:127.0.0.1:8080 user@vm
```

Thêm `EZY_ADMIN_PORT` hoặc `EZY_WEB_PORT` vào `.env` nếu port host bị trùng. Với triển khai thực tế, cấu hình HTTPS và quyền truy cập Admin ở reverse proxy riêng; không mở thẳng cổng Admin ra Internet.

```bash
docker compose ps
docker compose logs -f ezyplatform mysql
docker compose stop   # giữ dữ liệu
./scripts/up.sh       # chạy lại
```

Compose lưu DB và runtime trong hai volume. Sao lưu cả hai trước khi nâng cấp; build image mới không thay core hoặc module trong volume runtime cũ. `docker compose down -v` **xóa** toàn bộ dữ liệu local, chỉ dùng khi chủ động muốn tạo lại từ đầu.

## CLI, plugin và skill cho agent

```bash
python3 scripts/sync-upstream.py
./scripts/ezy --version
./scripts/ak --version
```

CLI chạy trực tiếp từ mã nguồn/binary đã khóa trong `.upstream/`, không cài global. Lệnh sync lấy toàn bộ kho [CPPAI Agents Plugins](https://github.com/cppai-vn/agents-plugins) vào `.upstream/agents-plugins/`, cài các thư mục skill từ repo đó và [EzyPlatform Skill Library](https://ezyplatform.com/ezyai/skill-library?lang=vi) vào `.agents/skills/`, đồng thời tải các bộ kit [AgentKit](https://docs.agentkit.best/en/stable/getting-started/quickstart) đã khóa (`engineer`, `marketing`, xuất dạng `portable`) vào `.upstream/agentkit/` và nạp toàn bộ skill `ak-*` vào `.agents/skills/`.

- **Xác thực AgentKit:** đặt biến môi trường `AGENTKIT_API_KEY` (hoặc chạy `./scripts/ak login` một lần; credential lưu tại `~/.agentkit/`, không ghi vào repo). Dùng `--require-agentkit` để buộc bước sync báo lỗi nếu thiếu xác thực, hoặc `--skip-agentkit` để chỉ đồng bộ phần EzyPlatform.
- `.upstream/` và `.agents/skills/` được tạo lại từ lock, không sửa trực tiếp. Chọn **một** cách nạp skill cho mỗi agent: thư mục `.agents/skills/` đã sync, hoặc marketplace theo README upstream, không dùng cả hai. Các runtime plugin dành cho từng ứng dụng khác với plugin của coding agent: stack có sẵn EzyArticle; cài/kích hoạt thêm module theo nhu cầu ứng dụng, không bật mọi module marketplace theo mặc định.
- Khi chạy agent trên VM khác, cấu hình URL Admin qua kết nối riêng được cấp quyền, không dùng loopback của máy khác.

### Đồng bộ phiên bản mới

1. Kiểm tra commit mong muốn của [CLI](https://github.com/cppai-vn/ezyplatform-cli), [Docker](https://github.com/cppai-vn/ezyplatform-docker) và [Agents Plugins](https://github.com/cppai-vn/agents-plugins) (ví dụ: `git ls-remote https://github.com/cppai-vn/agents-plugins.git HEAD`), rồi cập nhật `git` trong lock.
2. Danh mục skill công khai: <https://ezyplatform.com/api/v1/skill-library/skills?limit=100>. Với mỗi gói cập nhật, tải từ `https://ezyplatform.com/api/v1/skill-library/skills/<id>/package`, kiểm tra nội dung và tên trong `SKILL.md`, rồi ghi SHA-256 của ZIP vào `skill_library`. Script từ chối gói thay đổi nếu chưa cập nhật checksum.
3. Để nâng cấp AgentKit, kiểm tra phiên bản mới qua `./scripts/ak kit list-kits --json` và cập nhật `agentkit.cli_version` / `agentkit.kits` trong `upstream.lock.json` (không chạy `ak self-update` trực tiếp trên launcher đã khóa).
4. Khi đổi Docker hoặc phiên bản EzyPlatform/EzyArticle, cập nhật build args và tag image trong `compose.yaml`; thử trên volume mới trước khi lên kế hoạch nâng cấp volume có dữ liệu.
5. Chạy `python3 scripts/sync-upstream.py --require-agentkit` để áp dụng lock, rồi kiểm tra CLI (`./scripts/ezy`, `./scripts/ak`), Admin và Web.

## Tạo ứng dụng mới trên core

Giữ mã nguồn ứng dụng ở repo riêng; core này lo runtime và bộ công cụ. Ví dụ tạo project nội dung và tái sử dụng Admin đang chạy (chế độ `live` của CLI nghĩa là **dùng một Admin có sẵn**, không nhất thiết là production):

```bash
./scripts/ezy new ../my-app --mode live --admin-url http://127.0.0.1:9090
cd ../my-app
# Lấy Access Token từ /admins/me của Admin và điền vào environment.json.
../ezyplatform-stack/scripts/ezy check
```

Để thử nghiệm với DB/container riêng cho app, dùng `ezy new --mode local` thay vì nối vào core đang chạy. Nếu tạo plugin Java mới, dùng `ezy dev create`, không dùng `ezy new`. Xem [skill xây dựng plugin](skills/ezy-build-plugin/SKILL.md) để chuẩn bị môi trường build native, đóng gói và kiểm tra trên Docker dev. Không commit `environment.json`, token hay mật khẩu.

Tài liệu: [EzyPlatform Guide](https://youngmonkeys.org/projects/ezyplatform?tab=guide) · [FAQ](https://ezyplatform.com/faq).
