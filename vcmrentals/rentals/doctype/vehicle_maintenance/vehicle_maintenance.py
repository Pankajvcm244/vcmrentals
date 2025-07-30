# Copyright (c) 2025, Aman Soni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime
from frappe.model.naming import make_autoname


class VehicleMaintenance(Document):
    def autoname(self):
                today = now_datetime()
                date_prefix = today.strftime("%y%m")  # e.g., 2507 for July 2025
                prefix = f"VM-{date_prefix}-"
                self.name = make_autoname(prefix + ".#####")
    def validate(self):
        owner = self.paid_by_owner_amount or 0
        insurance = self.paid_by_insurance_amount or 0
        total = self.total_amount or 0

        if (owner + insurance) != total:
            frappe.throw(
                "Sum of 'Paid by Owner Amount' and 'Paid by Insurance Amount' must be equal to 'Total Amount'."
            )

	


