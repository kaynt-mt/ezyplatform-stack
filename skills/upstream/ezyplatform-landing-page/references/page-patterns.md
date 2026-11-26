# Page patterns for a standalone landing page

## Skeleton

`content.html` is the whole document: the platform does not add the site header, footer or theme CSS around a `STANDALONE_PAGE`.

```html
<!doctype html>
<html lang="vi" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Title with the main keyword | Brand</title>
  <meta name="description" content="150-160 characters that make people click">
  <meta property="og:type" content="website">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="/api/v1/media/<brand>-og-1200x630.jpg?v=1">
  <link rel="icon" href="/api/v1/media/<brand>-logo-square.png?v=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root { --primary: #...; --accent: #...; --bg: #...; --text: #...; --muted: #...; --radius: 14px; }
    @media (prefers-color-scheme: dark) { :root { --bg: #...; --text: #...; } }
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; font-family: 'Be Vietnam Pro', system-ui, sans-serif; background: var(--bg); color: var(--text); }
    .container { max-width: 1120px; margin-inline: auto; padding-inline: 16px; }
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; scroll-behavior: auto !important; } }
  </style>
</head>
<body>
  <header>...logo + one anchor button to the form / buy section...</header>
  <main>
    <section id="hero">...</section>
    ...
    <section id="contact">...form...</section>
  </main>
  <footer>...contact, social, legal links...</footer>
  <script>...</script>
</body>
</html>
```

- Absolute URLs are not needed: media is `/api/v1/media/<name>?v=<n>`; bump `v` after replacing a file.
- Keep CSS and JS in this file unless they are large (> 100 KB): then upload `landing-<slug>.css/js` with `media-upload` and link them.
- Use logical properties (`margin-inline`, `padding-inline`, `inset-inline-start`, `text-align: start`) so the page also works with `dir="rtl"`. User-typed text in inputs: `unicode-bidi: plaintext`.
- Images: `width`/`height` attributes, `loading="lazy"` except the hero image, `alt` text in the page language. Hero image ≤ 300 KB (WebP/JPG), logo SVG or PNG.
- Do not load jQuery or big frameworks for a landing page; plain JS is enough.

## Lead form

```html
<form id="lead-form" novalidate>
  <label>Họ tên* <input name="contactUsYourName" required maxlength="120" autocomplete="name"></label>
  <label>Email* <input name="contactUsYourEmail" type="email" required autocomplete="email"></label>
  <label>Số điện thoại <input name="contactUsYourPhoneNumber" type="tel" autocomplete="tel"></label>
  <label>Gói quan tâm
    <select name="contactUsSubject"><option>Gói cơ bản</option><option>Gói nâng cao</option></select>
  </label>
  <label>Lời nhắn <textarea name="contactUsMessage" maxlength="6000"></textarea></label>
  <input type="hidden" name="landingPage" value="<slug>">
  <label><input type="checkbox" name="consent" required> Tôi đồng ý được liên hệ ...</label>
  <button type="submit">Nhận tư vấn</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
<script>
(function () {
  var form = document.getElementById('lead-form');
  if (!form) return;
  var status = form.querySelector('.form-status');
  var button = form.querySelector('button[type="submit"]');
  var params = new URLSearchParams(location.search);
  ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) {
    if (params.get(k)) {
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = k.replace(/_([a-z])/g, function (m, c) { return c.toUpperCase(); });
      input.value = params.get(k);
      form.appendChild(input);
    }
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = Object.fromEntries(new FormData(form));
    delete data.consent;
    if (!data.contactUsSubject) data.contactUsSubject = 'Landing <slug>';
    if (!data.contactUsMessage) data.contactUsMessage = 'Đăng ký từ landing page <slug>';
    button.disabled = true;
    status.textContent = 'Đang gửi...';
    fetch('/api/v1/contact-us', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (res) {
      return res.text().then(function (text) {
        var body = {};
        try { body = text ? JSON.parse(text) : {}; } catch (err) { body = {}; }
        if (res.status === 204 || (res.ok && !Object.keys(body).length)) {
          form.reset();
          status.textContent = 'Cảm ơn bạn! Chúng tôi sẽ liên hệ sớm.';
          return;
        }
        if (res.status === 404) throw new Error('disabled');
        var names = Object.keys(body);
        status.textContent = names.indexOf('captchaToken') >= 0
          ? 'Xác minh chống spam thất bại, vui lòng thử lại.'
          : 'Vui lòng kiểm tra lại: ' + names.join(', ');
      });
    }).catch(function () {
      status.textContent = 'Không gửi được. Vui lòng gọi <phone> hoặc email <email>.';
    }).finally(function () {
      button.disabled = false;
    });
  });
})();
</script>
```

- Field names above are fixed by the API. Extra fields (here `landingPage`, `utmSource`, `utmMedium`, `utmCampaign`) are stored only if listed in **EzySupport → Settings → Accepted Contact Us Metadata Keys**.
- Limits: name ≤ 120 chars, subject ≤ 300, message ≤ 6000, no `<script>`/`<iframe>` in subject/message, phone must be a valid number if sent (send nothing rather than an empty or invalid value).
- Success = `204` with an empty body. Errors = `{"<field>":"required|invalid|overLength"}` with status 400 (some sites answer 200): check both. `404` = Contact Us is turned off in EzySupport settings.
- With captcha on, add `<script src="/ezysupport/js/captcha.js"></script>` before `</body>`; it adds the `X-Captcha-Token` header to the `fetch` automatically.
- Show field errors next to the fields in the page language; never show raw JSON.

## Buy buttons

```html
<a class="btn btn-primary" href="/products/<code>/checkout?quantity=1&discountCode=<CODE>">Mua ngay</a>
<a class="btn" href="/products/checkout?productCodes=<a>,<b>&productQuantities=1,1">Mua combo</a>
```

- The link adds the products to the cart and redirects to `/checkout/shopping-cart`; visitors who are not signed in may be asked to sign in or buy anonymously, depending on EzyLogin settings.
- Prices from GraphQL: read `<web>/api/v1/graphql/schema.graphql` first, write the query from the real schema (do not guess field names), call it from the page with `fetch('/graphql', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({query, variables})})`, and keep a fixed fallback text so the page still reads well if the call fails.

## Checklist before showing the user

- Hero answers in 5 seconds: what it is, for whom, why, what to do (one button).
- Main call to action visible without scrolling on mobile and repeated after key sections.
- No horizontal scroll at 360 px; tap targets ≥ 44 px; text ≥ 16 px on mobile.
- Contrast ≥ 4.5:1 for text, 3:1 for buttons and inputs borders.
- Every image has `alt`; headings in order (one `h1`).
- Form: labels, required marks, keyboard usable, clear success and error messages, button disabled while sending.
- Title, description, Open Graph image (1200×630), favicon.
- No placeholder left unless the user knows (list them in the report).
- No console errors; works with JavaScript errors in one section (guard every query).
