# Kiểm kê dự án và hướng dẫn Young Monkeys

**Đối chiếu: 26/11/2026 (UTC).** Từ [Projects tiếng Việt](https://youngmonkeys.org/projects?lang=vi) và [Projects tiếng Anh](https://youngmonkeys.org/projects?lang=en), duyệt đủ phân trang của `/api/v1/projects` thay vì chỉ lấy sáu thẻ đầu. Kiểm tra Overview, Guide và Samples của cả 11 dự án theo hai locale; theo các liên kết trong nội dung Guide. Phân tích sâu phần liên quan đến plugin; các bảng còn lại tóm tắt nội dung, không phải kết quả cài/chạy ví dụ.

- **162 link Guide** trên các trang dự án. Theo cross-link thu thêm 2 đường dẫn dạng `/{project}/guides/{slug}`: một alias Ubuntu cùng nội dung và một URL EzyHTTP lỗi. Tổng **164 URL Guide ứng viên, 163 đọc được ở cả hai locale, 162 nội dung Guide khác nhau** (so thân bài của cùng locale, bỏ alias).
- Ngoài ra đọc **13 URL bài kiểu cũ**: 12 có thân bài trùng Guide chính và 1 bài riêng về biến môi trường. Xem [link phụ và link hỏng](#link-phụ-và-link-hỏng).
- **VI**: thân bài Việt. **EN**: nội dung tiếng Anh dù mở tham số `lang=vi`; không coi có tham số locale là đã có bản dịch. Với từng Guide, đổi `lang=vi` thành `lang=en` để mở endpoint tiếng Anh. Không đếm URL locale, dấu gạch chéo cuối hay tab là bài riêng.

Đọc sâu: [EzyPlatform](ezyplatform.md) · [EzyHTTP](ezyhttp.md) · [EzyData](ezydata.md) · [EzyFox Library/Bean](ezyfox-library.md) · [EzyFox Server](ezyfox-server.md) · [dự án bổ trợ](related-projects.md).

## Trang dự án

Phiên bản dưới đây là nhãn trên trang dự án, không phải phiên bản framework được đóng trong stack. Samples là bài/mã demo được index trỏ tới; liệt kê để tra cứu, không kiểm kê toàn bộ repo ngoài hoặc chạy game/plugin.

| Dự án / Overview | Guide | Samples | Nội dung |
| --- | ---: | --- | --- |
| [EzyData](https://youngmonkeys.org/projects/ezydata?lang=vi) 1.3.2 | [15](https://youngmonkeys.org/projects/ezydata?tab=guide&lang=vi) | [Kotlin JPA](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-jpa-examples), [Kotlin Mongo](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-mongo-examples), [Kotlin Redis](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-redis-examples), [Ví dụ EzyData](https://github.com/youngmonkeys/ezydata/tree/master/ezydata-examples) | JPA/Hibernate, Mongo, Redis và repository theo datasource. |
| [EzyFox Boot](https://youngmonkeys.org/projects/ezyfox-boot?lang=vi) 1.1.6 | [0](https://youngmonkeys.org/projects/ezyfox-boot?tab=guide&lang=vi) | [Boot JPA](https://github.com/tvd12/ezyfox-examples/tree/master/ezydata-jpa), [Boot MongoDB](https://github.com/tvd12/ezyfox-examples/tree/master/ezydata-mongodb), [Boot Redis](https://github.com/tvd12/ezyfox-examples/tree/master/ezydata-redis) | Auto-config cho ứng dụng EzyFox độc lập; ba mẫu datastore, không có bài Guide. |
| [EzyFox Library](https://youngmonkeys.org/projects/ezyfox-library?lang=vi) 1.3.2 | [7](https://youngmonkeys.org/projects/ezyfox-library?tab=guide&lang=vi) | [Ví dụ EzyFox](https://github.com/youngmonkeys/ezyfox/tree/master/ezyfox-examples) | Thư viện Java nền; Bean, Binding, annotations và reflection. |
| [EzyFox Server](https://youngmonkeys.org/projects/ezyfox-server?lang=vi) 1.3.3 | [29](https://youngmonkeys.org/projects/ezyfox-server?tab=guide&lang=vi) | [Stress test](https://github.com/tvd12/ezyfox-server-example/tree/master/ezyfox-server-stresstest), [Hello World](https://github.com/tvd12/ezyfox-server-example/tree/master/hello-world), [Lucky Wheel](https://github.com/tvd12/ezyfox-server-example/tree/master/lucky-wheel), [Simple Chat](https://github.com/tvd12/ezyfox-server-example/tree/master/simple-chat), [EzySmashers](https://github.com/vu-luong/EzySmashers), [FreeChat](https://github.com/youngmonkeys/freechat), [Space Game](https://youngmonkeys.org/asset/space-game/), [Space Shooter](https://youngmonkeys.org/asset/space-shooter/) | TCP/UDP/WebSocket với zone, session, plugin và app. |
| [EzyHTTP](https://youngmonkeys.org/projects/ezyhttp?lang=vi) 1.6.7 | [17](https://youngmonkeys.org/projects/ezyhttp?tab=guide&lang=vi) | [Kotlin JPA](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-jpa-examples), [Kotlin Mongo](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-mongo-examples), [Kotlin Redis](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-redis-examples), [Ví dụ EzyHTTP (tab VI)](https://github.com/youngmonkeys/ezyhttp/tree/master/ezyhttp-examples), [Ví dụ EzyFox (tab EN)](https://github.com/tvd12/ezyfox-examples/tree/master) | HTTP server/client độc lập, controller, template, interceptor và REST/GraphQL. |
| [EzyMQ](https://youngmonkeys.org/projects/ezymq?lang=vi) 1.2.8 | [9](https://youngmonkeys.org/projects/ezymq?tab=guide&lang=vi) | [Ví dụ Kafka](https://github.com/tvd12/ezyfox-examples/tree/master/ezymq-kafka) | Adapter message broker; Overview lặp mô tả Quick RPC, Guide nói về Kafka/RabbitMQ/ActiveMQ/Mosquitto. |
| [EzyPlatform](https://youngmonkeys.org/projects/ezyplatform?lang=vi) 1.5.9 | [76](https://youngmonkeys.org/projects/ezyplatform?tab=guide&lang=vi) | [Ví dụ plugin/theme EzyPlatform](https://github.com/youngmonkeys/ezyplatform-examples) | Nền tảng plugin/theme; Admin/Web/Socket, SDK, auth, triển khai. |
| [Game Box](https://youngmonkeys.org/projects/game-box?lang=vi) 1.3.1 | [4](https://youngmonkeys.org/projects/game-box?tab=guide&lang=vi) | [FreeTank GameService](https://github.com/tvd12/freetank/blob/master/server-java/freetank-app-api/src/main/java/org/youngmonkeys/freetank/app/service/GameService.java), [EzySmashers](https://github.com/vu-luong/EzySmashers) | Thành phần game server như room, player và virtual world. |
| [Properties File](https://youngmonkeys.org/projects/properties-file?lang=vi) 1.1.8 | [2](https://youngmonkeys.org/projects/properties-file?tab=guide&lang=vi) | [Properties trong Kotlin](https://github.com/tvd12/kotlin-examples/blob/master/kotlin-properties-file-examples/src/main/kotlin/com/tvd12/kotlin/examples/properties_file/ApplicationConfig.kt) | Đọc, ghép cấu hình properties/YAML theo profile. |
| [Quick RPC](https://youngmonkeys.org/projects/quickrpc?lang=vi) 1.1.1 | [1](https://youngmonkeys.org/projects/quickrpc?tab=guide&lang=vi) | [Kotlin RPC](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-rpc-examples) | RPC nội bộ dựa trên MessagePack, server/client Java. |
| [Test Utilities](https://youngmonkeys.org/projects/test-utilities?lang=vi) 1.1.8 | [2](https://youngmonkeys.org/projects/test-utilities?tab=guide&lang=vi) | [Test utilities tests](https://github.com/tvd12/test-util/tree/master/src/test/java/com/tvd12/test/testing) | Trợ giúp test trên TestNG/Mockito, assertion, timing và fixture. |

## Guide: URL, ngôn ngữ và nội dung

### EzyData

| Bài | Nội dung |
| --- | --- |
| [EzyData: Default Functions](https://youngmonkeys.org/ezydata/guides/ezydatabase-default-functions?lang=vi) · EN | CRUD gốc: save, tìm kiếm, tồn tại, đếm và xóa theo ID/field; không tự kiểm scope. |
| [EzyJPA: Configuration](https://youngmonkeys.org/ezydata/guides/ezyjpa-configuration?lang=vi) · EN | Ánh xạ cấu hình JPA, auto/mẫu thủ công và EntityManagerFactory. |
| [EzyJPA Connect Multi-Datasources](https://youngmonkeys.org/ezydata/guides/ezyjpa-connect-multi-datasources?lang=vi) · EN | Khởi tạo factory và nhóm repository cho từng datasource. |
| [EzyJPA: Custom Query Result](https://youngmonkeys.org/ezydata/guides/ezyjpa-custom-query-result?lang=vi) · EN | Projection JPQL, scalar, aggregate và result class cho SQL native. |
| [EzyJPA: Query Data](https://youngmonkeys.org/ezydata/guides/ezyjpa-query-data?lang=vi) · EN | Repository, prefix/operator hỗ trợ, tham số, Next đứng cuối và @EzyQuery. |
| [EzyMongo: Configuration](https://youngmonkeys.org/ezydata/guides/ezymongo-configuration?lang=vi) · EN | Properties kết nối và khởi tạo database Mongo. |
| [EzyMongo: Connect Multi Databases](https://youngmonkeys.org/ezydata/guides/ezymongo-connect-multi-databases?lang=vi) · EN | Chọn config và repository theo từng database Mongo. |
| [EzyMongo: Custom Query Result](https://youngmonkeys.org/ezydata/guides/ezymongo-custom-query-result?lang=vi) · EN | Đọc projection Mongo sang kiểu kết quả riêng. |
| [EzyMongo: Query Data](https://youngmonkeys.org/ezydata/guides/ezymongo-query-data?lang=vi) · EN | Tạo repository Mongo và ánh xạ thao tác query dữ liệu. |
| [EzyRedis: Configuration](https://youngmonkeys.org/ezydata/guides/ezyredis-configuration?lang=vi) · EN | Properties client/cache Redis và mẫu khởi tạo. |
| [Guide to EzyDatabaseRepository, EzyJpaRepository, and Transactions](https://youngmonkeys.org/ezydata/guides/guide-to-ezydatabaserepository-ezyjparepository-and-transactions?lang=vi) · EN | CRUD/query tự sinh và transaction mỗi write so với EntityManager quản lý tay. |
| [Cách EzyJPA hoạt động](https://youngmonkeys.org/ezydata/guides/how-ezyjpa-works?lang=vi) · VI | Từ EntityManagerFactory/scanner tới proxy repository và triển khai query/transaction. |
| [Introduce EzyRedis](https://youngmonkeys.org/ezydata/guides/introduce-ezy-redis?lang=vi) · EN | Mẫu cache Redis, dữ liệu và publish/subscribe theo channel. |
| [Introduce EzyJPA](https://youngmonkeys.org/ezydata/guides/introduce-ezydata-jpa?lang=vi) · EN | Cài EzyJPA, cấu hình entity/repository và truy vấn ví dụ. |
| [Introduce EzyMongo](https://youngmonkeys.org/ezydata/guides/introduce-ezymongo?lang=vi) · EN | Khởi tạo Mongo, ánh xạ document và lưu/đọc qua repository. |

### EzyFox Boot

Tab Guide không liệt kê bài; xem Overview và Samples phía trên.

### EzyFox Library

| Bài | Nội dung |
| --- | --- |
| [EzyFox Annotations](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-annotations?lang=vi) · EN | Bảng annotation scan, DI, properties, lifecycle và đối tượng dùng làm dữ liệu. |
| [EzyFox Bean: Bean Creation](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-bean-bean-creation?lang=vi) · EN | Thứ tự cấu hình before/normal, bean và after; dependency và vòng lặp. |
| [EzyFox Binding: Marshal / Unmarshal](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-binding-marshal-unmarshal?lang=vi) · EN | Chuyển DTO/collection/map giữa đối tượng và biểu diễn truyền tải. |
| [Cách Reflections scan các lớp](https://youngmonkeys.org/ezyfox-library/guides/how-reflections-scans-classes?lang=vi) · VI | Package → URL/VFS → bộ lọc → scanner/index metadata. |
| [Introduce EzyFox](https://youngmonkeys.org/ezyfox-library/guides/introduce-ezyfox?lang=vi) · EN | Tiện ích Java cho generics/reflection, concurrency, future và lock. |
| [Introduce EzyFox Bean](https://youngmonkeys.org/ezyfox-library/guides/introduce-ezyfox-bean?lang=vi) · EN | Context, properties, singleton/prototype và constructor injection. |
| [Introduce EzyFox Binding](https://youngmonkeys.org/ezyfox-library/guides/introduce-ezyfox-binding?lang=vi) · EN | Mô-đun binding và cách tích hợp marshaller/unmarshaller. |

### EzyFox Server

| Bài | Nội dung |
| --- | --- |
| [Create EzyFox Server Project](https://youngmonkeys.org/ezyfox-server/guides/create-ezyfox-server-project?lang=vi) · EN | Tạo project từ Maven archetype bằng CLI hoặc IDE. |
| [Demo: EzySmashers MMO Game](https://youngmonkeys.org/ezyfox-server/guides/demo-ezy-smashers-mmo-game?lang=vi) · EN | MMO demo, client/gameplay và cách chạy sample. |
| [Demo: One-Two-Three Game](https://youngmonkeys.org/ezyfox-server/guides/demo-one-two-three-game?lang=vi) · EN | Game 1-2-3 minh họa luồng client và tổ chức demo. |
| [Deploy EzyFox Server](https://youngmonkeys.org/ezyfox-server/guides/deploy-ezyfox-server?lang=vi) · EN | Chuẩn bị máy chủ, đưa cấu hình/artifact lên và chạy server. |
| [EzyFox Android Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-android-client-sdk?lang=vi) · EN | Tạo Android client, handler kết nối/command và truy cập app. |
| [EzyFox C++ Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-cpp-client-sdk?lang=vi) · EN | Cài C++ SDK, cấu hình client và xử lý sự kiện/dữ liệu. |
| [EzyFox CSharp Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-csharp-client-sdk?lang=vi) · EN | C# SDK: setup, handler và gửi app request. |
| [EzyFox ES6 Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-es6-client-sdk?lang=vi) · EN | ES6 client, handshake/login/app access và dispatch theo command. |
| [EzyFox Flutter Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-flutter-client-sdk?lang=vi) · EN | Flutter SDK, pubspec và setup Android/iOS rồi kết nối. |
| [EzyFox Server Javascript Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-javascript-client-sdk?lang=vi) · EN | Kết nối với JavaScript client, event/data handler và app request. |
| [EzyFox Server React Native client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-react-native-client-sdk?lang=vi) · EN | React Native SDK, cấu hình và xử lý vòng đời kết nối/app. |
| [EzyFox Server Annotations](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-annotations?lang=vi) · EN | Mapping command/event, binding payload, interceptor và exception annotation. |
| [EzyFox Server Architecture](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-architecture?lang=vi) · EN | Server/zone/app/plugin, quản lý session/user và đăng ký event. |
| [EzyFox Server Config Websocket SSL](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-config-websocket-ssl?lang=vi) · EN | Thiết lập chứng chỉ và WSS cho WebSocket server. |
| [Handle Reconnection](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-handle-reconnection?lang=vi) · EN | Flow nối lại sau disconnect; không quy định replay nghiệp vụ. |
| [EzyFox Server Login](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-login?lang=vi) · EN | Mẫu login bằng thông tin đăng nhập hoặc access token ở zone. |
| [EzyFox Server Project Configuration](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-project-configuration?lang=vi) · EN | Profile, embedded/standalone và ánh xạ cấu hình tới class. |
| [EzyFox Server Scale Up](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-scale-up?lang=vi) · EN | So sánh tổ chức nhiều server truyền thống với kiến trúc dịch vụ. |
| [EzyFox Server SSL](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-ssl?lang=vi) · EN | Phân biệt cấu hình socket SSL, flow kết nối và client hỗ trợ. |
| [EzyFox Server Stress Test](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-stress-test?lang=vi) · EN | Chuẩn bị stress sample, tham số chạy và đọc kết quả. |
| [EzyFox Server With Unity](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-with-unity?lang=vi) · EN | Hai mô hình Unity client/server kết hợp kết nối EzyFox. |
| [EzyFox Swift Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-swift-client-sdk?lang=vi) · EN | Cài Swift SDK, cấu hình client, event handler và gọi app. |
| [Getting Started](https://youngmonkeys.org/ezyfox-server/guides/get-started?lang=vi) · EN | Chạy server mẫu bằng Docker hoặc native, kiểm môi trường. |
| [Handle Client Requests](https://youngmonkeys.org/ezyfox-server/guides/handle-client-requests?lang=vi) · EN | Controller, singleton/prototype handler, chọn User hay Session. |
| [Handle Exceptions](https://youngmonkeys.org/ezyfox-server/guides/handle-exceptions?lang=vi) · EN | Exception mặc định, handler theo controller và handler dùng chung. |
| [Handle Socket Events](https://youngmonkeys.org/ezyfox-server/guides/handle-socket-events?lang=vi) · EN | Đăng ký ServerReadyEvent cho plugin/app và UserLoginEvent. |
| [How to integrate EzyFox Server WebGL client into unity project](https://youngmonkeys.org/ezyfox-server/guides/how-to-integrate-ezyfox-server-csharp-client-into-?lang=vi) · EN | Tích hợp C# client vào Unity WebGL, scene login và SocketManager. |
| [Setup Embedded Server](https://youngmonkeys.org/ezyfox-server/guides/setup-embedded-server?lang=vi) · EN | Cấu hình socket/WebSocket và builder cho plugin/app entry. |
| [Use Embedded Server](https://youngmonkeys.org/ezyfox-server/guides/use-embedded-server?lang=vi) · EN | Dependency, entry app/plugin và lifecycle khởi động embedded. |

### EzyHTTP

| Bài | Nội dung |
| --- | --- |
| [EzyHTTP Annotations](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-annotations?lang=vi) · EN | Mapping route, auth, binding/converter, startup, interceptor, lỗi và GraphQL. |
| [EzyHTTP Create a Website](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-create-a-website?lang=vi) · EN | Controller/model/service, view/template và redirect. |
| [EzyHTTP Download File](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-download-file?lang=vi) · EN | ResourceRequestHandler và tải đồng bộ/bất đồng bộ. |
| [Hướng dẫn implement EzyHTTP GraphQL fetcher](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-graphql-fetcher-implementation-guide?lang=vi) · VI | Đăng ký fetcher, argument lồng nhau, validate và response shape. |
| [EzyHTTP Handle Exceptions](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-handle-exceptions?lang=vi) · EN | So sánh exception mặc định, handler cục bộ và global. |
| [EzyHTTP Handle Requests](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-handle-requests?lang=vi) · EN | Mapping verb và tách path/query/body, giữ controller nhỏ. |
| [EzyHTTP GraphQL hoạt động như thế nào](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-how-graphql-works?lang=vi) · VI | Bật GraphQL, parse request, dispatch fetcher và lọc kết quả. |
| [EzyHTTP How to Use Tomcat](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-how-to-use-tomcat?lang=vi) · EN | Tomcat standalone: dependency, config, multipart và CORS. |
| [EzyHTTP Request Arguments](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-request-arguments?lang=vi) · EN | Nguồn path/query/header/cookie/body, custom argument và converter. |
| [EzyHTTP Request Interceptor](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-request-interceptor?lang=vi) · EN | Lifecycle pre/postHandle, priority, auth và từ chối request. |
| [EzyHTTP Response Types](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-response-types?lang=vi) · EN | DTO, ResponseEntity, View, Redirect, ResponseAsync và content type. |
| [EzyHTTP Server Properties](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-server-properties?lang=vi) · EN | Tùy chọn server, multipart, CORS, static, template, async, GraphQL. |
| [EzyHTTP Serves Static Files](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-serves-static-files?lang=vi) · EN | Mapping asset công khai, filter, async, range và timeout. |
| [EzyHTTP Upload file](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-upload-file?lang=vi) · EN | FileUploader, cấu hình multipart, upload sync/async. |
| [Hướng dẫn gọi HTTP API với HttpClient](https://youngmonkeys.org/ezyhttp/guides/guide-to-calling-http-apis-with-httpclient?lang=vi) · VI | HTTP client: body/status/header, theo verb, response theo status và upload. |
| [Hướng dẫn gọi HTTP API với HttpClientProxy](https://youngmonkeys.org/ezyhttp/guides/guide-to-calling-http-apis-with-httpclientproxy?lang=vi) · VI | Facade call/request/fire/execute và các biến thể download. |
| [Introduce EzyHTTP](https://youngmonkeys.org/ezyhttp/guides/introduce-ezyhttp?lang=vi) · EN | Kiến trúc HTTP server/client và ví dụ ứng dụng độc lập. |

### EzyMQ

| Bài | Nội dung |
| --- | --- |
| [EzyActiveMQ Configuration](https://youngmonkeys.org/ezymq/guides/ezyactivemq-configuration?lang=vi) · EN | Properties ActiveMQ, thiết lập producer/consumer và topic. |
| [EzyKafka Configuration](https://youngmonkeys.org/ezymq/guides/ezykafka-configuration?lang=vi) · EN | Producer/consumer Kafka và ý nghĩa group.id. |
| [EzyMosquitto Configuration](https://youngmonkeys.org/ezymq/guides/ezymosquitto-configuration?lang=vi) · EN | Properties Mosquitto, producer/consumer và quy ước topic. |
| [EzyRabbitMQ Configration](https://youngmonkeys.org/ezymq/guides/ezyrabbitmq-configration?lang=vi) · EN | Properties RabbitMQ, producer/consumer và topic. |
| [Introduce EzyActiveMQ](https://youngmonkeys.org/ezymq/guides/introduce-ezyactivemq?lang=vi) · EN | Cấu trúc adapter ActiveMQ, payload và handler RPC ví dụ. |
| [Introduce EzyKafka](https://youngmonkeys.org/ezymq/guides/introduce-ezykafka?lang=vi) · EN | Kiến trúc adapter Kafka và ví dụ message producer/consumer. |
| [Introduce EzyMosquitto](https://youngmonkeys.org/ezymq/guides/introduce-ezymosquitto?lang=vi) · EN | Cấu trúc adapter MQTT/Mosquitto, handler và RPC mẫu. |
| [Introduce EzyRabbitMQ](https://youngmonkeys.org/ezymq/guides/introduce-ezyrabbitmq?lang=vi) · EN | Tích hợp adapter RabbitMQ với thông điệp/handler mẫu. |
| [Use EzyKafka For Push Message System](https://youngmonkeys.org/ezymq/guides/use-ezykafka-for-push-message-system?lang=vi) · EN | EzyHTTP gửi Kafka; worker Socket poll rồi đẩy tới client. |

### EzyPlatform

Xem [kiểm kê Guide EzyPlatform](../ezyplatform-guide-inventory.md#toàn-bộ-guide-theo-chủ-đề): có URL và tóm tắt tiếng Việt cho cả 76 bài trong tab Guide và alias Ubuntu. So lại với chỉ mục lần này: đủ 77 đường dẫn EzyPlatform đọc được ở cả hai locale; ưu tiên bản VI trong bảng gốc thay vì chép hai bản.

### Game Box

| Bài | Nội dung |
| --- | --- |
| [Game Box Getting Started](https://youngmonkeys.org/game-box/guides/game-box-getting-started?lang=vi) · EN | Tạo project, dependency Game Box và chạy ví dụ. |
| [Game Box MMO Game](https://youngmonkeys.org/game-box/guides/game-box-mmo-game?lang=vi) · EN | Virtual world, MMO room và handler đồng bộ vị trí. |
| [Game Box Player Management](https://youngmonkeys.org/game-box/guides/game-box-player-management?lang=vi) · EN | Player/located player/MMO player và quản lý vòng đời. |
| [Game Box Room Management](https://youngmonkeys.org/game-box/guides/game-box-room-management?lang=vi) · EN | Room thường, room theo tọa độ, MMO room và manager. |

### Properties File

| Bài | Nội dung |
| --- | --- |
| [Encrypt Configuration Properties](https://youngmonkeys.org/properties-file/guides/encrypt-configuration-properties?lang=vi) · EN | Sinh khóa, encrypt/decrypt giá trị; cần giữ khóa riêng. |
| [Read Configuration File](https://youngmonkeys.org/properties-file/guides/read-configuration-file?lang=vi) · EN | Đọc .properties/YAML, biến thể file và profile. |

### Quick RPC

| Bài | Nội dung |
| --- | --- |
| [Introduce Quick RPC](https://youngmonkeys.org/quickrpc/guides/introduce-quick-rpc?lang=vi) · EN | Tạo RPC server, handler, client và gửi request MessagePack. |

### Test Utilities

| Bài | Nội dung |
| --- | --- |
| [Introduce Test Utilities](https://youngmonkeys.org/test-utilities/guides/introduce-test-util?lang=vi) · EN | Test helper cho timing, assertion, random và reflection. |
| [Test Utilities Assertion](https://youngmonkeys.org/test-utilities/guides/test-utilities-assertion?lang=vi) · EN | assertXXX và assertThat, so kiểu lỗi và kết quả. |

## Link phụ và link hỏng

- [Add Environment Variables](https://youngmonkeys.org/add-environment-variables/?lang=vi) (EN): thiết lập `JAVA_HOME` qua shell profile và Windows Environment Variables; không cài JDK. Đây là bài phụ riêng, không phải một trong 162 Guide.
- Các URL cũ còn đọc được (EN), thân bài trùng bản ở bảng trên:
  - [Tạo project EzyFox Server](https://youngmonkeys.org/create-ezyfox-server-project/?lang=vi).
  - [Mã hóa properties](https://youngmonkeys.org/encrypt-configuration-properties/?lang=vi).
  - [Annotations EzyFox](https://youngmonkeys.org/ezyfox-annotations/?lang=vi).
  - [Xử lý lỗi HTTP](https://youngmonkeys.org/ezyhttp-handle-exceptions/?lang=vi).
  - [Bind đối số HTTP](https://youngmonkeys.org/ezyhttp-request-arguments/?lang=vi).
  - [Interceptor HTTP](https://youngmonkeys.org/ezyhttp-request-interceptor/?lang=vi).
  - [Tài nguyên tĩnh HTTP](https://youngmonkeys.org/ezyhttp-serves-static-files/?lang=vi).
  - [Xử lý lệnh Socket](https://youngmonkeys.org/handle-client-requests/?lang=vi).
  - [Socket event](https://youngmonkeys.org/handle-socket-events/?lang=vi).
  - [Giới thiệu EzyJPA](https://youngmonkeys.org/introduce-ezydata-jpa/?lang=vi).
  - [Đọc file cấu hình](https://youngmonkeys.org/read-configuration-file/?lang=vi).
  - [Embedded Socket server](https://youngmonkeys.org/use-embedded-server/?lang=vi).
- [URL sai nhóm ezyttp](https://youngmonkeys.org/ezyttp/guides/ezyhttp-create-a-website?lang=vi): trang không có thân bài ở cả VI/EN; [bản đúng](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-create-a-website?lang=vi) đọc được.
- Link cũ báo “Không tìm thấy” ở cả hai locale: `/ezyfox-sever/`, `/project/ezyfox-sever/`, `/guides/ezyfox-annotations/`, `/introduce-to-ezymongo/`; dùng [trang EzyFox Server](https://youngmonkeys.org/projects/ezyfox-server?lang=vi), [EzyFox Annotations](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-annotations?lang=vi) và [Introduce EzyMongo](https://youngmonkeys.org/ezydata/guides/introduce-ezymongo?lang=vi).
- Tám link `/blog/…` cùng host trả trang “Không tìm thấy” ở cả hai locale: `add-a-plugin-to-your-ezyplatform`, `ezyplatform-cli-commands`, `ezyplatform-plugin-development-quickstart`, `ezyplatform-sdk-commands`, `ezyplatform-setup-development-environment`, `fix-intellij-not-recognizing-path-variable`, `the-structure-of-a-plugin-project`, `update-a-plugin`. Các slug tương ứng đọc được dưới `/ezyplatform/guides/`; xem bảng EzyPlatform đã dẫn. [Hello EzyFox Server](https://youngmonkeys.org/hello-ezyfox-server.html) là trang demo, không phải bài viết.
