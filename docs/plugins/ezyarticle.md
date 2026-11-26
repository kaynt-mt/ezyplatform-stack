# ezyarticle

Articles, content pages, taxonomy, and publishing.

- **Marketplace version on core 1.5.9:** `1.5.6`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `socket-plugin`.
- **Installation:** View the environment and the general limits in [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyarticle` | `org.youngmonkeys.ezyarticle` | Not declared |
| `web-plugin` — `web/plugins/ezyarticle` | `org.youngmonkeys.ezyarticle` | Not declared |
| `socket-plugin` — `socket/plugins/ezyarticle` | `org.youngmonkeys.ezyarticle.socket.plugin` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 162 method/URI combinations identified; representative sample:

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

**web-plugin** — 41 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `posts: /post-menus`, `list: /posts`, `create: /posts/create`, `trash: /posts/trash`, `post_details: ~/posts/{id}`, `edit_post: ~/posts/{id}/edit` (+20).

- **admin-plugin – Template:** `ezyarticle/comments/edit.html`, `ezyarticle/comments/list.html`, `ezyarticle/comments/scripts.html`, `ezyarticle/fragments/add-user-author-modal.html`, `ezyarticle/fragments/data-mappings-from.html`, `ezyarticle/fragments/data-mappings-to.html`, `ezyarticle/fragments/data-mappings.html` (+46).

- **admin-plugin – Static resources:** `ezyarticle/css/right-toolbar-comment.css`, `ezyarticle/css/right-toolbar-tag.css`, `ezyarticle/css/style.css`, `ezyarticle/editorjs/editorjs.js` (+170).

- **admin-plugin – Configuration and template resources:** `ezyarticle/letter-templates/ezyarticle_entity_discussion_mention.properties`, `ezyarticle/notification-templates/ezyarticle_entity_discussion_mention.properties`.

- **web-plugin – Template:** `ezyarticle/comment-preview.html`, `ezyarticle/ezyarticle-template.html`, `ezyarticle/image-modal.html`, `ezyarticle/page-preview.html`, `ezyarticle/personalized-feed.html`, `ezyarticle/post-authentication.html`, `ezyarticle/post-preview.html` (+1).

- **web-plugin – Static resources:** `ezyarticle/css/editorjs.css`, `ezyarticle/css/style.css`, `ezyarticle/editorjs/editorjs.js`, `ezyarticle/editorjs/i18n.js` (+156).

## Data and migrations

- **Table in the DDL packaging (14):** `ezyarticle_comments`, `ezyarticle_menu_items`, `ezyarticle_menus`, `ezyarticle_personalized_contents`, `ezyarticle_personalized_feeds`, `ezyarticle_post_histories`, `ezyarticle_post_medias`, `ezyarticle_post_meta`, `ezyarticle_post_schedules`, `ezyarticle_post_terms`, `ezyarticle_posts`, `ezyarticle_posts_i18n`, `ezyarticle_term_medias`, `ezyarticle_terms`.
- **Class with JPA Entity/MappedSuperclass):** `Comment`, `Menu`, `MenuItem`, `PersonalizedContent`, `PersonalizedFeed`, `Post`, `PostHistory`, `PostI18n`, `PostMedia`, `PostMeta`, `PostSchedule`, `PostTerm`, `Term`, `TermMedia`.
- **SQL admin-plugin (43 files):** `resources/scripts/item_media.sql`, `resources/scripts/personalized_content.sql`, `resources/scripts/post_schedule.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_comment_add_content_type.sql`, `resources/scripts/alter_comment_content.sql`, `resources/scripts/alter_display_order_type.sql` (+36).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyarticle-admin-plugin-1.5.6.jar`, `ezyarticle-sdk-1.5.6.jar`; 685 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyarticle.sdk.pagination`, `org.youngmonkeys.ezyarticle.sdk.model`, `org.youngmonkeys.ezyarticle.admin.service` (+46).
- **Other library JARs:** `jsoup-1.18.3.jar`.
- **Controllers, services, and repositories (sample):** `AdminApiEzyArticleDataMappingController`, `AdminApiEzyArticleDataMetaController`, `AdminCommentControllerService`, `AdminDataMetaControllerService`, `AbstractPostService`, `AdminCheckPostExistsByIdEventSchemaFetcher`, `AdminCommentControllerService`, `AdminCommentRepository`, `AdminCommentService`.
- **Configuration and permission classes (sample):** `AdminEzyArticleMenuPostConfig`, `AdminEzyArticleMessageTemplateConfig`, `AdminEzyArticlePageFragmentConfig`, `AdminEzyArticleSettingPostConfig`, `AdminEzyArticleViewMetadataConfig`, `EzyArticlePageFragmentConfig`.
- **Configuration and template keys from resources (values omitted):** `content`, `title`.
- **Potential extension points based on class names:** `AdminAbstractPostPersonalizedContentCandidateProvider`, `AdminCheckPostExistsByIdEventHandler`, `AdminCommentEditorManager`, `AdminCommentFilterFactory`, `AdminCommentStatusManager`, `AdminCommentTypeManager`, `AdminEditablePostMetadataManager`, `AdminEditorManager`, `AdminEditorPickPostPersonalizedContentCandidateProvider` (+48).

### web-plugin

- **JARs inspected:** `ezyarticle-sdk-1.5.6.jar`, `ezyarticle-web-plugin-1.5.6.jar`; 605 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyarticle.sdk.pagination`, `org.youngmonkeys.ezyarticle.web.event`, `org.youngmonkeys.ezyarticle.sdk.model` (+41).
- **Other library JARs:** `jsoup-1.18.3.jar`.
- **Controllers, services, and repositories (sample):** `AnswerControllerService`, `ApCommonAuthenticationController`, `ApiAuthenticationController`, `ApiBlogController`, `AbstractPostService`, `AnswerControllerService`, `AnswerService`, `AnswerValidator`, `CheckPostExistsByIdEventSchemaFetcher`.
- **Configuration and permission classes (sample):** `EzyArticlePageFragmentConfig`, `WebEzyArticlePageFragmentConfig`.
- **Potential extension points based on class names:** `CheckPostExistsByIdEventHandler`, `CommentFilterFactory`, `EzyArticleExceptionHandler`, `EzyArticleFunctionEventHandler`, `EzyBlockTagReplaceAttributeProcessor`, `EzyBlockTagUtextAttributeProcessor`, `EzyViewDataFetcherFunctionsFactory`, `GetPageFragmentMapEventHandler`, `GetPostByIdEventHandler` (+48).

### socket-plugin

- **JARs inspected:** `ezyarticle-sdk-1.5.6.jar`, `ezyarticle-socket-plugin-1.5.6.jar`; 360 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyarticle.sdk.pagination`, `org.youngmonkeys.ezyarticle.sdk.model`, `org.youngmonkeys.ezyarticle.sdk.service` (+23).
- **Other library JARs:** `jsoup-1.18.3.jar`.
- **Controllers, services, and repositories (sample):** `AnswerControllerService`, `ApCommonAuthenticationController`, `ExtractUrlControllerService`, `MenuControllerService`, `AbstractPostService`, `AnswerControllerService`, `AnswerService`, `AnswerValidator`, `CheckPostExistsByIdEventSchemaFetcher`.
- **Configuration and permission classes (sample):** `EzyArticlePageFragmentConfig`.
- **Potential extension points based on class names:** `CheckPostExistsByIdEventHandler`, `CommentFilterFactory`, `EzyArticleExceptionHandler`, `EzyArticleFunctionEventHandler`, `EzyBlockTagReplaceAttributeProcessor`, `EzyBlockTagUtextAttributeProcessor`, `EzyViewDataFetcherFunctionsFactory`, `GetPageFragmentMapEventHandler`, `GetPostByIdEventHandler` (+11).
- **Zone / entry loader:** `chat` / `org.youngmonkeys.ezyarticle.socket.plugin.PluginEntryLoader`.
- **Controller, handler, event, and request classes (sample):** `EzyArticleExceptionHandler`, `ApCommonAuthenticationController`, `MenuModelDecorator`, `PageFragmentModelDecorator`, `AnswerControllerService`, `ExtractUrlControllerService`, `MenuControllerService`, `PageFragmentControllerService`, `QuestionControllerService`, `CheckPostExistsByIdEventHandler` (+33).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin created and read a `PUBLISHED` article. Freestyle returned HTTP 200 and displayed the expected article content.

See module-loading and TCP port evidence in the [Socket checks](test-report.md#installable-packages-and-http-tests). Socket communication was not verified with a client.

## Integration notes

Consider this module for content pages and documentation. Use a known fixture to check routes and permissions for reading, previews, and media. Do not use CMS articles in place of separate business entities.

[Back to the plugin index](README.md)
