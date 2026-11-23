# SARS Compliance Suite — Staging User Manual

**ERPNext / Frappe v16.53+**

Version 1.0 · Staging · November 2026

> Staging is clean. No demo transactions are preloaded. This manual creates each transaction from scratch.
>
> This is working-paper and configuration training, not tax advice. The accountant/tax practitioner signs off every return.

---

## 1. What is in the suite

| App | Used for |
|---|---|
| `za_local_core` | VAT settings, tax invoices, VAT201 working paper, governance and filings |
| `za_local_payroll` | PAYE, UIF, SDL, ETI, salary slips and EMP201/EMP501/IRP5 |
| `sars_tax_returns` | IRP6, IT14SD, dividends tax and customs VAT working papers |

**Not in staging:** old `sars_compliance` VAT app, demo VAT records, sample payroll, demo Phase 3 records.

---

## 2. Roles

| Role | Typical user | Can do |
|---|---|---|
| System Manager | Implementer | Everything, including setup |
| Accounts Manager | Accountant | VAT settings, returns, submit |
| Accounts User | Bookkeeper | Create invoices and view reports |
| Payroll Manager | Payroll accountant | Payroll, EMP201, certificates |
| ZA Compliance Reviewer / Manager | Reviewer | Approve statutory source, rate pack, filings |
| Auditor | External reviewer | Read/report only |

Do not use the Administrator account for day-to-day work. Create named users.

---

## 3. Before you start

1. Confirm the company is South African and VAT-registered.
2. Confirm the VAT registration number is 10 digits.
3. Confirm the company has a valid chart of accounts and payroll accounts.
4. Log in as a named user.
5. Open **SA Localisation** or the **SARS Tax Returns** workspace.

### Navigation used in this manual

- **VAT settings:** `Search → South Africa VAT Settings`
- **VAT return:** `Search → VAT201 Return`
- **Sales:** `Accounting → Sales Invoice`
- **Purchases:** `Accounting → Purchase Invoice`
- **Payroll:** `Payroll → Payroll Entry`
- **EMP201:** `Search → EMP201 Submission`
- **Phase 3:** **SARS Tax Returns** workspace

---

## 4. One-time setup — VAT

This section is for the System Manager/implementer. A bookkeeper can skip to Section 5 once setup is approved.

### 4.1 South Africa VAT Settings

Open **South Africa VAT Settings** for the company and complete:

| Field | Value |
|---|---|
| Company | The South African VAT vendor |
| VAT Registration Number | 10-digit SARS VAT number |
| VAT Filing Category | A, B, C, D or E — confirm on eFiling |
| VAT Filing Frequency | Monthly / Bi-Monthly, matching the category |
| VAT Filing Day | Usually 25 |
| VAT Vendor Type | Standard |
| Output VAT Account | Output VAT control account |
| Input VAT Account | Input VAT control account |

Save.

### 4.2 Approve the statutory source and rate pack

Do this once, with two different users.

1. Open **ZA Statutory Source**.
2. Confirm the SARS publication/gazette is attached as a **private file**.
3. Set **Reviewed By** to the reviewer.
4. Submit as the reviewer.
5. Open **ZA Statutory Rate Pack**.
6. Confirm every rate/threshold against the source.
7. Set **Reviewed By**; submit as the reviewer.

The reviewer needs `ZA Compliance Reviewer` or `ZA Compliance Manager`. The approver cannot be the creator.

### 4.3 Create/verify VAT templates

Under **Sales Taxes and Charges Template** and **Purchase Taxes and Charges Template**, confirm:

- Standard sales 15%
- Capital sales 15%
- Zero-rated sales 0%
- Export zero-rated sales 0%
- Exempt sales 0%
- Standard purchases 15%
- Capital purchases 15%

Use the templates created by `bootstrap_company_vat_setup` or map the company’s existing templates in **South Africa VAT Settings → VAT201 Classification Mapping**.

### 4.4 Item VAT category

