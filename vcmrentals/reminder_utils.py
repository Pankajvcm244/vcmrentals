import frappe
from frappe.utils import getdate, nowdate

# Common styled template
def build_card(title, content_html, days_left, expiry_label, expiry_date):
    return f"""
    <style>
        .reminder-card {{
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
            background: #f9f9f9;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }}
        .reminder-card h3 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .reminder-card p, .reminder-card li {{
            margin: 4px 0;
        }}
        .label {{
            font-weight: bold;
            color: #000;
        }}
    </style>

    <div class="reminder-card">
        <h3>{title}</h3>
        {content_html}
        <br>
        <p><span class="label">{expiry_label}:</span> <strong>{expiry_date}</strong></p>
        <p style="color:red; font-weight:bold;">
            ⚠️ Reminder: Expiry in {days_left} day(s). Please renew on time.
        </p>
    </div>
    """

@frappe.whitelist()
def send_insurance_expiry_reminders():
    today = nowdate()
    settings = frappe.get_single("Vehicle Booking Settings")
    cc_emails = [email.strip() for email in settings.ride_order_cc.split(",") if email.strip()] if settings.ride_order_cc else []

    records = frappe.get_all(
        "Vehicle Insurance Details",
        filters={"docstatus": 1},
        fields=["name", "vehicle", "policy_expiry_date"],
        ignore_permissions=True
    )

    sent_count = 0
    for record in records:
        expiry_date = record.policy_expiry_date
        days_left = (getdate(expiry_date) - getdate(today)).days

        if days_left in [30, 15, 7] or (0 <= days_left <= 6):
            insurance_doc = frappe.get_doc("Vehicle Insurance Details", record.name, ignore_permissions=True)
            vehicle_doc = frappe.get_doc("VcmVehicle", insurance_doc.vehicle, ignore_permissions=True)

            content_html = f"""
            <ul>
                <li><span class="label">Make:</span> {vehicle_doc.make}</li>
                <li><span class="label">Model:</span> {vehicle_doc.model}</li>
                <li><span class="label">Fuel Type:</span> {vehicle_doc.fuel_type}</li>
                <li><span class="label">BS Category:</span> {vehicle_doc.bs_category}</li>
                <li><span class="label">Color:</span> {vehicle_doc.color}</li>
                <li><span class="label">License Plate:</span> {vehicle_doc.license_plate}</li>
            </ul>
            """
            message = build_card("🚗 Vehicle Insurance Expiry Reminder", content_html, days_left, "Insurance Expiry Date", insurance_doc.policy_expiry_date)

            frappe.sendmail(
                recipients=["aman.soni@vcm.org.in"],
                cc=cc_emails,
                subject=f"Insurance Expiry Reminder ({days_left} days left) for Vehicle {vehicle_doc.license_plate}",
                message=message
            )
            frappe.msgprint(message, title="📢 Insurance Expiry Alert", indicator="orange")
            sent_count += 1

    return f"📧 Sent {sent_count} insurance expiry reminder(s) today"


@frappe.whitelist()
def send_pollution_expiry_reminders():
    today = nowdate()
    settings = frappe.get_single("Vehicle Booking Settings")
    cc_emails = [email.strip() for email in settings.ride_order_cc.split(",") if email.strip()] if settings.ride_order_cc else []

    records = frappe.get_all(
        "Vehicle Pollution Details",
        filters={"docstatus": 1},
        fields=["name", "vehicle", "expiry_date"],
        ignore_permissions=True
    )

    sent_count = 0
    for record in records:
        expiry_date = record.expiry_date
        days_left = (getdate(expiry_date) - getdate(today)).days

        if days_left in [30, 15, 7] or (0 <= days_left <= 6):
            pollution_doc = frappe.get_doc("Vehicle Pollution Details", record.name, ignore_permissions=True)
            vehicle_doc = frappe.get_doc("VcmVehicle", pollution_doc.vehicle, ignore_permissions=True)

            content_html = f"""
            <ul>
                <li><span class="label">Vehicle ID:</span> {vehicle_doc.name}</li>
                <li><span class="label">Make:</span> {vehicle_doc.make}</li>
                <li><span class="label">Model:</span> {vehicle_doc.model}</li>
                <li><span class="label">License Plate:</span> {vehicle_doc.license_plate}</li>
                <li><span class="label">Color:</span> {vehicle_doc.color}</li>
                <li><span class="label">Fuel Type:</span> {vehicle_doc.fuel_type}</li>
                <li><span class="label">BS Category:</span> {vehicle_doc.bs_category}</li>
            </ul>
            """
            message = build_card("🚨 Pollution Certificate Expiry Reminder", content_html, days_left, "Expiry Date", pollution_doc.expiry_date)

            frappe.sendmail(
                recipients=["aman.soni@vcm.org.in"],
                cc=cc_emails,
                subject=f"PUC Expiry Reminder ({days_left} days left) for Vehicle {vehicle_doc.license_plate}",
                message=message
            )
            frappe.msgprint(message, title="📢 Pollution Expiry Alert", indicator="orange")
            sent_count += 1

    return f"📧 Sent {sent_count} pollution expiry reminder(s) today"


@frappe.whitelist()
def send_driver_license_expiry_reminders():
    today = nowdate()
    settings = frappe.get_single("Vehicle Booking Settings")
    cc_emails = [email.strip() for email in settings.ride_order_cc.split(",") if email.strip()] if settings.ride_order_cc else []

    records = frappe.get_all(
        "Vehicle Driver",
        filters={"disable": 0, "driver_license_expiry_date": ["!=", None]},
        fields=["name", "driver_name", "driver_license_expiry_date", "driver_license_number", "mobile", "email"],
        ignore_permissions=True
    )

    sent_count = 0
    for record in records:
        expiry_date = record.driver_license_expiry_date
        if not expiry_date:
            continue

        days_left = (getdate(expiry_date) - getdate(today)).days

        if days_left in [30, 15, 7] or (0 <= days_left <= 6):
            driver_doc = frappe.get_doc("Vehicle Driver", record.name, ignore_permissions=True)

            content_html = f"""
            <ul>
                <li><span class="label">Driver Name:</span> {driver_doc.driver_name}</li>
                <li><span class="label">License Number:</span> {driver_doc.driver_license_number}</li>
                <li><span class="label">Mobile:</span> {driver_doc.mobile}</li>
                <li><span class="label">Email:</span> {driver_doc.email}</li>
            </ul>
            """
            message = build_card("🚨 Driver License Expiry Reminder", content_html, days_left, "Expiry Date", driver_doc.driver_license_expiry_date)

            recipients = [driver_doc.email] if driver_doc.email else ["aman.soni@vcm.org.in"]

            frappe.sendmail(
                recipients=recipients,
                cc=cc_emails,
                subject=f"Driver License Expiry Reminder ({days_left} days left) for {driver_doc.driver_name}",
                message=message
            )
            frappe.msgprint(message, title="📢 Driver License Expiry Alert", indicator="orange")
            sent_count += 1

    return f"📧 Sent {sent_count} driver license expiry reminder(s) today"
