# Copyright (c) 2025, Aman Soni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, getdate, now_datetime
from frappe.model.naming import make_autoname


class VehiclePollutionDetails(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # e.g., 2507 for July 2025
        prefix = f"VP-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")