Every invoice line must have **South Africa VAT Category**:

- Standard Rated
- Zero Rated
- Export Zero Rated
- Exempt
- Capital Goods
- Imported Capital Goods
- Imported Other Goods

On the Sales Invoice Item/Purchase Invoice Item, this field defaults from the Item but can be changed per line with a reason.

### 4.5 Company VAT number

Confirm **Company → Tax ID / VAT Registration Number** is the 10-digit VAT number. The VAT201 validates this.

---

## 5. VAT transaction tests

Create the transactions in this order. Use a dedicated customer `STAGING CUSTOMER` and supplier `STAGING SUPPLIER`, and a non-stock service item `STAGING SERVICE` so stock valuation does not interfere.

### 5.1 Standard-rated sale — R10 000 + 15%

**Path:** `Accounting → Sales Invoice → New`

| Field | Value |
|---|---|
| Customer | STAGING CUSTOMER |
| Posting Date | first day of the test month |
| Item | STAGING SERVICE |
| Qty | 1 |
| Rate | 10 000 |
| Income Account | Sales |
| South Africa VAT Category | Standard Rated |
| Taxes and Charges Template | Standard sales 15% |

Save → Submit.

**Expected:** grand total R11 500; VAT R1 500.

### 5.2 Zero-rated sale — R5 000

Same as 5.1, but:

- Rate R5 000
- VAT Category **Zero Rated**
- Template **Zero-rated sales 0%**

**Expected:** no VAT; R5 000 zero-rated.

### 5.3 Export sale — R7 000

- Rate R7 000
- VAT Category **Export Zero Rated**
- Template **Export zero-rated sales 0%**
- Keep customs/export evidence in the notes/attachment.

**Expected:** no VAT; R7 000 export.

### 5.4 Exempt sale — R2 000

- Rate R2 000
- VAT Category **Exempt**
- Template **Exempt sales 0%**

**Expected:** no VAT; R2 000 exempt.

### 5.5 Capital sale — R50 000 + 15%

- Income Account: capital sales/fixed asset disposal account
- Rate R50 000
- VAT Category **Capital Goods**
- Template **Capital sales 15%**

**Expected:** R57 500 including VAT; output VAT R7 500.

### 5.6 Standard purchase — R8 000 + 15%

**Path:** `Accounting → Purchase Invoice → New`

| Field | Value |
|---|---|
| Supplier | STAGING SUPPLIER |
| Bill No | unique staging bill number |
| Item | STAGING SERVICE |
| Rate | 8 000 |
| Expense Account | Administrative expenses |
| South Africa VAT Category | Standard Rated |
| Template | Standard purchases 15% |

**Expected:** input VAT R1 200; total R9 200.

### 5.7 Capital purchase — R100 000 + 15%

- Expense/Asset Account: fixed asset account
- Rate R100 000
- VAT Category **Capital Goods**
- Template **Capital purchases 15%**

**Expected:** input VAT R15 000.

### 5.8 Blocked entertainment — R1 000 + 15%

Create a standard purchase, then on the item set:

- **VAT Input Treatment:** Blocked
- **VAT Treatment Evidence:** a reference such as `ENT-001 — s17(2)`
- VAT Category: Standard Rated

**Expected:** VAT R150 is **not** claimed in Field 19; it is expensed/recorded as blocked. If no evidence reference is supplied, the line remains **Needs Review**.

### 5.9 Imported services — controlled manual

Do not force this into a standard test. Core marks imported services/second-hand goods/change in use/bad debts as **Needs Review** or requires a Box 18 adjustment with evidence. Use the technical manual and a tax practitioner for that scenario.

---

## 6. Review the VAT201

1. Open **VAT201 Return → New**.
2. Company: the staging company.
3. From/To: first and last day of the test month.
4. Filing Category: the company’s category.
5. Save.
6. Click **Get VAT Transactions**.
7. Open **Linked Transactions** and review every line.
8. Resolve all **Needs Review** items before relying on the totals.

