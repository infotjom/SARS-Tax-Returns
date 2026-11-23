# SARS Compliance Suite — Demo & Test Workbook

**Staging · ERPNext v16.53+**

Version 1.0 · November 2026

> Staging is clean. Do **not** run `sars_tax_returns...test_data.build` here. Create each transaction below in the staging site.
>
> The purpose of this workbook is to prove behaviour and to give you a repeatable showcase without asking AI or anyone else.

---

## 0. Test environment

| Item | Value |
|---|---|
| Site | staging site |
| Company | staging company |
| Currency | ZAR |
| Test month | one open month, e.g. 2026-12 |
| Prepared by |  |
| Reviewed by |  |
| App commits | core: ______ · payroll: ______ · tax returns: ______ |
| Date |  |

Create these masters first:

- Customer: `STAGING CUSTOMER`
- Supplier: `STAGING SUPPLIER`
- Item: `STAGING SERVICE` (non-stock, service)
- Expense account: `STAGING ADMIN EXPENSE`
- Capital account: `STAGING CAPITAL EQUIPMENT`
- Income account: `STAGING SALES`

---

## 1. VAT scenarios

Record each result. A scenario passes only when the document is submitted and the expected amount is visible in the VAT201.

### VAT-01 — Standard-rated sale

| Field | Input |
|---|---|
| Document | Sales Invoice |
| Customer | STAGING CUSTOMER |
| Posting date | first day of test month |
| Item / qty / rate | STAGING SERVICE / 1 / R10 000 |
| Income account | STAGING SALES |
| SA VAT Category | Standard Rated |
| Tax template | Standard sales 15% |

**Expected:** grand total R11 500; VAT R1 500.

| Result | Value |
|---|---:|
| Grand total |  |
| VAT |  |
| Pass / fail |  |

---

### VAT-02 — Zero-rated sale

Same as VAT-01 with R5 000, **Zero Rated**, zero-rated template.

**Expected:** no VAT; R5 000 zero-rated.

| Result | Value |
|---|---:|
| Grand total |  |
| VAT |  |
| Pass / fail |  |

---

### VAT-03 — Export sale

Same as VAT-01 with R7 000, **Export Zero Rated**, export template. Attach export/customs evidence.

**Expected:** no VAT; R7 000 export.

| Result | Value |
|---|---:|
| Grand total |  |
| VAT |  |
| Pass / fail |  |

---

### VAT-04 — Exempt sale

Same as VAT-01 with R2 000, **Exempt**, exempt template.

**Expected:** no VAT; R2 000 exempt.

| Result | Value |
|---|---:|
| Grand total |  |
| VAT |  |
| Pass / fail |  |

---

### VAT-05 — Capital sale

Same as VAT-01 with R50 000, **Capital Goods**, capital-sales template, capital income account.

**Expected:** R57 500 including VAT; output VAT R7 500.

| Result | Value |
|---|---:|
| Grand total |  |
| VAT |  |
| Pass / fail |  |

---

### VAT-06 — Standard purchase

| Field | Input |
|---|---|
| Document | Purchase Invoice |
| Supplier | STAGING SUPPLIER |
| Bill No | `STG-BILL-001` |
| Item / qty / rate | STAGING SERVICE / 1 / R8 000 |
| Expense account | STAGING ADMIN EXPENSE |
| SA VAT Category | Standard Rated |
| Tax template | Standard purchases 15% |

**Expected:** input VAT R1 200; total R9 200.

| Result | Value |
|---|---:|
| Total |  |
| Input VAT |  |
| Pass / fail |  |

---

### VAT-07 — Capital purchase

Same as VAT-06 with R100 000, **Capital Goods**, capital-purchase template, capital asset account.

**Expected:** input VAT R15 000.

| Result | Value |
|---|---:|
| Total |  |
| Input VAT |  |
| Pass / fail |  |

---

### VAT-08 — Blocked entertainment

Create a standard purchase of R1 000, then set on the item:

