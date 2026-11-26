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

## Mẫu tái sử dụng khi phát triển plugin

| Nhu cầu | Plugin/mẫu tham khảo | Giới hạn cần kiểm |
| --- | --- | --- |
| Đăng nhập, tài khoản và thông báo | [EzyAccount](ezyaccount.md), [EzyLogin](ezylogin.md), [EzyMail](ezymail.md) | Dùng danh tính core khi phù hợp; quyền tài nguyên của ứng dụng vẫn độc lập. Test email qua SMTP giả lập. |
| Form, lọc và lịch sử | [EzyCRM](ezycrm.md), [EzySupport](ezysupport.md) | Tham khảo luồng và cách tổ chức dữ liệu; không cần phụ thuộc runtime nếu chỉ lấy pattern. |
| Nội dung, giao diện | [EzyArticle](ezyarticle.md), [Freestyle](freestyle.md), [Markdown](markdown.md) | Kiểm render với fixture và theme cụ thể; kiểm quyền media và sanitize nội dung do người dùng nhập. |
| Realtime, connector và truy vấn | [EzyChat](ezychat.md), [EzyOA](ezyoa.md), [Omnichannel](omnichannel.md), [GraphQL](graphql.md) | Chỉ thêm khi có nhu cầu, kiểm quyền trên đường truy cập thật và kiểm phụ thuộc đi kèm. |

Phần Ezy skills/build plugin mới thuộc [tài liệu riêng](../../skills/ezy-build-plugin/SKILL.md); chỉ mục này bao quát plugin runtime và bằng chứng từ các gói đã cài.

For new Java plugins, use the end-to-end [plugin lifecycle verification recipe](pilot-verification.md) before treating the runtime as proven.
