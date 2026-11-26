# ezychat

Channels, profiles, conversations, and a Socket app and plugin.

- **Marketplace version on core 1.5.9:** `0.3.6`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`, `socket-app`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezychat` | `org.youngmonkeys.ezychat` | [ezyarticle](ezyarticle.md) |
| `web-plugin` — `web/plugins/ezychat` | `org.youngmonkeys.ezychat` | [ezyarticle](ezyarticle.md) |
| `socket-plugin` — `socket/plugins/ezychat` | `org.youngmonkeys.ezychat` | Not declared |
| `socket-app` — `socket/apps/ezychat` | `org.youngmonkeys.ezychat` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 80 method/URI combinations identified; representative sample:

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

**web-plugin** — 29 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezychat: /`, `channels: /channels`, `supporter: /supporters`, `chat: /chat`, `chat_profiles: /chat-profiles`, `chat_profiles_add: ~/chat-profiles/add` (+5).

- **admin-plugin – Template:** `ezychat/channel-webhook/list.html`, `ezychat/channel/list.html`, `ezychat/chat-profile/add-member.html`, `ezychat/chat-profile/add.html`, `ezychat/chat-profile/allowed-origins.html`, `ezychat/chat-profile/details.html`, `ezychat/chat-profile/edit-member.html` (+9).

- **admin-plugin – Static resources:** `ezychat/css/style.css`, `ezychat/js/list.min.css`, `ezychat/js/list.min.js`, `ezychat/js/main.js` (+2).

- **web-plugin – Template:** `ezychat/support.html`, `ezychat/widget.html`.

- **web-plugin – Static resources:** `ezychat/css/style.css`, `ezychat/css/support.css`, `ezychat/js/bs-custom-file-input.min.js`, `ezychat/js/embed.js` (+9).

## Data and migrations

- **Table in the DDL packaging (26):** `ezychat_channel_members`, `ezychat_channel_webhooks`, `ezychat_channels`, `ezychat_chat_message_resources`, `ezychat_chat_poll_options`, `ezychat_chat_poll_votes`, `ezychat_chat_polls`, `ezychat_chat_profile_members`, `ezychat_chat_profiles`, `ezychat_chat_reminders`, `ezychat_e2ee_channel_groups`, `ezychat_e2ee_commits`, `ezychat_e2ee_devices`, `ezychat_e2ee_epoch_key_backups`, `ezychat_e2ee_files`, `ezychat_e2ee_identities`, `ezychat_e2ee_key_backups`, `ezychat_e2ee_key_packages`, `ezychat_e2ee_welcomes`, `ezychat_message_actions`, `ezychat_message_reactions`, `ezychat_message_statuses`, `ezychat_messages`, `ezychat_online_daily_statistics`, `ezychat_online_histories`, `ezychat_user_channel_settings`.
- **Class with JPA Entity/MappedSuperclass):** `Channel`, `ChannelMember`, `ChannelWebhook`, `ChatMessageResource`, `ChatOnlineDailyStatistic`, `ChatOnlineHistory`, `ChatPoll`, `ChatPollOption`, `ChatPollVote`, `ChatProfile`, `ChatProfileMember`, `ChatReminder`, `E2eeChannelGroup`, `E2eeCommit`, `E2eeDevice`, `E2eeEpochKeyBackup`, `E2eeFile`, `E2eeIdentity` (+8).
- **SQL admin-plugin (25 files):** `resources/scripts/channel-webhooks.sql`, `resources/scripts/chat-message-action.sql`, `resources/scripts/chat-message-reaction.sql`, `resources/scripts/chat-message-resources.sql`, `resources/scripts/chat-poll.sql`, `resources/scripts/chat-profile-member.sql`, `resources/scripts/chat-profiles.sql` (+18).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezychat-admin-plugin-0.3.6.jar`, `ezychat-http-sdk-0.3.6.jar`, `ezychat-sdk-0.3.6.jar`; 534 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+35).
- **Other library JARs:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiChannelNoteController`, `AdminApiChatChannelController`, `AdminApiChatChannelUserController`, `AdminApiChatMessageEditController`, `AdminAdminChanelValidator`, `AdminAdminChannelMemberInformationFetcher`, `AdminChannelControllerService`, `AdminChannelMemberInformationFetcher`, `AdminChannelMemberRepository`.
- **Configuration and permission classes (sample):** `AdminEzyChatBotConfig`, `AdminEzyChatPostConfig`, `AdminEzyChatViewMetadataConfig`, `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `UserChannelSetting`.
- **Potential extension points based on class names:** `AdminChannelMemberInformationFetcherManager`, `AdminChatBotServiceManager`, `AdminCheckAdminSocketConnectedEventHandler`, `AdminEzyChatConnectorManager`, `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler` (+1).

