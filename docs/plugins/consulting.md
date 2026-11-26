# consulting

Consulting: customers, staff, documents, and a dedicated theme.

- **Marketplace version on core 1.5.9:** `0.1.6`.
- **Verified modules:** `admin-plugin`, `web-plugin`, `theme`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/consulting` | `org.youngmonkeys.consulting` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezylogin](ezylogin.md), [ezyoa](ezyoa.md) |
| `web-plugin` — `web/plugins/consulting` | `org.youngmonkeys.consulting` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezylogin](ezylogin.md), [ezyoa](ezyoa.md), [ecommerce](ecommerce.md), [ezycrm](ezycrm.md) |
| `theme` — `web/themes/consulting` | `org.youngmonkeys.consulting` | [ezyarticle](ezyarticle.md), [ezysupport](ezysupport.md), [ezylogin](ezylogin.md), [ezyaccount](ezyaccount.md), [ezyoa](ezyoa.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 4 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /branches` | `AdminBranchController` |
| `GET /customers` | `AdminCustomerController` |
| `GET /employees` | `AdminEmployeeController` |
| `GET /team-members` | `AdminTeamMembersController` |

**web-plugin** — 11 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `HomeController` |
| `GET /history` | `ServiceController` |
| `GET /services` | `ServiceController` |
| `GET /documents` | `DocumentController` |
| `GET /api/v1/documents` | `WebApiDocumentController` |
| `GET /api/v1/consultations/history` | `WebApiConsultationController` |
| `GET /faqs/{slug}` | `FaqController` |
| `POST /api/v1/services/{id}/consultation/register` | `WebApiConsultationController` |

**theme** — 11 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /` | `HomeController` |
| `GET /history` | `ServiceController` |
| `GET /services` | `ServiceController` |
| `GET /documents` | `DocumentController` |
| `GET /api/v1/documents` | `WebApiDocumentController` |
| `GET /api/v1/consultations/history` | `WebApiConsultationController` |
| `GET /faqs/{slug}` | `FaqController` |
| `POST /api/v1/services/{id}/consultation/register` | `WebApiConsultationController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `consulting: /`, `customers: /customers`, `employees: /employees`, `members: /team-members`, `branches: /branches`, `page_fragments: /pages/fragments` (+1).

- **theme – Template:** `about-us.html`, `consultations/history.html`, `contact-us.html`, `documents/details.html`, `documents/index.html`, `faqs/details.html`, `faqs/index.html` (+27).

- **theme - Resources:** `css/main.css`, `js/jquery.hoverdir.js`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `consulting-admin-plugin-0.1.6.jar`, `consulting-sdk-0.1.6.jar`; 12 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.consulting.admin.controller.view`, `org.youngmonkeys.consulting.admin.config`, `org.youngmonkeys.consulting.constant` (+1).
- **Controllers, services, and repositories (sample):** `AdminBranchController`, `AdminConsultingHelpController`, `AdminConsultingPageFragmentController`, `AdminCustomerController`.
- **Configuration and permission classes (sample):** `AdminConsultingPostConfig`, `AdminDocumentProductConfig`, `AdminPageFragmentConfig`, `PageFragmentConfig`.

### web-plugin

- **JARs inspected:** `consulting-sdk-0.1.6.jar`, `consulting-web-plugin-0.1.6.jar`; 24 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.consulting.web.controller.view`, `org.youngmonkeys.consulting.web.controller.api`, `org.youngmonkeys.consulting.web.view` (+11).
- **Controllers, services, and repositories (sample):** `ApiConsultingNewsController`, `ConsultationController`, `DocumentController`, `FaqController`, `WebConsultationHistoryControllerService`, `WebConsultationValidator`, `WebDocumentService`.
- **Configuration and permission classes (sample):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Potential extension points based on class names:** `ConsultingGlobalErrorHandler`, `ConsultingGlobalExceptionHandler`, `WebConsultationViewFactory`.

### theme

- **JARs inspected:** `consulting-sdk-0.1.6.jar`, `consulting-theme-0.1.6.jar`, `consulting-web-plugin-0.1.6.jar`; 35 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.consulting.web.controller.view`, `org.youngmonkeys.consulting.web.controller.api`, `org.youngmonkeys.consulting.web.view` (+11).
- **Controllers, services, and repositories (sample):** `ApiConsultingNewsController`, `ConsultationController`, `DocumentController`, `FaqController`, `WebConsultationHistoryControllerService`, `WebConsultationValidator`, `WebDocumentService`.
- **Configuration and permission classes (sample):** `PageFragmentConfig`, `WebPageFragmentConfig`.
- **Potential extension points based on class names:** `ConsultingGlobalErrorHandler`, `ConsultingGlobalExceptionHandler`, `WebConsultationViewFactory`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/consulting/customers` showed a user list; Web `/api/v1/documents` returned 200. The Consulting theme rendered `/services` and `/documents`.

## Integration notes

Keep business modules separate from theme templates. A redirect to core CRUD that returns HTTP 200 does not prove the plugin has its own screen.

[Back to the plugin index](README.md)
