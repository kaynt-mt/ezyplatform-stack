# Free runtime plugins on EzyPlatform 1.5.9

This catalog covers **37/37** ZIP packages downloaded from Marketplace and tested on core **1.5.9**. See the [test report](test-report.md) to reproduce the sandbox, read the HTTP and Socket results, and learn why 18 packages requiring download permission are out of scope.

This is a historical snapshot; see the [installer manifest](../../scripts/plugin-versions.tsv) for the current stack's versions and module types.

## How to read

- Versions and module types were checked against the [manifest](../../scripts/plugin-versions.tsv) and the installed package's `module.properties`. When the ZIP and module metadata disagree, the version column lists both (`ZIP/module`).
- The profiles are based on 82 installed modules. They draw on plugin and SDK JARs (`jar`/class files and `javap -v`), HTTP annotations, Socket entry loaders, menus, templates, configuration files, and bundled DDL. Do not add JARs, ZIPs, or configuration values to the repository.
- **Static analysis is not functional testing.** Class names show where to look next; they do not prove an extension is public or enabled. `CREATE TABLE` identifies declared tables but does not prove migrations ran. The mounted route can have a different prefix from the annotation. Each profile lists sandbox observations separately, including 401 responses and error pages returned with HTTP 200.

## Catalog

| Plugin | Version | Modules | Scope |
|---|---|---|---|
| [accounting](accounting.md) | `0.3.8` | admin-plugin, web-plugin | Accounting: accounting system, user and trading book |
| [consulting](consulting.md) | `0.1.6` | admin-plugin, web-plugin, theme | Consultancy: Customer, staff, personal documents and themes |
| [data-backup](data-backup.md) | `0.0.9` | admin-plugin | Backup data and schedule snapshot |
| [ecommerce](ecommerce.md) | `1.5.8` | admin-plugin, web-plugin, socket-plugin | Catalog, store, shopping cart, order and checkout |
| [ezyaccount](ezyaccount.md) | `0.2.4` | admin-plugin, web-plugin | Interface and API Membership Account |
| [ezyai](ezyai.md) | `0.1.8` | admin-plugin, web-plugin, socket-plugin | Configuration of AI services, skill and skill library |
| [ezyarticle](ezyarticle.md) | `1.5.6` | admin-plugin, web-plugin, socket-plugin | Articles, content pages, taxonomy and publication |
| [ezyblockchain](ezyblockchain.md) | `0.0.3` | admin-plugin, web-plugin | Chain, token and address management |
| [ezychat](ezychat.md) | `0.3.6` | admin-plugin, web-plugin, socket-plugin, socket-app | Channel, profile, conversation and Socket app/plugin |
| [ezycrm](ezycrm.md) | `0.6.3` | admin-plugin, web-plugin | Customers, responsibilities, groups and history |
| [ezydefence](ezydefence.md) | `0.1.5` | admin-plugin, web-plugin | IP policies, lists of permits/blocking and HTTP filter |
| [ezydelivery](ezydelivery.md) | `0.7.7` | admin-plugin, web-plugin | Order code, scan code and delivery |
| [ezygame](ezygame.md) | `0.0.8` | admin-plugin, web-plugin | Index, events and achievements |
| [ezyiot](ezyiot.md) | `0.0.3` | admin-plugin, web-plugin, socket-plugin | Equipment, configuration and lane socket |
| [ezylogin](ezylogin.md) | `0.4.7` | admin-plugin, web-plugin | Login, Configuration of the Supplier and Session |
| [ezymail](ezymail.md) | `0.3.3` | admin-plugin, web-plugin | Template email, mailing and tracking sending |
| [ezymarketing](ezymarketing.md) | `0.3.7` | admin-plugin, web-plugin | Advertising, campaigns and short links |
| [ezyoa](ezyoa.md) | `0.4.2` | admin-plugin, web-plugin | Official Account, Screenplay and Notification |
| [ezyocr](ezyocr.md) | `0.0.3` | admin-plugin | OCR script and identification configuration |
| [ezypayment](ezypayment.md) | `0.2.5` | admin-plugin, web-plugin | Payment, packaging and subscription services |
| [ezyrag](ezyrag.md) | `0.0.6` | admin-plugin, web-plugin, socket-plugin | RAG Management and Integrated Class AI |
| [ezyrating](ezyrating.md) | `0.4.5` | admin-plugin, web-plugin | User reviews, items and customer travel |
| [ezyseo](ezyseo.md) | `0.1.2` | admin-plugin, web-plugin | Sitemap, links and robots |
| [ezysupport](ezysupport.md) | `0.6.2` | admin-plugin, web-plugin | Contact, FAQ, Recruitment and Support Content |
| [ezyvector](ezyvector.md) | `0.0.5` | admin-plugin, web-plugin | Data collection and vector management |
| [freestyle](freestyle.md) | `0.2.9` | admin-plugin, theme | General Web Theme and Configuration Interface |
| [game-master-server](game-master-server.md) | `0.0.7` | admin-plugin, web-plugin, socket-plugin | Master and Instance Game Management |
| [graphql](graphql.md) | `0.3.1` | admin-plugin, web-plugin, socket-plugin | Endpoint and GraphQL Scheme |
| [logs-monitor](logs-monitor.md) | `0.0.5` | admin-plugin, web-plugin, socket-plugin | Console, log folder and lane socket |
| [lucky-wheel](lucky-wheel.md) | `0.0.1` | admin-plugin, web-plugin, theme, socket-plugin, socket-app | Bonus games include Admin, Web, Theme and Socket |
| [markdown](markdown.md) | `0.2.6` | admin-plugin, web-plugin | Markdown and Web Module |
| [omnichannel](omnichannel.md) | `0.0.4` | admin-plugin, web-plugin | External Channel Management and Social Network Connections |
| [postgresql](postgresql.md) | `0.0.1` | admin-plugin | PostgreSQL Management Surface |
| [semi-theme](semi-theme.md) | `1.0.2/1.0.1` | admin-plugin | Module Admin supports the interface; no Web theme |
| [sites](sites.md) | `0.0.3` | admin-plugin | Server management and site configuration |
| [socket-monitor](socket-monitor.md) | `0.0.3` | socket-plugin | Socket monitoring and entry loader |
| [wordpress](wordpress.md) | `0.1.4` | admin-plugin, web-plugin | Configuration and flow of WordPress data |

