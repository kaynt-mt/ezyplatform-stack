# Kiểm kê tài liệu công khai EzyPlatform

**Ngày đối chiếu:** 26/11/2026 (UTC). Bắt đầu từ thanh điều hướng [ezyplatform.com](https://ezyplatform.com/), đối chiếu [Guide tiếng Việt](https://youngmonkeys.org/projects/ezyplatform?tab=guide&lang=vi) và [Guide tiếng Anh](https://youngmonkeys.org/projects/ezyplatform?tab=guide&lang=en), rồi theo liên kết trong bài. Hai mục lục có cùng 76 bài; thêm một URL cũ `deploy-ezyplatform` có nội dung trùng bài Ubuntu: **77 URL hướng dẫn, 76 nội dung**. Ưu tiên bản Việt hoặc nội dung có sẵn nếu chưa dịch; không đếm bản dịch như bài khác. Không tìm được sitemap XML hay kho `/docs` riêng trên ezyplatform.com; độ bao phủ dưới đây là những gì menu, chỉ mục chính thức và liên kết bài dẫn đến, không phải lời khẳng định đã đọc mọi URL có thể tồn tại.

## Trang chính thức và tài liệu tra cứu

| Nguồn | Phạm vi |
| --- | --- |
| [Giới thiệu](https://ezyplatform.com/ezyplatform-introduction) | Nền tảng low-code, 5 phần runtime/công cụ, hệ sinh thái module; phân biệt giữa các module được nhắc và module thực sự có trong stack. |
| [Cài đặt](https://ezyplatform.com/installation-guide) | Tài nguyên, Java/MySQL, domain, cách tìm module, hỗ trợ và tài liệu riêng từng module. |
| [FAQ](https://ezyplatform.com/faq) | 12 mục: định nghĩa/mục tiêu, phạm vi mã mở, giao thức, cài đặt, mở rộng, thương mại, index và quy định/thời gian xét Marketplace. |
| [Java docs](https://ezyplatform.com/java-docs) | Theo `allclasses-noframe.html` và `overview-summary.html` dưới đường dẫn 1.5.9: lấy được 962 trang (881 class/interface và 81 package summary). Admin 552 + 35, Common 7 + 3, Web 241 + 25, Socket 81 + 18. Tra sâu các lớp liên quan tới plugin, không diễn giải từng method/overload. Tiêu đề trang có thể ghi module `0.0.2 API`; đó không phải số phiên bản distribution `1.5.9` trong URL. |
| [Marketplace](https://ezyplatform.com/market) | [Danh mục công khai](https://ezyplatform.com/api/v1/market/items?limit=100&lang=vi) trả 60 mục; lấy danh sách tab Tài liệu của từng mục, thu được nội dung 532 bài công khai. Đọc sâu phần liên quan đến thiết kế dưới đây; việc tải nội dung không đồng nghĩa với phân tích từng tài liệu Marketplace hay chạy plugin. |

Đọc tiếp: [tổng hợp kỹ thuật](ezyplatform-deep-research.md) · [nghiên cứu framework Young Monkeys](youngmonkeys/index.md).

## Toàn bộ Guide theo chủ đề

### Kiến trúc và hệ sinh thái

| Hướng dẫn | Nội dung / lưu ý |
| --- | --- |
| [Giới thiệu nền tảng](https://youngmonkeys.org/ezyplatform/guides/introduce-ezyplatform?lang=vi) | Host, framework, marketplace; phạm vi mã mở và thương mại có điều kiện. |
| [Lợi ích cho người dùng](https://youngmonkeys.org/ezyplatform/guides/-what-benefits-does-ezyplatform-provide-to-users?lang=vi) | Chi phí/thời gian xây sản phẩm, thử ý tưởng và nâng chất lượng; không phải benchmark. |
| [Cấu trúc runtime](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-structure?lang=vi) | Admin/Web/Socket; theme duy nhất, nhiều plugin, token socket phân loại. |
| [Tech stack](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-tech-stack?lang=vi) | EzyHTTP–Jetty–Thymeleaf, EzyData–Hibernate/JPA, EzyFox Server. |
| [Theme và plugin](https://youngmonkeys.org/ezyplatform/guides/understanding-ezyplatform-themes-and-plugins?lang=vi) | Bốn loại phần mở rộng runtime, theme, phối hợp và vị trí lưu module. |
| [Bảo mật](https://youngmonkeys.org/ezyplatform/guides/why-ezyplatform?lang=vi) | Tách Admin/Web, BCrypt, mã hóa, chính sách URI và upload; không tự cung cấp ACL của ứng dụng. |
| [Lộ trình](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-development-roadmap?lang=vi) | Phát triển cộng đồng/thị trường, tiến tới giảm code và AI; không coi roadmap là tính năng đã phát hành. |
| [Mô hình cho nhà phát triển](https://youngmonkeys.org/ezyplatform/guides/how-do-developers-make-money-through-ezyplatform?lang=vi) | Làm sản phẩm/module, phân phối qua Marketplace; cân nhắc điều kiện FAQ. |

### Phát triển và đóng gói

| Hướng dẫn | Nội dung / lưu ý |
| --- | --- |
| [Chuẩn bị môi trường dev](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-setup-development-environment?lang=vi) | Tách bước cài runtime, SDK và IDE khỏi lập trình từng module. |
| [Cài SDK](https://youngmonkeys.org/ezyplatform/guides/install-ezyplatform-sdk?lang=vi) | Chuẩn bị runtime, SDK và build thư viện phụ thuộc. |
| [Quickstart plugin](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-plugin-development-quickstart?lang=vi) | Thứ tự tạo/import, startup test, export và kiểm tra trên runtime. |
| [Tạo plugin](https://youngmonkeys.org/ezyplatform/guides/create-a-plugin?lang=vi) | Scaffold module, cấu hình working directory, chạy và export. |
| [Import project](https://youngmonkeys.org/ezyplatform/guides/import-a-plugin-project?lang=vi) | Kiểm kê module phụ thuộc và thiết lập run configuration. |
| [Import IntelliJ](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-import-a-plugin-project-to-intellij?lang=vi) | Maven/JDK, annotation processing và cấu hình chạy; tách lỗi IDE khỏi lỗi build. |
| [Lỗi path variable IntelliJ](https://youngmonkeys.org/ezyplatform/guides/fix-intellij-not-recognizing-path-variable?lang=vi) | Chẩn đoán IDE không nhận biến đường dẫn, không đổi source để né. |
| [Cấu trúc dự án](https://youngmonkeys.org/ezyplatform/guides/the-structure-of-a-plugin-project?lang=vi) | Maven module, SDK chia sẻ, assembly, metadata, menu, static, templates, TestNG. |
| [Liên kết plugin](https://youngmonkeys.org/ezyplatform/guides/link-a-plugin?lang=vi) | Module mục tiêu phải có sẵn; check dependency và `@ComponentsScan`. |
| [Lệnh SDK](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi) | `create`, `package`, `export`, `link`, phiên bản và đồng bộ dependency. |
| [Lệnh CLI runtime](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-cli-commands?lang=vi) | Quản lý DB/server/module/cập nhật; khác SDK và wrapper của stack. |
| [Module icon](https://youngmonkeys.org/ezyplatform/guides/guide-to-creating-icons-for-ezyplatform-plugin?lang=vi) | Chuẩn bị icon và định danh khi phân phối; không trộn với CSS icon của menu. |
| [Sinh unit test](https://youngmonkeys.org/ezyplatform/guides/generate-unit-test-class?lang=vi) | `UnitTestClassGenerator` tạo khung, không thay assertion. |
| [Build/chạy/export lỗi](https://youngmonkeys.org/ezyplatform/guides/nhung-ly-do-khien-ban-khong-the-build-chay-va-export-duoc-du-an-plugin-ezyplatform?lang=vi) | Chẩn đoán theo từng bước: JDK/Maven, working dir, dependency và export. |
| [Lỗi thường gặp khác](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-some-reasons-leading-to-errors?lang=vi) | Quên export/menu/`@Authenticated`, đường dẫn có khoảng trắng. |

### HTTP, giao diện, ngôn ngữ và xác thực

| Hướng dẫn | Nội dung / lưu ý |
| --- | --- |
| [Admin authentication](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-admin-authentication?lang=vi) | Cookie token, `@Authenticated`, `@AdminId`, proxy quyền; không dùng thay user Web. |
| [Web authentication](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-web-authentication?lang=vi) | Tích hợp interceptor, route anonymous tùy chọn, `@UserId`, bật feature permissions. |
| [Phân quyền](https://youngmonkeys.org/ezyplatform/guides/permission-in-ezyplatform?lang=vi) | Role–feature–API bằng `@EzyFeature`; hiệu lực Web phụ thuộc theme/cấu hình. |
| [Trang Admin](https://youngmonkeys.org/ezyplatform/guides/create-an-admin-page?lang=vi) | Controller trả Thymeleaf view; route có tên plugin đứng trước. |
| [Menu Admin](https://youngmonkeys.org/ezyplatform/guides/create-menus-for-admin-plugin?lang=vi) | `menus.properties`, vùng menu, icon, i18n và badge. |
| [Badge](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-add-badge-to-admin-menu-item?lang=vi) | Cung cấp dữ liệu số lượng theo menu item; tránh đếm dữ liệu ngoài quyền. |
| [Toolbar phải](https://youngmonkeys.org/ezyplatform/guides/add-admin-right-toolbar-tool?lang=vi) | `rightToolbarToolFragments`, region `content`, CSS/JS riêng và message key. |
| [Hotkeys](https://youngmonkeys.org/ezyplatform/guides/hotkeys-in-ezyplatform?lang=vi) | Phím toàn cục và theo màn; kiểm tra xung đột với trình soạn thảo và UI riêng của plugin. |
| [Popup xác nhận](https://youngmonkeys.org/ezyplatform/guides/confirmation-popup-usage?lang=vi) | Luồng Admin/Web cho thao tác nhạy cảm; server vẫn kiểm tra quyền. |
| [Điều hướng previousScreen](https://youngmonkeys.org/ezyplatform/guides/using-previousscreen-to-link-admin-screens?lang=vi) | Giữ filter/pagination và quay về màn hợp lệ khi lưu/redirect. |
| [JavaScript Admin](https://youngmonkeys.org/ezyplatform/guides/available-javascript-functions-in-admin?lang=vi) | `ezyadmin`: i18n, date/number, data table, toast, form errors, session, xử lý server. |
| [JavaScript Web](https://youngmonkeys.org/ezyplatform/guides/available-javascript-functions-in-web?lang=vi) | `ezyweb`: helpers date/number, API error/form, cookie, ngôn ngữ và media URL. |
| [Thiết kế theme](https://youngmonkeys.org/ezyplatform/guides/designing-and-programming-a-theme?lang=vi) | Tách template/fragment/layout, i18n, gắn nội dung động. |
| [ViewDecorator](https://youngmonkeys.org/ezyplatform/guides/guide-to-implement-viewdecorator?lang=vi) | Dữ liệu dùng chung trước render, `setVariableIfAbsent`, tránh query nặng toàn site. |
| [View schema](https://youngmonkeys.org/ezyplatform/guides/guide-to-installing-view-schema?lang=vi) | `ViewSchemaFetcher`/`ViewMultipleSchemaFetcher` mô tả URI và biến view cho tooling; không phải ACL. |
| [Đa ngôn ngữ](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-multi-languages?lang=vi) | Message bundles, label và dữ liệu nhiều ngôn ngữ; tránh hardcode tên state hệ thống. |
| [Cấu hình ngôn ngữ Web](https://youngmonkeys.org/ezyplatform/guides/setup-multiple-languages-for-web?lang=vi) | Bật ngôn ngữ người dùng và cấu hình mặc định; phân biệt với dịch nội dung. |
| [Lỗi Web](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-handle-exception-and-error-for-web?lang=vi) | Global exception/error handler của Web tách logic lỗi khỏi view. |
| [Cấu hình website](https://youngmonkeys.org/ezyplatform/guides/setup-a-website?lang=vi) | Các biến trang và cấu hình analytics; không phải công cụ đo cycle/task. |

### Dữ liệu, tác vụ và tích hợp

| Hướng dẫn | Nội dung / lưu ý |
| --- | --- |
| [Phân trang](https://youngmonkeys.org/ezyplatform/guides/pagination-implementation?lang=vi) | Cursor/offset, class pair theo sort, converter, repository, service và generator. |
| [Reactive](https://youngmonkeys.org/ezyplatform/guides/reactive-usage?lang=vi) | Chạy việc độc lập song song bằng `multiple`/`single`; không thay transaction. |
| [Tìm kiếm Admin](https://youngmonkeys.org/ezyplatform/guides/integrating-admin-global-search?lang=vi) | `AdminSearchService` và `SearchResultModel`; kiểm tra dữ liệu trả về theo người gọi. |
| [Cấu hình setting](https://youngmonkeys.org/ezyplatform/guides/setting-feature?lang=vi) | Kiểu dữ liệu, cập nhật cache, mã hóa, prefix key có tên plugin. |
| [Bảng link](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-insert-data-to-link-table?lang=vi) | `ezy_links`, `LinkService` và appender; không index deep link riêng tư. |
| [Hàm record ngẫu nhiên](https://youngmonkeys.org/ezyplatform/guides/how-to-install-the-random-record-query-function?lang=vi) | Phương án random skip/limit tránh `ORDER BY RAND` trên tập lớn. |
| [Event nội bộ](https://youngmonkeys.org/ezyplatform/guides/create-and-handle-internal-events-in-ezyplatform?lang=vi) | Phân luồng theo tên, priority, `VoidEvent` và handler trả kết quả. |
| [Batch AdminDataAppender](https://youngmonkeys.org/ezyplatform/guides/guide-to-implementing-batch-jobs-with-admindataappender?lang=vi) | Query/transform/save, checkpoint, kiểm soát batch và lifecycle. |
| [Cron](https://youngmonkeys.org/ezyplatform/guides/guide-to-using-cron-expressions-supported-by-ezyplatform?lang=vi) | 5/6 trường, chủ nhật = 0, không `? L W #` hoặc trường năm. |
| [Notification và letter](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-send-notification-and-letter?lang=vi) | Template, service, receiver và API/UI Web. Không đồng nhất với email ngoài. |
| [MediaControllerService](https://youngmonkeys.org/ezyplatform/guides/mediacontrollerservice-usage-guide?lang=vi) | Upload/replace/download/delete, metadata, private predicate, adapter storage và event. |
| [Media modal](https://youngmonkeys.org/ezyplatform/guides/guide-to-using-the-media-modal-in-the-admin-ui?lang=vi) | `showMediaModal`, callback/cách tách nhiều field chọn media. |
| [MIME](https://youngmonkeys.org/ezyplatform/guides/mime-types-detected-by-ezyplatform?lang=vi) | Danh sách nhóm nhận biết, không phải allowlist nghiệp vụ. |
| [Giảm dung lượng ảnh](https://youngmonkeys.org/ezyplatform/guides/how-ezyplatform-reduces-image-file-size?lang=vi) | Ngưỡng, xử lý theo định dạng, bản gốc, metadata và adapter ngoài. |
| [JavascriptService](https://youngmonkeys.org/ezyplatform/guides/guide-to-using-javascriptservice?lang=vi) | Rhino, scope/bean và object result; không nhận script không đáng tin. |
| [Socket](https://youngmonkeys.org/ezyplatform/guides/overview-of-ezyplatform-socket?lang=vi) | Luồng login theo loại user/admin, hook Socket và JS client mẫu. |

### Cài đặt và vận hành

| Hướng dẫn | Nội dung / lưu ý |
| --- | --- |
| [Cài EzyPlatform](https://youngmonkeys.org/ezyplatform/guides/install-ezyplatform?lang=vi) | Docker hoặc cài tay; Linux/macOS/Windows, `EZYPLATFORM_HOME`. |
| [Deploy nhanh](https://youngmonkeys.org/ezyplatform/guides/quickstart-deploy-ezyplatform-to-server?lang=vi) | Hosting hỗ trợ so với tự triển khai; dẫn bài Ubuntu/Docker/học thêm. |
| [Deploy Ubuntu](https://youngmonkeys.org/ezyplatform/guides/deploy-ezyplatform-on-ubuntu?lang=vi) | Tài nguyên, DB, JDK, Nginx, HTTPS và bảo toàn cấu hình mã hóa; [URL cũ cùng nội dung](https://youngmonkeys.org/ezyplatform/guides/deploy-ezyplatform?lang=vi). |
| [Deploy Docker](https://youngmonkeys.org/ezyplatform/guides/deploy-ezyplatform-with-docker?lang=vi) | Compose, biến triển khai, volume và load balancer; ưu tiên Compose của stack khi làm dự án này. |
| [Nhà cung cấp hạ tầng](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-deployment-guide-for-infrastructure-providers?lang=vi) | Quy trình triển khai khi cung cấp nhiều môi trường, quyền vận hành và checklist hạ tầng. |
| [Thêm plugin](https://youngmonkeys.org/ezyplatform/guides/add-a-plugin-to-your-ezyplatform?lang=vi) | Tìm module, tải/cài, kích hoạt, khởi động lại, xử lý điều kiện phụ thuộc. |
| [Cập nhật plugin](https://youngmonkeys.org/ezyplatform/guides/update-a-plugin?lang=vi) | Luồng cập nhật theo hệ điều hành; tránh nhầm update module với nâng core. |
| [Nâng cấp/khôi phục](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-update-and-recovery?lang=vi) | Điểm vào tài liệu cập nhật/khôi phục theo OS và lỗi. |
| [Cập nhật Windows](https://youngmonkeys.org/ezyplatform/guides/updating-ezyplatform-on-windows-guide?lang=vi) | Tải, chuẩn bị cài đặt theo quy trình Admin. |
| [Khôi phục khi lỗi](https://youngmonkeys.org/ezyplatform/guides/recover-ezyplatform-when-an-error-occurs?lang=vi) | Xác định JDK hoặc plugin thiếu/không hợp lệ và log trước khi sửa. |
| [Chuyển máy chủ](https://youngmonkeys.org/ezyplatform/guides/migrate-ezyplatform-from-server-a-to-server-b?lang=vi) | Copy runtime, DB dump/import, đổi DNS/Nginx. |
| [Nhiều cài đặt và DB](https://youngmonkeys.org/ezyplatform/guides/install-multiple-ezyplatforms-with-a-single-database?lang=vi) | Khóa riêng cho từng instance; tách database, không chia schema tùy tiện. |
| [Tên miền và SSL](https://youngmonkeys.org/ezyplatform/guides/set-up-domain-and-ssl-for-ezyplatform?lang=vi) | DNS, Nginx, Certbot; EzySupport hoặc thao tác thủ công. |
| [SSL WebSocket](https://youngmonkeys.org/ezyplatform/guides/set-up-ssl-for-ezyplatform-websocket?lang=vi) | Chứng chỉ, khởi động lại Socket/cập nhật WSS, gia hạn và xử lý lỗi. |
| [Tối ưu cấu hình](https://youngmonkeys.org/ezyplatform/guides/toi-uu-cau-hinh-cho-ezyplatform?lang=vi) | Có thể tắt Socket; heap/CPU/thread theo từng runtime và tải thực. |
| [LogbackAppender](https://youngmonkeys.org/ezyplatform/guides/installing-a-log-appender-in-ezyplatform?lang=vi) | Đăng ký và cấu hình appender, tách log vận hành khỏi audit dữ liệu. |
| [API thống kê](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-statistics-apis?lang=vi) | Events vòng đời server/module; điều khiển qua `allow_send_statistics_data`. |
| [Nhận diện riêng](https://youngmonkeys.org/ezyplatform/guides/brand-your-ezyplatform?lang=vi) | Chợ, logo, footer, liên hệ và fallback. |

## Tài liệu Marketplace có ích cho quyết định thiết kế

| Ứng viên | Chứng cứ và kết luận |
| --- | --- |
| **EzyArticle** | [Tổng quan](https://ezyplatform.com/market/items/ezyarticle/docs/gioi-thieu-plugin-ezyarticle), [tag dữ liệu](https://ezyplatform.com/market/items/ezyarticle/docs/huong-dan-tich-hop-cho-phep-tag-duoc-du-lieu), [bình luận dữ liệu](https://ezyplatform.com/market/items/ezyarticle/docs/gioi-thieu-tinh-nang-binh-luan-du-lieu-voi-ezyarticle), [page fragments](https://ezyplatform.com/market/items/ezyarticle/docs/huong-dan-su-dung-page-fragment). Ngoài CMS, tài liệu có tag tích hợp loại entity và thảo luận nội bộ Admin (luồng, mention, resolve). Đây là pattern có ích, nhưng chưa chứng minh có API Web bảo đảm ACL của ứng dụng, càng không mặc định tính năng tài liệu hiện tại có trong artifact **1.5.6** đã pin. |
| **EzyLogin / EzyAccount** | [EzyLogin](https://ezyplatform.com/market/items/ezylogin/docs/tong-quan-plugin-ezylogin) mô tả đăng ký/đăng nhập/khôi phục, OAuth/SSO, 2FA và session; [EzyAccount](https://ezyplatform.com/market/items/ezyaccount/docs/mo-ta-chi-tiet-tinh-nang-quan-ly-thong-bao-va-hom-thu) cho người dùng xem thông báo/hộp thư. Là ứng viên cho identity UI và inbox, không sở hữu membership/ACL hay mặc định đã cài. |
| **EzyMail** | [Tổng quan](https://ezyplatform.com/market/items/ezymail/docs/tong-quan-MjU4): gửi email, mẫu, nháp, theo dõi gửi, thiết lập SMTP. Dùng qua adapter nếu thực sự cần email/invite; notification core là kênh khác. |
| **Markdown** | [Tổng quan](https://ezyplatform.com/market/items/markdown/docs/tong-quan-plugin-markdown): editor và render cho CMS; có cú pháp HTML trực tiếp nên không mặc định an toàn khi render mô tả do user cung cấp. |
| **EzyChat / EzyOA / EzyCRM** | [Kiến trúc EzyChat](https://ezyplatform.com/market/items/ezychat/docs/kien-truc-cua-plugin-ezychat) hữu ích khi tham khảo Socket/channel; [EzyOA](https://ezyplatform.com/market/items/ezyoa/docs/tong-quan-plugin-ezyoa) là tích hợp Official Account/webhook; [EzyCRM](https://ezyplatform.com/market/items/ezycrm/docs/tong-quan-MzUw) xoay quanh khách hàng và nhóm người dùng. Chỉ cân nhắc phụ thuộc khi plugin thật sự dùng các tính năng đó. |

Không kiểm tra nội dung cần tài khoản/mua, các video khóa học ngoài website, phiên bản tài liệu không còn được liên kết hoặc hành vi thực tế của các plugin.
