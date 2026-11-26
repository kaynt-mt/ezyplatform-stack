# Young Monkeys project and guide inventory

**Reviewed November 26, 2026 (UTC).** Starting with the [Vietnamese Projects page](https://youngmonkeys.org/projects?lang=vi) and the [English Projects page](https://youngmonkeys.org/projects?lang=en), we went through every page of `/api/v1/projects` rather than stopping at the first six cards. We checked the Overview, Guide, and Samples tabs for all 11 projects in both locales and followed links within the guides. The plugin-related material received a closer review. The other tables summarize the sources; they do not report installation or runtime results.

- The project pages listed **162 guide links**. Cross-links supplied two more URLs of the form `/{project}/guides/{slug}`: an Ubuntu alias with identical content and a broken EzyHTTP URL. Of the **164 candidate guide URLs, 163 were readable in both locales, covering 162 distinct guides** after comparing article bodies within the same locale and excluding the alias.
- We also reviewed **13 older article URLs**: 12 duplicate the main guide texts, and one is a separate article on environment variables. See [additional and broken links](#additional-and-broken-links).
- **VI** means the article body is Vietnamese. **EN** means the body is English, even with `lang=vi`; a locale parameter alone does not prove a translation exists. For each guide, replace `lang=vi` with `lang=en` to open its English endpoint. Locale variants, trailing slashes, and tabs do not count as separate articles.

Detailed notes: [EzyPlatform](ezyplatform.md) · [EzyHTTP](ezyhttp.md) · [EzyData](ezydata.md) · [EzyFox Library/Bean](ezyfox-library.md) · [EzyFox Server](ezyfox-server.md) · [Supporting projects](related-projects.md).

## Project pages

Version numbers are the labels shown on the project pages, not the framework versions bundled in this stack. Samples are the articles or demo code linked from the index. They are listed for reference; this inventory does not cover every external repository or run games or plugins.

| Project / Overview | Guides | Samples | What it covers |
| --- | ---: | --- | --- |
| [EzyData](https://youngmonkeys.org/projects/ezydata?lang=vi) 1.3.2 | [15](https://youngmonkeys.org/projects/ezydata?tab=guide&lang=vi) | [Kotlin JPA](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-jpa-examples), [Kotlin Mongo](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-mongo-examples), [Kotlin Redis](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-redis-examples), [For example, EzyData](https://github.com/youngmonkeys/ezydata/tree/master/ezydata-examples) | JPA/Hibernate, MongoDB, Redis, and repositories grouped by data source. |
| [EzyFox Boot](https://youngmonkeys.org/projects/ezyfox-boot?lang=vi) 1.1.6 | [0](https://youngmonkeys.org/projects/ezyfox-boot?tab=guide&lang=vi) | [Boot JPA](https://github.com/tvd12/ezyfox-examples/tree/master/ezydata-jpa), [Boot MongoDB](https://github.com/tvd12/ezyfox-examples/tree/master/ezydata-mongodb), [Boot Redis](https://github.com/tvd12/ezyfox-examples/tree/master/ezydata-redis) | Auto-configuration for standalone EzyFox applications; three data-store samples and no guides. |
| [EzyFox Library](https://youngmonkeys.org/projects/ezyfox-library?lang=vi) 1.3.2 | [7](https://youngmonkeys.org/projects/ezyfox-library?tab=guide&lang=vi) | [For example, EzyFox](https://github.com/youngmonkeys/ezyfox/tree/master/ezyfox-examples) | Core Java library for Bean, Binding, annotations, and reflection. |
| [EzyFox Server](https://youngmonkeys.org/projects/ezyfox-server?lang=vi) 1.3.3 | [29](https://youngmonkeys.org/projects/ezyfox-server?tab=guide&lang=vi) | [Stress test](https://github.com/tvd12/ezyfox-server-example/tree/master/ezyfox-server-stresstest), [Hello World](https://github.com/tvd12/ezyfox-server-example/tree/master/hello-world), [Lucky Wheel](https://github.com/tvd12/ezyfox-server-example/tree/master/lucky-wheel), [Simple Chat](https://github.com/tvd12/ezyfox-server-example/tree/master/simple-chat), [EzySmashers](https://github.com/vu-luong/EzySmashers), [FreeChat](https://github.com/youngmonkeys/freechat), [Space Game](https://youngmonkeys.org/asset/space-game/), [Space Shooter](https://youngmonkeys.org/asset/space-shooter/) | TCP, UDP, and WebSocket support with zones, sessions, plugins, and apps. |
| [EzyHTTP](https://youngmonkeys.org/projects/ezyhttp?lang=vi) 1.6.7 | [17](https://youngmonkeys.org/projects/ezyhttp?tab=guide&lang=vi) | [Kotlin JPA](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-jpa-examples), [Kotlin Mongo](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-mongo-examples), [Kotlin Redis](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-redis-examples), [Examples of EzyHTTP (tab VI)](https://github.com/youngmonkeys/ezyhttp/tree/master/ezyhttp-examples), [Examples of EzyFox (tab EN)](https://github.com/tvd12/ezyfox-examples/tree/master) | Standalone HTTP server and client, controllers, templates, interceptors, REST, and GraphQL. |
| [EzyMQ](https://youngmonkeys.org/projects/ezymq?lang=vi) 1.2.8 | [9](https://youngmonkeys.org/projects/ezymq?tab=guide&lang=vi) | [For example Kafka](https://github.com/tvd12/ezyfox-examples/tree/master/ezymq-kafka) | Message broker adapters. The Overview repeats the Quick RPC description; the guides cover Kafka, RabbitMQ, ActiveMQ, and Mosquitto. |
| [EzyPlatform](https://youngmonkeys.org/projects/ezyplatform?lang=vi) 1.5.9 | [76](https://youngmonkeys.org/projects/ezyplatform?tab=guide&lang=vi) | [Plugin and Theme of EzyPlatform](https://github.com/youngmonkeys/ezyplatform-examples) | Plugin and theme platform covering Admin, Web, Socket, the SDK, authentication, and deployment. |
| [Game Box](https://youngmonkeys.org/projects/game-box?lang=vi) 1.3.1 | [4](https://youngmonkeys.org/projects/game-box?tab=guide&lang=vi) | [FreeTank GameService](https://github.com/tvd12/freetank/blob/master/server-java/freetank-app-api/src/main/java/org/youngmonkeys/freetank/app/service/GameService.java), [EzySmashers](https://github.com/vu-luong/EzySmashers) | Game server components such as rooms, players, and virtual worlds. |
| [Properties File](https://youngmonkeys.org/projects/properties-file?lang=vi) 1.1.8 | [2](https://youngmonkeys.org/projects/properties-file?tab=guide&lang=vi) | [Properties in Kotlin](https://github.com/tvd12/kotlin-examples/blob/master/kotlin-properties-file-examples/src/main/kotlin/com/tvd12/kotlin/examples/properties_file/ApplicationConfig.kt) | Read and merge properties and YAML configuration by profile. |
| [Quick RPC](https://youngmonkeys.org/projects/quickrpc?lang=vi) 1.1.1 | [1](https://youngmonkeys.org/projects/quickrpc?tab=guide&lang=vi) | [Kotlin RPC](https://github.com/tvd12/kotlin-examples/tree/master/kotlin-rpc-examples) | Internal RPC over MessagePack with a Java server and client. |
| [Test Utilities](https://youngmonkeys.org/projects/test-utilities?lang=vi) 1.1.8 | [2](https://youngmonkeys.org/projects/test-utilities?tab=guide&lang=vi) | [Test utilities tests](https://github.com/tvd12/test-util/tree/master/src/test/java/com/tvd12/test/testing) | TestNG and Mockito helpers for assertions, timing, and fixtures. |

## Guide URLs, languages, and topics

### EzyData

| Article | What it covers |
| --- | --- |
| [EzyData: Default Functions](https://youngmonkeys.org/ezydata/guides/ezydatabase-default-functions?lang=vi) · EN | Built-in CRUD: save, find, check existence, count, or delete by ID or field. These methods do not enforce access scope. |
| [EzyJPA: Configuration](https://youngmonkeys.org/ezydata/guides/ezyjpa-configuration?lang=vi) · EN | JPA configuration mapping, automatic and manual setup, and EntityManagerFactory. |
| [EzyJPA Connect Multi-Datasources](https://youngmonkeys.org/ezydata/guides/ezyjpa-connect-multi-datasources?lang=vi) · EN | Initialize factories and group repositories by data source. |
| [EzyJPA: Custom Query Result](https://youngmonkeys.org/ezydata/guides/ezyjpa-custom-query-result?lang=vi) · EN | JPQL projections, scalars, aggregates, and result classes for native SQL. |
| [EzyJPA: Query Data](https://youngmonkeys.org/ezydata/guides/ezyjpa-query-data?lang=vi) · EN | Repositories, supported prefixes and operators, parameter binding, Next as the last argument, and @EzyQuery. |
| [EzyMongo: Configuration](https://youngmonkeys.org/ezydata/guides/ezymongo-configuration?lang=vi) · EN | Connection properties and database initialization for MongoDB. |
| [EzyMongo: Connect Multi Databases](https://youngmonkeys.org/ezydata/guides/ezymongo-connect-multi-databases?lang=vi) · EN | Select configuration and repositories for each MongoDB database. |
| [EzyMongo: Custom Query Result](https://youngmonkeys.org/ezydata/guides/ezymongo-custom-query-result?lang=vi) · EN | Map MongoDB projections to custom result types. |
| [EzyMongo: Query Data](https://youngmonkeys.org/ezydata/guides/ezymongo-query-data?lang=vi) · EN | Create MongoDB repositories and map data queries. |
| [EzyRedis: Configuration](https://youngmonkeys.org/ezydata/guides/ezyredis-configuration?lang=vi) · EN | Redis client and cache properties and initialization examples. |
| [Guide to EzyDatabaseRepository, EzyJpaRepository, and Transactions](https://youngmonkeys.org/ezydata/guides/guide-to-ezydatabaserepository-ezyjparepository-and-transactions?lang=vi) · EN | Generated CRUD and query methods and per-write transactions versus manual EntityManager management. |
| [How EzyJPA works](https://youngmonkeys.org/ezydata/guides/how-ezyjpa-works?lang=vi) · VI | From EntityManagerFactory and scanning to repository proxies, query execution, and transactions. |
| [Introduce EzyRedis](https://youngmonkeys.org/ezydata/guides/introduce-ezy-redis?lang=vi) · EN | Redis caching samples, data structures, and channel-based publish/subscribe. |
| [Introduce EzyJPA](https://youngmonkeys.org/ezydata/guides/introduce-ezydata-jpa?lang=vi) · EN | Set up EzyJPA, configure entities and repositories, and run a sample query. |
| [Introduce EzyMongo](https://youngmonkeys.org/ezydata/guides/introduce-ezymongo?lang=vi) · EN | Initialize MongoDB, map documents, and save and load through repositories. |

### EzyFox Boot

The Guide tab lists no articles; see the Overview and Samples above.

### EzyFox Library

| Article | What it covers |
| --- | --- |
| [EzyFox Annotations](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-annotations?lang=vi) · EN | Annotations for scanning, dependency injection, properties, lifecycle, and data objects. |
| [EzyFox Bean: Bean Creation](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-bean-bean-creation?lang=vi) · EN | Order of before and regular configuration, bean creation, and after-configuration; dependencies and cycles. |
| [EzyFox Binding: Marshal / Unmarshal](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-binding-marshal-unmarshal?lang=vi) · EN | Convert DTOs, collections, and maps to and from their wire representations. |
| [How Reflections scan the classes](https://youngmonkeys.org/ezyfox-library/guides/how-reflections-scans-classes?lang=vi) · VI | From packages through URL/VFS locations and filters to scanning and metadata indexing. |
| [Introduce EzyFox](https://youngmonkeys.org/ezyfox-library/guides/introduce-ezyfox?lang=vi) · EN | Java utilities for generics, reflection, concurrency, futures, and locks. |
| [Introduce EzyFox Bean](https://youngmonkeys.org/ezyfox-library/guides/introduce-ezyfox-bean?lang=vi) · EN | Contexts, properties, singleton and prototype beans, and constructor injection. |
| [Introduce EzyFox Binding](https://youngmonkeys.org/ezyfox-library/guides/introduce-ezyfox-binding?lang=vi) · EN | The binding module and how to integrate marshallers and unmarshallers. |

### EzyFox Server

| Article | What it covers |
| --- | --- |
| [Create EzyFox Server Project](https://youngmonkeys.org/ezyfox-server/guides/create-ezyfox-server-project?lang=vi) · EN | Create a project from a Maven archetype with the CLI or an IDE. |
| [Demo: EzySmashers MMO Game](https://youngmonkeys.org/ezyfox-server/guides/demo-ezy-smashers-mmo-game?lang=vi) · EN | MMO demo, client and gameplay, and how to run the sample. |
| [Demo: One-Two-Three Game](https://youngmonkeys.org/ezyfox-server/guides/demo-one-two-three-game?lang=vi) · EN | A One-Two-Three game illustrating the client flow and the demo layout. |
| [Deploy EzyFox Server](https://youngmonkeys.org/ezyfox-server/guides/deploy-ezyfox-server?lang=vi) · EN | Prepare the host, deploy configuration and artifacts, and start the server. |
| [EzyFox Android Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-android-client-sdk?lang=vi) · EN | Build an Android client with connection and command handlers and app access. |
| [EzyFox C++ Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-cpp-client-sdk?lang=vi) · EN | Install the C++ SDK, configure the client, and handle events and data. |
| [EzyFox CSharp Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-csharp-client-sdk?lang=vi) · EN | Install the C# SDK, register handlers, and send app requests. |
| [EzyFox ES6 Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-es6-client-sdk?lang=vi) · EN | ES6 client setup, handshake, login, app access, and command dispatch. |
| [EzyFox Flutter Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-flutter-client-sdk?lang=vi) · EN | Flutter SDK, pubspec and Android/iOS setup, and connecting to the server. |
| [EzyFox Server Javascript Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-javascript-client-sdk?lang=vi) · EN | Connect a JavaScript client, handle events and data, and send app requests. |
| [EzyFox Server React Native client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-react-native-client-sdk?lang=vi) · EN | React Native SDK setup and handling the connection and app lifecycle. |
| [EzyFox Server Annotations](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-annotations?lang=vi) · EN | Command and event mappings, payload binding, interceptors, and exception annotations. |
| [EzyFox Server Architecture](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-architecture?lang=vi) · EN | Server, zone, app, and plugin architecture; session and user management; event registration. |
| [EzyFox Server Config Websocket SSL](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-config-websocket-ssl?lang=vi) · EN | Set up certificates and WSS for a WebSocket server. |
| [Handle Reconnection](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-handle-reconnection?lang=vi) · EN | Reconnect after a disconnect. The guide does not define replay of business events. |
| [EzyFox Server Login](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-login?lang=vi) · EN | Zone login using credentials or an access token. |
| [EzyFox Server Project Configuration](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-project-configuration?lang=vi) · EN | Profiles, embedded and standalone modes, and configuration-to-class mapping. |
| [EzyFox Server Scale Up](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-scale-up?lang=vi) · EN | Compare traditional multi-server deployments with a service architecture. |
| [EzyFox Server SSL](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-ssl?lang=vi) · EN | Socket TLS configuration, the connection flow, and supported clients. |
| [EzyFox Server Stress Test](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-stress-test?lang=vi) · EN | Prepare the stress-test sample, set run parameters, and interpret results. |
| [EzyFox Server With Unity](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-server-with-unity?lang=vi) · EN | Two Unity client/server models using EzyFox connections. |
| [EzyFox Swift Client SDK](https://youngmonkeys.org/ezyfox-server/guides/ezyfox-swift-client-sdk?lang=vi) · EN | Install the Swift SDK, configure the client and event handlers, and call the app. |
| [Getting Started](https://youngmonkeys.org/ezyfox-server/guides/get-started?lang=vi) · EN | Run the sample server with Docker or natively and verify the environment. |
| [Handle Client Requests](https://youngmonkeys.org/ezyfox-server/guides/handle-client-requests?lang=vi) · EN | Controllers, singleton and prototype handlers, and when to use User or Session. |
| [Handle Exceptions](https://youngmonkeys.org/ezyfox-server/guides/handle-exceptions?lang=vi) · EN | Default exceptions, controller-specific handlers, and shared handlers. |
| [Handle Socket Events](https://youngmonkeys.org/ezyfox-server/guides/handle-socket-events?lang=vi) · EN | Register ServerReadyEvent for plugins or apps and register UserLoginEvent. |
| [How to integrate EzyFox Server WebGL client into unity project](https://youngmonkeys.org/ezyfox-server/guides/how-to-integrate-ezyfox-server-csharp-client-into-?lang=vi) · EN | Integrate the C# client into Unity WebGL using a login scene and SocketManager. |
| [Setup Embedded Server](https://youngmonkeys.org/ezyfox-server/guides/setup-embedded-server?lang=vi) · EN | Configure sockets and WebSockets and build plugin and app entry points. |
| [Use Embedded Server](https://youngmonkeys.org/ezyfox-server/guides/use-embedded-server?lang=vi) · EN | Dependencies, app and plugin entry points, and the embedded startup lifecycle. |

### EzyHTTP

| Article | What it covers |
| --- | --- |
| [EzyHTTP Annotations](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-annotations?lang=vi) · EN | Route mapping, authentication, binding and converters, startup, interceptors, errors, and GraphQL. |
| [EzyHTTP Create a Website](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-create-a-website?lang=vi) · EN | Controllers, models, services, views, templates, and redirects. |
| [EzyHTTP Download File](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-download-file?lang=vi) · EN | ResourceRequestHandler and synchronous or asynchronous downloads. |
| [Implement an EzyHTTP GraphQL Fetcher](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-graphql-fetcher-implementation-guide?lang=vi) · VI | Register fetchers, bind nested arguments, validate inputs, and shape responses. |
| [EzyHTTP Handle Exceptions](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-handle-exceptions?lang=vi) · EN | Compare default exceptions with local and global handlers. |
| [EzyHTTP Handle Requests](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-handle-requests?lang=vi) · EN | Map HTTP methods and separate path, query, and body handling to keep controllers small. |
| [How EzyHTTP GraphQL Works](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-how-graphql-works?lang=vi) · VI | Enable GraphQL, parse requests, dispatch fetchers, and filter results. |
| [EzyHTTP How to Use Tomcat](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-how-to-use-tomcat?lang=vi) · EN | Standalone Tomcat dependencies, configuration, multipart requests, and CORS. |
| [EzyHTTP Request Arguments](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-request-arguments?lang=vi) · EN | Bind path, query, header, cookie, and body values, plus custom arguments and converters. |
| [EzyHTTP Request Interceptor](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-request-interceptor?lang=vi) · EN | preHandle and postHandle lifecycle, priorities, authentication, and rejecting requests. |
| [EzyHTTP Response Types](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-response-types?lang=vi) · EN | DTO, ResponseEntity, View, Redirect, ResponseAsync, and content types. |
| [EzyHTTP Server Properties](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-server-properties?lang=vi) · EN | Options for the server, multipart requests, CORS, static files, templates, async handling, and GraphQL. |
| [EzyHTTP Serves Static Files](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-serves-static-files?lang=vi) · EN | Map public assets and configure filters, async responses, byte ranges, and timeouts. |
| [EzyHTTP Upload file](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-upload-file?lang=vi) · EN | FileUploader, multipart configuration, and synchronous or asynchronous uploads. |
| [Calling HTTP API with HttpClient](https://youngmonkeys.org/ezyhttp/guides/guide-to-calling-http-apis-with-httpclient?lang=vi) · VI | HTTP methods, bodies, status codes, headers, status-specific responses, and uploads. |
| [Calling HTTP API with HttpClientProxy](https://youngmonkeys.org/ezyhttp/guides/guide-to-calling-http-apis-with-httpclientproxy?lang=vi) · VI | The call, request, fire, and execute facade methods and download variants. |
| [Introduce EzyHTTP](https://youngmonkeys.org/ezyhttp/guides/introduce-ezyhttp?lang=vi) · EN | HTTP server and client architecture with standalone application examples. |

### EzyMQ

| Article | What it covers |
| --- | --- |
| [EzyActiveMQ Configuration](https://youngmonkeys.org/ezymq/guides/ezyactivemq-configuration?lang=vi) · EN | ActiveMQ properties, producer and consumer setup, and topics. |
| [EzyKafka Configuration](https://youngmonkeys.org/ezymq/guides/ezykafka-configuration?lang=vi) · EN | Kafka producers and consumers and the meaning of group.id. |
| [EzyMosquitto Configuration](https://youngmonkeys.org/ezymq/guides/ezymosquitto-configuration?lang=vi) · EN | Mosquitto properties, producers and consumers, and topic conventions. |
| [EzyRabbitMQ Configuration](https://youngmonkeys.org/ezymq/guides/ezyrabbitmq-configration?lang=vi) · EN | RabbitMQ properties, producers and consumers, and topics. |
| [Introduce EzyActiveMQ](https://youngmonkeys.org/ezymq/guides/introduce-ezyactivemq?lang=vi) · EN | ActiveMQ adapter structure, payloads, and a sample RPC handler. |
| [Introduce EzyKafka](https://youngmonkeys.org/ezymq/guides/introduce-ezykafka?lang=vi) · EN | Kafka adapter architecture and a sample producer and consumer. |
| [Introduce EzyMosquitto](https://youngmonkeys.org/ezymq/guides/introduce-ezymosquitto?lang=vi) · EN | MQTT/Mosquitto adapter structure, handlers, and an RPC example. |
| [Introduce EzyRabbitMQ](https://youngmonkeys.org/ezymq/guides/introduce-ezyrabbitmq?lang=vi) · EN | Integrate the RabbitMQ adapter with a sample message and handler. |
| [Use EzyKafka For Push Message System](https://youngmonkeys.org/ezymq/guides/use-ezykafka-for-push-message-system?lang=vi) · EN | EzyHTTP publishes to Kafka; a Socket worker polls and pushes messages to the client. |

### EzyPlatform

See the [EzyPlatform guide inventory](../ezyplatform-guide-inventory.md#complete-guide-by-topic) for URLs and summaries of all 76 articles in the Guide tab plus the Ubuntu alias. All 77 EzyPlatform URLs were readable in both locales; the inventory links to the Vietnamese sources rather than listing both variants.

### Game Box

| Article | What it covers |
| --- | --- |
| [Game Box Getting Started](https://youngmonkeys.org/game-box/guides/game-box-getting-started?lang=vi) · EN | Create a project, add the Game Box dependency, and run the example. |
| [Game Box MMO Game](https://youngmonkeys.org/game-box/guides/game-box-mmo-game?lang=vi) · EN | Virtual worlds, MMO rooms, and position synchronization handlers. |
| [Game Box Player Management](https://youngmonkeys.org/game-box/guides/game-box-player-management?lang=vi) · EN | Player, located-player, and MMO-player types and lifecycle management. |
| [Game Box Room Management](https://youngmonkeys.org/game-box/guides/game-box-room-management?lang=vi) · EN | Standard rooms, rooms with coordinates, MMO rooms, and room managers. |

### Properties File

| Article | What it covers |
| --- | --- |
| [Encrypt Configuration Properties](https://youngmonkeys.org/properties-file/guides/encrypt-configuration-properties?lang=vi) · EN | Generate keys and encrypt or decrypt values. Keep the keys separate. |
| [Read Configuration File](https://youngmonkeys.org/properties-file/guides/read-configuration-file?lang=vi) · EN | Read properties and YAML files, file variants, and profiles. |

### Quick RPC

| Article | What it covers |
| --- | --- |
| [Introduce Quick RPC](https://youngmonkeys.org/quickrpc/guides/introduce-quick-rpc?lang=vi) · EN | Set up an RPC server, handler, and client, and send a MessagePack request. |

### Test Utilities

| Article | What it covers |
| --- | --- |
| [Introduce Test Utilities](https://youngmonkeys.org/test-utilities/guides/introduce-test-util?lang=vi) · EN | Test helpers for timing, assertions, randomness, and reflection. |
| [Test Utilities Assertion](https://youngmonkeys.org/test-utilities/guides/test-utilities-assertion?lang=vi) · EN | Compare assertXXX and assertThat for exception types and results. |

## Additional and broken links

- [Add Environment Variables](https://youngmonkeys.org/add-environment-variables/?lang=vi) (EN): Set `JAVA_HOME` through your shell profile or Windows Environment Variables; this does not install a JDK. This is a separate article and is not one of the 162 guides.
- These older URLs are still readable in English and duplicate the guide text listed above:
  - [Create an EzyFox Server Project](https://youngmonkeys.org/create-ezyfox-server-project/?lang=vi).
  - [Encrypt Configuration Properties](https://youngmonkeys.org/encrypt-configuration-properties/?lang=vi).
  - [EzyFox Annotations](https://youngmonkeys.org/ezyfox-annotations/?lang=vi).
  - [Handle HTTP Exceptions](https://youngmonkeys.org/ezyhttp-handle-exceptions/?lang=vi).
  - [Bind HTTP Request Arguments](https://youngmonkeys.org/ezyhttp-request-arguments/?lang=vi).
  - [HTTP Request Interceptors](https://youngmonkeys.org/ezyhttp-request-interceptor/?lang=vi).
  - [Serve Static Files over HTTP](https://youngmonkeys.org/ezyhttp-serves-static-files/?lang=vi).
  - [Handle Socket Commands](https://youngmonkeys.org/handle-client-requests/?lang=vi).
  - [Handle Socket Events](https://youngmonkeys.org/handle-socket-events/?lang=vi).
  - [Introduction to EzyJPA](https://youngmonkeys.org/introduce-ezydata-jpa/?lang=vi).
  - [Read a Configuration File](https://youngmonkeys.org/read-configuration-file/?lang=vi).
  - [Use an Embedded Socket Server](https://youngmonkeys.org/use-embedded-server/?lang=vi).
- The [incorrect `ezyttp` URL](https://youngmonkeys.org/ezyttp/guides/ezyhttp-create-a-website?lang=vi) has no article body in either locale. The [correct URL](https://youngmonkeys.org/ezyhttp/guides/ezyhttp-create-a-website?lang=vi) works.
- These old links returned “Not found” in both locales: `/ezyfox-sever/`, `/project/ezyfox-sever/`, `/guides/ezyfox-annotations/`, `/introduce-to-ezymongo/`; use the [EzyFox Server project page](https://youngmonkeys.org/projects/ezyfox-server?lang=vi), [EzyFox Annotations](https://youngmonkeys.org/ezyfox-library/guides/ezyfox-annotations?lang=vi) and [Introduce EzyMongo](https://youngmonkeys.org/ezydata/guides/introduce-ezymongo?lang=vi).
- Eight `/blog/…` links on the same host return a “Not found” page in both locales: `add-a-plugin-to-your-ezyplatform`, `ezyplatform-cli-commands`, `ezyplatform-plugin-development-quickstart`, `ezyplatform-sdk-commands`, `ezyplatform-setup-development-environment`, `fix-intellij-not-recognizing-path-variable`, `the-structure-of-a-plugin-project`, and `update-a-plugin`. The same slugs work under `/ezyplatform/guides/`; see the linked EzyPlatform inventory. [Hello EzyFox Server](https://youngmonkeys.org/hello-ezyfox-server.html) is a demo page, not an article.