- VAT Input Treatment: **Blocked**
- VAT Treatment Evidence: `ENT-001 — s17(2)`
- VAT Category: Standard Rated

**Expected:** R150 VAT is excluded from Field 19; the line is blocked/evidenced. If evidence is blank, it is **Needs Review**.

| Result | Value |
|---|---:|
| VAT on invoice |  |
| Included in Field 19? | No |
| Evidence reference |  |
| Pass / fail |  |

---

## 2. VAT201 reconciliation

1. Create **VAT201 Return** for the test month.
2. Save → **Get VAT Transactions**.
3. Resolve all **Needs Review**.
4. Open **Linked Transactions**.
5. Compare Field 20 to the VAT control account.

### Expected for VAT-01 to VAT-07

| Field | Expected |
|---|---:|
| 1 — standard non-capital | R11 500 |
| 1A — capital | R57 500 |
| 2 — zero-rated | R5 000 |
| 2A — exports | R7 000 |
| 3 — exempt | R2 000 |
| 13 — output | R9 000 |
| 14 — capital input | R15 000 |
| 15 — other input | R1 200 |
| 19 — input | R16 200 |
| 20 — net | −R7 200 |
| VAT control | −R7 200 |
| Difference | R0.00 |

Blocked entertainment must not change Field 19.

| Check | Expected | Actual | Pass |
|---|---|---|---|
| Field 1 | R11 500 |  |  |
| Field 1A | R57 500 |  |  |
| Field 2 | R5 000 |  |  |
| Field 2A | R7 000 |  |  |
| Field 3 | R2 000 |  |  |
| Field 13 | R9 000 |  |  |
| Field 14 | R15 000 |  |  |
| Field 15 | R1 200 |  |  |
| Field 19 | R16 200 |  |  |
| Field 20 | −R7 200 |  |  |
| Control difference | R0.00 |  |  |
| Needs Review | 0 |  |  |

---

## 3. Payroll and EMP201

### PAY-01 — Three employees

Create:

| Employee | Base | Expected PAYE | UIF employee | Net |
|---|---:|---:|---:|---:|
| STAGING EMPLOYEE A | R30 000 | R4 681.00 | R177.12 | R25 141.88 |
| STAGING EMPLOYEE B | R12 000 | R675.00 | R120.00 | R11 205.00 |
| STAGING EMPLOYEE C | R6 000 | R0.00 | R60.00 | R5 940.00 |

Use Payroll Period 2026-2027, Income Tax Slab 2026-2027, Monthly structure, August 2026.

| Check | Expected | Actual | Pass |
|---|---|---|---|
| Slip A PAYE | R4 681.00 |  |  |
| Slip A UIF | R177.12 |  |  |
| Slip B PAYE | R675.00 |  |  |
| Slip C PAYE | R0.00 |  |  |
| Slip C ETI | R1 125.00 |  |  |
| Total gross | R48 000 |  |  |

### PAY-02 — EMP201

Create **EMP201 Submission**, August 2026, fetch data, review, submit.

| Field | Expected | Actual | Pass |
|---|---|---|---|
| Gross PAYE before ETI | R5 356.00 |  |  |
| ETI generated / utilised | R1 125.00 |  |  |
| Net PAYE | R4 231.00 |  |  |
| UIF | R714.24 |  |  |
| SDL | R480.00 |  |  |

Reconcile with **Payroll Register** and **EMP201 Reconciliation**.

| Report | Expected | Actual | Pass |
|---|---|---|---|
| Payroll Register PAYE | R5 356.00 |  |  |
| Payroll Register UIF | R714.24 |  |  |
| Payroll Register SDL | R480.00 |  |  |
| EMP201 Reconciliation difference | R0.00 |  |  |

Do not attempt a zero-value EMP201; it requires submitted salary slips.

---

## 4. Phase 3 scenarios

### P3-01 — IRP6

| Field | Value |
|---|---|
| Year | 2026-2027 |
| Period | First |
| From / To | 2026-03-01 / 2026-08-31 |
| Taxable income estimate | R1 000 000 |
| Rate | 27% |
| Provisional payments | R200 000 |

