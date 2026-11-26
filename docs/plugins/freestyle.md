# freestyle

General-purpose Web theme and interface settings.

- **Marketplace version on core 1.5.9:** `0.2.9`.
- **Verified modules:** `admin-plugin`, `theme`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/freestyle` | `org.youngmonkeys.freestyle` | [ezyarticle](ezyarticle.md) |
| `theme` — `web/themes/freestyle` | `org.youngmonkeys.freestyle` | [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 4 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminFreestyleSettingController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/pages/{pageId}/settings` | `AdminApiFreestylePageSettingController` |
| `PUT /api/v1/posts/{postId}/settings` | `AdminApiFreestylePostSettingController` |

**theme** — 5 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `FreestyleHomeController` |
| `GET /freestyle/api/v1/shorted-posts` | `FreestyleNewApiPostController` |
| `GET /freestyle/api/v1/shorted-posts-by-ids` | `FreestyleNewApiPostController` |
| `GET /freestyle/api/v1/posts/{slug}/children` | `FreestyleNewApiPostController` |
| `GET /freestyle/api/v1/users/{uuid}/shorted-posts` | `FreestyleNewApiPostController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `freestyle: /`, `settings: /settings`.

- **admin-plugin – Template:** `freestyle/settings/index.html`.

- **admin-plugin – Static resources:** `freestyle/js/post-settings.js`.

- **theme – Template:** `account/register-success.html`, `account/reset-password.html`, `fragments/comments.html`, `fragments/footer.html`, `fragments/header.html`, `fragments/post-menu.html`, `fragments/posts.html` (+8).

- **theme - Resources:** `css/ezyarticle.css`, `css/styles.css`, `css/styles.rtl.css`, `js/main.js`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `freestyle-admin-plugin-0.2.9.jar`, `freestyle-sdk-0.2.9.jar`; 20 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.freestyle.admin.controller.api`, `org.youngmonkeys.freestyle.constant`, `org.youngmonkeys.freestyle.admin.controller.view` (+9).
- **Controllers, services, and repositories (sample):** `AdminApiFreestylePageSettingController`, `AdminApiFreestylePostSettingController`, `AdminApiSettingController`, `AdminFreestylePostControllerService`, `AdminFreestylePostControllerService`, `AdminFreestylePostService`, `AdminFreestyleSettingService`, `FreestylePostService`, `FreestyleSettingService`.
- **Configuration and permission classes (sample):** `AdminPageFragmentConfig`, `PageFragmentConfig`.

### theme

- **JARs inspected:** `freestyle-sdk-0.2.9.jar`, `freestyle-theme-0.2.9.jar`; 49 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.freestyle.theme.controller.view`, `org.youngmonkeys.freestyle.theme.event`, `org.youngmonkeys.freestyle.theme.service` (+16).
- **Controllers, services, and repositories (sample):** `FreestyleApiCommentController`, `FreestyleApiPostController`, `FreestyleApiTermController`, `FreestyleErrorController`, `FreestylePostService`, `FreestyleSettingService`, `WebFreestylePostControllerService`, `WebFreestylePostRepository`, `WebFreestylePostService`.
- **Configuration and permission classes (sample):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Potential extension points based on class names:** `ArticleWebGlobalErrorHandler`, `ArticleWebGlobalExceptionHandler`, `WebGetChildrenListBySlugSortByPriorityAscIdAscEzyFunctionEventHandler`, `WebGetMostViewPostsByAuthorUserIdEzyFunctionEventHandler`, `WebGetMostViewPostsByAuthorUserUuidEzyFunctionEventHandler`, `WebGetPostTitleAndChildrenListByMenuNameEzyFunctionEventHandler`, `WebRandomSameTermsPostsByPostIdEzyFunctionEventHandler`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/freestyle/settings` returned 200; the theme rendered an EzyArticle post on Web.

## Integration notes

See how layouts, fragments, and templates are organized by area. Test rendering with fixtures on the chosen theme.

[Back to the plugin index](README.md)
