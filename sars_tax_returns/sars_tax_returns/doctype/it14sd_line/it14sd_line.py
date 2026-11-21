import frappe
from frappe.model.document import Document
from frappe.utils import flt

class IT14SDLine(Document):
    def validate(self):
        self.difference = flt(self.return_amount) - flt(self.financial_amount)
