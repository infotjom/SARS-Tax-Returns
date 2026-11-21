import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class DividendsTaxReturn(Document):
    def validate(self):
        if self.period_start and self.period_end and self.period_start > self.period_end:
            frappe.throw(_("Period Start cannot be after Period End."))
        self.taxable_dividends = flt(self.gross_dividends) - flt(self.exempt_dividends)
        rate = flt(self.dividends_tax_rate) or 20
        self.withholding_tax = flt(self.taxable_dividends * rate / 100, 2)
        self.net_dividends = flt(self.taxable_dividends - self.withholding_tax, 2)
        for row in self.beneficiaries:
            row.taxable_dividend = flt(row.gross_dividend) - flt(row.exempt_dividend)
            row.withholding_tax = flt(row.taxable_dividend * rate / 100, 2)
            row.net_dividend = flt(row.taxable_dividend - row.withholding_tax, 2)
        if self.beneficiaries:
            total_gross = sum(flt(r.gross_dividend) for r in self.beneficiaries)
            if abs(total_gross - flt(self.gross_dividends)) > 0.01:
                frappe.msgprint(_("Beneficiary gross dividends do not agree to the summary gross dividends."), indicator="orange")

    def before_submit(self):
        self.status = "Prepared"
