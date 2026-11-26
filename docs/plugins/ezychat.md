# ezychat

Channel, profile, hội thoại và Socket app/plugin.

- **Bản Marketplace trên core 1.5.9:** `0.3.6`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`, `socket-app`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezychat` | `org.youngmonkeys.ezychat` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezychat` | `org.youngmonkeys.ezychat` | [ezyarticle](ezyarticle.md) |
| `socket-plugin` — `socket/plugins/ezychat` | `org.youngmonkeys.ezychat` | Không khai báo |
| `socket-app` — `socket/apps/ezychat` | `org.youngmonkeys.ezychat` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 80 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /channels` | `AdminChannelController` |
| `GET /api/v1/channels` | `AdminApiChatChannelController` |
| `GET /api/v1/channels/{id}/messages` | `AdminApiChatChannelController` |
| `GET /api/v1/channels/{id}/messages/pinned` | `AdminApiChatMessagePinController` |
| `GET /chat-profiles` | `AdminChatProfileController` |
| `GET /chat-profiles/add` | `AdminChatProfileController` |
| `GET /chat` | `AdminChatController` |
| `POST /api/v1/channels` | `AdminApiChatChannelController` |
| `POST /api/v1/channels/{id}/leave` | `AdminApiChatChannelController` |
| `POST /api/v1/channels/{id}/messages/{messageId}/reactions/add` | `AdminApiChatMessageReactionController` |
| `POST /api/v1/chat-profiles/add` | `AdminApiChatProfilesController` |
| `PUT /api/v1/channels/{id}/mute` | `AdminApiUserChannelSettingController` |
| `PUT /api/v1/channels/{id}/read` | `AdminApiChatChannelController` |
| `PUT /api/v1/channels/{id}/messages/{messageId}` | `AdminApiChatMessageEditController` |
| `PUT /api/v1/channels/{id}/messages/{messageId}/pin` | `AdminApiChatMessagePinController` |
| `DELETE /api/v1/channels/{id}` | `AdminApiChatChannelController` |
| `DELETE /api/v1/channels/{id}/notes/{noteId}` | `AdminApiChannelNoteController` |
| `DELETE /api/v1/channels/{id}/messages/{messageId}` | `AdminApiChatMessageRemovalController` |
| `DELETE /api/v1/channels/{id}/messages/{messageId}/for-me` | `AdminApiChatMessageRemovalController` |

