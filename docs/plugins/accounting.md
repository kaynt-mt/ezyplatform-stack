# accounting

Kế toán: hệ thống tài khoản, người dùng và sổ giao dịch.

- **Bản Marketplace trên core 1.5.9:** `0.3.8`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/accounting` | `org.youngmonkeys.accounting` | [ecommerce](ecommerce.md) |
| `web-plugin` — `web/plugins/accounting` | `org.youngmonkeys.accounting` | [ecommerce](ecommerce.md) |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 71 tổ hợp phương thức/URI đọc được; mẫu đại diện:

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

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `accounting: /`, `overview: /overview`, `accounts: /accounts`, `accounts_details: ~/accounts/{id}`, `employees_details: ~/employees/{username}`, `users: /users` (+20).

- **admin-plugin – Template:** `accounting/account-balance-changes/details.html`, `accounting/account-balance-changes/histories.html`, `accounting/account-balance-changes/list.html`, `accounting/account-balance-changes/scripts.html`, `accounting/accounts/balance-change-list.html`, `accounting/accounts/details.html`, `accounting/accounts/list.html` (+54).

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (27):** `accounting_account_balance_change_histories`, `accounting_account_balance_changes`, `accounting_account_balances`, `accounting_accounts`, `accounting_annual_financial_reports`, `accounting_annual_quantity_reports`, `accounting_daily_financial_reports`, `accounting_daily_quantity_reports`, `accounting_fixed_cost_amounts`, `accounting_fixed_cost_histories`, `accounting_fixed_costs`, `accounting_formula_histories`, `accounting_formulas`, `accounting_invoices`, `accounting_ledger_entries`, `accounting_monthly_financial_reports`, `accounting_monthly_quantity_reports`, `accounting_quantity_changes`, `accounting_transfer_histories`, `accounting_transfers`, `accounting_user_formula_histories`, `accounting_user_formulas`, `accounting_voucher_histories`, `accounting_voucher_invoices`, `accounting_vouchers`, `accounting_weekly_financial_reports`, `accounting_weekly_quantity_reports`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (27):** `AAccount`, `AAccountBalance`, `AAccountBalanceChange`, `AAccountBalanceChangeHistory`, `AAnnualFinancialReport`, `AAnnualQuantityReport`, `ADailyFinancialReport`, `ADailyQuantityReport`, `AFixedCost`, `AFixedCostAmount`, `AFixedCostHistory`, `AFormula`, `AFormulaHistory`, `AInvoice`, `ALedgerEntry`, `AMonthlyFinancialReport`, `AMonthlyQuantityReport`, `AQuantityChange` (+9).
- **SQL admin-plugin (13 tệp):** `resources/scripts/fixed_cost.sql`, `resources/scripts/invoice_voucher_report.sql`, `resources/scripts/scripts.sql`, `resources/scripts/alter_account_balance_change_add_issue_date.sql`, `resources/scripts/alter_invoice_remove_fields.sql`, `resources/scripts/alter_ledger_entry_add_entry_type_pagination_index.sql`, `resources/scripts/alter_report_tables.sql` (+6).

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `accounting-admin-plugin-0.3.8.jar`, `accounting-sdk-0.3.8.jar`; 666 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.accounting.pagination`, `org.youngmonkeys.accounting.admin.repo`, `org.youngmonkeys.accounting.repo` (+32).
- **Controller/service/repository (mẫu):** `AAccountControllerService`, `AdminAAccountBalanceChangeController`, `AdminAAccountBalanceChangeControllerService`, `AdminAAccountBalanceChangeHistoryControllerService`, `AAccountBalanceChangeHistoryRepository`, `AAccountBalanceChangeRepository`, `AAccountBalanceChangeService`, `AAccountBalanceChangeTransactionalRepository`, `AAccountBalanceChangeValidator`.
- **Điểm mở rộng tiềm năng theo tên class:** `AVoucherEntityHandler`, `AVoucherEntityHandlerManager`, `AVoucherHandler`, `AVoucherHandlerManager`, `AccountingEntityFetcherManager`, `AdminAVoucherEntityHandlerManager`, `AdminAVoucherHandlerManager`, `AdminAccountingEntityFetcherManager`, `AdminAccountingTransactionProcessor` (+15).

### web-plugin

- **JAR kiểm tra:** `accounting-sdk-0.3.8.jar`, `accounting-web-plugin-0.3.8.jar`; 524 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.accounting.pagination`, `org.youngmonkeys.accounting.repo`, `org.youngmonkeys.accounting.web.repo` (+21).
- **Controller/service/repository (mẫu):** `AAccountControllerService`, `WebAAccountControllerService`, `AAccountBalanceChangeHistoryRepository`, `AAccountBalanceChangeRepository`, `AAccountBalanceChangeService`, `AAccountBalanceChangeTransactionalRepository`, `AAccountBalanceChangeValidator`.
- **Điểm mở rộng tiềm năng theo tên class:** `AVoucherEntityHandler`, `AVoucherEntityHandlerManager`, `AVoucherHandler`, `AVoucherHandlerManager`, `AccountingEntityFetcherManager`, `ConsolidatedDebitAVoucherHandler`, `DebtAVoucherHandler`, `GeneralPaymentAVoucherHandler`, `PaymentAVoucherHandler` (+4).

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/accounting/overview`, `/accounting/accounts` → 200. Chưa ghi sổ hoặc xuất chứng từ.

## Lưu ý khi tích hợp

Tham khảo cách tách giao dịch nghiệp vụ khỏi dữ liệu tổng hợp của màn hình Overview.

[Về chỉ mục plugin](README.md)
