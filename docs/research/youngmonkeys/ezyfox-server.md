# EzyFox Server: nghiên cứu realtime, không phải phụ thuộc MVP

Nguồn: [Overview và Samples](https://youngmonkeys.org/projects/ezyfox-server?tab=samples&lang=vi), [kiến trúc](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-architecture?lang=vi), [socket events](https://youngmonkeys.org/ezyfox-server/guides/handle-socket-events?lang=vi), [client requests](https://youngmonkeys.org/ezyfox-server/guides/handle-client-requests?lang=vi), [ES6 SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-es6-client-sdk?lang=vi).

## Các lớp và giao thức

- Server chứa session/event và zone; zone phân chia plugin và app. Plugin thường xử lý event cấp zone như login; app có handler theo command cho nghiệp vụ. Tài liệu ví dụ controller, singleton/prototype handler, phân biệt `EzySession` là kết nối với `EzyUser` đã login. Không lớp nào tự cấp quyền truy cập tài nguyên nghiệp vụ.
- SDK mô tả kết nối → handshake → login → app access, ping/pong và disconnect; gói ứng dụng qua named command. Một kết nối WS mở hoặc handshake thành công chưa tạo phiên ứng dụng hợp lệ. [Login](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-login?lang=vi) có ví dụ credential và access token cho server độc lập; dùng [cơ chế Socket của EzyPlatform](https://youngmonkeys.org/ezyplatform/guides/overview-of-ezyplatform-socket?lang=vi) khi tích hợp core, không đem nguyên luồng login demo hoặc token Admin sang client Web.
- [Reconnection](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-handle-reconnection?lang=vi) giải thích flow nối lại; nó không hứa phát lại event ứng dụng đã bỏ lỡ. [Scale up](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-scale-up?lang=vi) đối chiếu mô hình chia server với dịch vụ riêng; session cục bộ và gửi nhiều node không tự đồng bộ. [Stress test](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-stress-test?lang=vi) là mẫu đo, không phải cam kết tải.
- TLS socket và WebSocket qua [hướng dẫn WSS](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-config-websocket-ssl?lang=vi) là setup hạ tầng riêng. Dùng WSS ở deployment thật, kiểm kết nối qua proxy/timeout, không dùng cặp key hay endpoint của sample. Compose stack chỉ tự chạy Admin/Web; [báo cáo sandbox](../../plugins/test-report.md) xác nhận socket bind và đăng ký module, **không** xác nhận giao thức client hay push đầu-cuối.

## Spike đề xuất sau MVP

1. HTTP + DB vẫn là nguồn chuẩn. Chỉ phát sự kiện sau commit, payload gồm event ID, ID tài nguyên và version tối thiểu; refetch có ACL thay vì gửi nguyên bản ghi.
2. Resolve actor từ phiên Socket tin cậy; kiểm membership lúc subscribe, khi reconnect và trước fan-out hoặc áp policy thu hồi subscription đáng tin cậy. Không lấy actor/role do client gửi, không dùng tên app như ACL.
3. Test anonymous, khác phạm vi truy cập, thu hồi quyền khi đang kết nối, rớt mạng rồi resume, duplicate/reorder và nhiều node nếu triển khai. Nếu không chứng minh kênh fan-out giữ ACL và xử lý reconnect, giữ polling HTTP.
