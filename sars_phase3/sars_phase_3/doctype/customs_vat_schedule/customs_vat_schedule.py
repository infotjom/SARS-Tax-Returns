import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class CustomsVATSchedule(Document):
    def validate(self):
        if self.period_start and self.period_end and self.period_start > self.period_end:
            frappe.throw(_("Period Start cannot be after Period End."))
        self.total_customs_value = sum(flt(r.customs_value) for r in self.lines)
        self.total_customs_duty = sum(flt(r.customs_duty) for r in self.lines)
        self.total_import_vat = sum(flt(r.import_vat) for r in self.lines)
        self.total_diesel_litres = sum(flt(r.diesel_litres) for r in self.lines)
        self.total_diesel_refund = sum(flt(r.diesel_refund) for r in self.lines)

    def before_submit(self):
        self.status = "Prepared"
