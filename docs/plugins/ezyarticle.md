# ezyarticle

Bài viết, trang nội dung, taxonomy và xuất bản.

- **Bản Marketplace trên core 1.5.9:** `1.5.6`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Cài đặt:** Có sẵn. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyarticle` | `org.youngmonkeys.ezyarticle` | Không khai báo |
| `web-plugin` — `web/plugins/ezyarticle` | `org.youngmonkeys.ezyarticle` | Không khai báo |
| `socket-plugin` — `socket/plugins/ezyarticle` | `org.youngmonkeys.ezyarticle.socket.plugin` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 162 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /posts` | `PostController` |
| `GET /posts/trash` | `PostController` |
| `GET /api/v1/post-by-slug/{slug}` | `ApiPostController` |
| `GET /api/v1/post-by-slug/{slug}/terms` | `ApiPostTermController` |
| `GET /pages` | `PageController` |
| `GET /pages/trash` | `PageController` |
| `GET /menus` | `MenuController` |
| `POST /api/v1/posts/save-simply` | `ApiPostController` |
| `POST /api/v1/posts/add` | `ApiPostController` |
| `POST /posts/{id}/authenticate` | `ApCommonAuthenticationController` |
| `POST /api/v1/convert-content` | `ApiContentController` |
| `PUT /api/v1/posts/type` | `ApiPostController` |
| `PUT /api/v1/posts/status` | `ApiPostController` |
| `PUT /api/v1/settings` | `ApiEzyArticleSettingController` |
| `PUT /api/v1/posts/publish` | `ApiPostController` |
| `DELETE /api/v1/posts` | `ApiPostController` |
| `DELETE /api/v1/posts/trash` | `ApiPostController` |
| `DELETE /api/v1/terms` | `ApiTermController` |
| `DELETE /api/v1/comments` | `ApiCommentController` |

**web-plugin** — 41 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /posts` | `ApiPostController` |
| `GET /notification-posts` | `ApiNotificationPostController` |
| `GET /pages/{slug}/preview` | `PageManagementController` |
| `GET /` | `HomeController` |
| `GET /blog` | `ApiBlogController` |
| `GET /news` | `ApiNewsController` |
| `GET /terms` | `ApiTermController` |
| `POST /posts/{id}/schedule` | `ApiPostScheduleController` |
| `POST /posts/{id}/authenticate` | `ApCommonAuthenticationController` |
| `POST /api/v1/convert-content` | `ApiContentController` |
| `POST /api/v1/editorjs-json-to-html` | `ApiEditorJsController` |
| `DELETE /posts/{id}/schedule` | `ApiPostScheduleController` |
| `DELETE /posts/{postId}/comments/{commentId}` | `ApiCommentController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `posts: /post-menus`, `list: /posts`, `create: /posts/create`, `trash: /posts/trash`, `post_details: ~/posts/{id}`, `edit_post: ~/posts/{id}/edit` (+20).

- **admin-plugin – Template:** `ezyarticle/comments/edit.html`, `ezyarticle/comments/list.html`, `ezyarticle/comments/scripts.html`, `ezyarticle/fragments/add-user-author-modal.html`, `ezyarticle/fragments/data-mappings-from.html`, `ezyarticle/fragments/data-mappings-to.html`, `ezyarticle/fragments/data-mappings.html` (+46).

- **admin-plugin – Tài nguyên tĩnh:** `ezyarticle/css/right-toolbar-comment.css`, `ezyarticle/css/right-toolbar-tag.css`, `ezyarticle/css/style.css`, `ezyarticle/editorjs/editorjs.js` (+170).

- **admin-plugin – Tài nguyên cấu hình/mẫu:** `ezyarticle/letter-templates/ezyarticle_entity_discussion_mention.properties`, `ezyarticle/notification-templates/ezyarticle_entity_discussion_mention.properties`.

- **web-plugin – Template:** `ezyarticle/comment-preview.html`, `ezyarticle/ezyarticle-template.html`, `ezyarticle/image-modal.html`, `ezyarticle/page-preview.html`, `ezyarticle/personalized-feed.html`, `ezyarticle/post-authentication.html`, `ezyarticle/post-preview.html` (+1).