### Expected result for scenarios 5.1–5.7

| Field | Amount |
|---|---:|
| 1 — standard non-capital | R 11 500 |
| 1A — capital | R 57 500 |
| 2 — zero-rated | R 5 000 |
| 2A — exports | R 7 000 |
| 3 — exempt | R 2 000 |
| 13 — total output | R 9 000 |
| 14 — capital input | R 15 000 |
| 15 — other input | R 1 200 |
| 19 — total input | R 16 200 |
| 20 — net | **−R 7 200** |
| Reconciliation difference | **R 0.00** |

Blocked entertainment (5.8) should not change Field 19.

### Review checks

- Field 20 agrees to the VAT control account.
- No line is **Needs Review**.
- Capital purchases appear in 14, not 15.
- Zero/export/exempt are in 2/2A/3, not Field 1.
- Blocked VAT is excluded and evidenced.
- Source-to-GL reconciliation = 0.

---

## 7. Payroll and EMP201

### 7.1 One-time payroll setup

| Item | Value |
|---|---|
| Company PAYE reference | 10 digits |
| Company UIF reference | UIF reference |
| Company SDL reference | SDL reference |
| Payroll Settings | PAYE, UIF employee/employer, SDL components |
| Payroll Period | 2026-2027 (March–February) |
| Income Tax Slab | South Africa 2026-2027 |
| Salary Component | Basic, PAYE, UIF Employee, UIF Employer, SDL |
| Salary Structure | Basic = base; deduction PAYE |
| Salary Structure Assignment | Employee, structure, base, tax slab, payroll period |

Ensure statutory rates are approved in a **Payroll** rate pack. If the company has recorded the decision to use packaged rates, confirm that in **Payroll Settings → Allow Packaged Statutory Rates**.

### 7.2 Create three employees

Create employees with:

- Company, gender, date of birth, date of joining
- SA ID number and income tax reference
- Employee type
- Residential address
- Bank account, account type, holder relationship
- Hours per month

Use gross monthly bases:

| Employee | Base |
|---|---:|
| STAGING EMPLOYEE A | R30 000 |
| STAGING EMPLOYEE B | R12 000 |
| STAGING EMPLOYEE C | R6 000 |

### 7.3 Run payroll

1. `Payroll → Payroll Entry → New`
2. Company, posting date, start/end dates, Monthly
3. Add the three employees
4. Save → Submit
5. Open each **Salary Slip** and check PAYE, UIF and net
6. Submit the slips if not already submitted

### Expected salary slips

| Employee | Gross | PAYE | UIF employee | Net |
|---|---:|---:|---:|---:|
| A | R30 000 | R4 681.00 | R177.12 | R25 141.88 |
| B | R12 000 | R675.00 | R120.00 | R11 205.00 |
| C | R6 000 | R0.00 | R60.00 | R5 940.00 |

### 7.4 EMP201

1. `Search → EMP201 Submission → New`
2. Company, fiscal year 2026-2027, month August, posting date 31 August
3. Save → **Fetch EMP201 Data**
4. Review PAYE, UIF, SDL and ETI
5. Set the payable/review fields as required
6. Reviewed By: a Payroll Manager other than the preparer
7. Submit

### Expected EMP201

| Field | Amount |
|---|---:|
| Gross PAYE before ETI | R5 356.00 |
| ETI generated / utilised | R1 125.00 |
| Net PAYE payable | R4 231.00 |
| UIF payable | R714.24 |
| SDL payable | R480.00 |

A zero-value month cannot be submitted; the app requires submitted salary slips. Do not try to force an empty EMP201.

---

## 8. Phase 3 returns

Open the **SARS Tax Returns** workspace.

### 8.1 IRP6 — provisional tax

`IRP6 Provisional Tax → New`

| Field | Value |
|---|---|
| Company | staging company |
| Year of Assessment | 2026-2027 |
| Return Period | First |
| From / To | 2026-03-01 / 2026-08-31 |
| Taxable Income Estimate | 1 000 000 |
| Tax Rate | 27% |
| Provisional Payments | 200 000 |

