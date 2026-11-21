import frappe
from frappe.model.document import Document
from frappe.utils import flt

class DividendBeneficiary(Document):
    def validate(self):
        self.taxable_dividend = flt(self.gross_dividend) - flt(self.exempt_dividend)
        self.withholding_tax = 0
        self.net_dividend = flt(self.taxable_dividend)
