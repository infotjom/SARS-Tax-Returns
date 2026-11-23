# SARS Compliance Suite — Staging Technical Manual

**ERPNext / Frappe v16.53+ · Staging build**

Version 1.0 · November 2026

---

## 1. Architecture

```text
ERPNext / Frappe v16
│
├── za_local_core          VAT settings, tax invoices, VAT201 working paper, filings
├── za_local_payroll       PAYE/UIF/SDL/ETI, salary slips, EMP201, EMP501, IRP5
└── sars_tax_returns       IRP6, IT14SD, dividends tax, customs VAT
```

- `za_local_payroll` requires `za_local_core`.
- `sars_tax_returns` requires `za_local_core`.
- All three are separate Frappe apps; no core ERPNext code is modified.
- `sars_tax_returns` does **not** write to the GL. It is a working-paper layer.
- Core owns VAT classification and the source-to-GL snapshot.
- Payroll owns HRMS salary-slip calculation and EMP201/EMP501/IRP5.

---

## 2. Supported versions

| Component | Tested |
|---|---|
| ERPNext | 16.53.0 on `.131`; 16.55.0 on `.17` |
| Frappe | 16.54.0 / 16.56.0 |
| Python | 3.14 |
| Node | 24 |
| MariaDB | 10.6+ recommended |
| Bench | 5.31+ |

Target production for the website is ERPNext **v16.60**, but the SARS apps are tested on v16.53+. Do not deploy to v15.

---

## 3. Repositories

| App | Repository | Branch |
|---|---|---|
| Core | `https://github.com/EPIUSECX/za_local_core` | `main` |
| Payroll | `https://github.com/EPIUSECX/za_local_payroll` | `main` |
| Tax returns | `https://github.com/infotjom/SARS-Tax-Returns` | `main` |

Tested tax-returns commit: `32589fb`.

Pin exact tags/commits for staging and record them in the staging runbook. Do not deploy `main` without recording the commit.

---

## 4. Install order

```bash
cd ~/frappe-bench

bench get-app https://github.com/EPIUSECX/za_local_core.git --branch main
bench get-app https://github.com/EPIUSECX/za_local_payroll.git --branch main
bench get-app https://github.com/infotjom/SARS-Tax-Returns.git --branch main

bench --site staging.local install-app za_local_core
bench --site staging.local install-app za_local_payroll
bench --site staging.local install-app sars_tax_returns

bench --site staging.local migrate
bench build --app za_local_core
bench build --app za_local_payroll
bench build --app sars_tax_returns
bench --site staging.local clear-cache
```

Requirements:

- HRMS installed before `za_local_payroll`.
- South African company exists.
- Company country = South Africa.
- Payroll Period and Fiscal Year exist.
- Chart of accounts includes payroll/PAYE/UIF/SDL accounts.

---

## 5. Staging domain

Production remains `tjomtek.co.za` on the v15 server until cutover.

Staging uses the **same site name** on the new server:

```text
tjomtek.co.za
```

Test access uses a local hosts override on the reviewer’s machine:

```text
NEW_SERVER_IP    tjomtek.co.za
```

DNS is **not** changed until sign-off.

### SSL

Because public DNS still points to the old server, use **DNS-01** Let’s Encrypt validation (or copy the existing certificate temporarily). Do not use HTTP-01 for the new server while DNS is on the old one.

### Protect staging

- Enable HTTP basic auth or an IP allowlist.
- Add `noindex` / `robots.txt` disallow.
- `pause_scheduler = 1` in site config unless the test explicitly needs scheduled jobs.
- Disable outbound email or point it to a test mailbox.
- Do not use production customer data.

---

## 6. Configuration

### 6.1 VAT

1. **South Africa VAT Settings** — company, 10-digit VAT number, filing category, filing day, output/input accounts, vendor type.
2. **ZA Statutory Source** — private evidence, reviewer, submit.
3. **ZA Statutory Rate Pack** — verify values, reviewer, submit.
4. **VAT201 Classification Mapping** — sales/purchase templates.
5. **Item → South Africa VAT Category** — Standard Rated, Zero Rated, Export Zero Rated, Exempt, Capital Goods, Imported Capital Goods, Imported Other Goods.
6. **Account mapping** — output/input/capital/import VAT accounts.

Use `bootstrap_company_vat_setup(company, date)` only after the source/rate pack is approved; it creates the recommended templates.

### 6.2 Payroll

- Company PAYE/UIF/SDL references.
- `Payroll Settings` statutory components.
- Payroll Period (March–February).
- Income Tax Slab for 2026-2027.
- Salary Components with SARS payroll codes.
- Salary Structure and Salary Structure Assignment.
- Payroll rate pack or recorded packaged-rate decision.

### 6.3 Phase 3

- **SARS Tax Returns Settings** per company.
- Corporate tax rate (default 27%).
- Dividends tax rate (default 20%).
- VAT rate 15% read-only.

---

## 7. Data model

### Core

| DocType | Purpose |
|---|---|
| `South Africa VAT Settings` | Company VAT configuration |
| `ZA Statutory Source` | Approved SARS evidence |
| `ZA Statutory Rate Pack` | Effective VAT/payroll rates |
| `VAT201 Return` | Working paper + immutable snapshot |
| `ZA Filing` | Shared filing record |
| `ZA Submission Receipt` | eFiling acknowledgement evidence |

### Payroll

