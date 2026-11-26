# HTTP APIs used by this skill

Use these directly (curl, PowerShell `Invoke-RestMethod`) only when `scripts/ezylanding.py` cannot run. `<admin>` is the admin address, `<web>` the public site address, `<token>` the admin access token sent as `Authorization: Bearer <token>`. Never print the token.

## EzyLogin CLI login (admin side, EzyLogin 0.4.1+)

| Step | Request |
|---|---|
| Probe (no token) | `POST <admin>/ezylogin/api/v1/cli/me/token` body `{}` → `404` EzyLogin missing/inactive, `403 {"cliLogin":"notAllowed"}` admin CLI login disabled, `400` enabled |
| Approval page | open `<admin>/ezylogin/cli/authorize?client_name=<name>&redirect_uri=http://127.0.0.1:<port>/callback&state=<random>&code_challenge=<BASE64URL(SHA256(verifier)) without =>&code_challenge_method=S256` while a local HTTP server listens on `127.0.0.1:<port>` |
| Callback | `http://127.0.0.1:<port>/callback?code=<code>&state=<state>`; compare `state`; the code is valid 2 minutes, once |
| Exchange | `POST <admin>/ezylogin/api/v1/cli/me/token` `{"code","codeVerifier","redirectUri"}` → `{"accessToken","accessTokenExpiredAt"}` |

## Site

| Request | Result |
|---|---|
| `GET /api/v1/admins/me` | the signed-in admin (`401` = token invalid) |
| `GET /api/v1/settings/web-url` | public site URL (plain text) |
| `GET /api/v1/settings` | `{items:[{name,value}]}` (paginated); `web_languages` (JSON list) and `web_default_language`, absent on a fresh install |
| `GET /api/v1/settings/current-server-urls` | `{adminUrl, webUrl, websocketUrl}`: internal addresses the servers use to reach each other |
| `PUT /api/v1/settings/set-web-urls` `{"webUrl","currentServerWebUrl"}` | public web address (Dashboard → Web); keep `currentServerWebUrl` from the GET above |
| `PUT /api/v1/settings/set-admin-url` `{"adminUrl","currentServerAdminUrl"}` | public admin address (Dashboard → Admin) |
| `PUT /api/v1/settings/data-appenders/ezysupport_contact_us_user/start` (`stop`, `restart`) | EzySupport "Contact Us user creator" job (CRM users from leads) |

## Plugins and themes (permission "plugin management")

| Request | Result |
|---|---|
| `GET /api/v1/projects/<name>` | `{name, displayName, version}`; `404` not installed |
| `GET /api/v1/projects/<name>/module-types[?active=true]` | module types, e.g. `["theme","admin-plugin"]` for Freestyle |
| `POST /api/v1/projects/<name>/<version>/install?marketUrl=https://ezyplatform.com` | download and install |
| `POST /api/v1/projects/<name>/activate` `{"moduleTypes":[...],"restart":true}` | activate and restart; `403 {"projectMissingDependencies":[{"projectName"...}]}` / `projectInactiveDependencies` / `projectNeedToUpdateDependencies` = install, activate or update those first |
| `GET https://ezyplatform.com/api/v1/released-projects/<name>` (public) | `latestVersion.name`, `includeModuleTypes`, `price` |

Names used: `freestyle` (theme), `ezyarticle`, `ezylogin`, `ezysupport`, `ezymail`, `ecommerce`, `graphql`, `ezypayment`, `ezydelivery`.

## Pages (EzyArticle)

| Request | Result |
|---|---|
| `GET /ezyarticle/api/v1/post-by-slug/<slug>[?i18n_lang=<lang>]` | the page (`id`, `title`, `content`, `status`, `postType`...); `404` none |
| `POST /ezyarticle/api/v1/posts/save-simply[?publish=true]` | create or update by `slug`: `{slug, postType:"STANDALONE_PAGE", title, summary, content, additionalHead:"", additionalFoot:"", contentType:"HTML", status:"DRAFT"|"PUBLISHED", language?, featuredImageName?}`. Updating a page that is already `PUBLISHED` without `?publish=true` only stores a revision. |
| Preview | `<admin>/ezyarticle/pages/<slug>/preview[?lang=<lang>]` |
| Public | `<web>/<slug>` |

## Media

| Request | Result |
|---|---|
| `GET /api/v1/media/<name>/contains` | `{contains: bool}` |
| `POST /api/v1/media/add?notPublic=false` | multipart field `file`; `400 {"fileType":"invalid"}` when the MIME type is not accepted (SVG by default); stored under a hash name, the original name still serves |
| `POST /api/v1/media/<name>/replace-by-name` | multipart field `file` |
| Public URL | `<web>/api/v1/media/<name>?v=<n>` |

## Contact Us (EzySupport, public)

`POST <web>/api/v1/contact-us` JSON `{contactUsYourName*, contactUsYourEmail*, contactUsYourPhoneNumber, contactUsSubject*, contactUsMessage*, <accepted metadata keys>...}` → `204` ok; `400` (or `200` on some sites) `{"<field>":"required|invalid|overLength"}`; `400 {"captchaToken":"invalid"}`; `404` contact disabled. Settings and the "Contact Us user creator" job are in `<admin>/ezysupport/settings`; requests in `<admin>/ezysupport/contact-us`; captcha in **EzySupport → Captcha settings**.

## E-Commerce checkout links (public)

- `/products/<code>/checkout?quantity=&colorName=&sizeName=&materialName=&discountCode=&clearShoppingCart=true`
- `/products/checkout?productCodes=a,b&productQuantities=1,2&productColorNames=&productSizeNames=&productMaterialNames=&discountCode=`

Both add to the cart and redirect to `/checkout/shopping-cart`. `403 {"createAnonymous":"forbidden"}` = visitor not signed in and EzyLogin anonymous users off; `404` = unknown or unpublished product. In the cart, `GET /api/v1/vouchers/<code>/discount-amount?shoppingCartId=&currencyId=` answers `404 {"voucherTarget":"notFound"}` when the voucher has no target products/categories.

## GraphQL (public, when the plugin is installed)

- Query: `POST <web>/graphql` with `{"query": "...", "variables": {...}}` (the web user's session/permissions apply)
- Schema: `GET <web>/api/v1/graphql/schema.graphql`
- Docs page: `<web>/graphql/schema` (only when enabled in GraphQL settings)
