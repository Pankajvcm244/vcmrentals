# Copyright (c) 2024, Aman Soni and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class VcmVehicle(Document):
	def before_save(self):
		self.set_title()

	def set_title(self):
		self.title = f"{self.make} , {self.license_plate}"
