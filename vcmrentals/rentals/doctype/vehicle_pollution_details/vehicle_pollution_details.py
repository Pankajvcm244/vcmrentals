# Copyright (c) 2025, Aman Soni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, get_url_to_form
from frappe.core.doctype.communication.email import make
from frappe.utils import getdate, now_datetime
from frappe.model.naming import make_autoname




class VehiclePollutionDetails(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # e.g., 2507 for July 2025
        prefix = f"VP-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")
	
	



def send_pollution_expiry_reminders():
    print("✅ Function started")
    
    today = nowdate()
    tomorrow = frappe.utils.add_days(today, 1)

    records = frappe.get_all(
        "Vehicle Pollution Details",
        filters={
            "expiry_date": tomorrow,
            "docstatus": 1  # only submitted documents
        },
        fields=["name", "vehicle", "expiry_date"]
    )

    print(f"🔍 Found {len(records)} record(s)")

    for record in records:
        doc = frappe.get_doc("Vehicle Pollution Details", record.name)
        vehicle_doc = frappe.get_doc("VcmVehicle", doc.vehicle)

        recipients = ["aman.soni@vcm.org.in"]  # 👈 change this if needed

        message = f"""
        <h3>🚨 Pollution Certificate Expiry Reminder</h3>
        <p>The Pollution Under Control (PUC) certificate for the following vehicle is expiring on <strong>{doc.expiry_date}</strong>:</p>
        <ul>
            <li><strong>Vehicle ID:</strong> {vehicle_doc.name}</li>
            <li><strong>Make:</strong> {vehicle_doc.make}</li>
            <li><strong>Model:</strong> {vehicle_doc.model}</li>
            <li><strong>License Plate:</strong> {vehicle_doc.license_plate}</li>
            <li><strong>Color:</strong> {vehicle_doc.color}</li>
            <li><strong>Fuel Type:</strong> {vehicle_doc.fuel_type}</li>
            <li><strong>BS Category:</strong> {vehicle_doc.bs_category}</li>
        </ul>
        <p>Please ensure timely renewal to avoid penalties.</p>
        """

        frappe.sendmail(
            recipients=recipients,
            subject=f"PUC Expiry Reminder for Vehicle {vehicle_doc.license_plate}",
            message=message,
        )

        print(f"📧 Email sent for Vehicle: {vehicle_doc.name} ({vehicle_doc.license_plate})")

