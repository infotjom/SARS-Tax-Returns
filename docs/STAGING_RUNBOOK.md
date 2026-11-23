# Staging Runbook — SARS Compliance Suite

**Use this page to build/redeploy staging without asking anyone.**

---

## 1. Record before deploy

| Item | Value |
|---|---|
| Date |  |
| Site |  |
| Server |  |
| ERPNext |  |
| Frappe |  |
| Core commit/tag |  |
| Payroll commit/tag |  |
| Tax returns commit/tag |  |
| Deployed by |  |

Expected tested baseline:

- `za_local_core` 2.0.0
- `za_local_payroll` 2.1.0
- `sars_tax_returns` `5287606` or later
- ERPNext/Frappe v16.53+
- Python 3.14, Node 24, MariaDB 10.6+

---

## 2. Pre-flight

- [ ] Fresh backup exists.
- [ ] Staging site is not production.
- [ ] DNS still points production to the old server.
- [ ] `/etc/hosts` override ready for testers.
- [ ] Scheduler paused.
- [ ] Outbound email disabled or test mailbox.
- [ ] No live customer data.
- [ ] GitHub access confirmed.

---

## 3. Install order

```bash
cd ~/frappe-bench

bench get-app https://github.com/EPIUSECX/za_local_core.git --branch main
bench get-app https://github.com/EPIUSECX/za_local_payroll.git --branch main
bench get-app https://github.com/infotjom/SARS-Tax-Returns.git --branch main

bench --site <site> install-app za_local_core
bench --site <site> install-app za_local_payroll
bench --site <site> install-app sars_tax_returns

bench --site <site> migrate
bench build --app za_local_core
bench build --app za_local_payroll
bench build --app sars_tax_returns
bench --site <site> clear-cache
```

Do not install the old `sars_compliance` app alongside `za_local_core`.

---

## 4. Configure

- [ ] Company is South Africa + VAT registered.
- [ ] 10-digit VAT number.
- [ ] VAT filing category and day.
- [ ] Output/input VAT control accounts.
- [ ] Statutory source approved by reviewer.
- [ ] Statutory rate pack approved by reviewer.
- [ ] VAT templates mapped.
- [ ] Item VAT categories available.
- [ ] Payroll company references, Payroll Period, tax slab, structures/assignments.
- [ ] `SARS Tax Returns Settings` for the company.
- [ ] Named users/roles; no shared Administrator.

---

## 5. Smoke test

Use [STAGING_DEMO_WORKBOOK.md](STAGING_DEMO_WORKBOOK.md), not a test-data builder.

Minimum:

1. Create a standard sale R10 000 + 15%.
2. Create a standard purchase R8 000 + 15%.
3. VAT201: Get VAT Transactions; Field 20 = −R7 200 for the full workbook; difference 0.
4. Payroll: 3 employees; EMP201 net PAYE R4 231, UIF R714.24, SDL R480.
5. IRP6: balance R70 000.
6. IT14SD: difference R200.
7. Dividends: withholding R18 000.
8. Customs: import VAT R17 250.
9. Print each Phase 3 format.

Any `Needs Review`, missing field or nonzero reconciliation is a no-go until explained.

---

## 6. Backup / restore

```bash
bench --site <site> backup --with-files
```

S3 sync:

```bash
aws s3 sync sites/<site>/private/backups/ \
  s3://tjomtek-backups/staging/$(date +%Y/%m/%d/%H%M%S)/ \
  --sse AES256 --only-show-errors
```

Restore test on a throwaway site:

```bash
bench new-site restore-test.local
bench --site restore-test.local restore <database.sql.gz> \
  --with-public-files <files.tar> \
  --with-private-files <private-files.tar>
```

---

## 7. Go / no-go

**Go only if:**

- [ ] Install/migrate/build clean.
- [ ] All workbook scenarios pass.
- [ ] No `Needs Review` without disposition.
- [ ] VAT control reconciles.
- [ ] EMP201 reconciles to payroll.
- [ ] Phase 3 totals match.
- [ ] Print formats render.
- [ ] Backup/restore tested.
- [ ] No secrets in Git.
- [ ] UAT signed.

**No-go if:** any blocking check fails, or the documented app commit is not the deployed commit.

---

## 8. Rollback

1. Stop the site.
2. Restore the last good database/files backup.
3. Checkout the previous app tag/commit.
4. `bench migrate`, `bench build`, `clear-cache`.
5. Run the smoke test.
6. Record the rollback and notify the business owner.

A v15 → v16 migration is one-way; the backup is the rollback.

---

## Deployment record — 23 November 2026

| Item | Value |
|---|---|
| Server | `erpnxtdemo` / `83.147.37.86` |
| Site | `rom.tjomtek.co.za` |
| OS | Ubuntu 24.04.4 LTS |
| Python / Node | 3.14.6 / 24.18.0 |
| MariaDB | 10.11.14 |
| Frappe | `v16.60.2` |
| ERPNext | `v16.60.0` |
| HRMS | `v16.60.0` |
| `za_local_core` | 2.0.0 · `6973efe` |
| `za_local_payroll` | 2.1.0 · `8f902f8` |
| `sars_tax_returns` | 0.0.1 · `1f4c7f9` |
| Backup before change | `20261123_110100-rom_tjomtek_co_za` |
| Health | `https://rom.tjomtek.co.za/login` → 200; `/api/method/ping` → 200 |
| SARS workspace | Present |
| `VAT201 Return` records | 0 (clean) |

### What changed

- Upgraded Frappe/ERPNext/HRMS from 16.36/16.37/16.20 to v16.60.
- Removed `sa_vat_app` completely (app, tables, orphan sidebars).
- Installed `za_local_core`, `za_local_payroll`, `sars_tax_returns`.
- Preserved `flight_booking`, `rgn_lab`, `raven`, `wiki`, `weighbridge`, `rgn_timecards`, `offsite_backups`.
- No SARS test data loaded.

### Still to do on staging

- Smoke-test the unrelated custom apps after the v16.60 upgrade.
- Configure the staging company (VAT settings, statutory source/rate pack, payroll masters).
- Execute `STAGING_DEMO_WORKBOOK.md`.
- Record UAT sign-off.