### web-plugin

- **JARs inspected:** `ezychat-http-sdk-0.3.6.jar`, `ezychat-sdk-0.3.6.jar`, `ezychat-web-plugin-0.3.6.jar`; 474 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+31).
- **Other library JARs:** `ezyfox-server-java-client-1.3.1.jar`.
- **Controllers, services, and repositories (sample):** `ChannelControllerService`, `E2eeFileControllerService`, `WebApiChannelWebhookController`, `WebApiChatChannelUserController`, `AdminChannelMemberInformationFetcher`, `ChannelControllerService`, `ChannelMemberInformationFetcher`, `ChannelMemberRepository`, `ChannelMemberService`.
- **Configuration and permission classes (sample):** `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `UserChannelSetting`.
- **Potential extension points based on class names:** `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler`, `EzyChatConnectorManager`, `WebChannelMemberInformationFetcherManager`, `WebChatBotServiceManager`, `WebEzyChatConnectorManager`.

### socket-plugin

- **JARs inspected:** `ezychat-sdk-0.3.6.jar`, `ezychat-socket-plugin-0.3.6.jar`; 345 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+15).
- **Controllers, services, and repositories (sample):** `AdminChannelMemberInformationFetcher`, `ChannelMemberInformationFetcher`, `ChannelMemberRepository`, `ChannelMemberService`, `ChannelRepository`.
- **Configuration and permission classes (sample):** `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `UserChannelSetting`.
- **Potential extension points based on class names:** `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler`, `EzyChatConnectorManager`, `PluginEntryLoader`.
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezychat.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `ChatBotStreamHandler`, `ChatBotTypingHandler`, `SendMessageRequest`.

### socket-app

- **JARs inspected:** `ezychat-sdk-0.3.6.jar`, `ezychat-socket-app-0.3.6.jar`; 461 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezychat.sdk.entity`, `org.youngmonkeys.ezychat.sdk.pagination`, `org.youngmonkeys.ezychat.sdk.model` (+26).
- **Controllers, services, and repositories (sample):** `SocketAdminAccessedAppController`, `SocketAdminPresenceController`, `SocketAdminRemovedController`, `SocketChannelMemberController`, `AdminChannelMemberInformationFetcher`, `ChannelMemberInformationFetcher`, `ChannelMemberRepository`, `ChannelMemberService`, `ChannelRepository`.
- **Configuration and permission classes (sample):** `ChatPollAddOptionPermission`, `ChatPollOption`, `ChatReminderPermission`, `SocketChatOnlineHistoryConfig`, `UserChannelSetting`.
- **Potential extension points based on class names:** `AppEntryLoader`, `ChannelMemberInformationFetcherManager`, `ChatBotChatStreamManager`, `ChatBotServiceManager`, `ChatBotStreamHandler`, `ChatBotTypingHandler`, `EzyChatConnectorManager`, `SocketAdminPresenceManager`, `SocketChatBotServiceManager` (+5).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezychat.socket.app.AppEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `ChatBotStreamHandler`, `ChatBotTypingHandler`, `SendMessageRequest`, `SocketAdminAccessedAppController`, `SocketAdminPresenceController`, `SocketAdminRemovedController`, `SocketChannelMemberController`, `SocketChatBotController`, `SocketChatPollController`, `SocketChatReminderController` (+43).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezychat/channels` returned 200; the Web channels API returned 401 without a login. Without an embed key, `/ezychat/widget` returned an error page with status 200, and logs showed a `NullPointerException` while reading the chat profile.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Persistence uses `ezychat_channels` and `ezychat_channel_members`. Web reads channels and messages; the Socket app belongs to the `chat` zone. Log entries for `USER_ACCESSED_APP`, `USER_REMOVED`, and `SESSION_REMOVED` show registration, not that subscription authorization or push delivery works.

[Back to the plugin index](README.md)