**web-plugin** — 29 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /ezychat/api/v1/channels` | `WebApiUserChannelController` |
| `GET /ezychat/api/v1/channels/last-message` | `WebApiUserChannelController` |
| `GET /ezychat/api/v1/channels/{id}/messages` | `WebApiUserChannelController` |
| `GET /ezychat/api/v1/channels/{id}/messages/pinned` | `WebApiChatMessagePinController` |
| `GET /ezychat/api/v1/chat-profiles/joined` | `WebApiUserChatProfileController` |
| `GET /ezychat/widget` | `WebChatProfileController` |
| `GET /ezychat/support` | `WebChatProfileController` |
| `POST /ezychat/api/v1/channels/find-by-password` | `WebApiUserChannelSettingController` |
| `POST /ezychat/api/v1/support/channels/add` | `WebApiUserChannelController` |
| `POST /ezychat/api/v1/webhooks/{id}/{token}/messages` | `WebApiChannelWebhookController` |
| `POST /ezychat/api/v1/support/channels/add-new` | `WebApiUserChannelController` |
| `PUT /ezychat/api/v1/channels/{id}/lock` | `WebApiUserChannelSettingController` |
| `PUT /ezychat/api/v1/channels/{id}/spam` | `WebApiUserChannelSettingController` |
| `PUT /ezychat/api/v1/channels/{id}/messages/{messageId}/pin` | `WebApiChatMessagePinController` |
| `PUT /ezychat/api/v1/channels/{id}/messages/{messageId}/unpin` | `WebApiChatMessagePinController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezychat: /`, `channels: /channels`, `supporter: /supporters`, `chat: /chat`, `chat_profiles: /chat-profiles`, `chat_profiles_add: ~/chat-profiles/add` (+5).

- **admin-plugin – Template:** `ezychat/channel-webhook/list.html`, `ezychat/channel/list.html`, `ezychat/chat-profile/add-member.html`, `ezychat/chat-profile/add.html`, `ezychat/chat-profile/allowed-origins.html`, `ezychat/chat-profile/details.html`, `ezychat/chat-profile/edit-member.html` (+9).

- **admin-plugin – Tài nguyên tĩnh:** `ezychat/css/style.css`, `ezychat/js/list.min.css`, `ezychat/js/list.min.js`, `ezychat/js/main.js` (+2).

- **web-plugin – Template:** `ezychat/support.html`, `ezychat/widget.html`.

- **web-plugin – Tài nguyên tĩnh:** `ezychat/css/style.css`, `ezychat/css/support.css`, `ezychat/js/bs-custom-file-input.min.js`, `ezychat/js/embed.js` (+9).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (26):** `ezychat_channel_members`, `ezychat_channel_webhooks`, `ezychat_channels`, `ezychat_chat_message_resources`, `ezychat_chat_poll_options`, `ezychat_chat_poll_votes`, `ezychat_chat_polls`, `ezychat_chat_profile_members`, `ezychat_chat_profiles`, `ezychat_chat_reminders`, `ezychat_e2ee_channel_groups`, `ezychat_e2ee_commits`, `ezychat_e2ee_devices`, `ezychat_e2ee_epoch_key_backups`, `ezychat_e2ee_files`, `ezychat_e2ee_identities`, `ezychat_e2ee_key_backups`, `ezychat_e2ee_key_packages`, `ezychat_e2ee_welcomes`, `ezychat_message_actions`, `ezychat_message_reactions`, `ezychat_message_statuses`, `ezychat_messages`, `ezychat_online_daily_statistics`, `ezychat_online_histories`, `ezychat_user_channel_settings`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (26):** `Channel`, `ChannelMember`, `ChannelWebhook`, `ChatMessageResource`, `ChatOnlineDailyStatistic`, `ChatOnlineHistory`, `ChatPoll`, `ChatPollOption`, `ChatPollVote`, `ChatProfile`, `ChatProfileMember`, `ChatReminder`, `E2eeChannelGroup`, `E2eeCommit`, `E2eeDevice`, `E2eeEpochKeyBackup`, `E2eeFile`, `E2eeIdentity` (+8).
- **SQL admin-plugin (25 tệp):** `resources/scripts/channel-webhooks.sql`, `resources/scripts/chat-message-action.sql`, `resources/scripts/chat-message-reaction.sql`, `resources/scripts/chat-message-resources.sql`, `resources/scripts/chat-poll.sql`, `resources/scripts/chat-profile-member.sql`, `resources/scripts/chat-profiles.sql` (+18).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezychat-admin-plugin-0.3.6.jar`, `ezychat-http-sdk-0.3.6.jar`, `ezychat-sdk-0.3.6.jar`; 534 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+35).
- **JAR thư viện khác:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controller/service/repository (mẫu):** `AdminApiChannelNoteController`, `AdminApiChatChannelController`, `AdminApiChatChannelUserController`, `AdminApiChatMessageEditController`, `AdminAdminChanelValidator`, `AdminAdminChannelMemberInformationFetcher`, `AdminChannelControllerService`, `AdminChannelMemberInformationFetcher`, `AdminChannelMemberRepository`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyChatBotConfig`, `AdminEzyChatPostConfig`, `AdminEzyChatViewMetadataConfig`, `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `UserChannelSetting`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminChannelMemberInformationFetcherManager`, `AdminChatBotServiceManager`, `AdminCheckAdminSocketConnectedEventHandler`, `AdminEzyChatConnectorManager`, `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler` (+1).

### web-plugin

- **JAR kiểm tra:** `ezychat-http-sdk-0.3.6.jar`, `ezychat-sdk-0.3.6.jar`, `ezychat-web-plugin-0.3.6.jar`; 474 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+31).
- **JAR thư viện khác:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controller/service/repository (mẫu):** `ChannelControllerService`, `E2eeFileControllerService`, `WebApiChannelWebhookController`, `WebApiChatChannelUserController`, `AdminChannelMemberInformationFetcher`, `ChannelControllerService`, `ChannelMemberInformationFetcher`, `ChannelMemberRepository`, `ChannelMemberService`.
- **Class cấu hình/quyền (mẫu):** `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `UserChannelSetting`.
- **Điểm mở rộng tiềm năng theo tên class:** `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler`, `EzyChatConnectorManager`, `WebChannelMemberInformationFetcherManager`, `WebChatBotServiceManager`, `WebEzyChatConnectorManager`.

