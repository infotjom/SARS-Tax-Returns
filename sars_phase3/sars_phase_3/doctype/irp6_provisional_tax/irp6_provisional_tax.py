import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class IRP6ProvisionalTax(Document):
    def validate(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            frappe.throw(_("From Date cannot be after To Date."))
        if not self.tax_rate:
            settings = frappe.db.get_value("SARS Phase 3 Settings", self.company, "corporate_tax_rate") or 27
            self.tax_rate = settings
        self.tax_payable = flt(flt(self.taxable_income_estimate) * flt(self.tax_rate) / 100, 2)
        self.balance_payable = flt(self.tax_payable - flt(self.provisional_payments), 2)
        if self.balance_payable < 0 and not self.notes:
            frappe.msgprint(_("The provisional payments exceed the calculated tax. Record the overpayment reason in Notes."), indicator="orange")

    def before_submit(self):
        self.status = "Prepared"
