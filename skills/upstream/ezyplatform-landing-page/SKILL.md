---
name: ezyplatform-landing-page
description: Build a landing page on an EzyPlatform website for a non-technical user (vibe coder) from a guided interview - what the page is for, its audience and sections, a lead/contact form saved by EzySupport (with automatic user creation for CRM), "buy now" product links through E-Commerce checkout (with GraphQL, EzyLogin, EzyPayment), brand identity from the user's logo or from a brand brief when there is no logo yet, images and copy - then installs the theme (Freestyle by default) and plugins it needs, writes the page as a standalone page, uploads images, saves it as a draft, checks it and publishes it after approval, with backups and rollback, and optionally points the user's own domain to it with EzySupport (DNS, Nginx, SSL). Signs in through EzyLogin CLI login (browser approval, no password or token copied). Use when the user asks to create / build / làm / tạo a landing page, trang đích, trang giới thiệu sản phẩm, trang bán hàng một trang, trang thu lead / thu thập khách hàng tiềm năng, or a one-page marketing site on EzyPlatform.
---

# Build a landing page on EzyPlatform

The user is usually a "vibe coder": they know what they want to sell or promote, not HTML, APIs or EzyPlatform internals. Your job is mostly to **ask the right questions in the right order**, then do all the building yourself. Talk to them in their language, in simple words, with examples they can just accept.

How it works: a landing page is an EzyArticle page of type `STANDALONE_PAGE` (a blank page with its own full HTML, CSS and JS, without the site header and footer) on an installed theme (Freestyle by default, a blank theme made for building pages freely). Forms post to the EzySupport Contact Us API; buy buttons are E-Commerce checkout links. You write the page as local files, upload images to the media library and save the page through the admin API.

## Rules

