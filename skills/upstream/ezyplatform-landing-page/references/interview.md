# Interview: questions to ask before building

Ask one group per message. For each question give 2-4 examples or a suggested answer the user can accept with "ok". Skip what the user already told you. Write the answers into `landing-pages/<slug>/brief.md` as you go (headings = groups below).

## 1. The page

1. What is this landing page about? (a product, a service, a course, an event, an app, a launch, a promotion...)
2. What is it for, the one goal? (collect leads / sell directly / sign-ups for an event or webinar / app downloads / pre-orders / bookings)
3. Who is it for? (age, job, where they live, what problem they have, what they want)
4. What single action must a visitor take? (fill the form, click "Buy now", call, message on Zalo/Messenger, download). This becomes the main button text.
5. Why should they choose you rather than others? 3 main benefits or differences.
6. Address: suggest a slug from the topic (`khoa-hoc-ai-co-ban`, `black-friday-2026`); English or Vietnamese without accents, no spaces.
7. Languages: only the site's default language, or also others? (`check` prints `web_languages`)
8. Deadline or campaign dates? (needed for a countdown or "offer ends" text)

## 2. Sections and features

Propose an outline that fits the goal, then let the user tick, remove or add:

| Goal | Suggested sections |
|---|---|
| Leads | hero with form or button to form, problem → solution, benefits, how it works, social proof, FAQ, final form, footer with contact |
| Sell | hero with product image + price + Buy now, benefits, details/specs, packages or variants, reviews, guarantee/shipping/returns, FAQ, final Buy now |
| Event | hero with date/place + Register, agenda, speakers, countdown, venue/map, FAQ, registration form |

Features to offer: sticky call-to-action bar on mobile, countdown, video (YouTube embed), image gallery/slider, pricing table, comparison table, testimonials, FAQ accordion, floating Zalo / Messenger / phone buttons, map, social links, analytics (Google Analytics / Facebook Pixel through EzySupport), cookie notice.

## 3. Lead / contact form (EzySupport)

1. Do you want a form to collect customer information? (yes / no)
2. Which fields? Offer: full name*, email*, phone, company, job title, city, budget, product/package of interest, preferred contact time, message. (* the API requires name and email; subject and message are filled automatically if the user does not want them visible)
3. Which fields are required?
4. Who receives a notification email for each new lead? (one or more addresses)
5. Should the visitor get a thank-you email? What should it say?
6. After submitting, show a thank-you message on the page or open another page?
7. Do you want every lead to become a customer record (user) for CRM/customer care? (explain: EzySupport creates a user per email automatically, without admin rights)
8. Anti-spam: OK to turn on captcha? (invisible "proof of work", no account needed)
9. Consent text for personal data (e.g. "I agree to be contacted...")? Link to a privacy page?

## 4. Product links (E-Commerce)

1. Do you sell products/services directly on this page? (yes / no)
2. Which products? Their **codes** in E-Commerce → Products (show the user where to find them). Not created yet → help create them first.
3. For each: default quantity, color/size/material variant (variant codes), one product per button or a bundle of several products?
4. A discount code to pre-fill? (must exist and be valid in E-Commerce → Vouchers)
5. Should the link empty the visitor's current cart first? (`clearShoppingCart=true`)
6. Physical goods (needs shipping, EzyDelivery) or digital/service?
7. Is the shop ready: currency, store, bank account, payment service (VNPAY, PayPal, PAYFS, PAY2S...)? If not, plan these steps with the user.
8. Show price from the shop automatically (GraphQL) or fixed text?

## 5. Logo and brand identity

First ask: **Do you already have a logo?**

### 5a. Has a logo

1. Send the logo file (SVG best, else PNG with transparent background, large).
2. Do you have variants: square icon (favicon), horizontal (header), white (dark backgrounds)?
3. Brand colors and fonts already defined (brand guide)? If yes, use them exactly.
4. If not: propose a palette taken from the logo (primary, accent, neutral, dark background, as hex), a heading font and a body font, a style in 3 words; ask for a yes.
5. Light only, dark only, or follow the visitor's system setting?

### 5b. No logo yet: brand brief

From chapter 7 "Thiết kế giao diện bằng AI" of the EzyPlatform vibe-coding book (https://ezyplatform.com/blog/chuong-7-thiet-ke-giao-dien-bang-ai). The user does not have to answer everything, but **brand name, brand personality and main color** are required before designing.

**Business**
1. History: how many years, size, number of staff?
2. Mission and vision: what problem does it solve, what does it want to become?
3. Field: main products or services?

**Brand**
4. Identity goal: what should the brand convey (smart, friendly, trustworthy...)?
5. Brand name and its meaning / origin.
6. Slogan (if any) and its meaning.
7. Brand message: the one sentence customers should remember.
8. Brand personality: up to 5 adjectives, most important first.
9. Differentiation (USP): how is it different from competitors?
10. Segment: budget, mid-range, premium or luxury?

**Target customers**
11. Demographics: gender, age, where they live, job.
12. Insight: what they want when using the product/service.
13. Why they choose you over competitors.

**Competitors**
14. Domestic competitors: names and their brand look.
15. Foreign competitors: names and their brand look.

**Identity design**
16. Logo type: symbol + text (combination mark), text only (logotype), or mascot + text?
17. Where it will be used: website, events, printed material, social media?
18. Brand colors: suggested colors and why.
19. Images or symbols wanted in the logo and their meaning.

Then:

- Propose palette (hex), style (e.g. "warm minimal", "modern tech", "playful") and a logo concept; get a yes.
- Give the user a prompt for an image tool (ChatGPT, Ideogram, Midjourney...), filled with their answers, for example: *"Design a combination-mark logo for '<brand>', <field>. Symbol: <idea>. Style: <style>, flat, simple, readable at small size. Colors: <hex list>. Font: <serif/sans/script feel>. Transparent background, square 1:1."* Then ask for variants: square icon only (favicon), horizontal (header), all white (dark backgrounds).
- Most image tools give PNG/JPG: ask for the largest size with transparent background; for SVG use a vectorizer.
- File names in English, no accents or spaces (`<brand>-logo-square.png`, `<brand>-logo-horizontal.svg`).

## 6. Content

1. Main headline and sub-headline (offer to write 3 options from the brief).
2. Texts for each section: the user's own, or you draft from the brief and they review. Never invent facts, numbers, testimonials or partner logos.
3. Images: product photos, team, customers, background. Their own files, or royalty-free stock (say where from), or AI-generated (say so). Ask for the right to use people's photos and testimonials.
4. Video link (YouTube)?
5. Contact details shown on the page: phone, Zalo, email, address, opening hours, map.
6. Social links: Facebook, TikTok, YouTube, Instagram, LinkedIn...
7. Legal: company name, tax code, privacy policy and terms links (required in some countries for collecting personal data and selling online).
8. Tracking: Google Analytics / Facebook Pixel / TikTok Pixel IDs (configured in EzySupport, not pasted into the page when possible).

## 7. Domain (optional)

1. Should the page run on your own domain? Which one (`example.com`, or a separate domain only for this page such as `kairowatch.vn`)?
2. Do you already own the domain and can you log in to the registrar to add DNS records?
3. Does the site run on a server (VPS) with a public IP? (a laptop install cannot get a public domain this way)
4. Should the domain root open the landing page directly, or the main site with the page at `/<slug>`?
5. Which email should receive SSL certificate notices (Certbot contact email)?
