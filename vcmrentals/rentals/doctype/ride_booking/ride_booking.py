import frappe
from frappe import _
from frappe.utils import get_datetime
from frappe.model.document import Document
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.model.naming import make_autoname
from frappe.utils import now_datetime

class RideBooking(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # day-month, e.g., 2507 for 25 July
        prefix = f"RIDE-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")

    def validate(self):
        self.set_start_and_end()
        self.check_vehicle_availability()

        # Send email only if the document is new
        if self.is_new():
            self.send_draft_email()

    def on_update(self):
        if self.ride_status == "Completed":
            self.close_linked_ride_order()

    def set_start_and_end(self):
        if self.date and self.from_time and self.to_time:
            self.starttime = f"{self.date}T{self.from_time}"
            self.endtime = f"{self.date}T{self.to_time}"

    def close_linked_ride_order(self):
        if self.order:
            frappe.db.set_value("Ride Order", self.order, "state", "Close")

    def check_vehicle_availability(self):
        if not (self.vehicle and self.date and self.from_time and self.to_time):
            return

        start_time = get_datetime(f"{self.date} {self.from_time}")
        end_time = get_datetime(f"{self.date} {self.to_time}")

        overlapping_vehicle = frappe.db.sql(
            """
            SELECT name FROM `tabRide Booking`
            WHERE name != %s
              AND vehicle = %s
              AND date = %s
              AND (
                   (%s BETWEEN CONCAT(date,' ',from_time) AND CONCAT(date,' ',to_time))
                OR (%s BETWEEN CONCAT(date,' ',from_time) AND CONCAT(date,' ',to_time))
                OR (CONCAT(date,' ',from_time) BETWEEN %s AND %s)
              )
            """,
            (self.name, self.vehicle, self.date, start_time, end_time, start_time, end_time),
            as_dict=True,
        )
        if overlapping_vehicle:
            frappe.throw(_("This vehicle is already booked for the selected date and time."))

        if self.driver:
            overlapping_driver = frappe.db.sql(
                """
                SELECT name FROM `tabRide Booking`
                WHERE name != %s
                  AND driver = %s
                  AND date = %s
                  AND (
                       (%s BETWEEN CONCAT(date,' ',from_time) AND CONCAT(date,' ',to_time))
                    OR (%s BETWEEN CONCAT(date,' ',from_time) AND CONCAT(date,' ',to_time))
                    OR (CONCAT(date,' ',from_time) BETWEEN %s AND %s)
                  )
                """,
                (self.name, self.driver, self.date, start_time, end_time, start_time, end_time),
                as_dict=True,
            )
            if overlapping_driver:
                frappe.throw(_("This driver is already assigned to another ride during the selected date and time."))

    def send_draft_email(self):
        recipients = [self.customer_email] if self.customer_email else []
        if self.email and self.email not in recipients:
            recipients.append(self.email)

        cc_emails = ["aman.sonimtr@vcm.org.in"]

        subject = f"🚘 Ride Booking Created: {self.name}"

        message = frappe.render_template("""
        <div style="font-family: 'Segoe UI', sans-serif; max-width: 700px; margin: auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden; box-shadow: 0 0 12px rgba(0,0,0,0.05);">
            <div style="background-color: #00796b; color: white; padding: 20px;">
                <h2 style="margin: 0;">🚖 Ride Booking Confirmation</h2>
                <p>Hi {{ doc.customer_name or "Customer" }}, your ride booking has been received!</p>
            </div>

            <div style="padding: 20px;">
                <h3 style="margin-bottom: 10px;">Ride Details</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    {% set fields = [
                        ("📄 Order", doc.order),
                        ("👤 Customer Name", doc.customer_name),
                        ("📞 Customer Number", doc.customer_number),
                        ("📅 Date", doc.date),
                        ("🕒 From Time", doc.from_time),
                        ("🕓 To Time", doc.to_time),
                        ("📍 Pickup Address", doc.pickup_address),
                        ("🏁 Drop Address", doc.drop_address),
                        ("🎨 Color", doc.color),
                        ("🚘 Assigned Vehicle", doc.assign_vehicle_number),
                        ("👨‍✈️ Driver", doc.driver),
                        ("📧 Driver Email", doc.email),
                        ("📱 Driver Mobile", doc.driver_mobile_number)
                    ] %}
                    {% for label, value in fields %}
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>{{ label }}</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;">{{ value or "-" }}</td>
                        </tr>
                    {% endfor %}
                </table>

                <p style="margin-top: 20px;">We'll keep you updated. For any changes, please contact VCM Rentals support.</p>

                <p style="margin-top: 30px;">Safe journey!<br><strong>— Team VCM Rentals</strong></p>
            </div>

            <div style="background-color: #f9f9f9; padding: 10px 20px; text-align: center; font-size: 12px; color: #777;">
                © 2025 VCM Rentals • All rights reserved
            </div>
        </div>
        """, {"doc": self})

        frappe.sendmail(
            recipients=recipients,
            cc=cc_emails,
            subject=subject,
            message=message,
            reference_doctype=self.doctype,
            reference_name=self.name
        )
