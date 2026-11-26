# accounting

Accounting: accounts, users, and a transaction ledger.

- **Marketplace version on core 1.5.9:** `0.3.8`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/accounting` | `org.youngmonkeys.accounting` | [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/accounting` | `org.youngmonkeys.accounting` | [ecommerce](ecommerce.md) |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 71 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /users` | `AdminAccountingUserController` |
| `GET /ledger` | `AdminALedgerController` |
| `GET /accounts` | `AdminAAccountController` |
| `GET /formulas` | `AdminAFormulaController` |
| `GET /overview` | `AdminAccountingOverviewController` |
| `GET /settings` | `AdminAccountingSettingController` |
| `GET /avouchers` | `AdminAVoucherController` |
| `POST /api/v1/avouchers/add` | `AdminApiAVoucherController` |
| `POST /api/v1/fixed-costs/add` | `AdminApiAFixedCostController` |
| `POST /api/v1/ledger-entries/{id}/cancel` | `AdminApiALedgerEntryController` |
| `POST /api/v1/account-balance-changes/{id}/cancel` | `AdminApiAAccountBalanceChangeController` |
| `PUT /api/v1/settings/displayed-report-data-fields` | `AdminApiAccountingSettingController` |
| `PUT /api/v1/settings/displayed-user-report-data-fields` | `AdminApiAccountingSettingController` |
| `PUT /api/v1/formulas/{id}` | `AdminApiAFormulaController` |
| `PUT /api/v1/avouchers/{id}` | `AdminApiAVoucherController` |
| `DELETE /api/v1/fixed-costs/{id}` | `AdminApiAFixedCostController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `accounting: /`, `overview: /overview`, `accounts: /accounts`, `accounts_details: ~/accounts/{id}`, `employees_details: ~/employees/{username}`, `users: /users` (+20).

- **admin-plugin – Template:** `accounting/account-balance-changes/details.html`, `accounting/account-balance-changes/histories.html`, `accounting/account-balance-changes/list.html`, `accounting/account-balance-changes/scripts.html`, `accounting/accounts/balance-change-list.html`, `accounting/accounts/details.html`, `accounting/accounts/list.html` (+54).

## Data and migrations

- **Table in the DDL package (27):** `accounting_account_balance_change_histories`, `accounting_account_balance_changes`, `accounting_account_balances`, `accounting_accounts`, `accounting_annual_financial_reports`, `accounting_annual_quantity_reports`, `accounting_daily_financial_reports`, `accounting_daily_quantity_reports`, `accounting_fixed_cost_amounts`, `accounting_fixed_cost_histories`, `accounting_fixed_costs`, `accounting_formula_histories`, `accounting_formulas`, `accounting_invoices`, `accounting_ledger_entries`, `accounting_monthly_financial_reports`, `accounting_monthly_quantity_reports`, `accounting_quantity_changes`, `accounting_transfer_histories`, `accounting_transfers`, `accounting_user_formula_histories`, `accounting_user_formulas`, `accounting_voucher_histories`, `accounting_voucher_invoices`, `accounting_vouchers`, `accounting_weekly_financial_reports`, `accounting_weekly_quantity_reports`.
- **Class with JPA Entity/MappedSuperclass):** `AAccount`, `AAccountBalance`, `AAccountBalanceChange`, `AAccountBalanceChangeHistory`, `AAnnualFinancialReport`, `AAnnualQuantityReport`, `ADailyFinancialReport`, `ADailyQuantityReport`, `AFixedCost`, `AFixedCostAmount`, `AFixedCostHistory`, `AFormula`, `AFormulaHistory`, `AInvoice`, `ALedgerEntry`, `AMonthlyFinancialReport`, `AMonthlyQuantityReport`, `AQuantityChange` (+9).
- **SQL admin-plugin (13 files):** `resources/scripts/fixed_cost.sql`, `resources/scripts/invoice_voucher_report.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_account_balance_change_add_issue_date.sql`, `resources/scripts/alter_invoice_remove_fields.sql`, `resources/scripts/alter_ledger_entry_add_entry_type_pagination_index.sql`, `resources/scripts/alter_report_tables.sql` (+6).

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `accounting-admin-plugin-0.3.8.jar`, `accounting-sdk-0.3.8.jar`; 666 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.accounting.pagination`, `org.youngmonkeys.accounting.admin.repo`, `org.youngmonkeys.accounting.repo` (+32).
- **Controllers, services, and repositories (sample):** `AAccountControllerService`, `AdminAAccountBalanceChangeController`, `AdminAAccountBalanceChangeControllerService`, `AdminAAccountBalanceChangeHistoryControllerService`, `AAccountBalanceChangeHistoryRepository`, `AAccountBalanceChangeRepository`, `AAccountBalanceChangeService`, `AAccountBalanceChangeTransactionalRepository`, `AAccountBalanceChangeValidator`.
- **Potential extension points based on class names:** `AVoucherEntityHandler`, `AVoucherEntityHandlerManager`, `AVoucherHandler`, `AVoucherHandlerManager`, `AccountingEntityFetcherManager`, `AdminAVoucherEntityHandlerManager`, `AdminAVoucherHandlerManager`, `AdminAccountingEntityFetcherManager`, `AdminAccountingTransactionProcessor` (+15).

### web-plugin

- **JARs inspected:** `accounting-sdk-0.3.8.jar`, `accounting-web-plugin-0.3.8.jar`; 524 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.accounting.pagination`, `org.youngmonkeys.accounting.repo`, `org.youngmonkeys.accounting.web.repo` (+21).
- **Controllers, services, and repositories (sample):** `AAccountControllerService`, `WebAAccountControllerService`, `AAccountBalanceChangeHistoryRepository`, `AAccountBalanceChangeRepository`, `AAccountBalanceChangeService`, `AAccountBalanceChangeTransactionalRepository`, `AAccountBalanceChangeValidator`.
- **Potential extension points based on class names:** `AVoucherEntityHandler`, `AVoucherEntityHandlerManager`, `AVoucherHandler`, `AVoucherHandlerManager`, `AccountingEntityFetcherManager`, `ConsolidatedDebitAVoucherHandler`, `DebtAVoucherHandler`, `GeneralPaymentAVoucherHandler`, `PaymentAVoucherHandler` (+4).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/accounting/overview` and `/accounting/accounts` returned 200. Ledger entries and document exports were not tested.

## Integration notes

Use the Overview screen as an example of separating business transactions from aggregate data.

[Back to the plugin index](README.md)