- **web-plugin – Tài nguyên tĩnh:** `ezyarticle/css/editorjs.css`, `ezyarticle/css/style.css`, `ezyarticle/editorjs/editorjs.js`, `ezyarticle/editorjs/i18n.js` (+156).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (14):** `ezyarticle_comments`, `ezyarticle_menu_items`, `ezyarticle_menus`, `ezyarticle_personalized_contents`, `ezyarticle_personalized_feeds`, `ezyarticle_post_histories`, `ezyarticle_post_medias`, `ezyarticle_post_meta`, `ezyarticle_post_schedules`, `ezyarticle_post_terms`, `ezyarticle_posts`, `ezyarticle_posts_i18n`, `ezyarticle_term_medias`, `ezyarticle_terms`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (14):** `Comment`, `Menu`, `MenuItem`, `PersonalizedContent`, `PersonalizedFeed`, `Post`, `PostHistory`, `PostI18n`, `PostMedia`, `PostMeta`, `PostSchedule`, `PostTerm`, `Term`, `TermMedia`.
- **SQL admin-plugin (43 tệp):** `resources/scripts/item_media.sql`, `resources/scripts/personalized_content.sql`, `resources/scripts/post_schedule.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_comment_add_content_type.sql`, `resources/scripts/alter_comment_content.sql`, `resources/scripts/alter_display_order_type.sql` (+36).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyarticle-admin-plugin-1.5.6.jar`, `ezyarticle-sdk-1.5.6.jar`; 685 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyarticle.sdk.pagination`, `org.youngmonkeys.ezyarticle.sdk.model`, `org.youngmonkeys.ezyarticle.admin.service` (+46).
- **JAR thư viện khác:** `jsoup-1.18.3.jar`.
- **Controller/service/repository (mẫu):** `AdminApiEzyArticleDataMappingController`, `AdminApiEzyArticleDataMetaController`, `AdminCommentControllerService`, `AdminDataMetaControllerService`, `AbstractPostService`, `AdminCheckPostExistsByIdEventSchemaFetcher`, `AdminCommentControllerService`, `AdminCommentRepository`, `AdminCommentService`.
- **Class cấu hình/quyền (mẫu):** `AdminEzyArticleMenuPostConfig`, `AdminEzyArticleMessageTemplateConfig`, `AdminEzyArticlePageFragmentConfig`, `AdminEzyArticleSettingPostConfig`, `AdminEzyArticleViewMetadataConfig`, `EzyArticlePageFragmentConfig`.
- **Khóa cấu hình/mẫu từ resource (không trích giá trị):** `content`, `title`.
- **Điểm mở rộng tiềm năng theo tên class:** `AdminAbstractPostPersonalizedContentCandidateProvider`, `AdminCheckPostExistsByIdEventHandler`, `AdminCommentEditorManager`, `AdminCommentFilterFactory`, `AdminCommentStatusManager`, `AdminCommentTypeManager`, `AdminEditablePostMetadataManager`, `AdminEditorManager`, `AdminEditorPickPostPersonalizedContentCandidateProvider` (+48).

### web-plugin

- **JAR kiểm tra:** `ezyarticle-sdk-1.5.6.jar`, `ezyarticle-web-plugin-1.5.6.jar`; 605 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyarticle.sdk.pagination`, `org.youngmonkeys.ezyarticle.web.event`, `org.youngmonkeys.ezyarticle.sdk.model` (+41).
- **JAR thư viện khác:** `jsoup-1.18.3.jar`.
- **Controller/service/repository (mẫu):** `AnswerControllerService`, `ApCommonAuthenticationController`, `ApiAuthenticationController`, `ApiBlogController`, `AbstractPostService`, `AnswerControllerService`, `AnswerService`, `AnswerValidator`, `CheckPostExistsByIdEventSchemaFetcher`.
- **Class cấu hình/quyền (mẫu):** `EzyArticlePageFragmentConfig`, `WebEzyArticlePageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `CheckPostExistsByIdEventHandler`, `CommentFilterFactory`, `EzyArticleExceptionHandler`, `EzyArticleFunctionEventHandler`, `EzyBlockTagReplaceAttributeProcessor`, `EzyBlockTagUtextAttributeProcessor`, `EzyViewDataFetcherFunctionsFactory`, `GetPageFragmentMapEventHandler`, `GetPostByIdEventHandler` (+48).

### socket-plugin

- **JAR kiểm tra:** `ezyarticle-sdk-1.5.6.jar`, `ezyarticle-socket-plugin-1.5.6.jar`; 360 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyarticle.sdk.pagination`, `org.youngmonkeys.ezyarticle.sdk.model`, `org.youngmonkeys.ezyarticle.sdk.service` (+23).
- **JAR thư viện khác:** `jsoup-1.18.3.jar`.
- **Controller/service/repository (mẫu):** `AnswerControllerService`, `ApCommonAuthenticationController`, `ExtractUrlControllerService`, `MenuControllerService`, `AbstractPostService`, `AnswerControllerService`, `AnswerService`, `AnswerValidator`, `CheckPostExistsByIdEventSchemaFetcher`.
- **Class cấu hình/quyền (mẫu):** `EzyArticlePageFragmentConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `CheckPostExistsByIdEventHandler`, `CommentFilterFactory`, `EzyArticleExceptionHandler`, `EzyArticleFunctionEventHandler`, `EzyBlockTagReplaceAttributeProcessor`, `EzyBlockTagUtextAttributeProcessor`, `EzyViewDataFetcherFunctionsFactory`, `GetPageFragmentMapEventHandler`, `GetPostByIdEventHandler` (+11).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezyarticle.socket.plugin.PluginEntryLoader`.
- **Class controller/handler/event/request (mẫu):** `EzyArticleExceptionHandler`, `ApCommonAuthenticationController`, `MenuModelDecorator`, `PageFragmentModelDecorator`, `AnswerControllerService`, `ExtractUrlControllerService`, `MenuControllerService`, `PageFragmentControllerService`, `QuestionControllerService`, `CheckPostExistsByIdEventHandler` (+33).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin tạo và đọc bài `PUBLISHED`; Freestyle hiển thị đúng nội dung bài qua HTTP 200.

Xem bằng chứng nạp module và cổng TCP trong [kiểm thử Socket](test-report.md#gói-cài-được-và-kiểm-thử-http). Không kiểm chứng trao đổi Socket bằng client.

## Áp dụng cho plugin quản lý công việc

Phù hợp cho wiki, tài liệu và nội dung hướng dẫn. Không dùng bảng post làm issue: workflow, assignee, ACL theo workspace, thứ tự trong cột và audit trail là miền khác. Kiểm tra route bằng nội dung bài đã biết, không chỉ status.

[Về chỉ mục plugin](README.md)
