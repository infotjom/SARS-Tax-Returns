"""Repeatable Phase 3 test data for a sandbox site.

Run:
    bench --site dev.local execute sars_tax_returns.sars_tax_returns.test_data.build
"""

import frappe

COMPANY = "DEV.V16"


def _settings(company):
    if not frappe.db.exists("SARS Tax Returns Settings", company):
        frappe.get_doc({
            "doctype": "SARS Tax Returns Settings", "company": company,
            "corporate_tax_rate": 27, "dividends_tax_rate": 20, "vat_rate": 15,
            "notes": "Sandbox working-paper defaults; confirm against the applicable SARS year of assessment.",
        }).insert(ignore_permissions=True)


def _irp6(company):
    existing = frappe.db.get_value("IRP6 Provisional Tax", {"company": company, "fiscal_year": "2026-2027", "period": "First"}, "name")
    if existing:
        return existing
    doc = frappe.get_doc({
        "doctype": "IRP6 Provisional Tax", "company": company, "fiscal_year": "2026-2027",
        "period": "First", "from_date": "2026-03-01", "to_date": "2026-08-31",
        "due_date": "2026-08-31", "taxable_income_estimate": 1000000,
        "provisional_payments": 200000, "payment_reference": "IRP6-TEST-001",
        "notes": "Synthetic working paper. Not a SARS submission.",
    }).insert(ignore_permissions=True)
    doc.submit()
    return doc.name


def _it14sd(company):
    existing = frappe.db.get_value("IT14SD Reconciliation", {"company": company, "fiscal_year": "2026-2027"}, "name")
    if existing:
        return existing
    doc = frappe.get_doc({
        "doctype": "IT14SD Reconciliation", "company": company, "fiscal_year": "2026-2027",
        "from_date": "2026-03-01", "to_date": "2027-02-28",
        "lines": [
            {"section": "VAT", "description": "VAT201 net amount", "return_amount": 7200, "financial_amount": 7000, "reason": "Timing of input credit"},
            {"section": "PAYE", "description": "PAYE per EMP201s", "return_amount": 16068, "financial_amount": 16068, "reason": "Agrees"},
            {"section": "SDL", "description": "SDL per EMP201s", "return_amount": 1440, "financial_amount": 1440, "reason": "Agrees"},
            {"section": "UIF", "description": "UIF per EMP201s", "return_amount": 2142.72, "financial_amount": 2142.72, "reason": "Agrees"},
            {"section": "Customs", "description": "Import VAT per customs schedule", "return_amount": 15000, "financial_amount": 15000, "reason": "Agrees"},
            {"section": "Dividends Tax", "description": "Dividends tax withheld", "return_amount": 18000, "financial_amount": 18000, "reason": "Agrees"},
        ],
        "notes": "Synthetic working paper. Differences require evidence before filing.",
    }).insert(ignore_permissions=True)
    doc.submit()
    return doc.name


def _dividends(company):
    existing = frappe.db.get_value("Dividends Tax Return", {"company": company, "period_start": "2026-09-01"}, "name")
    if existing:
        return existing
    doc = frappe.get_doc({
        "doctype": "Dividends Tax Return", "company": company,
        "period_start": "2026-09-01", "period_end": "2026-09-30",
        "gross_dividends": 100000, "exempt_dividends": 10000, "dividends_tax_rate": 20,
        "beneficiaries": [
            {"shareholder": "Synthetic Shareholder A", "gross_dividend": 60000, "exempt_dividend": 0},
            {"shareholder": "Synthetic Shareholder B", "gross_dividend": 40000, "exempt_dividend": 10000},
        ],
        "notes": "Synthetic DTR working paper. Exemptions and treaties require evidence.",
    }).insert(ignore_permissions=True)
    doc.submit()
    return doc.name


def _customs(company):
    existing = frappe.db.get_value("Customs VAT Schedule", {"company": company, "period_start": "2026-09-01"}, "name")
    if existing:
        return existing
    doc = frappe.get_doc({
        "doctype": "Customs VAT Schedule", "company": company,
        "period_start": "2026-09-01", "period_end": "2026-09-30",
        "lines": [
            {"entry_type": "Import", "document_no": "CUS-TEST-001", "posting_date": "2026-09-10", "customs_value": 100000, "customs_duty": 0, "import_vat": 15000, "diesel_litres": 0, "diesel_refund": 0},
            {"entry_type": "Import", "document_no": "CUS-TEST-002", "posting_date": "2026-09-20", "customs_value": 15000, "customs_duty": 0, "import_vat": 2250, "diesel_litres": 0, "diesel_refund": 0},
        ],
        "notes": "Synthetic customs VAT schedule. Customs duty and diesel eligibility are practitioner-controlled.",
    }).insert(ignore_permissions=True)
    doc.submit()
    return doc.name


def build(company=COMPANY):
    company = company or COMPANY
    _settings(company)
    out = {
        "irp6": _irp6(company),
        "it14sd": _it14sd(company),
        "dividends": _dividends(company),
        "customs": _customs(company),
    }
    frappe.db.commit()
    return out