Save → Submit.

**Expected:** tax R270 000; balance R70 000.

### 8.2 IT14SD — reconciliation

`IT14SD Reconciliation → New`

Add lines:

| Section | Description | Per Return | Financials | Reason |
|---|---|---:|---:|---|
| VAT | VAT201 net | 7 200 | 7 000 | Timing of input credit |
| PAYE | PAYE per EMP201s | 16 068 | 16 068 | Agrees |
| SDL | SDL per EMP201s | 1 440 | 1 440 | Agrees |
| UIF | UIF per EMP201s | 2 142.72 | 2 142.72 | Agrees |
| Customs | Import VAT | 15 000 | 15 000 | Agrees |
| Dividends Tax | Withheld | 18 000 | 18 000 | Agrees |

Submit.

**Expected:** return R59 850.72; financials R59 650.72; difference R200.00.

### 8.3 Dividends tax

`Dividends Tax Return → New`

- Period: September 2026
- Gross dividends R100 000
- Exempt R10 000
- Rate 20%
- Beneficiaries:
  - A: gross R60 000, exempt R0
  - B: gross R40 000, exempt R10 000

Submit.

**Expected:** taxable R90 000; withholding R18 000; net R72 000.

### 8.4 Customs VAT

`Customs VAT Schedule → New`

- Period: September 2026
- Import line 1: customs value R100 000; import VAT R15 000
- Import line 2: customs value R15 000; import VAT R2 250

Submit.

**Expected:** customs value R115 000; import VAT R17 250; diesel refund R0.

### 8.5 Print

Open a submitted return → **Print** → select the matching **SA ...** print format. Use the printed PDF as the review copy. It is not a SARS submission.

---

## 9. 15-minute showcase

1. **2 min — VAT settings/AI:** show the workspace and explain ERPNext v16.60 + Frappe Flow AI (assisted, permission-aware, optional).
2. **4 min — standard sale + purchase:** create R10 000 sale and R8 000 purchase; show VAT R1 500 output and R1 200 input.
3. **3 min — VAT201:** Get VAT Transactions; show Fields 1/15/19/20; highlight reconciliation.
4. **3 min — payroll/EMP201:** open the submitted EMP201; show R4 231 PAYE, R714.24 UIF, R480 SDL.
5. **2 min — Phase 3:** open IRP6 and IT14SD print views.
6. **1 min — close:** open the linked `ZA Filing`/review trail and explain governance.

Do not preload data. Create it in the meeting.

---

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| VAT201 fields blank | Period/category wrong or no transactions | Check dates/category; Get VAT Transactions |
| Capital purchase in Field 15 | Item category/mapping wrong | Set Capital Goods and capital template |
| Zero-rated in Field 1 | Missing zero template/category | Set Zero Rated + 0% template |
| Needs Review | Imported/blocked/mixed treatment | Add evidence; review with practitioner |
| Field 20 ≠ control | Missing/duplicate ledger lines | Run linked transactions; rebuild per technical manual |
| EMP201 cannot submit | No salary slips | Run payroll for that month first |
| EMP201 totals zero | Payroll period/slips not submitted | Check dates and slip status |
| IRP6 print missing | Print format not selected | Print → SA IRP6 Provisional Tax |
| Phase 3 form not visible | App not installed/permission | Check `list-apps` and roles |
| Can't approve rate pack | Creator cannot approve | Use a different reviewer with ZA Compliance role |

---

## 11. Data cleanup after a demo

Cancel and delete the staging test documents in reverse order:

1. Phase 3 returns
2. EMP201 / salary slips / payroll entry
3. Salary structure assignment / structure / employees
4. VAT201
5. Sales/purchase invoices
6. Customer/supplier/item

Do **not** delete a submitted document without cancelling it first. Never clean up production.

---

*Working paper training only. Every return requires practitioner review before filing.*
