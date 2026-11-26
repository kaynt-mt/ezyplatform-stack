# Vận hành, kiến trúc và cập nhật

[Về chỉ mục blog](README.md) · [Hướng dẫn theo hệ điều hành và hạ tầng](../ezyplatform-guide-inventory.md#cài-đặt-và-vận-hành)

## Tách runtime, module và ứng dụng

- [Kiến trúc phần mềm](https://ezyplatform.com/blog/kien-truc-phan-mem-cua-ezyplatform?lang=vi): core cung cấp các phần dùng chung như user/Admin, quyền, media, lịch tác vụ và cơ chế quản lý module; plugin thực hiện các khả năng bổ sung như nội dung, thương mại điện tử hay mail; theme là lớp giao diện. Đừng sửa core chỉ để thay một trang hay một quy trình nghiệp vụ.
- [Triển khai một máy chủ](https://ezyplatform.com/blog/mo-hinh-trien-khai-ezyplatform-tren-mot-may-chu?lang=vi): Admin (9090), Web (8080) và Socket là các runtime có thể chạy riêng. Không bật Socket chỉ vì cài EzyPlatform. Bài ghi cổng Socket mặc định TCP 3005, UDP 2611, WS 2208, WSS 2812; kiểm tra cấu hình thực tế thay vì dùng danh sách này làm quy tắc mở cổng.
- [Quản lý setting](https://ezyplatform.com/blog/ezyplatform-quan-ly-cai-dat-the-nao?lang=vi): `ezy_settings` có khóa `setting_name` duy nhất (quy ước snake_case), kiểu, giá trị và thời điểm cập nhật để hỗ trợ cache. Dùng API kiểu dữ liệu qua `SettingService` (ví dụ `getLongValue`/`setLongValue`); thao tác thay đổi ưu tiên Admin, không tự mở thao tác ghi cho Web/Socket. Setting ứng dụng khác cấu hình bootstrap datasource.

## Cài, deploy và vận hành Admin

- [Local cài tay](https://ezyplatform.com/blog/cai-dat-ezyplatform-tren-may-local?lang=vi): chuẩn bị JDK/MySQL, sửa datasource trong `settings/setup.properties`, đặt `JAVA_HOME` và `EZYPLATFORM_HOME`, kiểm tra `java -version`. Bài dùng `bash cli.sh "console admin"` để mở `/setup-admin`, rồi dừng console trước khi chạy `bash cli.sh "start admin"`. Web/Socket có nút Start trên dashboard của từng runtime. Đây là distribution CLI, không phải `./scripts/ezy` của repo.
- [Ubuntu server](https://ezyplatform.com/blog/trien-khai-ezyplatform-len-ubuntu-server?lang=vi): chọn máy chủ, cấu hình SSH, firewall, timezone, MySQL và user DB; dùng Nginx và Certbot; kiểm thử Admin/Web trước, thêm SSL Socket chỉ nếu có dùng. Bài dùng JDK 8 và có ghi chú Java 17+; [stack này](../../../README.md) dùng Java 11 và Docker Compose. Làm theo repo khi chạy stack dev; không sao chép trực tiếp cấu hình firewall, datasource hay reverse proxy từ ví dụ sang production.
- [Cài theme/plugin](https://ezyplatform.com/blog/huong-dan-cai-dat-theme-plugin-cho-ezyplatform?lang=vi): trong Admin vào Components → Themes → Add New, tìm theme, mua nếu cần rồi Add. Cài dependency bị thiếu, dùng Activate & Restart để bật theme, và kiểm tra URL Web. Nút **Deactivate** nghĩa là theme đang hoạt động; thấy **Activate** là còn tắt. Quy trình plugin có thể khác theme; kiểm tra yêu cầu restart trên runtime đang dùng.
- [Nâng phiên bản theme/plugin](https://ezyplatform.com/blog/ezyplatform-quan-ly-cac-phien-ban-plugin-va-theme-the-nao?lang=vi): tách bước tải xuống ZIP và Apply; bản tải được giải nén ở vùng upload, Apply gọi quy trình restart/copy sang runtime liên quan. Kiểm tra điều kiện phiên bản core và dependency trước (ví dụ ELearning phụ thuộc Ecommerce). Dùng phiên bản đã pin và kế hoạch sao lưu/khôi phục của stack, không cập nhật production chỉ vì thấy nút Update.

## Phân biệt cập nhật và tin tức

Mô tả cơ chế cập nhật không phải release note. Bài về dự án, đối tác hoặc lộ trình không xác nhận rằng phiên bản đang chạy đã có tính năng. Đối chiếu phiên bản core trong [README của stack](../../../README.md), điều kiện plugin trong [danh mục plugin runtime](../../plugins/README.md), phiên bản upstream và tài liệu phát hành trước khi dựa vào một tính năng.
