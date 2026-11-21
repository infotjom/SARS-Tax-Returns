import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class IT14SDReconciliation(Document):
    def validate(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            frappe.throw(_("From Date cannot be after To Date."))
        for row in self.lines:
            row.difference = flt(row.return_amount) - flt(row.financial_amount)
        self.total_return = sum(flt(r.return_amount) for r in self.lines)
        self.total_financial = sum(flt(r.financial_amount) for r in self.lines)
        self.total_difference = flt(self.total_return - self.total_financial, 2)

    def before_submit(self):
        self.status = "Prepared"
