---
name: ezy-build-plugin
description: Tạo, lập trình, build, đóng gói, cài thử hoặc nâng cấp một plugin Java mới trên EzyPlatform Core Stack. Dùng khi cần scaffold Admin/Web, thêm API, menu, view, phân quyền, i18n, migration hoặc chuẩn bị phát hành plugin lên Marketplace.
---

# Tạo plugin EzyPlatform mới

Đây là skill hướng dẫn riêng cho **stack này**, không thay các skill upstream. App nằm ở repo riêng; repo core giữ runtime và công cụ. Nếu chỉ sửa bài viết, giao diện low-code hoặc nội dung EzyArticle, dùng nhóm skill nội dung bên dưới, không tạo plugin Java.

## 1. Chọn đúng skill

Đọc `.agents/skills/ezy-guide/SKILL.md` trước. Nếu chưa đồng bộ skill, làm theo [README](../../README.md#cli-plugin-và-skill-cho-agent). Workspace chỉ dùng Ezy có thể chạy `python3 scripts/sync-upstream.py --skip-agentkit` ở repo core; không dùng tùy chọn này trên workspace đang dùng AgentKit vì sync tạo lại `.agents/skills/` mà không nạp `ak-*`. Bản pin hiện tại có 19 skill Ezy. Ghép theo công việc:

| Việc | Skill nên đọc |
| --- | --- |
| Tạo project nội dung, kéo trạng thái về, viết và xem trước | `ezy-new` → `ezy-sync` → `ezy-author` → `ezy-verify`; `ezy-publish` khi cần đẩy nội dung đã duyệt. |
| Media, dịch chuỗi giao diện đang chạy, email | `ezy-media`, `ezy-i18n`, `ezy-mail`. Chuỗi đi kèm plugin Java nằm trong source; không dùng `ezy-i18n` để thay việc commit message bundles. |
| Tạo/build Java plugin hoặc theme | `ezy-develop` (CPPAI, bề mặt của `ezy dev`) hoặc `ezyplatform-develop` (Young Monkeys, script riêng); chọn một quy trình, không chạy cả hai. |
| Sửa giao diện Admin qua EzySupport; làm landing page | `ezy-admin-customize` hoặc `ezyplatform-admin-customize`; `ezyplatform-landing-page`. Không dùng tùy biến toàn site để thay menu/view riêng của plugin. |
| Chuẩn bị môi trường native hoặc khôi phục tài khoản | `ezyplatform-install`; `ezyplatform-reset-admin-password` chỉ cho ca khôi phục đã được chủ sở hữu cho phép, không phải bước build. |
| Nộp **plugin/theme** để xét duyệt; đăng **skill AI** | `ezy-market-submit` hoặc `ezyplatform-market-submit` cho plugin/theme; `ezyplatform-publish-skill` cho skill AI. `ezy-publish` là nội dung EzyArticle, không phát hành plugin. |

`.agents/skills/` và `.upstream/` được sync sinh lại; chỉ đọc, không chỉnh hoặc commit. Nếu agent không tự nhận thư mục `skills/` của repo, đọc trực tiếp file này qua [AGENTS.md](../../AGENTS.md); không chép vào thư mục generated. Xem [danh mục skill chính thức](https://ezyplatform.com/ezyai/skill-library?lang=vi).

## 2. Tạo project Maven trong môi trường build native

Đừng nhầm `./scripts/ezy new` với generator plugin: `new --mode live|local|both` tạo **project nội dung** có `environment.json`; không tạo module Java. `./scripts/ezy dev create` gọi **SDK** `ezy.sh create` và cần một `EZYPLATFORM_HOME` native có `cli.sh`, JDK 8, Maven, SDK và thư viện phát triển. Không trỏ `--home` vào checkout của core hoặc đường dẫn volume Compose. Dùng **native riêng để build** và **Docker của stack để chạy nghiệm thu**. Không cài native lên máy hoặc động vào môi trường dùng chung nếu chưa được phép.

Ví dụ Linux/WSL/macOS, thay hai đường dẫn tuyệt đối trước khi chạy. Nếu chưa có EzyPlatform native, đọc `ezyplatform-install` và [hướng dẫn cài môi trường phát triển](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-setup-development-environment?lang=vi) để chuẩn bị một môi trường riêng, tương thích với core đích; không thay bản Compose đang dùng. Kiểm tra các phiên bản runtime, SDK, artifact core trong POM và dependency thực sự cần. Stack hiện pin runtime **1.5.9**, **Java 11**, **MySQL 8.0**; SDK/CLI là các công cụ có version riêng. Windows dùng hướng dẫn PowerShell của skill upstream. Nếu chạy native và Compose trên cùng máy, tách cổng Admin/Web và dùng DB riêng.

```bash
STACK=/duong/dan/ezyplatform-stack
NATIVE_HOME=/duong/dan/runtime-native-rieng
OUT="$(dirname "$STACK")"

"$STACK/scripts/ezy" dev check --home "$NATIVE_HOME"
# Chỉ chạy setup nếu thiếu tool; có thể tải JDK/Maven/SDK và cài artifact vào ~/.m2.
"$STACK/scripts/ezy" dev setup --home "$NATIVE_HOME" --no-profile
"$STACK/scripts/ezy" dev create work-management --home "$NATIVE_HOME" \
  --group com.example --package com.example.workmanagement \
  --modules admin-plugin,web-plugin --out "$OUT"
cd "$OUT/work-management"
```

Dùng group/package do dự án sở hữu. Chọn thư mục mới, không ghi đè project có sẵn. Nếu gọi SDK trực tiếp trong môi trường đã cài, lệnh tương đương là `ezy.sh cp work-management -g com.example -p com.example.workmanagement -i admin-plugin,web-plugin -o "$OUT"`. Xem [quickstart](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-plugin-development-quickstart?lang=vi) và [lệnh SDK](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi).

| Thư mục/file | Công việc |
| --- | --- |
| Root `pom.xml`, `export.sh`/`export.bat` | Maven reactor, version/profiles, quy trình build và export theo scaffold. Đọc script thực tế trước khi chạy. |
| `work-management-sdk` | Phần **common** của plugin: entity, repository, domain service/policy, DTO/enum dùng chung. Không phải module cài riêng; không tạo thêm `*-common` nếu chưa có lý do và không nhầm với `ezyplatform-common` của core. |
| `work-management-admin-plugin` | Controller/view vận hành, cấu hình module, menu và SQL script do Admin áp dụng. |
| `work-management-web-plugin` | Controller/API cho user, Web auth, view/fragment tương thích với theme và static files nếu cần. |
| Module triển khai | `module.properties` chứa loại và dependency runtime; `assembly.xml` điều khiển bundle; `src/main/resources/{templates,static,messages}` cho UI. `menus.properties` ở root Admin module. Theme và Socket là tùy chọn, không bật nếu không cần; mỗi Web runtime chỉ có một theme active. |

Xem [cấu trúc plugin](https://youngmonkeys.org/ezyplatform/guides/the-structure-of-a-plugin-project?lang=vi) và [book-store mẫu](https://github.com/youngmonkeys/ezyplatform-examples/tree/main/book-store). Với plugin phụ thuộc module đã quản lý, đối chiếu cả dependency/version ở POM, `dependencies` trong `module.properties` và `@ComponentsScan` của startup test. Chỉ khi được phép, dùng `"$STACK/scripts/ezy" dev link <tên-plugin> --home "$NATIVE_HOME" -m admin-plugin,web-plugin` với module thực sự sử dụng. **Lệnh có thể tải/cài/kích hoạt dependency còn thiếu**; không chạy khi chỉ đang tra cứu. [Hướng dẫn liên kết](https://youngmonkeys.org/ezyplatform/guides/link-a-plugin?lang=vi).

## 3. Lập trình một lát cắt hoàn chỉnh

1. **Schema và Java:** lấy ví dụ một work item có project, tiêu đề, trạng thái và người được giao. Đặt entity JPA, repository theo EzyData (ví dụ `@EzyRepository` và `EzyDatabaseRepository`), service và policy ở SDK. Luồng ghi: DTO → validate → kiểm tra scope → transaction ghi entity và activity → response DTO; query theo project/workspace ngay ở repository và index theo các bộ lọc dùng thật. Tái sử dụng core User làm danh tính, không tái sử dụng bài viết CMS như bảng công việc. [Nghiên cứu EzyPlatform](../../docs/research/ezyplatform-deep-research.md) · [Thiết kế kiểu Plane](../../docs/research/plane-plugin-design-notes.md).
2. **Migration:** đặt SQL có prefix của plugin ở `<project>-admin-plugin/src/main/resources/scripts/`; xem [SQL mẫu](https://github.com/youngmonkeys/ezyplatform-examples/tree/main/personal/personal-admin-plugin/src/main/resources/scripts). Skill phát triển mô tả script áp dụng một lần theo tên file; giữ nguyên file đã phát hành, mỗi thay đổi thêm file riêng. Kiểm chứng cài mới và nâng từ bản trước; đừng giả định migration tự rollback hoặc Web-only plugin tự chạy script Admin. Sao lưu cả DB và runtime trước khi ghi vào môi trường có dữ liệu; dùng quy trình expand–migrate–contract nếu thay đổi không tương thích.
3. **Admin:** thêm `menus.properties` cho menu và khai báo route ẩn theo convention của mẫu nếu đó là màn chi tiết; đặt template dưới `templates/<project>/`, dùng controller EzyHTTP trả `View`. Kiểm tra prefix thực tế của plugin. Dùng `@Authenticated`, `@AdminId` và `@EzyFeature` cho quyền Admin; ẩn nút bằng UI không phải kiểm quyền server. [Trang Admin](https://youngmonkeys.org/ezyplatform/guides/create-an-admin-page?lang=vi) · [Menu](https://youngmonkeys.org/ezyplatform/guides/create-menus-for-admin-plugin?lang=vi).
   - Khi cần đóng góp vào layout chung, dùng fragment và `ViewDecorator` thay vì sửa template core. Ví dụ toolbar phải nhận tên fragment qua `rightToolbarToolFragments`, render region `content`; vẫn phải bảo vệ API đằng sau nút. [Toolbar Admin](https://youngmonkeys.org/ezyplatform/guides/add-admin-right-toolbar-tool?lang=vi).
4. **Web:** controller API dùng danh tính `@UserId` sau khi xác nhận Web auth interceptor được đăng ký cho route của mình; nếu có view, dùng namespace riêng, Thymeleaf/fragment hoặc mount UI qua điểm mở rộng của theme đang dùng. Kiểm tra quyền theo user, project và tài nguyên ở service, kể cả download, search và count; không cấp quyền hệ thống Admin cho thành viên. Test anonymous, sai role, workspace khác, thành viên hợp lệ và sau khi thu hồi quyền. [Xác thực Web](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-web-authentication?lang=vi) · [Phân quyền](https://youngmonkeys.org/ezyplatform/guides/permission-in-ezyplatform?lang=vi) · [Theme/plugin](https://youngmonkeys.org/ezyplatform/guides/understanding-ezyplatform-themes-and-plugins?lang=vi).
5. **i18n và static:** đưa nhãn menu, lỗi form và chuỗi mặc định vào `messages/messages.properties`, thêm `messages_vi.properties` và ngôn ngữ cần hỗ trợ. Template dùng key thay text hardcode; chỉ expose key cần cho JS. `static/` có thể truy cập qua HTTP, không để cấu hình bí mật bên trong. [Đa ngôn ngữ](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-multi-languages?lang=vi).

## 4. Test, build, export và kiểm ZIP

Từ repo plugin, kiểm tra các Maven profile và địa chỉ DB dành cho test; chỉ dùng DB dev. Chạy kiểm tra/test bằng Maven trong môi trường của helper, sau đó dùng script scaffold để đóng gói. Với các dự án mẫu, profile export có thể tắt test nên lần export thành công **không thay** lần chạy suite test riêng.

```bash
"$STACK/scripts/ezy" dev run --home "$NATIVE_HOME" -- mvn clean verify
"$STACK/scripts/ezy" dev run --home "$NATIVE_HOME" -- bash export.sh
```

Theo [script mẫu](https://github.com/youngmonkeys/ezyplatform-examples/blob/main/book-store/export.sh), script build từng module theo profile của POM → `ezy.sh package` → `ezy.sh export`. Export ghi vào **native**; lệnh trên không tự kích hoạt/restart. Nếu muốn package mà không ghi vào native runtime, dùng các bước Maven của chính scaffold đến trước dòng export và gọi `ezy.sh package` (không chạy riêng package khi chưa có artifact Maven). Nếu dùng `ezy dev export` thay thế, helper **tự kích hoạt module native và mặc định restart**, có thể đổi theme active. Chỉ dùng trong sandbox nếu đó là hành vi mong muốn.

Lấy ZIP project trong `target/project/` theo output thật. Kiểm tra cấu trúc và nội dung ZIP: module đúng loại/version, có templates/messages/SQL dự kiến, không có test config, token, core JAR trùng hay file thay cấu hình nền tảng. Lưu tên artifact, version và SHA-256 dùng để chuyển sang Docker. [Lệnh package/export](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi).

## 5. Cài artifact của chính mình vào Docker dev

1. Ở repo core, làm theo [README](../../README.md): `./scripts/up.sh`; nếu mới hoàn toàn, vào `http://127.0.0.1:9090/setup-admin`, tạo super admin rồi đăng nhập `/login`. Web mặc định ở `http://127.0.0.1:8080/`; nếu đổi cổng, dùng URL script báo. Không dùng Admin production.
2. Trong **Modules** ở Admin local, chọn **Upload Project** cho ZIP project của mình, kiểm tra tên/version rồi **Active** đúng loại Admin/Web. Không dùng Upload Project thay đường cài Marketplace có kiểm chữ ký cho plugin bên thứ ba; `cli.sh "install <name>"` tra Marketplace, không phải lệnh cài ZIP local. Không tự chép JAR vào volume hoặc chỉnh plugin đã cài.
3. Khi UI đã lưu việc kích hoạt và không tự restart, chạy `docker compose restart ezyplatform` từ repo core. Dùng `docker compose ps` và `docker compose logs --tail=100 ezyplatform mysql` để xác nhận; nếu UI báo còn chờ **Apply**, xử lý theo UI trước khi coi module đã chạy. Sau đó kiểm tra version active, menu/view Admin, route Web, lược đồ và dữ liệu; HTTP 200 ở trang chủ chỉ là kiểm tra core sống. [Cài, kích hoạt module](https://youngmonkeys.org/ezyplatform/guides/add-a-plugin-to-your-ezyplatform?lang=vi) · [Báo cáo cài Marketplace riêng](https://github.com/kaynt-mt/ezyplatform-stack/pull/5).

Compose chỉ tự khởi động Admin/Web. Nếu chọn thêm module Socket, phải bật và khởi động Socket rồi kiểm riêng kết nối/giao thức; Admin/Web lên không chứng minh Socket hoạt động.

## 6. Gỡ lỗi, nâng cấp và phát hành

| Triệu chứng | Kiểm tra trước |
| --- | --- |
| Thiếu parent/Test SDK hoặc không thấy `systemPath` | Kiểm `ezy dev check --home …`, JDK/Maven/SDK, native path và version JAR. `ezy dev sync-versions --home …` cập nhật version của dependency **đã cài**; xem diff, không tự nâng core. |
| Không thấy menu/JS/i18n, 404 | Kiểm ZIP, active/version theo loại module, prefix controller và menu, namespace template, asset/message bundle. Với `*StartupTest` trong IDE đặt working dir là module; tránh trùng cổng với runtime đang chạy. |
| 401/403 hoặc Web lấy user ID rỗng | Kiểm interceptor/theme và annotation; chạy lại cả ca có quyền lẫn không quyền, không bỏ xác thực để né lỗi. |
| App không lên sau cài, DB lỗi, lỗi class/linkage | Xem log Admin/Web trước, đối chiếu SQL/migration, `dependencies`, version, JAR core bị đóng gói trùng. Không xóa volume để “sửa” dữ liệu. [Lỗi build/export](https://youngmonkeys.org/ezyplatform/guides/nhung-ly-do-khien-ban-khong-the-build-chay-va-export-duoc-du-an-plugin-ezyplatform?lang=vi). |

Trên native, các lệnh chẩn đoán chạy qua `"$STACK/scripts/ezy" dev <lệnh> --home "$NATIVE_HOME"`:

- `status` để xem URL, trạng thái Admin/Web và module active; xem thêm `$NATIVE_HOME/logs/{admin,web}-server.log`. `restart` khởi động lại Admin/Web native, không điều khiển Compose.
- `tables core` hoặc `tables <tên-plugin>` chỉ lập danh mục SQL tạo bảng, không đọc lược đồ DB đã migrate.
- `find-class <tên-lớp>` chỉ ra JAR chứa lớp; `decompile <tên-đầy-đủ-hoặc-đường-dẫn-JAR>` chỉ dùng với artifact cục bộ có quyền kiểm tra, ưu tiên public SDK/source. Không sao chép mã giải biên dịch vào plugin.

**Nâng cấp local:** tăng version của bundle, chạy test fresh install và upgrade có dữ liệu mẫu; sao lưu DB/runtime. Trong Admin chọn **Update Manually**, tải ZIP mới, **Apply** theo [hướng dẫn cập nhật](https://youngmonkeys.org/ezyplatform/guides/update-a-plugin?lang=vi), rồi xác nhận phiên bản thực tế, schema và quyền. Rebuild image không thay plugin trong volume cũ. Rollback artifact không đảo ngược migration; nếu không tương thích, khôi phục cặp DB/runtime đã kiểm tra.

**Marketplace:** chỉ làm khi được yêu cầu và có quyền; xin duyệt riêng trước mỗi thao tác ghi. Đọc [FAQ](https://ezyplatform.com/faq) và `ezy-market-submit` hoặc `ezyplatform-market-submit`. Kiểm tra tương thích từ Java 8, i18n, license tài nguyên, namespace dành riêng, kích thước và nội dung bundle; đối chiếu giới hạn thực tế của server. Chuẩn bị icon/banner, metadata và release notes, ZIP tên `<url-name>-<X.Y.Z>.zip`. Với wrapper, quy trình là `ezy market login` (người dùng phê duyệt trong trình duyệt) → `projects`/`categories` → `create --json …` nếu chưa có project → `upload-version --name … --version … --zip … --notes-file …` → `status --name …` → `release --name …` **chỉ sau khi** bản đạt `RELEASABLE` và được duyệt phát hành. Mỗi lệnh đều đi qua `"$STACK/scripts/ezy"`.

Nếu Marketplace yêu cầu mã nguồn, chỉ nộp bản đã được phép chia sẻ bằng `upload-source --name … --version … --zip … --notes-file …`, với ZIP `<url-name>-<version>-sources.zip`. Viết hướng dẫn cài đặt, cấu hình, quyền và nâng cấp trong mục Docs của project (`/account/projects/<url-name>/docs`). CLI lưu token ở `~/.ezyplatform/credentials.json`; không đưa file này, token, mật khẩu, cookie hay DB dump vào log, ZIP hoặc Git. Tài liệu này không yêu cầu login hoặc publish thật.

### Checklist bàn giao

- [ ] Repo plugin riêng; module/dependency/version đúng; các lệnh chạy đúng môi trường native hay Docker.
- [ ] Test domain, phân quyền chéo scope và migration mới/nâng cấp; không dựa vào kết quả build hay trang chủ.
- [ ] ZIP sạch; cài đúng version ở sandbox; kiểm Admin và Web, i18n, log, rollback.
- [ ] Báo đường dẫn artifact, version, SHA-256, kết quả đã chứng minh và phần chưa kiểm. Chỉ đưa lên Marketplace khi có phê duyệt riêng.