| DocType | Purpose |
|---|---|
| `Salary Slip` | HRMS calculation + SA statutory rows |
| `EMP201 Submission` | Monthly employer return |
| `EMP501 Reconciliation` | Interim/final reconciliation |
| `IRP5 Certificate` | IRP5/IT3(a) certificate |

### Tax returns

| DocType | Purpose |
|---|---|
| `IRP6 Provisional Tax` | Provisional tax working paper |
| `IT14SD Reconciliation` | Return-to-financials reconciliation |
| `Dividends Tax Return` | Dividends withholding working paper |
| `Customs VAT Schedule` | Customs/import VAT/diesel schedule |

`sars_tax_returns` has no `doc_events` writing to accounting documents. It stores working papers only.

---

## 8. Permissions

- System Manager: install/configure.
- Accounts Manager: VAT settings and VAT201.
- Payroll Manager: payroll, EMP201, EMP501, certificates.
- ZA Compliance Reviewer/Manager: statutory approval and filing review.
- Auditor: read/report.
- Do not grant System Manager for day-to-day bookkeeping.

Maker/checker:

- The preparer cannot be the reviewer/approver.
- A System Manager can override with an audit record; do not use override in production except a documented emergency.

---

## 9. Backups

### Local

```bash
bench --site tjomtek.co.za backup --with-files
```

Backups are in `sites/tjomtek.co.za/private/backups/`.

### AWS S3

Use a private bucket in `af-south-1`.

Example wrapper (secrets from `~/.aws/credentials`, never Git):

```bash
#!/usr/bin/env bash
set -euo pipefail
SITE="tjomtek.co.za"
STAMP="$(date +%Y/%m/%d/%H%M%S)"
cd /home/erpnxtadmin/frappe-bench
bench --site "$SITE" backup --with-files
aws s3 sync "sites/$SITE/private/backups/" \
  "s3://tjomtek-backups/production/$STAMP/" \
  --sse AES256 --only-show-errors
```

S3 requirements:

- Block all public access
- Versioning
- SSE-S3 (avoid KMS cost unless required)
- Lifecycle: 30 daily, 90 weekly, 365 monthly
- IAM user only `PutObject`, `ListBucket`, `GetObject`
- Test a restore quarterly

### Restore test

```bash
bench new-site restore-test.local
bench --site restore-test.local restore /path/to/database.sql.gz \
  --with-public-files /path/to/files.tar \
  --with-private-files /path/to/private-files.tar
```

Never restore over production without a maintenance window and a fresh backup.

---

## 10. Staging deployment checklist

- [ ] Git commit/tag recorded.
- [ ] Apps installed in order.
- [ ] `bench migrate` clean.
- [ ] `bench build` clean.
- [ ] Company/VAT number valid.
- [ ] Statutory source/rate pack approved.
- [ ] Item VAT categories tested.
- [ ] Payroll period/slab/structures assigned.
- [ ] Scheduler paused, outbound email disabled.
- [ ] Backup/restore tested.
- [ ] UAT workbook executed.
- [ ] No demo data loaded from test builders.
- [ ] No secrets in Git.

---

## 11. Upgrade / rollback

Before upgrade:

```bash
bench --site tjomtek.co.za backup --with-files
```

Upgrade staging only:

```bash
cd apps/<app>
git fetch --all
git checkout <tag>
cd ../..
bench --site tjomtek.co.za migrate
bench build --app <app>
bench --site tjomtek.co.za clear-cache
```

Rollback:

1. Stop the site.
2. Restore the database and files backup.
3. Checkout the previous app tag.
4. `bench migrate`, build, clear cache.
5. Run smoke tests.

A v15 → v16 database migration is effectively one-way. The backup is the rollback.

---

## 12. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| App install fails | Dependency order / Python/Node version | Install core → payroll → tax returns; check versions |
| `No module named ...` | App not pip-installed | `./env/bin/pip install -e apps/<app>` |
| No VAT201 field values | No transactions or wrong period | Get VAT Transactions |
| Needs Review | Specialist VAT scenario | Practitioner review / Box 18 evidence |
| Field 20 ≠ GL | Snapshot/source mismatch | Linked transactions, rebuild, reconcile |
| EMP201 cannot submit | No submitted slips | Run payroll first |
| Payroll totals zero | Assignment/tax slab missing | Check structure assignment, Payroll Period, slab |
| IRP6 print blank | Wrong print format | Select **SA IRP6 Provisional Tax** |
| Workspace missing | Migration/assets not built | `bench migrate`, `bench build`, clear cache |
| Staging emails sent | Scheduler/email enabled | Pause scheduler, disable outgoing email |

Logs:

```text
~/frappe-bench/logs/web.log
~/frappe-bench/logs/worker.log
sites/<site>/logs/
```

---

## 13. Known limitations

- No direct SARS eFiling submission.
- No BRS/e@syFile export.
- Core VAT201 supports standard/zero/export/exempt/capital purchases and blocked evidence; imported services, bad debts, change in use, second-hand goods, apportionment and diesel remain practitioner-controlled / Needs Review.
- Payroll EMP501 requires full-period coverage (six months interim, twelve months final); empty months cannot be submitted.
- `sars_tax_returns` is a working-paper layer; IRP6 uses a taxable-income estimate and configurable rate, not a full tax computation.
- Staging must not use production credentials or live data.

---

## 14. Related docs

- [Build Standard](BUILD_STANDARD.md)
- [Staging User Manual](STAGING_USER_MANUAL.md)
- [Demo & Test Workbook](STAGING_DEMO_WORKBOOK.md)
- [Print samples](print_samples/)