**Expected:** tax R270 000; balance R70 000.

| Result | Expected | Actual | Pass |
|---|---|---|---|
| Tax | R270 000 |  |  |
| Balance | R70 000 |  |  |
| Print format | SA IRP6 |  |  |

### P3-02 — IT14SD

| Section | Per return | Financials | Difference |
|---|---:|---:|---:|
| VAT | R7 200 | R7 000 | R200 |
| PAYE | R16 068 | R16 068 | R0 |
| SDL | R1 440 | R1 440 | R0 |
| UIF | R2 142.72 | R2 142.72 | R0 |
| Customs | R15 000 | R15 000 | R0 |
| Dividends Tax | R18 000 | R18 000 | R0 |

**Expected:** return R59 850.72; financials R59 650.72; difference R200.00.

| Result | Expected | Actual | Pass |
|---|---|---|---|
| Total return | R59 850.72 |  |  |
| Total financials | R59 650.72 |  |  |
| Difference | R200.00 |  |  |
| Print format | SA IT14SD |  |  |

### P3-03 — Dividends tax

| Field | Value |
|---|---|
| Period | 2026-09-01 to 2026-09-30 |
| Gross dividends | R100 000 |
| Exempt | R10 000 |
| Rate | 20% |
| Beneficiary A | gross R60 000, exempt R0 |
| Beneficiary B | gross R40 000, exempt R10 000 |

**Expected:** taxable R90 000; withholding R18 000; net R72 000.

| Result | Expected | Actual | Pass |
|---|---|---|---|
| Taxable dividends | R90 000 |  |  |
| Withholding | R18 000 |  |  |
| Net | R72 000 |  |  |
| Print format | SA Dividends Tax |  |  |

### P3-04 — Customs VAT

| Line | Type | Document | Customs value | Import VAT |
|---|---|---|---:|---:|
| 1 | Import | CUS-TEST-001 | R100 000 | R15 000 |
| 2 | Import | CUS-TEST-002 | R15 000 | R2 250 |

**Expected:** customs value R115 000; import VAT R17 250; diesel refund R0.

| Result | Expected | Actual | Pass |
|---|---|---|---|
| Customs value | R115 000 |  |  |
| Import VAT | R17 250 |  |  |
| Diesel refund | R0 |  |  |
| Print format | SA Customs VAT |  |  |

---

## 5. 15-minute showcase

Use a clean staging site. Do not preload.

1. **Minute 0–2 — Context:** open the **SARS Tax Returns** workspace; state ERPNext v16.60 + Frappe Flow AI (AI is assisted, permission-aware, optional).
2. **Minute 2–5 — VAT:** create VAT-01 (R10 000 sale) and VAT-06 (R8 000 purchase). Show R1 500 output and R1 200 input.
3. **Minute 5–8 — VAT201:** create the return, Get VAT Transactions, show Fields 1/15/19/20 and reconciliation.
4. **Minute 8–11 — Payroll:** open EMP201; show R4 231 PAYE, R714.24 UIF, R480 SDL; open a salary slip.
5. **Minute 11–14 — Phase 3:** open IRP6 and print/view; open IT14SD and show R200 difference with reason.
6. **Minute 14–15 — Governance:** open linked transactions/snapshot/review; explain maker-checker and the working-paper disclaimer.

Do not claim the app submits to SARS. It prepares the working paper; filing is manual.

---

## 6. Cleanup

After the demo, cancel/delete in reverse order:

1. Phase 3 returns
2. EMP201 / salary slips / payroll entry
3. Salary structure assignment / structure / employees
4. VAT201
5. Sales and purchase invoices
6. Supplier/customer/item

Cancel before delete. Never delete submitted documents in production.

---

## 7. Sign-off

| Item | Name | Date |
|---|---|---|
| Tested by |  |  |
| Reviewed by |  |  |
| Accepted by |  |  |

*All numeric expectations are working-paper acceptance values; the tax practitioner signs off the statutory treatment.*
