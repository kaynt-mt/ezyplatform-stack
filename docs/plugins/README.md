# Plugin runtime miễn phí trên EzyPlatform 1.5.9

Danh mục nghiên cứu **37/37** gói ZIP tải được từ Marketplace trên core **1.5.9**. Xem [báo cáo kiểm thử](test-report.md) để tái lập sandbox, đọc kết quả HTTP/Socket và biết vì sao 18 gói cần quyền tải không nằm trong phạm vi này.

## Cách đọc

- Phiên bản và loại module đối chiếu [manifest](../../scripts/plugin-versions.tsv) với `module.properties` trong thư mục đã cài từ gói Marketplace. Nếu bản ZIP và metadata khác nhau, cột phiên bản ghi cả hai (`ZIP/module`).
- Hồ sơ từng gói dựa trên 82 module đã cài: đọc JAR của plugin/SDK (`jar`/classfile và `javap -v`), annotation HTTP, entry loader Socket, menu, template, tệp cấu hình và DDL đi kèm; không đưa JAR, ZIP hay giá trị cấu hình vào repo.
- **Phân tích tĩnh ≠ kiểm thử chức năng.** Tên class chỉ ra vị trí nên đọc tiếp, không chứng minh extension là API công khai hoặc được bật; `CREATE TABLE` cho biết bảng được khai báo, không chứng minh migration đã chạy. URL annotation có thể nhận prefix khác khi mount. Mỗi hồ sơ tách riêng quan sát sandbox, kể cả 401 hoặc trang lỗi được trả với HTTP 200.

## Danh mục

| Plugin | Bản | Module | Phạm vi chính |
|---|---|---|---|
| [accounting](accounting.md) | `0.3.8` | admin-plugin, web-plugin | Kế toán: hệ thống tài khoản, người dùng và sổ giao dịch |
| [consulting](consulting.md) | `0.1.6` | admin-plugin, web-plugin, theme | Tư vấn: khách hàng, nhân sự, tài liệu và theme riêng |
| [data-backup](data-backup.md) | `0.0.9` | admin-plugin | Sao lưu dữ liệu và lập lịch snapshot |
| [ecommerce](ecommerce.md) | `1.5.8` | admin-plugin, web-plugin, socket-plugin | Catalog, cửa hàng, giỏ hàng, đơn hàng và checkout |
| [ezyaccount](ezyaccount.md) | `0.2.4` | admin-plugin, web-plugin | Giao diện và API tài khoản thành viên |
| [ezyai](ezyai.md) | `0.1.8` | admin-plugin, web-plugin, socket-plugin | Cấu hình dịch vụ AI, skill và thư viện kỹ năng |
| [ezyarticle](ezyarticle.md) | `1.5.6` | admin-plugin, web-plugin, socket-plugin | Bài viết, trang nội dung, taxonomy và xuất bản |
| [ezyblockchain](ezyblockchain.md) | `0.0.3` | admin-plugin, web-plugin | Chain, token và quản lý địa chỉ ví |
| [ezychat](ezychat.md) | `0.3.6` | admin-plugin, web-plugin, socket-plugin, socket-app | Channel, profile, hội thoại và Socket app/plugin |
| [ezycrm](ezycrm.md) | `0.6.3` | admin-plugin, web-plugin | Khách hàng, phụ trách, nhóm và lịch sử |
| [ezydefence](ezydefence.md) | `0.1.5` | admin-plugin, web-plugin | Chính sách IP, danh sách cho phép/chặn và filter HTTP |
| [ezydelivery](ezydelivery.md) | `0.7.7` | admin-plugin, web-plugin | Mã vận đơn, quét mã và giao nhận |
| [ezygame](ezygame.md) | `0.0.8` | admin-plugin, web-plugin | Chỉ số, sự kiện và thành tích |
| [ezyiot](ezyiot.md) | `0.0.3` | admin-plugin, web-plugin, socket-plugin | Thiết bị, cấu hình và lane Socket |
| [ezylogin](ezylogin.md) | `0.4.7` | admin-plugin, web-plugin | Đăng nhập, cấu hình nhà cung cấp và phiên |
| [ezymail](ezymail.md) | `0.3.3` | admin-plugin, web-plugin | Template email, thư nháp và theo dõi gửi |
| [ezymarketing](ezymarketing.md) | `0.3.7` | admin-plugin, web-plugin | Quảng cáo, chiến dịch và liên kết rút gọn |
| [ezyoa](ezyoa.md) | `0.4.2` | admin-plugin, web-plugin | Tài khoản Official Account, kịch bản và thông báo |
| [ezyocr](ezyocr.md) | `0.0.3` | admin-plugin | Kịch bản OCR và cấu hình nhận dạng |
| [ezypayment](ezypayment.md) | `0.2.5` | admin-plugin, web-plugin | Dịch vụ thanh toán, gói và thuê bao |
| [ezyrag](ezyrag.md) | `0.0.6` | admin-plugin, web-plugin, socket-plugin | Quản trị RAG và tích hợp lớp AI |
| [ezyrating](ezyrating.md) | `0.4.5` | admin-plugin, web-plugin | Đánh giá người dùng, mục và hành trình khách hàng |
| [ezyseo](ezyseo.md) | `0.1.2` | admin-plugin, web-plugin | Sitemap, liên kết và robots |
| [ezysupport](ezysupport.md) | `0.6.2` | admin-plugin, web-plugin | Liên hệ, FAQ, tuyển dụng và nội dung hỗ trợ |
| [ezyvector](ezyvector.md) | `0.0.5` | admin-plugin, web-plugin | Collection và quản trị dữ liệu vector |
| [freestyle](freestyle.md) | `0.2.9` | admin-plugin, theme | Theme Web tổng quát và cấu hình giao diện |
| [game-master-server](game-master-server.md) | `0.0.7` | admin-plugin, web-plugin, socket-plugin | Quản lý game master và các instance |
| [graphql](graphql.md) | `0.3.1` | admin-plugin, web-plugin, socket-plugin | Cấu hình endpoint và schema GraphQL |
| [logs-monitor](logs-monitor.md) | `0.0.5` | admin-plugin, web-plugin, socket-plugin | Console, thư mục log và lane Socket |
| [lucky-wheel](lucky-wheel.md) | `0.0.1` | admin-plugin, web-plugin, theme, socket-plugin, socket-app | Trò quay thưởng có Admin, Web, theme và Socket |
| [markdown](markdown.md) | `0.2.6` | admin-plugin, web-plugin | Giao diện Markdown và module Web |
| [omnichannel](omnichannel.md) | `0.0.4` | admin-plugin, web-plugin | Quản trị kênh ngoài và kết nối mạng xã hội |
| [postgresql](postgresql.md) | `0.0.1` | admin-plugin | Bề mặt quản trị PostgreSQL |
| [semi-theme](semi-theme.md) | `1.0.2/1.0.1` | admin-plugin | Module Admin hỗ trợ giao diện; không có Web theme |
| [sites](sites.md) | `0.0.3` | admin-plugin | Quản lý máy chủ và cấu hình site |
| [socket-monitor](socket-monitor.md) | `0.0.3` | socket-plugin | Module Socket giám sát và entry loader |
| [wordpress](wordpress.md) | `0.1.4` | admin-plugin, web-plugin | Cấu hình và luồng nhập dữ liệu WordPress |

