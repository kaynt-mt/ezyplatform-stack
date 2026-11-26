# UI/UX guidelines for EzyPlatform apps

Use the host interface for navigation, identity and theme. Build app-specific workflows inside it. These guidelines apply to Admin and Web; the two surfaces do not have to look identical.

## Design approval gate

Do not build any UI (app, plugin, Admin theme) before the project owner approves a **full detailed design**. The more complete the design, the faster the build and the fewer the rebuilds.

The design must include:

- **Every screen** with its mockup, not only the main ones.
- **Every UI element with its states**: controls, tables, forms and dialogs in default, hover/active, loading, empty, no-results, error, and permission-denied states where they apply.
- **Every flow** end to end: navigation between screens, form submission and validation, create/edit/delete cycles, and the irreversible-action confirmations.
- **The feature toggle list**: which features are turned on or off, so the owner can approve what is built and what is deliberately left out.

Research documents, comparison notes, or a chosen design direction are not an approved design — they inform one. The owner approves the mockups and the toggle list before implementation starts.

## Choose the surface and extension point

| Surface | Put here | Start with |
| --- | --- | --- |
| **Admin** (local :9090) | Installation, site-wide configuration, operator diagnostics and privileged maintenance. | A namespaced Admin plugin view using Thymeleaf and `layout:decorate="~{ezyadmin}"`. Fill its `content` slot and follow neighboring Admin pages for headers, cards, tables, forms and modal/script slots. Use the SDK menu registration convention (`menus.properties`) for Admin navigation. |
| **Web** (local :8080) | Public discovery where applicable, signed-in customer/member workflows and user-owned settings. | Namespaced Web plugin pages/fragments composed into the active theme where supported. The SDK theme uses Thymeleaf, `ezytheme` and a `content` fragment; check the target theme's actual hooks, dimensions, assets and login adapter before relying on them. Use a separate Web theme only when the whole site needs its own presentation; only one theme is active. |

The Admin shell bundles AdminLTE 3, Bootstrap 4 and jQuery. Reuse its controls and spacing instead of adding another Bootstrap, icon bundle, sidebar or modal runtime. That dependency set is **not** a Web contract. Scope app CSS, IDs, storage keys and JavaScript to the app; load assets only on pages that need them. Don't modify core templates for an individual app. Site-wide Admin branding is a separate choice; use the [Admin customization skill](../skills/upstream/ezy-admin-customize/SKILL.md) when that is the requested surface.

Admin identities and Web identities are separate. An Admin menu entry, hidden Web button or theme login is not authorization: enforce access on the server for each view and action, including search, counts, exports and autocomplete. Never show private object names or metadata in navigation, errors or empty states to users without access.

## Make routine work predictable

- **Layout and navigation:** Keep host chrome, one clear page heading and one obvious primary action. Put scope before actions (for example, workspace → project → item) and highlight the current section. Use distinct, linkable URLs for destinations; use browser Back to restore list context. Keep task navigation inside the Web content area, not in a second global shell. On small screens, collapse secondary navigation into a labeled control and stack the toolbar.
- **Tables, lists and boards:** Use native table semantics for tabular data and real links for detail; do not turn a whole row into the only target. Show meaningful fields first and keep action names clear. Keep filters (which records) separate from display options (how they appear); make applied filters visible and easy to clear. Paginate on the server with stable ordering; keep search, filters and sort in the URL where useful. On narrow screens use a simpler list or a labeled scroll region for genuinely two-dimensional data; do not make the entire page scroll horizontally.
- **Forms and dialogs:** Label each control, identify required fields in text and show errors next to fields plus a summary on long forms. Keep entered values after failures. Use specific verbs (for example, **Save settings**) and show scope and consequences before irreversible actions. Give dialogs accessible names, move focus in, contain it while modal, and return it to the trigger or a logical successor. Use a full page for long or multi-step forms.
- **Feedback and recovery:** Distinguish first-run emptiness (explain and offer a permitted next action), no filter matches (clear or edit filters), no access (follow disclosure policy), loading, stale data and failure (retry or reload). Announce meaningful asynchronous changes without stealing focus. Do not use disappearing toasts as the only error channel. While saving, prevent duplicate submissions; on conflict, preserve the draft and offer to reload the current version.
- **Performance:** Render a useful first screen with server templates where feasible. Bound list/column queries and payloads; defer secondary details, avoid loading every record for filters, and debounce remote search when applicable. Check a realistic data volume on the target theme and a slower connection; verify that late responses cannot overwrite newer state.

## Accessibility, localization and appearance

- Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/). Check keyboard-only operation and screen-reader names, order and announcements; provide visible focus that sticky bars or overlays cannot cover. Provide a non-drag pointer action and a keyboard path for every drag operation. Do not introduce global single-character shortcuts unless they can be turned off, remapped or are active only on focus.
- Aim for targets at least 24 × 24 CSS pixels (or meet the WCAG spacing/other exceptions); prefer larger touch controls. Check contrast for text (4.5:1 for normal text, 3:1 for large text) and required control boundaries or state indicators (3:1). Use text or shape as well as color for status. Check 200% text resize and reflow at 320 CSS pixels, allowing the standard exceptions for inherently two-dimensional content.
- Use the module's existing `src/main/resources/messages/messages*.properties` bundles and Thymeleaf message keys. Localize validation, empty states, accessible names and JavaScript through the host's message helper (for example, Admin's `ezyadmin.messages`); don't assume Web themes share one JS API. Format dates, times and numbers by locale, make time zone semantics explicit, and test English and Vietnamese. Allow labels to wrap; use logical CSS properties and test RTL when supported.
- Match host light/dark behavior rather than forcing a per-page theme. If a host supports both, verify foregrounds, borders, badges, focus, tables and dialogs in both. Start with comfortable density; add compact modes only where repeated scanning warrants them, without shrinking click targets or hiding essential information. Respect reduced-motion preferences for optional animation.

## UI PR review checklist

- [ ] The intended operator or Web user can complete the main task in the pinned runtime, theme and login configuration. The app reuses the host shell; module assets don't affect other pages.
- [ ] Labels, empty/no-results states, loading, validation and recovery are clear. Authorization is checked server-side with permitted and denied identities on the correct surface.
- [ ] Tab order, focus restoration, visible focus, zoom/reflow, contrast and non-drag actions are checked. Test a narrow viewport, supported color modes and English/Vietnamese.
- [ ] Filter/sort/deep-link state survives navigation as designed, with bounded data requests and no regressions to the host navigation or login.
- [ ] Evidence names the runtime and theme and includes changed screens in relevant states (not just a successful build or an HTTP response). For Java plugins, use the [build and Docker verification skill](../skills/ezy-build-plugin/SKILL.md).

Platform references: [Admin layout and bundled helpers](../skills/upstream/ezy-admin-customize/references/admin-layout.md), [theme and plugin development](../skills/upstream/ezy-develop/SKILL.md), [localization skill](../skills/upstream/ezy-i18n/SKILL.md), and the [EzyPlatform Guide index](research/ezyplatform-guide-inventory.md#http-ui-localization-and-authentication).
