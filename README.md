# SARS Tax Returns

**IRP6, IT14SD, dividends tax and customs VAT working papers for ERPNext v16.**

MIT licensed. Built as a thin add-on to [`za_local_core`](https://github.com/EPIUSECX/za_local_core); it does not modify core or duplicate VAT201/payroll.

## What it does

| Return | DocType | What it calculates |
|---|---|---|
| IRP6 provisional tax | `IRP6 Provisional Tax` | Tax on a taxable-income estimate at a configurable rate; payments and balance |
| IT14SD supplementary declaration | `IT14SD Reconciliation` | Return-to-financial-statements differences by section |
| Dividends tax | `Dividends Tax Return` | Taxable dividends, withholding at the configured rate, beneficiary split |
| Customs / diesel | `Customs VAT Schedule` | Customs value, duty, import VAT, diesel litres and refund totals |

Each working paper has a **Prepared** status after submit, an optional link to core `ZA Filing`, an attachment field and notes.

## What it does not do

- It does **not** submit to SARS eFiling.
- It does **not** replace the official IRP6, IT14SD, DTR01/DTR02 or customs forms.
- It does **not** calculate assessed losses, rebates, provisional-tax interest, treaty relief, customs duty or diesel eligibility.
- The tax rate and amounts are working-paper inputs. A tax practitioner must approve every return.

## Install

```bash
cd ~/frappe-bench
bench get-app https://github.com/infotjom/SARS-Tax-Returns.git --branch main
bench --site dev.local install-app sars_tax_returns
bench --site dev.local migrate
bench build --app sars_tax_returns
```

Open **SARS Tax Returns** in the Desk workspace, or go to:

```text
/desk/sars-tax-returns
```

## Print formats

Standard print formats are included:

- **SA IRP6 Provisional Tax**
- **SA IT14SD Reconciliation**
- **SA Dividends Tax Return**
- **SA Customs VAT Schedule**

Sample PDFs are in [`docs/print_samples`](docs/print_samples). They are rendered from the installed formats against the synthetic test records.

## Test data

```bash
bench --site dev.local execute sars_tax_returns.sars_tax_returns.test_data.build
```

Expected results:

| Return | Expected |
|---|---|
| IRP6 | Tax R 270 000; payments R 200 000; balance R 70 000 |
| IT14SD | Return R 59 850.72; financials R 59 650.72; difference R 200 |
| Dividends tax | Taxable R 90 000; withholding R 18 000; net R 72 000 |
| Customs | Customs value R 115 000; import VAT R 17 250 |

## Design

```text
IRP6 / IT14SD / DTR / Customs
        │
        ├── optional ZA Filing (core governance)
        ├── working_paper attachment
        └── notes / evidence
```

No hooks write to source accounting documents. These are read/capture working papers.

## Licence

MIT. See `license.txt`.