## Tái sử dụng cho plugin quản lý công việc kiểu Plane

| Ưu tiên | Plugin/mẫu | Nên lấy | Không nên sao chép |
|---|---|---|---|
| 1 — nền nhận dạng | [EzyAccount](ezyaccount.md), [EzyLogin](ezylogin.md) | Định danh và phiên core; bề mặt tài khoản và đăng nhập | Quyền hệ thống không cấp quyền xem issue. Tự xây workspace membership, lời mời, permission và audit theo workspace. |
| 2 — mẫu nghiệp vụ | [EzyCRM](ezycrm.md) | Gán người phụ trách, lọc/danh sách nhóm, lịch sử và dữ liệu mở rộng | Không dùng khách hàng làm issue hoặc kéo Ecommerce vào MVP chỉ để lấy assignment. |
| 3 — intake | [EzySupport](ezysupport.md) | Form tiếp nhận, danh sách triage, template thông báo | Form hỗ trợ không phải board. Tạo bản ghi intake riêng; chuyển thành issue có idempotency và quyền rõ ràng. |
| 4 — thông báo | [EzyMail](ezymail.md), [EzyChat](ezychat.md) | Template email; tách HTTP, Socket app/plugin và event lifecycle; dùng SMTP giả lập và Socket client local khi kiểm thử | Không lấy chat làm nguồn dữ liệu issue; chỉ phát sau commit, kiểm quyền mỗi subscription, không gửi mail thật trong smoke test. |
| 5 — automation đa kênh | [EzyOA](ezyoa.md), [Omnichannel](omnichannel.md) | Tách connector, template, tham số và kịch bản; adapter kênh bổ sung sau MVP | Không coi mẫu `task_list_message.properties` là engine task hoặc biến OA thành phụ thuộc bắt buộc. |
| 6 — nội dung và giao diện | [EzyArticle](ezyarticle.md), [Freestyle](freestyle.md), [Markdown](markdown.md) | Wiki, template/fragment Web, nội dung mô tả và kiểm thử render có fixture | Không lấy post làm issue; không để template, Markdown hay Media làm lộ dữ liệu nội bộ. |
| Sau MVP | [GraphQL](graphql.md), [EzyAI](ezyai.md), [EzyRAG](ezyrag.md), [EzyVector](ezyvector.md) | Giao diện truy vấn, bot hoặc tìm kiếm có lọc quyền, nếu SQL/HTTP không còn đáp ứng | Tránh kéo phụ thuộc Ecommerce, provider AI và vector vào luồng tạo/sửa issue. Phải kiểm quyền ở resolver và ở bước truy xuất. |

**Lộ trình đề xuất:** bắt đầu bằng Admin module cấu hình và Web module có CRUD workspace → project → issue. Tạo schema/migration riêng cho trạng thái, assignee, thứ tự trên board, cycle và lịch sử; dùng session core nhưng kiểm membership trên từng API, kể cả truy vấn con theo ID. Viết test hai workspace để phát hiện đọc/ghi chéo, test migration từ database trống và khi nâng phiên bản. Thêm intake, email và Socket theo từng đợt; kiểm tra Web với fixture riêng thay vì chỉ dựa vào HTTP 200.

Phần Ezy skills/build plugin mới thuộc tài liệu riêng; chỉ mục này chỉ bao quát plugin runtime và bằng chứng từ các gói đã cài.
