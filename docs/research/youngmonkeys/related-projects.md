# Young Monkeys: các dự án bổ trợ, khi nào mới dùng

Đây là các đường mở rộng sau MVP, không phải danh sách dependency bắt buộc. [Kiểm kê](index.md) có link từng bài.

## Tích hợp và cấu hình

- [EzyMQ](https://youngmonkeys.org/projects/ezymq?lang=vi) có các guide cho Kafka, RabbitMQ, ActiveMQ và Mosquitto: cấu hình transport, producer/consumer/topic và ví dụ. Trang Overview hiện lặp mô tả Quick RPC; dùng nội dung Guides để phân loại. [Ví dụ push](https://youngmonkeys.org/ezymq/guides/use-ezykafka-for-push-message-system?lang=vi) là client → EzyHTTP → Kafka → EzyFox Server → client, tách ingress và phân phối. Với Work Management, giữ outbox cùng transaction cho tới khi có nhu cầu broker; nếu thêm broker, kiểm retry/dedupe, thứ tự theo item/project, replay và kiểm ACL trước fan-out. Ví dụ không cung cấp những bảo đảm đó cho plugin.
- [Quick RPC](https://youngmonkeys.org/quickrpc/guides/introduce-quick-rpc?lang=vi) tách server đăng ký handler và client gửi request; chỉ cân nhắc cho ranh giới dịch vụ đã tách, không dùng RPC giữa controller và SDK trong cùng runtime. Khi thật sự tách worker, xác định auth service-to-service, timeouts, payload version, idempotency; không dùng credential minh họa.
- [EzyFox Boot](https://youngmonkeys.org/projects/ezyfox-boot?lang=vi) mô tả auto-configuration và có sample JPA, MongoDB, Redis nhưng không có guide riêng trên index. Hữu ích khi viết worker Java độc lập; plugin trong core dùng context của host, không tự bootstrap stack.
- [Properties File](https://youngmonkeys.org/projects/properties-file?lang=vi) đọc YAML/`.properties`, có profile và hướng dẫn mã hóa giá trị. Giữ config nhỏ, ưu tiên cơ chế runtime và secret injection sẵn có; key giải mã tách khỏi dữ liệu/ZIP, mã hóa giá trị không thay thế quản lý và luân chuyển secret.

## Pattern không nên bê nguyên vào plugin

- [Game Box](https://youngmonkeys.org/projects/game-box?lang=vi) mô hình hóa player, room và đồng bộ vị trí. Có ích để hiểu phân phối sự kiện theo tập người nhận, nhưng không dùng room làm workspace ACL: membership bền vững, thu hồi quyền và audit khác với trạng thái room. Không kéo dependency vào CRUD plugin.
- [Test Utilities](https://youngmonkeys.org/projects/test-utilities?lang=vi) có assertion TestNG/Mockito, exception, dữ liệu mẫu, reflection và timing. Dùng test thuần cho state transition và policy, nhưng kiểm transaction, SQL, HTTP binding và auth bằng startup/integration trên SDK + MySQL đích; mock không chứng minh mapping/rollback. Test concurrency cần dữ liệu/seed kiểm soát, không lấy timing nhỏ trong ví dụ làm SLA.
