# Kiểm thử plugin Marketplace trên EzyPlatform 1.5.9

Xem [chỉ mục phân tích 37 plugin miễn phí](README.md) để tra JAR, API, dữ liệu, menu/template, điểm mở rộng và ưu tiên tái sử dụng cho dự án quản lý công việc.

Ngày 26/11/2026, sandbox Compose local: EzyPlatform **1.5.9**, Java **11**, MySQL **8.0.46**. [Danh mục công khai](https://ezyplatform.com/api/v1/market/items?limit=100&type=plugin) trả đủ **55** mục (`total=55`, `hasNext=false`). Endpoint ZIP có `platformVersion=1.5.9` trả `200 application/zip` cho **37** mục miễn phí và `403` cho **18** mục trả phí. Đã cài và đối chiếu phiên bản/module thực tế của **37/37** gói tải được; 403 không phải kết luận không tương thích.

## Tái lập trong sandbox

```sh
./scripts/up.sh
# Tạo super admin tại http://127.0.0.1:9090/setup-admin; không có mật khẩu mặc định.
python3 scripts/install-plugins.py --theme freestyle
```

Script chỉ chạy với core 1.5.9 tại cổng Compose bind loopback. Nó dùng `cli.sh "install <tên>"` với danh sách [phiên bản đã kiểm thử](../../scripts/plugin-versions.tsv), kiểm tra bản Marketplace trước khi tải và dừng nếu bản cài khác manifest. CLI không có tham số chọn phiên bản cho `install`. Script đọc `dependencies=` từ `module.properties`, kích hoạt **từng loại có thật** theo thứ tự phụ thuộc, kiểm tra cache `.runtime` và khởi động lại Admin/Web. Không dùng `activate all`: trong sandbox, lệnh này đã tạo cả mục cache theme và socket cho `ezyaccount` dù gói không có các module đó. Khi đổi theme, script tắt cờ cache của theme không còn module; CLI không nhận lệnh deactivate cho mục dạng này. Nếu không chỉ định `--theme`, script giữ nguyên theme đang bật. Có thể thử `consulting`, `lucky-wheel` hoặc trở về `welcome`.

Nếu trình tải CLI lỗi, dùng mục Modules của Admin để cài bản chính xác, rồi chạy lại script; hoặc dùng `--admin-cookie-jar /đường/dẫn/cookie-local.txt` với cookie Netscape của phiên Admin **sandbox**, để script dùng endpoint Marketplace có kiểm chữ ký `POST /api/v1/projects/<tên>/<phiên-bản>/install`. Giữ cookie ngoài repo, chỉ dùng tài khoản local. Hai gói `ezyrag` và `ezyblockchain` cài thành công bằng đường Admin (`204`) sau khi CLI gặp `NoSuchFileException` ở tệp `.zip.downloading`. `ezymail` cài được khi thử lại CLI sau lỗi tương tự. Không dùng Upload Project thủ công vì đường đó không kiểm chữ ký Marketplace.

Compose mặc định chỉ khởi chạy Admin/Web. Muốn thử Socket, bật Socket trong Admin rồi chạy `docker compose exec -T ezyplatform bash cli.sh 'start socket'`. Sau restart Compose, nếu Socket không chạy, kiểm tra `socket/.runtime/ezyfox_server_instance.pid` trong container: `socket/start-service.sh` chỉ kiểm tra tệp PID. Chỉ xóa tệp PID cũ sau khi xác minh tiến trình đó không còn tồn tại. Đừng chỉ dựa vào dòng “Start socket server successfully”; kiểm tra port nội bộ/log khởi động.

## Gói cài được và kiểm thử HTTP

Ký hiệu module: **A** = admin-plugin, **W** = web-plugin, **S** = socket-plugin, **G** = socket-app, **T** = theme. Các URL Admin được gọi với phiên đăng nhập local. HTTP 200 chứa trang lỗi “Not Found” hoặc “Server error” không được tính là đạt. URL Web/API ghi dưới đây dùng Freestyle trừ khi nêu khác. Đây là smoke test chức năng cục bộ, không phải chứng nhận toàn bộ tính năng hay tương thích production.

| Plugin | Bản phát hành | Module | Cài đặt | Kiểm thử / giới hạn |
|---|---|---|---|---|
| accounting | 0.3.8 | A, W | Đạt | Admin `/accounting/overview`, `/accounting/accounts` → 200. Chưa ghi sổ hoặc xuất chứng từ. |
| consulting | 0.1.6 | A, W, T | Đạt | Admin `/consulting/customers` → danh sách người dùng; Web `/api/v1/documents` → 200; theme Consulting render được `/services`, `/documents`. |
| data-backup | 0.0.9 | A | Đạt | Admin `/data-backup/backup-clients` → 200; backup tự động lỗi vì container ứng dụng thiếu MySQL/MariaDB CLI; chưa thử restore. |
| ecommerce | 1.5.8 | A, W, S | Đạt | Admin `/ecommerce/orders`, `/ecommerce/products` → 200; trang Web `/products` chưa có trong Freestyle. Không đặt hàng hay thanh toán thật. |
| ezyaccount | 0.2.4 | A, W | Đạt | Admin `/ezyaccount/settings` → 200; Web `/ezyaccount/api/v1/account` → 401 khi chưa đăng nhập. |
| ezyai | 0.1.8 | A, W, S | Đạt | Admin `/ezyai/ai-chat-services` và Web `/ezyai/skill-library` → 200; không gọi nhà cung cấp AI. |
| ezyarticle | 1.5.6 | A, W, S | Có sẵn | Admin tạo và đọc bài `PUBLISHED`; Freestyle hiển thị đúng nội dung bài qua HTTP 200. |
| ezyblockchain | 0.0.3 | A, W | Đạt qua Admin | Admin `/ezyblockchain/control-panel` và Web `/ezyblockchain/api/v1/chains/current` → 200; log Admin cảnh báo migration xóa index không tồn tại. Chưa nối ví hoặc chạy giao dịch. |
| ezychat | 0.3.6 | A, W, S, G | Đạt | Admin `/ezychat/channels` → 200, Web API channels chưa đăng nhập → 401. `/ezychat/widget` không có embed key trả trang lỗi 200; log có `NullPointerException` khi đọc chat profile. |
| ezycrm | 0.6.3 | A, W | Đạt | Admin `/ezycrm/customers`, `/ezycrm/user-groups` → 200. Chưa bắn thông báo hoặc nhập dữ liệu khách hàng. |
| ezydefence | 0.1.5 | A, W | Đạt | Admin `/ezydefence/blacklist`, `/ezydefence/whitelist` → 200; không thay chính sách. |
| ezydelivery | 0.7.7 | A, W | Đạt | Admin `/ezydelivery/scan-delivery-order-codes` → 200; `/track-shipment` chưa có trong Freestyle. Không gọi đơn vị vận chuyển. |
| ezygame | 0.0.8 | A, W | Đạt | Admin `/ezygame/metrics` → 200. Danh mục ghi S, G nhưng ZIP thực tế không chứa hai module này. |
| ezyiot | 0.0.3 | A, W, S | Đạt | Admin `/ezyiot/devices` → 200; chưa thử thiết bị vật lý. |
| ezylogin | 0.4.7 | A, W | Đạt | Admin `/ezylogin/settings/regular` → 200; chưa kết nối OAuth/SSO bên ngoài. |
| ezymail | 0.3.3 | A, W | Đạt sau thử lại | Admin `/ezymail/templates`, `/ezymail/sent-mails` → 200. Không gửi email thật. |
| ezymarketing | 0.3.7 | A, W | Đạt | Admin `/ezymarketing/advertisements` và Web `/ezymarketing/api/v1/advertisements` → 200. |
| ezyoa | 0.4.2 | A, W | Đạt | Admin `/ezyoa/oa-services`, `/ezyoa/templates` → 200. Chưa tích hợp tài khoản Official Account. |
| ezyocr | 0.0.3 | A | Đạt | Admin `/ezyocr/ocr-business-scripts` → 200. Chưa cấu hình OCR bên ngoài. |
| ezypayment | 0.2.5 | A, W | Đạt | Admin `/ezypayment/payment-services` và Web `/api/v1/payment-plans` → 200; không gọi cổng thanh toán. |
| ezyrag | 0.0.6 | A, W, S | Đạt qua Admin | Admin `/ezyrag/settings` → 200; phụ thuộc `ezyai`; chưa gọi nhà cung cấp embedding/LLM. |
| ezyrating | 0.4.5 | A, W | Đạt | Admin `/ezyrating/dashboard` và Web `/ezyrating/user-ratings` → 200. |
| ezyseo | 0.1.2 | A, W | Đạt | Admin `/ezyseo/sitemaps`, Web `/robots.txt` và `/api/v1/sitemaps` → 200. |
| ezysupport | 0.6.2 | A, W | Đạt | Admin `/ezysupport/contact-us` và Web `/contact-us`, `/faq` → 200; không gửi yêu cầu ra ngoài. |
| ezyvector | 0.0.5 | A, W | Đạt | Admin `/ezyvector/vector-collections` → 200; chưa nạp bộ dữ liệu/đo truy vấn vector. |
| freestyle | 0.2.9 | A, T | Đạt | Admin `/freestyle/settings` → 200; theme render được bài EzyArticle ở Web. |
| game-master-server | 0.0.7 | A, W, S | Đạt | Admin `/game-master-server/game-master-server` → 200; Web API instances → 401 khi chưa đăng nhập. Chưa chạy game instance. |
| graphql | 0.3.1 | A, W, S | Đạt | Admin `/graphql/system-endpoints` → 200; `/rest/swagger` và URL schema đã thử trả trang “Not found” trên Freestyle. Chưa chạy truy vấn GraphQL. |
| logs-monitor | 0.0.5 | A, W, S | Đạt | Admin `/logs-monitor/console` và `/logs-monitor/log-folder` → 200. |
| lucky-wheel | 0.0.1 | A, W, S, G, T | Đạt | Admin `/lucky-wheel/settings` → 200. Theme Lucky Wheel đưa `/` đến `/index.html` (200); `/api/v1/lucky-wheel` → JSON 200, nhưng `/lucky-wheel` là trang “Not found”. Chưa thử lượt quay có giải thưởng. |
| markdown | 0.2.6 | A, W | Đạt | Admin `/markdown/` hiển thị trang Markdown (200). |
| omnichannel | 0.0.4 | A, W | Đạt | Admin `/omnichannel/social-networks` → 200; chưa nối kênh bên ngoài. |
| postgresql | 0.0.1 | A | Đạt | Admin `/postgresql/dashboard` → 200 trên stack MySQL; chưa đổi datasource hay thử PostgreSQL thật. |
| semi-theme | 1.0.2 | A | Đạt | Admin `/semi-theme/` → 200; ZIP `1.0.2` khai `version=1.0.1` trong `module.properties`; đây là module Admin chứ không có Web theme. |
| sites | 0.0.3 | A | Đạt | Admin `/sites/servers` và `/sites/settings` → 200; chưa tạo site/host mới. |
| socket-monitor | 0.0.3 | S | Có sẵn | Đã thấy entry loader đăng ký `AdminLoginController` khi Socket khởi động; không có trang Web riêng. |
| wordpress | 0.1.4 | A, W | Đạt | Admin `/wordpress/migration` → 200; chưa nhập dữ liệu từ WordPress. |

**Kiểm tra theme:** với Welcome, URL bài chưa render nội dung (trang “Not found”). Với Freestyle, `GET http://127.0.0.1:8080/posts/plugin-smoke-fixture` → 200, tiêu đề `Plugin Smoke Fixture`, nội dung `Sandbox plugin smoke test`. Đã chuyển lần lượt qua Consulting, Lucky Wheel rồi về Freestyle; không bật cùng lúc nhiều theme.

**Kiểm tra Socket:** sau lần restart cuối, tiến trình Java lắng nghe TCP nội bộ 3005 và 2208. Log đăng ký đủ 11 socket-plugin trong manifest và 2 socket-app (EzyChat, Lucky Wheel). Chưa kiểm thử giao thức bằng client hoặc luồng nhắn tin đầu-cuối.

## Gói bị chặn bởi quyền Marketplace

Mỗi mục dưới đây trả HTTP 403 cho yêu cầu ZIP không xác thực nhắm core 1.5.9. Không mua, cài hay kích hoạt, và chưa xác minh được bản nào chạy với core này. Bản/module lấy từ danh mục, chưa đối chiếu ZIP.

| Plugin | Bản niêm yết | Module niêm yết | Kết quả |
|---|---|---|---|
| ai-skill-marketplace | 0.0.4 | A, W, T | Chưa cài (403) |
| code | 1.0.3 | A | Chưa cài (403) |
| community | 0.0.3 | A, W, T | Chưa cài (403) |
| dropship | 0.0.5 | A, W, T | Chưa cài (403) |
| elearning | 0.8.5 | A, W, T | Chưa cài (403) |
| enhancement | 1.0.1 | A | Chưa cài (403) |
| ezysmashers | 0.2.3 | A, W, S, G, T | Chưa cài (403) |
| ezytank | 0.1.6 | A, W, S, G, T | Chưa cài (403) |
| fashion | 0.3.9 | A, W, T | Chưa cài (403) |
| logistics | 0.3.9 | A, W, T | Chưa cài (403) |
| official-shipping | 0.0.8 | A, W, T | Chưa cài (403) |
| publishing | 0.2.7 | A, W, T | Chưa cài (403) |
| retail | 0.0.3 | A, W, T | Chưa cài (403) |
| stackask | 0.3.0 | A, W, T | Chưa cài (403) |
| story | 0.0.7 | A, W, T | Chưa cài (403) |
| tournament | 0.0.7 | A, W, T | Chưa cài (403) |
| viettel-post-sandbox | 0.0.6 | A, W | Chưa cài (403) |
| zalo-sandbox | 0.1.2 | A, W | Chưa cài (403) |

## Thứ tự phụ thuộc đáng lưu ý

- `ezyarticle` và `ecommerce` là hai nút gốc. Bật `ecommerce` trước `accounting`, rồi `ezydelivery` (còn cần `ezyarticle`). `graphql` cần cả `ezyarticle` và `ecommerce`.
- `ezyarticle` → `ezymail` → `ezysupport`, `ezylogin` và (cùng `ecommerce`) `ezycrm`, `ezyrating`. `ezymarketing` còn cần EzySupport. `omnichannel` cần Ecommerce, EzyArticle, EzyRating và EzySupport.
- `ezyarticle` → `ezychat`; `graphql` + `ezychat` → `ezyai` → `ezyrag`. `ezyoa` cần EzyArticle, EzySupport và EzyChat. `consulting` cần CRM, OA, Account, Login, Support, Article và Ecommerce.
- Lần bật hàng loạt đầu tiên, khi Admin và Web khởi động song song, log có lỗi thiếu bảng (`ecommerce_product_categories`, `ecommerce_shops`, `ecommerce_product_currencies`, `ezydefence_white_uri_ips`, `ezygame_metrics`) và một số request Web lỗi. Chạy lại sau khi Admin/Web đã lên thì route bài kiểm thử trả đúng nội dung. Sandbox không đạt tiêu chí log hoàn toàn sạch: Admin vẫn cảnh báo SQL của EzyBlockchain và lỗi backup định kỳ của Data Backup. Đánh giá log theo lần khởi động, không coi HTTP 200 là bằng chứng migration hay backup đã chạy thành công.

## Bài học cho plugin quản lý công việc kiểu Plane

1. Dùng phân lane Admin/Web/Socket của core, nhưng xây schema riêng cho workspace, membership, dự án, issue, trạng thái, assignee, chu kỳ và lịch sử thay đổi. Không mượn `post` làm issue: EzyArticle hữu ích cho wiki và nội dung, còn tên trạng thái, truy vấn và phân quyền của issue khác hẳn.
2. Tận dụng tài khoản/phiên của core cùng EzyLogin/EzyAccount cho đăng nhập; xác thực và kiểm quyền theo workspace ở mỗi API của plugin. Không đồng nhất quyền global Admin với quyền xem/sửa issue của thành viên. Core Media API là ứng viên cho đính kèm nếu kiểm tra quyền truy cập và không đặt tệp nội bộ ở chế độ public.
3. Bắt đầu với API CRUD, danh sách phân trang và lọc trạng thái ở Web; dùng Admin cho cấu hình, không bắt người dùng dự án vào Admin. GraphQL plugin có màn hình schema/system endpoints, nhưng có thêm phụ thuộc Ecommerce; chỉ chọn khi lợi ích vượt chi phí. EzyChat/Socket hữu ích để nghiên cứu thông báo realtime; dùng sự kiện issue riêng và kiểm quyền subscription thay vì dùng kênh chat làm nguồn dữ liệu.
4. EzyMail phù hợp cho template thông báo/mời thành viên. Giữ SMTP, OAuth ngoài, AI, thanh toán và backup tách khỏi smoke test local; dùng adapter/mock hoặc sandbox của nhà cung cấp trong giai đoạn tiếp theo. Tách theme UI khỏi logic plugin; theme Welcome mặc định không render bài EzyArticle, còn Freestyle đã render được cùng một fixture.
