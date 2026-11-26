# EzyPlatform public documentation inventory

**Reviewed November 26, 2026 (UTC).** We started from the navigation on [ezyplatform.com](https://ezyplatform.com/), compared the [Vietnamese Guide](https://youngmonkeys.org/projects/ezyplatform?tab=guide&lang=vi) with the [English Guide](https://youngmonkeys.org/projects/ezyplatform?tab=guide&lang=en), then followed links inside the articles. Both indexes list the same 76 articles. An older `deploy-ezyplatform` URL duplicates the Ubuntu article: **77 guide URLs, 76 distinct articles**. We use the Vietnamese version where available, or the available content where no translation exists; language variants do not count as separate articles. We found no XML sitemap or separate `/docs` repository on ezyplatform.com. Coverage is limited to what the navigation, official indexes, and article links expose.

## Official sites and reference documentation

| Source | Scope |
| --- | --- |
| [Introduction](https://ezyplatform.com/ezyplatform-introduction) | Low-code platform, five runtime and tooling components, and the module ecosystem. Distinguish modules mentioned in the guide from those actually installed in the stack. |
| [Installation](https://ezyplatform.com/installation-guide) | Resources, Java and MySQL, domain setup, finding modules, support, and per-module documentation. |
| [FAQ](https://ezyplatform.com/faq) | Twelve topics: definition and goals, open-source scope, protocols, installation, extensions, commercial use, indexes, and Marketplace rules and review timelines. |
| [Javadoc](https://ezyplatform.com/java-docs) | The 1.5.9 `allclasses-noframe.html` and `overview-summary.html` indexes yielded 962 pages: 881 classes or interfaces and 81 package summaries. Admin: 552 + 35; Common: 7 + 3; Web: 241 + 25; Socket: 81 + 18. The research focuses on plugin-related classes, not every method or overload. A page title may show module version `0.0.2 API`; that is not the distribution version `1.5.9` in the URL. |
| [Marketplace](https://ezyplatform.com/market) | The [public catalog](https://ezyplatform.com/api/v1/market/items?limit=100&lang=vi) returned 60 items. We listed each item's Docs tab and retrieved 532 public articles. The design-relevant material was reviewed in more depth. Retrieval alone does not imply analysis of each Marketplace document or runtime testing. |

Related reading: [technical research](ezyplatform-deep-research.md) · [Young Monkeys framework research](youngmonkeys/index.md).

## Complete Guide by topic

### Architecture and ecosystem

| Guide | Scope and notes |
| --- | --- |
| [Platform introduction](https://youngmonkeys.org/ezyplatform/guides/introduce-ezyplatform?lang=vi) | Host, framework, and Marketplace; scope of open source and conditions for commercial use. |
| [Benefits for users](https://youngmonkeys.org/ezyplatform/guides/-what-benefits-does-ezyplatform-provide-to-users?lang=vi) | Product development time and cost, testing ideas, and improving quality. This is not a benchmark. |
| [Runtime structure](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-structure?lang=vi) | Admin, Web, and Socket; one active theme, multiple plugins, and distinct Socket token types. |
| [Tech stack](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-tech-stack?lang=vi) | EzyHTTP–Jetty–Thymeleaf, EzyData–Hibernate/JPA, and EzyFox Server. |
| [Themes and plugins](https://youngmonkeys.org/ezyplatform/guides/understanding-ezyplatform-themes-and-plugins?lang=vi) | Four runtime extension types, themes, how they work together, and where modules are stored. |
| [Security](https://youngmonkeys.org/ezyplatform/guides/why-ezyplatform?lang=vi) | Separation of Admin and Web, BCrypt, encryption, URI policy, and uploads. This does not supply application ACLs. |
| [Roadmap](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-development-roadmap?lang=vi) | Community and Marketplace growth, less code, and AI. The roadmap does not establish that a feature has shipped. |
| [Developer model](https://youngmonkeys.org/ezyplatform/guides/how-do-developers-make-money-through-ezyplatform?lang=vi) | Build products or modules and distribute them through Marketplace, subject to the FAQ conditions. |

### Development and packaging

| Guide | Scope and notes |
| --- | --- |
| [Prepare the development environment](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-setup-development-environment?lang=vi) | Separate installation of the runtime, SDK, and IDE from development of individual modules. |
| [Install the SDK](https://youngmonkeys.org/ezyplatform/guides/install-ezyplatform-sdk?lang=vi) | Prepare the runtime and SDK and build dependent libraries. |
| [Plugin quickstart](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-plugin-development-quickstart?lang=vi) | Create or import the project, run startup tests, export, and verify on the runtime. |
| [Create a plugin](https://youngmonkeys.org/ezyplatform/guides/create-a-plugin?lang=vi) | Scaffold modules, configure the working directory, run, and export. |
| [Import a project](https://youngmonkeys.org/ezyplatform/guides/import-a-plugin-project?lang=vi) | Inventory module dependencies and set up run configurations. |
| [Import into IntelliJ](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-import-a-plugin-project-to-intellij?lang=vi) | Maven, JDK, annotation processing, and run configuration. Separate IDE issues from build failures. |
| [IntelliJ path variable errors](https://youngmonkeys.org/ezyplatform/guides/fix-intellij-not-recognizing-path-variable?lang=vi) | Diagnose missing IDE path variables without editing source to work around the issue. |
| [Project structure](https://youngmonkeys.org/ezyplatform/guides/the-structure-of-a-plugin-project?lang=vi) | Maven modules, shared SDK, assembly, metadata, menus, static assets, templates, and TestNG. |
| [Link a plugin](https://youngmonkeys.org/ezyplatform/guides/link-a-plugin?lang=vi) | The target module must already be available. Check dependencies and `@ComponentsScan`. |
| [SDK commands](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi) | `create`, `package`, `export`, and `link`, plus versioning and dependency synchronization. |
| [Runtime CLI commands](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-cli-commands?lang=vi) | Manage the database, server, modules, and updates. This CLI is distinct from the SDK and the stack wrapper. |
| [Module icon](https://youngmonkeys.org/ezyplatform/guides/guide-to-creating-icons-for-ezyplatform-plugin?lang=vi) | Prepare an icon and identity for distribution, separate from menu CSS icons. |
| [Generate unit test classes](https://youngmonkeys.org/ezyplatform/guides/generate-unit-test-class?lang=vi) | `UnitTestClassGenerator` scaffolds tests; it does not supply assertions. |
| [Build, run, and export errors](https://youngmonkeys.org/ezyplatform/guides/nhung-ly-do-khien-ban-khong-the-build-chay-va-export-duoc-du-an-plugin-ezyplatform?lang=vi) | Diagnose each stage: JDK and Maven, working directory, dependencies, and export. |
| [Other common errors](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-some-reasons-leading-to-errors?lang=vi) | Missing exports, menus, or `@Authenticated`, and paths containing spaces. |

### HTTP, UI, localization, and authentication

| Guide | Scope and notes |
| --- | --- |
| [Admin authentication](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-admin-authentication?lang=vi) | Cookie tokens, `@Authenticated`, `@AdminId`, and permission proxies. This does not replace Web user authentication. |
| [Web authentication](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-web-authentication?lang=vi) | Integrate interceptors, optionally allow anonymous requests on designated routes, use `@UserId`, and enable feature permissions. |
| [Permissions](https://youngmonkeys.org/ezyplatform/guides/permission-in-ezyplatform?lang=vi) | Connect roles, features, and APIs using `@EzyFeature`. Enforcement on Web depends on the theme and configuration. |
| [Admin page](https://youngmonkeys.org/ezyplatform/guides/create-an-admin-page?lang=vi) | A controller returns a Thymeleaf view; the route is prefixed with the plugin name. |
| [Admin menus](https://youngmonkeys.org/ezyplatform/guides/create-menus-for-admin-plugin?lang=vi) | `menus.properties`, menu regions, icons, localization, and badges. |
| [Badges](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-add-badge-to-admin-menu-item?lang=vi) | Provide counts per menu item without counting data outside the caller's permissions. |
| [Right toolbar](https://youngmonkeys.org/ezyplatform/guides/add-admin-right-toolbar-tool?lang=vi) | `rightToolbarToolFragments`, the `content` region, dedicated CSS and JS, and message keys. |
| [Hotkeys](https://youngmonkeys.org/ezyplatform/guides/hotkeys-in-ezyplatform?lang=vi) | Global and per-screen shortcuts. Check for conflicts with editors and plugin UI. |
| [Confirmation dialog](https://youngmonkeys.org/ezyplatform/guides/confirmation-popup-usage?lang=vi) | Admin and Web flows for sensitive operations. The server must still check permissions. |
| [previousScreen navigation](https://youngmonkeys.org/ezyplatform/guides/using-previousscreen-to-link-admin-screens?lang=vi) | Preserve filters and pagination and return to a valid screen after saving or redirecting. |
| [Admin JavaScript](https://youngmonkeys.org/ezyplatform/guides/available-javascript-functions-in-admin?lang=vi) | `ezyadmin`: localization, dates and numbers, data tables, toasts, form errors, sessions, and server handling. |
| [Web JavaScript](https://youngmonkeys.org/ezyplatform/guides/available-javascript-functions-in-web?lang=vi) | `ezyweb`: dates and numbers, API and form errors, cookies, languages, and media URLs. |
| [Theme design](https://youngmonkeys.org/ezyplatform/guides/designing-and-programming-a-theme?lang=vi) | Separate templates, fragments, layouts, and localization; mount dynamic content. |
| [ViewDecorator](https://youngmonkeys.org/ezyplatform/guides/guide-to-implement-viewdecorator?lang=vi) | Share data before rendering using `setVariableIfAbsent`; avoid expensive site-wide queries. |
| [View schema](https://youngmonkeys.org/ezyplatform/guides/guide-to-installing-view-schema?lang=vi) | `ViewSchemaFetcher` and `ViewMultipleSchemaFetcher` describe URIs and view variables for tools; they do not enforce ACLs. |
| [Multiple languages](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-multi-languages?lang=vi) | Message bundles, labels, and multilingual data. Do not hard-code system state labels. |
| [Web language configuration](https://youngmonkeys.org/ezyplatform/guides/setup-multiple-languages-for-web?lang=vi) | Enable user languages and set defaults; this is distinct from translating content. |
| [Web errors](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-handle-exception-and-error-for-web?lang=vi) | The global Web exception and error handler separates errors from view logic. |
| [Website configuration](https://youngmonkeys.org/ezyplatform/guides/setup-a-website?lang=vi) | Page variables and analytics configuration, not cycle or task measurement. |

### Data, tasks, and integrations

| Guide | Scope and notes |
| --- | --- |
| [Pagination](https://youngmonkeys.org/ezyplatform/guides/pagination-implementation?lang=vi) | Cursors and offsets, class pairs for sort order, converters, repositories, services, and a generator. |
| [Reactive](https://youngmonkeys.org/ezyplatform/guides/reactive-usage?lang=vi) | Run independent work in parallel with `multiple` and `single`. This does not replace transactions. |
| [Admin search](https://youngmonkeys.org/ezyplatform/guides/integrating-admin-global-search?lang=vi) | `AdminSearchService` and `SearchResultModel`. Check the data returned for each caller. |
| [Settings](https://youngmonkeys.org/ezyplatform/guides/setting-feature?lang=vi) | Data types, cache updates, encryption, and keys prefixed with the plugin name. |
| [Link table](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-insert-data-to-link-table?lang=vi) | `ezy_links`, `LinkService`, and appenders. Do not index private deep links. |
| [Random record function](https://youngmonkeys.org/ezyplatform/guides/how-to-install-the-random-record-query-function?lang=vi) | Random skip and limit avoids `ORDER BY RAND` on large data sets. |
| [Internal events](https://youngmonkeys.org/ezyplatform/guides/create-and-handle-internal-events-in-ezyplatform?lang=vi) | Dispatch by name, priorities, `VoidEvent`, and result-returning handlers. |
| [AdminDataAppender batch jobs](https://youngmonkeys.org/ezyplatform/guides/guide-to-implementing-batch-jobs-with-admindataappender?lang=vi) | Query, transform, and save, plus checkpoints, batch controls, and lifecycle. |
| [Cron](https://youngmonkeys.org/ezyplatform/guides/guide-to-using-cron-expressions-supported-by-ezyplatform?lang=vi) | Five or six fields, Sunday is 0, and no `? L W #` syntax or year field. |
| [Notifications and internal messages](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-send-notification-and-letter?lang=vi) | Templates, services, recipients, and Web APIs and UI. Distinct from external email. |
| [MediaControllerService](https://youngmonkeys.org/ezyplatform/guides/mediacontrollerservice-usage-guide?lang=vi) | Upload, replace, download, and delete, plus metadata, private predicates, storage adapters, and events. |
| [Media modal](https://youngmonkeys.org/ezyplatform/guides/guide-to-using-the-media-modal-in-the-admin-ui?lang=vi) | `showMediaModal`, callbacks, and separating multiple media selection fields. |
| [MIME types](https://youngmonkeys.org/ezyplatform/guides/mime-types-detected-by-ezyplatform?lang=vi) | Recognized type groups, not an application-specific allowlist. |
| [Reduce image size](https://youngmonkeys.org/ezyplatform/guides/how-ezyplatform-reduces-image-file-size?lang=vi) | Thresholds, format-specific processing, originals, metadata, and external adapters. |
| [JavascriptService](https://youngmonkeys.org/ezyplatform/guides/guide-to-using-javascriptservice?lang=vi) | Rhino, scope and beans, and object results. Do not accept untrusted scripts. |
| [Socket](https://youngmonkeys.org/ezyplatform/guides/overview-of-ezyplatform-socket?lang=vi) | Separate user and admin login flows, Socket hooks, and a sample JavaScript client. |

### Installation and operations

| Guide | Scope and notes |
| --- | --- |
| [Install EzyPlatform](https://youngmonkeys.org/ezyplatform/guides/install-ezyplatform?lang=vi) | Docker or manual installation on Linux, macOS, or Windows, with `EZYPLATFORM_HOME`. |
| [Quick deployment](https://youngmonkeys.org/ezyplatform/guides/quickstart-deploy-ezyplatform-to-server?lang=vi) | Managed hosting versus self-hosting, with links to Ubuntu and Docker instructions and further reading. |
| [Deploy on Ubuntu](https://youngmonkeys.org/ezyplatform/guides/deploy-ezyplatform-on-ubuntu?lang=vi) | Resources, databases, JDK, Nginx, HTTPS, and preserving encryption configuration; [older URL with the same content](https://youngmonkeys.org/ezyplatform/guides/deploy-ezyplatform?lang=vi). |
| [Deploy with Docker](https://youngmonkeys.org/ezyplatform/guides/deploy-ezyplatform-with-docker?lang=vi) | Compose, deployment variables, volumes, and load balancing. Use this stack's Compose configuration for this project. |
| [Infrastructure providers](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-deployment-guide-for-infrastructure-providers?lang=vi) | Deploying multiple environments, operational access, and an infrastructure checklist. |
| [Add a plugin](https://youngmonkeys.org/ezyplatform/guides/add-a-plugin-to-your-ezyplatform?lang=vi) | Find, download, install, and activate a module, restart, and handle dependencies. |
| [Update a plugin](https://youngmonkeys.org/ezyplatform/guides/update-a-plugin?lang=vi) | Update steps by operating system. Do not confuse module updates with core upgrades. |
| [Upgrade and recovery](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-update-and-recovery?lang=vi) | Update and recovery entry points by operating system and error. |
| [Update on Windows](https://youngmonkeys.org/ezyplatform/guides/updating-ezyplatform-on-windows-guide?lang=vi) | Download and prepare the installation using the Admin workflow. |
| [Recover from a failure](https://youngmonkeys.org/ezyplatform/guides/recover-ezyplatform-when-an-error-occurs?lang=vi) | Identify JDK errors and missing or invalid plugins, and consult logs before making changes. |
| [Move to a new server](https://youngmonkeys.org/ezyplatform/guides/migrate-ezyplatform-from-server-a-to-server-b?lang=vi) | Copy the runtime, dump and import the database, and update DNS and Nginx. |
| [Multiple installations and databases](https://youngmonkeys.org/ezyplatform/guides/install-multiple-ezyplatforms-with-a-single-database?lang=vi) | Separate encryption keys per instance. Separate databases and do not share schemas arbitrarily. |
| [Domain names and SSL](https://youngmonkeys.org/ezyplatform/guides/set-up-domain-and-ssl-for-ezyplatform?lang=vi) | DNS, Nginx, and Certbot via EzySupport or manual setup. |
| [WebSocket SSL](https://youngmonkeys.org/ezyplatform/guides/set-up-ssl-for-ezyplatform-websocket?lang=vi) | Certificates, restarting Socket and updating WSS, renewals, and error handling. |
| [Tune configuration](https://youngmonkeys.org/ezyplatform/guides/toi-uu-cau-hinh-cho-ezyplatform?lang=vi) | Socket is optional. Size heap, CPU, and threads by runtime and real load. |
| [LogbackAppender](https://youngmonkeys.org/ezyplatform/guides/installing-a-log-appender-in-ezyplatform?lang=vi) | Register and configure appenders and separate operational logs from audit data. |
| [Statistics APIs](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-statistics-apis?lang=vi) | Server and module lifecycle events controlled by `allow_send_statistics_data`. |
| [Custom branding](https://youngmonkeys.org/ezyplatform/guides/brand-your-ezyplatform?lang=vi) | Marketplace, logo, footer, contact information, and fallbacks. |

## Marketplace documentation for design decisions

| Candidate | Evidence and conclusion |
| --- | --- |
| **EzyArticle** | [Overview](https://ezyplatform.com/market/items/ezyarticle/docs/gioi-thieu-plugin-ezyarticle), [data tags](https://ezyplatform.com/market/items/ezyarticle/docs/huong-dan-tich-hop-cho-phep-tag-duoc-du-lieu), [data comments](https://ezyplatform.com/market/items/ezyarticle/docs/gioi-thieu-tinh-nang-binh-luan-du-lieu-voi-ezyarticle), and [page fragments](https://ezyplatform.com/market/items/ezyarticle/docs/huong-dan-su-dung-page-fragment). In addition to CMS features, the docs cover tags associated with entity types and internal Admin discussions with threads, mentions, and resolution. These are useful patterns, not evidence of a Web API that enforces application ACLs or of feature availability in the pinned **1.5.6** artifact. |
| **EzyLogin / EzyAccount** | [EzyLogin](https://ezyplatform.com/market/items/ezylogin/docs/tong-quan-plugin-ezylogin) covers registration, sign-in, recovery, OAuth and SSO, 2FA, and sessions. [EzyAccount](https://ezyplatform.com/market/items/ezyaccount/docs/mo-ta-chi-tiet-tinh-nang-quan-ly-thong-bao-va-hom-thu) lets users view notifications and their inbox. These are options for identity UI and inbox features; they do not own membership or ACLs or come installed by default. |
| **EzyMail** | [Overview](https://ezyplatform.com/market/items/ezymail/docs/tong-quan-MjU4): email delivery, templates, drafts, delivery tracking, and SMTP setup. Use an adapter if email or invitations are needed. Core notifications are a separate channel. |
| **Markdown** | [Overview](https://ezyplatform.com/market/items/markdown/docs/tong-quan-plugin-markdown): editing and rendering for CMS content. Direct HTML syntax means rendering user-supplied descriptions is not inherently safe. |
| **EzyChat / EzyOA / EzyCRM** | The [EzyChat architecture](https://ezyplatform.com/market/items/ezychat/docs/kien-truc-cua-plugin-ezychat) illustrates Socket and channels. [EzyOA](https://ezyplatform.com/market/items/ezyoa/docs/tong-quan-plugin-ezyoa) integrates Official Accounts and webhooks. [EzyCRM](https://ezyplatform.com/market/items/ezycrm/docs/tong-quan-MzUw) covers customers and user groups. Consider dependencies only when the plugin needs those features. |

We did not review content that requires an account or purchase, off-site course videos, unlinked documentation versions, or actual plugin behavior.
