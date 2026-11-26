# Testing Marketplace plugins on EzyPlatform 1.5.9

See the [index of 37 free plugins](README.md) for JARs, APIs, data, menus, templates, and potential extension points.

On November 26, 2026, the local Compose sandbox ran EzyPlatform **1.5.9**, Java **11**, and MySQL **8.0.46**. The [public catalog](https://ezyplatform.com/api/v1/market/items?limit=100&type=plugin) returned all **55** entries (`total=55`, `hasNext=false`). The ZIP endpoint with `platformVersion=1.5.9` returned `200 application/zip` for **37** free entries and `403` for **18** paid entries. We installed and verified the actual versions and modules of **37/37** downloadable packages. A 403 is not evidence of incompatibility.

## Reproduce in a sandbox

```sh
./scripts/up.sh
# Create a super admin at http://127.0.0.1:9090/setup-admin; there is no default password.
python3 scripts/install-plugins.py --theme freestyle
```

The script only runs against core 1.5.9 on the loopback-bound Compose port. It discovers the host bindings through Compose and inherits `COMPOSE_PROJECT_NAME`, so sandbox port overrides need no script arguments. It uses `cli.sh "install <name>"` with the [tested version list](../../scripts/plugin-versions.tsv), checks the Marketplace version before downloading, and stops if the installed version differs from the manifest. The CLI's `install` command has no version selector. The script reads `dependencies=` from `module.properties`, activates **only module types that are actually present** in dependency order, checks the `.runtime` cache, and restarts Admin and Web. Do not use `activate all`: in the sandbox it created theme and socket cache entries for `ezyaccount` even though the package had neither module. When switching themes, the script clears the cache flag for any theme that no longer has a module; the CLI does not accept deactivation for such entries. Without `--theme`, the script preserves the active theme. Try `consulting` or `lucky-wheel`, or switch back to `welcome`.

For a custom plugin, do not install every tested project. Pass the direct Marketplace dependencies declared by its modules, for example `python3 scripts/install-plugins.py --only ezylogin` or `--only ezylogin,ezysupport`. The script installs the transitive closure and activates it in dependency order, so the EzyLogin example also handles EzyMail. Declare only direct dependencies in the custom plugin's `module.properties`; the platform itself resolves transitive dependencies during activation.

If the CLI download fails, install the exact version from the Admin Modules page and rerun the script. Alternatively, use `--admin-cookie-jar /path/to/local-cookie.txt` with the Netscape cookie file for a **sandbox** Admin session so the script uses the signature-verified Marketplace endpoint `POST /api/v1/projects/<name>/<version>/install`. Keep the cookie file outside the repository and use only a local account. The Admin route installed `ezyrag` and `ezyblockchain` successfully (`204`) after the CLI raised `NoSuchFileException` for the `.zip.downloading` file. Retrying the CLI succeeded for `ezymail` after a similar failure. Do not use Upload Project as a workaround because that route does not verify Marketplace signatures.

Compose starts only Admin and Web by default. To test Socket, enable it in Admin and run `docker compose exec -T ezyplatform bash cli.sh 'start socket'`. If Socket does not start after a Compose restart, inspect `socket/.runtime/ezyfox_server_instance.pid` in the container: `socket/start-service.sh` only checks the PID file. Remove a stale PID file only after confirming that the process no longer exists. Do not rely on “Start socket server successfully” alone; check the internal port and startup logs.

## Installable packages and HTTP tests

Module key: **A** = admin-plugin, **W** = web-plugin, **S** = socket-plugin, **G** = socket-app, **T** = theme. Admin URLs were called with a local authenticated session. HTTP 200 responses containing “Not Found” or “Server error” pages did not count as passing. Web and API URLs below use Freestyle unless noted. These are local functional smoke tests, not full feature or production compatibility certification.

| Plugin | Release | Modules | Installation | Checks and limitations |
|---|---|---|---|---|
| accounting | 0.3.8 | A, W | Passed | Admin `/accounting/overview` and `/accounting/accounts` → 200. No entries posted or vouchers exported. |
| consulting | 0.1.6 | A, W, T | Passed | Admin `/consulting/customers` → user list; Web `/api/v1/documents` → 200; the Consulting theme rendered `/services` and `/documents`. |
| data-backup | 0.0.9 | A | Passed | Admin `/data-backup/backup-clients` → 200. Automatic backup failed because the app container lacked the MySQL/MariaDB CLI; restore was not tested. |
| ecommerce | 1.5.8 | A, W, S | Passed | Admin `/ecommerce/orders` and `/ecommerce/products` → 200. Freestyle does not provide the Web `/products` page. No real order or payment placed. |
| ezyaccount | 0.2.4 | A, W | Passed | Admin `/ezyaccount/settings` → 200; unauthenticated Web `/ezyaccount/api/v1/account` → 401. |
| ezyai | 0.1.8 | A, W, S | Passed | Admin `/ezyai/ai-chat-services` and Web `/ezyai/skill-library` → 200. No AI provider called. |
| ezyarticle | 1.5.6 | A, W, S | Bundled | Admin created and read a `PUBLISHED` article; Freestyle rendered the expected article content over HTTP 200. |
| ezyblockchain | 0.0.3 | A, W | Passed via Admin | Admin `/ezyblockchain/control-panel` and Web `/ezyblockchain/api/v1/chains/current` → 200. Admin logs warned that a migration tried to drop a nonexistent index. No wallet connected or transaction executed. |
| ezychat | 0.3.6 | A, W, S, G | Passed | Admin `/ezychat/channels` → 200; unauthenticated Web channels API → 401. `/ezychat/widget` without an embed key returned an error page with status 200; logs showed `NullPointerException` while reading the chat profile. |
| ezycrm | 0.6.3 | A, W | Passed | Admin `/ezycrm/customers` and `/ezycrm/user-groups` → 200. No notifications sent or customer data imported. |
| ezydefence | 0.1.5 | A, W | Passed | Admin `/ezydefence/blacklist` and `/ezydefence/whitelist` → 200. No policy changed. |
| ezydelivery | 0.7.7 | A, W | Passed | Admin `/ezydelivery/scan-delivery-order-codes` → 200. Freestyle does not provide `/track-shipment`. No carrier called. |
| ezygame | 0.0.8 | A, W | Passed | Admin `/ezygame/metrics` → 200. The catalog lists S and G, but neither module was in the ZIP. |
| ezyiot | 0.0.3 | A, W, S | Passed | Admin `/ezyiot/devices` → 200. No physical device tested. |
| ezylogin | 0.4.7 | A, W | Passed | Admin `/ezylogin/settings/regular` → 200. No external OAuth or SSO connected. |
| ezymail | 0.3.3 | A, W | Passed on retry | Admin `/ezymail/templates` and `/ezymail/sent-mails` → 200. No real email sent. |
| ezymarketing | 0.3.7 | A, W | Passed | Admin `/ezymarketing/advertisements` and Web `/ezymarketing/api/v1/advertisements` → 200. |
| ezyoa | 0.4.2 | A, W | Passed | Admin `/ezyoa/oa-services` and `/ezyoa/templates` → 200. No Official Account integrated. |
| ezyocr | 0.0.3 | A | Passed | Admin `/ezyocr/ocr-business-scripts` → 200. No external OCR configured. |
| ezypayment | 0.2.5 | A, W | Passed | Admin `/ezypayment/payment-services` and Web `/api/v1/payment-plans` → 200. No payment gateway called. |
| ezyrag | 0.0.6 | A, W, S | Passed via Admin | Admin `/ezyrag/settings` → 200. Depends on `ezyai`; no embedding or LLM provider called. |
| ezyrating | 0.4.5 | A, W | Passed | Admin `/ezyrating/dashboard` and Web `/ezyrating/user-ratings` → 200. |
| ezyseo | 0.1.2 | A, W | Passed | Admin `/ezyseo/sitemaps`, Web `/robots.txt`, and `/api/v1/sitemaps` → 200. |
| ezysupport | 0.6.2 | A, W | Passed | Admin `/ezysupport/contact-us` and Web `/contact-us` and `/faq` → 200. No outbound request sent. |
| ezyvector | 0.0.5 | A, W | Passed | Admin `/ezyvector/vector-collections` → 200. No dataset loaded or vector queries measured. |
| freestyle | 0.2.9 | A, T | Passed | Admin `/freestyle/settings` → 200. The theme rendered an EzyArticle post on Web. |
| game-master-server | 0.0.7 | A, W, S | Passed | Admin `/game-master-server/game-master-server` → 200; unauthenticated Web instances API → 401. No game instance run. |
| graphql | 0.3.1 | A, W, S | Passed | Admin `/graphql/system-endpoints` → 200. `/rest/swagger` and the tested schema URLs returned “Not found” pages on Freestyle. No GraphQL query run. |
| logs-monitor | 0.0.5 | A, W, S | Passed | Admin `/logs-monitor/console` and `/logs-monitor/log-folder` → 200. |
| lucky-wheel | 0.0.1 | A, W, S, G, T | Passed | Admin `/lucky-wheel/settings` → 200. Lucky Wheel theme sent `/` to `/index.html` (200). `/api/v1/lucky-wheel` → JSON 200, but `/lucky-wheel` displayed “Not found.” Prize-bearing spins were not tested. |
| markdown | 0.2.6 | A, W | Passed | Admin `/markdown/` displayed the Markdown page (200). |
| omnichannel | 0.0.4 | A, W | Passed | Admin `/omnichannel/social-networks` → 200. No external channel connected. |
| postgresql | 0.0.1 | A | Passed | Admin `/postgresql/dashboard` → 200 on the MySQL stack. No datasource changed or actual PostgreSQL instance tested. |
| semi-theme | 1.0.2 | A | Passed | Admin `/semi-theme/` → 200. ZIP `1.0.2` declares `version=1.0.1` in `module.properties`. This is an Admin module, not a Web theme. |
| sites | 0.0.3 | A, W | Passed | Admin `/sites/servers` and `/sites/settings` → 200. No new site or host created. |
| socket-monitor | 0.0.3 | S | Bundled | The entry loader registered `AdminLoginController` at Socket startup; there is no separate Web page. |
| wordpress | 0.1.4 | A, W | Passed | Admin `/wordpress/migration` → 200. No WordPress data imported. |

**Theme checks:** Welcome did not render article content at the URL (“Not found”). With Freestyle, `GET http://127.0.0.1:8080/posts/plugin-smoke-fixture` → 200, title `Plugin Smoke Fixture`, body `Sandbox plugin smoke test`. We switched to Consulting, then Lucky Wheel, then back to Freestyle. Multiple themes were not active at the same time.

**Socket checks:** After the final restart, the Java process listened on internal TCP ports 3005 and 2208. Logs showed registration of all 11 socket plugins in the manifest and both Socket apps (EzyChat and Lucky Wheel). Client-level protocol checks and end-to-end messaging were not tested.

## Packages blocked by Marketplace permissions

Each entry below returned HTTP 403 for the unauthenticated ZIP request targeting core 1.5.9. None were purchased, installed, or activated, and compatibility with this core remains unverified. The versions and modules are from the catalog, not verified against ZIP contents.

| Plugin | Listed version | Listed modules | Result |
|---|---|---|---|
| ai-skill-marketplace | 0.0.4 | A, W, T | Not installed (403) |
| code | 1.0.3 | A | Not installed (403) |
| community | 0.0.3 | A, W, T | Not installed (403) |
| dropship | 0.0.5 | A, W, T | Not installed (403) |
| elearning | 0.8.5 | A, W, T | Not installed (403) |
| enhancement | 1.0.1 | A | Not installed (403) |
| ezysmashers | 0.2.3 | A, W, S, G, T | Not installed (403) |
| ezytank | 0.1.6 | A, W, S, G, T | Not installed (403) |
| fashion | 0.3.9 | A, W, T | Not installed (403) |
| logistics | 0.3.9 | A, W, T | Not installed (403) |
| official-shipping | 0.0.8 | A, W, T | Not installed (403) |
| publishing | 0.2.7 | A, W, T | Not installed (403) |
| retail | 0.0.3 | A, W, T | Not installed (403) |
| stackask | 0.3.0 | A, W, T | Not installed (403) |
| story | 0.0.7 | A, W, T | Not installed (403) |
| tournament | 0.0.7 | A, W, T | Not installed (403) |
| viettel-post-sandbox | 0.0.6 | A, W | Not installed (403) |
| zalo-sandbox | 0.1.2 | A, W | Not installed (403) |

## Dependency order notes

- `ezyarticle` and `ecommerce` are the two root nodes. Activate `ecommerce` before `accounting`, then `ezydelivery`, which also needs `ezyarticle`. `graphql` needs both `ezyarticle` and `ecommerce`.
- `ezyarticle` → `ezymail` → `ezysupport`, `ezylogin`, and (with `ecommerce`) `ezycrm` and `ezyrating`. `ezymarketing` also needs EzySupport. `omnichannel` needs Ecommerce, EzyArticle, EzyRating, and EzySupport. Activating EzyLogin before EzyMail fails validation with HTTP 403 and `projectMissingDependencies: ezymail`; this is the platform's transitive dependency check, not a reason to add EzyMail to a custom plugin that only uses EzyLogin.
- `ezyarticle` → `ezychat`; `graphql` + `ezychat` → `ezyai` → `ezyrag`. `ezyoa` needs EzyArticle, EzySupport, and EzyChat. `consulting` needs CRM, OA, Account, Login, Support, Article, and Ecommerce.
- On the first bulk activation, Admin and Web started in parallel. The logs showed missing tables (`ecommerce_product_categories`, `ecommerce_shops`, `ecommerce_product_currencies`, `ezydefence_white_uri_ips`, and `ezygame_metrics`) and some Web requests failed. After Admin and Web were fully up, retrying the test post route returned the expected content. The sandbox did not meet a clean-log criterion: Admin still logged EzyBlockchain SQL warnings and periodic Data Backup failures. Assess the logs for each startup; HTTP 200 does not prove that migrations or backups succeeded.

## General lessons for plugin development

1. Use each Admin, Web, or Socket lane as needed. Keep business data and permissions separate from system permissions, and authorize access per resource even after authentication.
2. Test both fresh-install and upgrade migrations before confirming that Web is stable. Review each boot's logs rather than checking HTTP 200 alone.
3. Test the UI with the active theme. The default Welcome theme did not render the EzyArticle post, while Freestyle rendered the same fixture.
4. Keep SMTP, OAuth, AI, payments, and backups out of smoke tests; test integrations with a suitable adapter, mock, or sandbox.
