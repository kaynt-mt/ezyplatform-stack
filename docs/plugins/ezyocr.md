# ezyocr

OCR workflows and recognition configuration.

- **Marketplace version on core 1.5.9:** `0.0.3`.
- **Verified modules:** `admin-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyocr` | `org.youngmonkeys.ezyocr` | [ezyarticle](ezyarticle.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 21 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingsController` |
| `GET /ocr-business-scripts` | `AdminOcrBusinessScriptController` |
| `GET /ocr-business-scripts/add` | `AdminOcrBusinessScriptController` |
| `GET /api/v1/ocr-operators` | `AdminApiOcrOperatorController` |
| `GET /api/v1/ocr-business-scripts` | `AdminApiOcrBusinessScriptController` |
| `GET /api/v1/app-releases/latest` | `AdminApiAppReleaseController` |
| `GET /api/v1/ocr-business-scripts/categories` | `AdminApiOcrBusinessScriptController` |
| `POST /api/v1/ocr-operators/add` | `AdminApiOcrOperatorController` |
| `POST /api/v1/ocr-business-scripts/add` | `AdminApiOcrBusinessScriptController` |
| `PUT /api/v1/settings` | `AdminApiSettingController` |
| `PUT /api/v1/ocr-business-scripts/{scriptId}` | `AdminApiOcrBusinessScriptController` |
| `PUT /api/v1/ocr-operators/{adminId}/settings` | `AdminApiOcrOperatorController` |
| `PUT /api/v1/ocr-business-scripts/{scriptId}/publish` | `AdminApiOcrBusinessScriptController` |
| `DELETE /api/v1/ocr-operators/{adminId}` | `AdminApiOcrOperatorController` |
| `DELETE /api/v1/ocr-business-scripts/{scriptId}` | `AdminApiOcrBusinessScriptController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyocr: /`, `ocr_business_scripts: /ocr-business-scripts`, `ocr_business_scripts_add: ~/ocr-business-scripts/add`, `ocr_business_scripts_edit: ~/ocr-business-scripts/{scriptId}/edit`, `ocr_business_scripts_details: ~/ocr-business-scripts/{scriptId}`, `settings: /settings`.

- **admin-plugin – Template:** `ezyocr/ocr-business-scripts/add.html`, `ezyocr/ocr-business-scripts/category-list.html`, `ezyocr/ocr-business-scripts/details.html`, `ezyocr/ocr-business-scripts/edit.html`, `ezyocr/ocr-business-scripts/form.html`, `ezyocr/ocr-business-scripts/list.html`, `ezyocr/ocr-business-scripts/script-list.html` (+3).

- **admin-plugin – Static resources:** `ezyocr/css/style.css`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyocr-admin-plugin-0.0.3.jar`; 52 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyocr.admin.response`, `org.youngmonkeys.ezyocr.admin.constant`, `org.youngmonkeys.ezyocr.admin.controller.api` (+12).
- **Controllers, services, and repositories (sample):** `AdminApiAppReleaseController`, `AdminApiOcrBusinessScriptController`, `AdminApiOcrOperatorController`, `AdminApiOcrOperatorMeController`, `AdminAppReleaseControllerService`, `AdminAppReleaseService`, `AdminAppReleaseValidator`, `AdminEzyocrSettingService`, `AdminEzyocrSettingsValidator`.
- **Configuration and permission classes (sample):** `AdminEzyocrAdminRoleConfig`, `AdminEzyocrBusinessScriptConfig`, `AdminEzyocrPostConfig`, `AdminEzyocrTermTypeConfig`, `OcrOperatorSetting`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyocr/ocr-business-scripts` returned 200. No external OCR service was configured.

## Integration notes

For asynchronous OCR, verify retries and file permissions and limit the data sent externally. The settings screen does not prove OCR works.

[Back to the plugin index](README.md)