## Patterns to reuse in plugin development

| Need | Reference plugins or patterns | Limits to verify |
| --- | --- | --- |
| Sign-in, accounts, and notifications | [EzyAccount](ezyaccount.md), [EzyLogin](ezylogin.md), [EzyMail](ezymail.md) | Reuse core identity where appropriate, but enforce resource permissions separately. Test email with simulated SMTP. |
| Forms, filters, and history | [EzyCRM](ezycrm.md), [EzySupport](ezysupport.md) | Use the workflows and data organization as examples. A pattern alone does not require a runtime dependency. |
| Content and interfaces | [EzyArticle](ezyarticle.md), [Freestyle](freestyle.md), [Markdown](markdown.md) | Test rendering with a fixture and the selected theme. Check media permissions and sanitize user input. |
| Real-time features, connectors, and queries | [EzyChat](ezychat.md), [EzyOA](ezyoa.md), [Omnichannel](omnichannel.md), [GraphQL](graphql.md) | Add these only when needed. Verify access on the actual routes and check their dependencies. |

See the [stack's plugin build skill](../../skills/ezy-build-plugin/SKILL.md) for agent skills and new plugin builds. This index covers runtime plugins and evidence from installed packages.

For new Java plugins, use the end-to-end [plugin lifecycle verification recipe](pilot-verification.md) before treating the runtime as proven.