### socket-plugin

- **JAR kiểm tra:** `ezychat-sdk-0.3.6.jar`, `ezychat-socket-plugin-0.3.6.jar`; 345 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+15).
- **Controller/service/repository (mẫu):** `AdminChannelMemberInformationFetcher`, `ChannelMemberInformationFetcher`, `ChannelMemberRepository`, `ChannelMemberService`, `ChannelRepository`.
- **Class cấu hình/quyền (mẫu):** `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `UserChannelSetting`.
- **Điểm mở rộng tiềm năng theo tên class:** `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler`, `EzyChatConnectorManager`, `PluginEntryLoader`.
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezychat.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `ChatBotStreamHandler`, `ChatBotTypingHandler`, `SendMessageRequest`.

### socket-app

- **JAR kiểm tra:** `ezychat-sdk-0.3.6.jar`, `ezychat-socket-app-0.3.6.jar`; 461 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+26).
- **Controller/service/repository (mẫu):** `SocketAdminAccessedAppController`, `SocketAdminPresenceController`, `SocketAdminRemovedController`, `SocketChannelMemberController`, `AdminChannelMemberInformationFetcher`, `ChannelMemberInformationFetcher`, `ChannelMemberRepository`, `ChannelMemberService`, `ChannelRepository`.
- **Class cấu hình/quyền (mẫu):** `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `SocketChatOnlineHistoryConfig`, `UserChannelSetting`.
- **Điểm mở rộng tiềm năng theo tên class:** `AppEntryLoader`, `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler`, `EzyChatConnectorManager`, `SocketAdminPresenceManager`, `SocketChatBotServiceManager` (+5).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezychat.socket.app.AppEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `ChatBotStreamHandler`, `ChatBotTypingHandler`, `SendMessageRequest`, `SocketAdminAccessedAppController`, `SocketAdminPresenceController`, `SocketAdminRemovedController`, `SocketChannelMemberController`, `SocketChatBotController`, `SocketChatPollController`, `SocketChatReminderController` (+43).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezychat/channels` → 200, Web API channels chưa đăng nhập → 401. `/ezychat/widget` không có embed key trả trang lỗi 200; log có `NullPointerException` khi đọc chat profile.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Áp dụng cho plugin quản lý công việc

Phân vai quan sát được: persistence có `ezychat_channels` và `ezychat_channel_members`; Web đọc channel/message; app Socket ở zone `chat`. Log khởi động app ghi các hook `USER_ACCESSED_APP`, `USER_REMOVED` và `SESSION_REMOVED`. Với task realtime, chỉ dùng các hook phiên để quản lý kết nối; lấy quyền nhận sự kiện từ membership hiện hành và gửi lại danh sách issue qua HTTP khi reconnect.

Tham khảo tách dữ liệu chat, API HTTP và lifecycle Socket. Issue nên có sự kiện riêng và chỉ phát sau commit; kiểm tra quyền subscription theo workspace/issue, không dùng việc biết tên channel làm quyền truy cập.

[Về chỉ mục plugin](README.md)