- **You do the work.** Run every command, write every file, check every result. When something can only be done in the admin UI, do it yourself through the browser if you have browser tools; otherwise give short numbered steps (address, menu, field, button names in the user's admin language), wait, then check again.
- Ask the user only for: what the page is about and what it must do (the interview), their own content (logo, images, texts, product codes, contact details), approvals in the browser, and choices with a cost (installing plugins, switching the site's theme, restarting, publishing, sending a real test mail).
- Never print, log or paste the access token, never ask for a password, SMTP password or payment API key in chat. The script keeps the token in `~/.ezyplatform/landing-page.json` (owner-only). Payment and mail credentials are typed by the user in the admin.
- Only real content. Never invent prices, testimonials, customer logos, statistics, certifications or contact details. Use clearly marked placeholders (`[Ảnh sản phẩm]`, `[Giá]`) and list them in the report.
- Save as **draft** first; publish only after the user has seen the preview and said yes. Every save backs up the previous server version.
- Installing plugins or switching the theme restarts the admin/web for 1-3 minutes and switching the theme changes the look of the **whole site**: say so before doing it.

## Tools

`<skill>` is the folder of this file. Requires Python 3.8+ (`python3 --version`; Windows: `py -3 --version`). If Python is missing, install it after telling the user (macOS: `xcode-select --install`; Windows: `winget install -e --id Python.Python.3.12`; Linux: the package manager), or call the APIs in `references/api.md` with `curl` / PowerShell.

```
python3 -I <skill>/scripts/ezylanding.py <command> [--admin-url URL] [options]
```

| Command | What it does |
|---|---|
| `check [--web-url URL]` | admin reachable, EzyLogin CLI login, saved token, web URL (and whether it answers from here), site languages, EzyArticle, EzyPlatform installed on this computer (`local_home`, native or Docker); ends with `READY` or `NEED <code>` |
| `login` / `logout` | EzyLogin CLI login (browser approval) / forget the token |
| `plugins [--theme freestyle] [--lead] [--shop [--delivery]] [names...]` | status of everything the page needs, `ACTION=install/upgrade/activate/none` per item, `TODO=` list |
| `plugin-status <name>` / `plugin-install <name>` | one plugin or theme: status / install or upgrade from the market, install and activate missing dependencies automatically, activate, restart and wait (`--no-restart` to install several and restart once, `--version`, `--paid-ok`) |
| `site-url [--web URL] [--admin URL] [--yes]` | show or set the public web/admin address saved in the admin (Dashboard → Web / Admin); dry run without `--yes` |
| `crm-start [--action start/restart/stop]` | start the EzySupport "Contact Us user creator" job |
| `page-pull <slug> [--dir D] [--lang L]` | download an existing page into a folder |
| `page-push --dir D [--lang L] [--publish] [--yes]` | dry run without `--yes`; with it: back up the server version to `D/.backups/<time>/`, save the default language and every `content.<lang>.html`, print preview and public URLs |
| `page-restore --dir D [--backup P] --yes` | save a backup again (latest by default) |
| `media-upload <files...> [--replace]` | upload to the media library, print the `/api/v1/media/<name>?v=` URL |
| `web-check --path /<slug> [--expect TEXT]` | load public pages, report HTTP errors, unrendered template markers, missing texts |
| `link-check <links...>` | open buy-now links without following redirects (expects a redirect to the cart) |
| `contact-test --email E [--field key=value] --yes` | send one real Contact Us request (real mail) |
| `open --path /p` | open an admin page in the browser |
| `local-install <name>` / `local-restart` | EzyPlatform on this computer only (native or Docker install of the `ezyplatform-install` skill; runs `cli.sh` inside the container for Docker); needs the admin address already given |

Exit code `0` = done, `3` = `NEED <code>: <what to do>`, `1` = error with the reason. **Always pass `--admin-url` on the first command**: it is remembered from then on, and the `local-*` commands refuse to guess it, so they never touch another EzyPlatform on the same computer (for example a developer's install found through `EZYPLATFORM_HOME`). `local_home` is accepted only when its admin port matches the admin address.

## Steps

### 1. Connect

Run `check` and fix what it asks for, in this order, until it prints `READY`:

| NEED | What to do |
|---|---|
| `admin_url` | Ask for the address of their admin (where they sign in to manage the site). |
| `admin_down` | Local install (`local_home` set): `local-restart`. Otherwise ask the user to start EzyPlatform or check the address. |
| `ezylogin_missing` / `ezylogin_outdated` | EzyLogin (free, needs 0.4.1+) lets you sign in. Local (`local_home` set, also Docker): `local-install ezylogin [--update]` + `local-restart`. Otherwise in the admin: **Modules → Add new / Market**, search **EzyLogin**, **Install** (or **Update**), then activate **admin-plugin** and **web-plugin** with **Restart**. A fresh Docker image has no plugin at all, not even EzyArticle. |
| `admin_cli_login_disabled` | Open `<admin>/ezylogin/settings/regular`, tick **Allow admins to sign in from the command line (CLI)** (VI: **Cho phép quản trị viên đăng nhập từ dòng lệnh (CLI)**), **Save**. |
| `login` | Tell the user a browser page opens, they sign in if asked, check the tool name *AI landing page builder*, click **Approve**. Run `login` (waits up to 10 minutes). No browser (`BROWSER_OPENED=no`): give them the `OPEN_URL` to open on the same computer. |
| `plugin_permission`, `content_permission` | The approved account lacks rights: approve with a super admin (`logout`, `login`) or ask for the permissions. |
| `paid_plugin` | Never buy for the user. Explain the price and ask. |

Run `check` again after each fix until it prints `READY`.

If `check` prints `WARNING: the web URL saved in the admin does not answer` (typical for Docker, where the admin saved `http://localhost:8080` but the site is published on another port, or a site behind a proxy), find the real public address (for the `ezyplatform-install` skill: `RESULT_WEB_URL`), tell the user, and fix the setting with `site-url --web <address>` then `--yes`. Until then the admin preview redirects to a dead address. For a read-only check without changing the site use `check --web-url <address>`.

### 2. Interview

Load `references/interview.md` now and follow it. Ask **one group at a time**, give examples and a suggested answer, summarize what you understood before moving on. Keep the answers in `landing-pages/<slug>/brief.md` (local only, never uploaded) so work can continue in another session.

1. **The page**: what it is about, its goal, audience, the one action a visitor must take, slug, languages.
2. **Sections and features**: propose an outline from the goal; the user ticks, removes, adds.
3. **Lead form**: yes/no, which fields, who receives the notification, thank-you mail, CRM. → step 4.
4. **Product links**: yes/no, which products (codes), quantities, variants, discount code, physical or digital. → step 5.
5. **Logo and identity**: has a logo → use it; no logo → brand brief. → step 6.
6. **Content**: images, texts, contact details, social links, legal pages.

After groups 1-2, show the outline (sections in order, the call to action of each) and get a "yes" before going on.

### 3. Theme and plugins

```
python3 -I <skill>/scripts/ezylanding.py plugins --theme freestyle [--lead] [--shop [--delivery]]
```

- `--lead` when the page has a form (EzySupport, EzyMail); `--shop` when it sells (E-Commerce, GraphQL, EzyLogin, EzyPayment); `--delivery` for physical goods (EzyDelivery).
- For each item in `TODO`, tell the user what it is for and that the site restarts, then `plugin-install <name>` one by one and `plugins ...` again until `TODO=none`. All of them are free on the market today; if one has a price, ask first.
- **Theme:** if the site already has an active theme the user likes, ask before installing/activating Freestyle (it replaces the look of every page). A standalone page carries its own design, so it works on the current theme too; Freestyle is recommended for new sites. Check `<admin>/themes` afterwards.
- Plugins depend on others (EzyDelivery needs Accounting...): `plugin-install` installs and activates missing dependencies itself. To install many, run `plugin-install <name> --no-restart` for each and leave the restart for the last one.
- GraphQL publishes its schema only when **GraphQL → Settings → GraphQL docs** is on (otherwise `/api/v1/graphql/schema.graphql` answers 404).
- If the account cannot install, do it in the admin (**Modules → Add new / Market** → Install, then activate the module types with **Restart**) through the browser or by guiding the user.

### 4. Lead form → EzySupport (only if wanted)

- Map fields to the Contact Us API (`POST /api/v1/contact-us`, JSON): name → `contactUsYourName`, email → `contactUsYourEmail`, phone → `contactUsYourPhoneNumber`, topic/package → `contactUsSubject`, message → `contactUsMessage`. Name, email, subject and message are **required** by the API: if the user does not want a subject or message field, send a fixed subject (`Landing <slug>`) and build the message from the other answers.
- Any other field (company, budget, product interest, `utmSource`, `utmCampaign`, `landingPage`...) is sent at the same level in the body and is stored **only** if listed in **EzySupport → Settings → Accepted Contact Us Metadata Keys** (comma separated, case-sensitive; other keys are silently dropped). Always add hidden `landingPage=<slug>` and UTM fields from the URL so the owner knows where leads come from.
- In **EzySupport → Settings** (`open --path /ezysupport/settings`), do yourself or guide: tick **Allow contact** (otherwise the API answers 404), fill **Supporter Emails** (who gets notified), tick **Allow contact response email** if the visitor should get a thank-you mail, add the metadata keys, **Save**.
- **CRM:** run `crm-start` (or on the same page, row **Contact Us user creator**, VI: **Trình tạo người dùng từ liên hệ**, click **Start**; the page has several similar Start buttons, use the right row). It turns every lead into a user (no role, display name `[Contact us]<name>`, email, phone) and links the message to it, so leads appear in the user list and CRM tools. Explain this to the user and get their OK.
- **Mail:** EzyMail sends nothing until a mail service is set up (fresh installs fail silently). Ask the user to fill **EzyMail → Settings** (SMTP host, port, user, password or a provider like Resend) themselves; never type credentials for them. Mail texts are the templates `contact_us_notification` and `thanks_for_contacting_us` in **EzySupport → Templates**; offer to translate them.
- **Spam:** suggest captcha: **EzySupport → Captcha settings**, set a default service (*Proof of work* needs no account), tick `POST /api/v1/contact-us`, save; then the page loads `<script src="/ezysupport/js/captcha.js"></script>` before `</body>`.
- Form code: see `references/page-patterns.md` (validation, `204` = success, errors `{"<field>":"required|invalid|overLength"}` with status 200 or 400, button disabled while sending, fallback phone/email link).

### 5. Product links → E-Commerce (only if selling)

- The shop must be ready before links work: active default currency, country data, a default store with a bank account, payment service configured, products **published**.
- Visitors who are not signed in can only buy if **EzyLogin → Regular settings → Allow anonymous users** (VI: **Cho phép người dùng ẩn danh**) is on, or they sign in first. Otherwise every buy link answers `403 {"createAnonymous":"forbidden"}`. Ask the user which they want; for a landing page anonymous buying is usually expected.
- A discount code must exist, be `ACTIVATED`, valid now, and have **targets** (the products or categories it applies to, in the voucher's targets). Without targets the cart shows the code but says *Not found* (`{"voucherTarget":"notFound"}`). If not, send the user through the E-Commerce quick start (`https://ezyplatform.com/market/items/ecommerce/docs/bat-dau-nhanh`) and help with each step in the admin; do not fake it.
- Ask for product **codes** (in **E-Commerce → Products**), not display names. Links:
  - one product: `/products/<code>/checkout?quantity=2&colorName=<c>&sizeName=<s>&materialName=<m>&discountCode=<CODE>&clearShoppingCart=true`
  - several: `/products/checkout?productCodes=a,b&productQuantities=1,2&productColorNames=...&productSizeNames=...&productMaterialNames=...&discountCode=<CODE>` (every list in the order of `productCodes`)
  - all parameters optional; variant values are the variant codes; URL-encode accents and spaces.
- Prices and names: GraphQL gives the site an API automatically (schema at `<web>/api/v1/graphql/schema.graphql`; docs at `<web>/graphql/schema` when enabled in **GraphQL → Settings**). Read the schema and fetch name, price and image on the page so they never drift from the shop. If it is not available, write them in the page and tell the user they must update the page when prices change.
- `link-check` every buy link before publishing: `ok redirect 302 -> /checkout/shopping-cart` is good, `http_403` is the anonymous-buy setting, `http_404` a wrong or unpublished product code. Then open one link in a browser and check the cart (products, quantities, the discount actually applied, not just the code shown).

### 6. Brand identity

- **Has a logo:** ask for the file (SVG best, else PNG with transparent background) and variants (square icon, horizontal, white for dark backgrounds). Take the palette from it (primary, accent, neutral, dark background), propose a heading font and a body font (Google Fonts with Vietnamese support when the page is in Vietnamese), show hex codes and a short description of the style, and get a yes.
- **No logo:** run the brand brief in `references/interview.md` (from chapter 7 of the EzyPlatform vibe-coding book: https://ezyplatform.com/blog/chuong-7-thiet-ke-giao-dien-bang-ai). At minimum fix **brand name, brand personality, main color**. Then propose palette, style and a logo concept, and give the user a ready-to-paste prompt for an image tool (combination mark, transparent background, square, plus icon / horizontal / white variants). Draw a simple SVG wordmark yourself only if the user wants a temporary logo, and say it is temporary.

### 7. Build

1. Folder `landing-pages/<slug>/` with `content.html` and `meta.json`:
   ```json
   {"slug": "<slug>", "title": "<SEO title>", "summary": "<meta description>", "pageType": "STANDALONE_PAGE", "contentType": "HTML", "status": "DRAFT"}
   ```
   Use `"contentType": "THYMELEAF"` only if you use `th:*` / `ezy:*`.
2. `content.html` is a **complete HTML document** (`<!doctype html>`, `<html lang dir>`, `<head>` with charset, viewport, title, description, Open Graph, favicon, fonts, `<style>`; `<body>` with the sections and `<script>`). Patterns and checklist: `references/page-patterns.md`.
3. Images: rename to English without accents or spaces, `media-upload` them. Use PNG, JPG or WebP: by default EzyPlatform rejects SVG (`{"fileType":"invalid"}`, it is not in the accepted media types), and social networks do not show SVG as `og:image` (make a 1200×630 PNG/JPG). The server stores the file under a hash name; both the printed hash URL and `/api/v1/media/<original name>` work. No base64 images except tiny icons.
4. Other languages: `content.<lang>.html` (+ `meta.<lang>.json` with translated title/summary), same structure, IDs and classes, translated text only.
5. Quality: mobile first (no horizontal scroll at 360 px), light/dark if the brand allows, contrast ≥ 4.5:1, works right-to-left (logical CSS properties), `prefers-reduced-motion`, one primary call to action repeated (hero, middle, end, sticky on mobile), fast (lazy images, few fonts).

### 8. Save, check, publish

```
python3 -I <skill>/scripts/ezylanding.py page-push --dir landing-pages/<slug>          # dry run, show the plan
python3 -I <skill>/scripts/ezylanding.py page-push --dir landing-pages/<slug> --yes    # save as draft
```

- Open `RESULT_PREVIEW` (admin preview) for the user, or look yourself with browser tools: desktop and 375 px, `?lang=<each language>`, light/dark, console errors. Iterate (edit, `page-push --yes` again).
- When the user approves: `page-push --dir landing-pages/<slug> --publish --yes`, then `web-check --path /<slug> --expect "<hero headline>"`, `link-check` the buy links, and, with the user's OK and an inbox they control, `contact-test --email <inbox> --field landingPage=<slug> --yes` (or submit the real form in the browser when captcha is on). Check the request in **EzySupport → Contact Us** and, if the user creator runs, the new user in **Users**.
- Something wrong after publishing: `page-restore --dir landing-pages/<slug> --yes`.

### 9. Own domain (optional, EzySupport)

Ask: "Bạn có muốn landing page chạy trên tên miền riêng (ví dụ `kairowatch.vn`) không?" This needs a server (VPS) with a public IP running EzyPlatform, with EzySupport installed; Nginx and Certbot can be installed from the EzySupport pages. It does not apply to EzyPlatform on a laptop. Follow the EzySupport guide (`https://ezyplatform.com/market/items/ezysupport/docs/huong-dan-su-dung-tinh-nang-cai-dat-ten-mien-voi-ezysupport`):

1. **DNS** (the user does it at their domain registrar; never ask for their registrar password): an **A** record `@` → server IP for the site, an **A** record `admin` → server IP for the admin. Wait about 5 minutes; check with `nslookup <domain>` (or `dig +short <domain>`) until it returns the server IP.
2. **Addresses**: `site-url --web https://<domain> --admin https://admin.<domain>` (dry run, then `--yes`).
3. **Nginx** (admin, **EzySupport → Load balancing → Nginx**): install Nginx there if it says it is missing; in **Main domain configuration** click **Save** for the admin domain and the web domain (the generated config is usually right), then **Check** (must show no error) and only then **Reload**. `http://<domain>/<slug>` now works.
4. **SSL**: **EzySupport → Load balancing → Certbot**: install Certbot if missing, fill the contact email, **Save**; back on the Nginx page click **Install SSL** for each domain. Only after DNS points to the server and Nginx was reloaded, otherwise Certbot cannot verify the domain.
5. **A separate domain only for the landing page** (e.g. `kairowatch.vn` while the main site uses another domain): add it under **Extra domain configuration → Add**, Save, Check, Reload, Install SSL. To open the landing page at the root of that domain, ask the user first, then in that domain's Nginx config add `location = / { return 302 /<slug>; }` before the main `location /`, Check, Reload. Never change the main domain's config this way.
6. Verify: `check` (web URL answers), `web-check --path /<slug>`, open `https://<domain>/<slug>` and the admin over HTTPS, `link-check` the buy links again.

Reloading Nginx with a broken config takes the whole site down: always **Check** before **Reload**, and keep the previous config text so it can be pasted back.

## Report to the user

In their language, simply: the page address (and domain, if set up), the sections, what the form collects and where leads go (notification emails, EzySupport → Contact Us, users/CRM), the buy links, the plugins/theme installed, the switches still to flip in the admin (mail service, payment, captcha, user creator) with where to find them, placeholders still to replace, what was tested, and that the previous version is backed up and can be restored. Do not paste code, tokens or logs unless asked.
