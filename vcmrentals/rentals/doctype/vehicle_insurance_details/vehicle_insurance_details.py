# Copyright (c) 2025, Aman Soni and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, add_days, get_url_to_form
from frappe.utils import getdate, now_datetime
from frappe.core.doctype.communication.email import make
from frappe.model.naming import make_autoname




class VehicleInsuranceDetails(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # e.g., 2507 for July 2025
        prefix = f"VI-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")
	
	
def send_insurance_expiry_reminders():
    print("✅ Function started")

    today = nowdate()
    tomorrow = frappe.utils.add_days(today, 1)

    records = frappe.get_all(
        "Vehicle Insurance Details",
        filters={
            "policy_expiry_date": tomorrow,
            "docstatus": 1
        },
        fields=["name", "vehicle", "policy_expiry_date"]
    )

    print(f"🔍 Found {len(records)} record(s)")

    for record in records:
        insurance_doc = frappe.get_doc("Vehicle Insurance Details", record.name)
        vehicle_name = insurance_doc.vehicle

        # Get vehicle details from VcmVehicle Doctype
        vehicle_doc = frappe.get_doc("VcmVehicle", vehicle_name)

        # Construct message
        vehicle_info = f"""
        <b>🚗 Vehicle Details:</b><br>
        <b>Make:</b> {vehicle_doc.make}<br>
        <b>Model:</b> {vehicle_doc.model}<br>
        <b>Fuel Type:</b> {vehicle_doc.fuel_type}<br>
        <b>BS Category:</b> {vehicle_doc.bs_category}<br>
        <b>Color:</b> {vehicle_doc.color}<br>
        <b>License Plate:</b> {vehicle_doc.license_plate}<br>
        <br>
        <b>📅 Insurance Expiry Date:</b> {insurance_doc.policy_expiry_date}
        """

        # Send email
        recipients = ["aman.soni@vcm.org.in"]  # change as needed

        frappe.sendmail(
            recipients=recipients,
            subject=f"Insurance Expiry Reminder for Vehicle {vehicle_doc.license_plate}",
            message=vehicle_info
        )

        print(f"📧 Email sent for Vehicle: {vehicle_doc.license_plate}")

        # Also show popup in UI
        frappe.msgprint(f"""
            <p><b>Insurance Expiry Reminder</b></p>
            {vehicle_info}
        """, title="📢 Expiry Alert", indicator="orange")


