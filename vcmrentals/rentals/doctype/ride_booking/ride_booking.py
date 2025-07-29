
import frappe
from frappe import _
from frappe.utils import get_datetime, now_datetime
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class RideBooking(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # e.g., 2507 for July 2025
        prefix = f"RIDE-CON-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")

    # def validate(self):
    #     self.set_start_and_end()
    #     self.check_vehicle_availability()

    #     # Send email only if the document is new
    #     if self.is_new():
    #         self.send_draft_email()
    def validate(self):
        self.set_start_and_end()
        self.check_vehicle_availability()
        self.validate_odometer_start()
        self.check_vehicle_assignment()


        # Send email only if the document is new
        if self.is_new():
            self.send_draft_email()

    def before_save(self):
        self.set_info_field()

    # def before_save(self):
    #     def before_save(self):
    #         self.set_info_field()

    #     self.starttime = f"{self.date}T{self.from_time}"
    #     self.endtime = f"{self.date}T{self.to_time}"
  

    def on_update(self):
        if self.ride_status == "Completed":
            self.close_linked_ride_order()
            self.send_completion_email()


    def set_start_and_end(self):
        if self.date and self.from_time and self.to_time:
            self.starttime = f"{self.date}T{self.from_time}"
            self.endtime = f"{self.date}T{self.to_time}"

    def close_linked_ride_order(self):
        if self.order:
            frappe.db.set_value("Ride Order", self.order, "state", "Close")



    def check_vehicle_availability(self):
        if not (self.vehicle and self.date and self.trip_end_date and self.from_time and self.to_time):
            return

        start_time = get_datetime(f"{self.date} {self.from_time}")
        end_time = get_datetime(f"{self.trip_end_date} {self.to_time}")

        # --- Vehicle Overlap Check ---
        overlapping_vehicle = frappe.db.sql("""
            SELECT name FROM `tabRide Booking`
            WHERE name != %s
            AND vehicle = %s
            AND (
                (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(trip_end_date, ' ', to_time))
                OR (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(trip_end_date, ' ', to_time))
                OR (CONCAT(date, ' ', from_time) BETWEEN %s AND %s)
                OR (CONCAT(trip_end_date, ' ', to_time) BETWEEN %s AND %s)
            )
        """, (self.name, self.vehicle, start_time, end_time, start_time, end_time, start_time, end_time), as_dict=True)

        if overlapping_vehicle:
            frappe.throw(_("This vehicle is already booked for the selected date and time range."))

        # --- Driver Overlap Check ---
        if self.driver:
            overlapping_driver = frappe.db.sql("""
                SELECT name FROM `tabRide Booking`
                WHERE name != %s
                AND driver = %s
                AND (
                    (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(trip_end_date, ' ', to_time))
                    OR (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(trip_end_date, ' ', to_time))
                    OR (CONCAT(date, ' ', from_time) BETWEEN %s AND %s)
                    OR (CONCAT(trip_end_date, ' ', to_time) BETWEEN %s AND %s)
                )
            """, (self.name, self.driver, start_time, end_time, start_time, end_time, start_time, end_time), as_dict=True)

            if overlapping_driver:
                frappe.throw(_("This driver is already assigned to another ride during the selected date and time range."))
    
    def _build_cc_list(self):
            try:
                settings = frappe.get_cached_doc("Vehicle Booking Settings")
            except frappe.DoesNotExistError:
                return []

            cc = []
            if settings.enable_email == "Yes" and settings.ride_order_cc:
                cc = [email.strip() for email in settings.ride_order_cc.split(",") if email.strip()]
            return cc


        
    def send_draft_email(self):
        try:
            settings = frappe.get_cached_doc("Vehicle Booking Settings")
        except frappe.DoesNotExistError:
            return

        if settings.enable_email != "Yes":
            return

        recipients = [self.customer_email] if self.customer_email else []
        if self.email and self.email not in recipients:
            recipients.append(self.email)

        cc_emails = self._build_cc_list()

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
    def send_completion_email(self):
        if not self.customer_email:
            return

        subject = f"✅ Ride Completed: {self.name}"

        message = frappe.render_template("""
        <div style="font-family: 'Segoe UI', sans-serif; max-width: 700px; margin: auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden; box-shadow: 0 0 12px rgba(0,0,0,0.05);">
            <div style="background-color: #4caf50; color: white; padding: 20px;">
                <h2 style="margin: 0;">🎉 Ride Completed</h2>
                <p>Hi {{ doc.customer_name or "Customer" }}, your ride has been successfully completed!</p>
            </div>

            <div style="padding: 20px;">
                <h3>Thank you for riding with us 🚖</h3>
                <p>Your ride from <strong>{{ doc.pickup_address }}</strong> to <strong>{{ doc.drop_address }}</strong> on <strong>{{ doc.date }}</strong> has been closed by the driver.</p>

                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <tr><td style="padding: 8px;"><strong>Vehicle</strong></td><td style="padding: 8px;">{{ doc.assign_vehicle_number or "-" }}</td></tr>
                    <tr><td style="padding: 8px;"><strong>Driver</strong></td><td style="padding: 8px;">{{ doc.driver or "-" }}</td></tr>
                    <tr><td style="padding: 8px;"><strong>Driver Mobile</strong></td><td style="padding: 8px;">{{ doc.driver_mobile_number or "-" }}</td></tr>
                    <tr><td style="padding: 8px;"><strong>Ride ID</strong></td><td style="padding: 8px;">{{ doc.name }}</td></tr>
                </table>

                <p style="margin-top: 20px;">If you have any questions or feedback, feel free to reach out.</p>
                <p>Thanks again for choosing <strong>VCM Rentals</strong>!</p>

                <p style="margin-top: 30px;">Warm regards,<br><strong>Team VCM Rentals</strong></p>
            </div>

            <div style="background-color: #f1f1f1; padding: 10px 20px; text-align: center; font-size: 12px; color: #555;">
                © 2025 VCM Rentals • All rights reserved
            </div>
        </div>
        """, {"doc": self})

        frappe.sendmail(
            recipients=[self.customer_email],
            subject=subject,
            message=message,
            reference_doctype=self.doctype,
            reference_name=self.name
        )

    def validate_odometer_start(self):
        if self.vehicle and self.odometer_start is not None:
            last_ride = frappe.db.get_value(
                "Ride Booking",
                {
                    "vehicle": self.vehicle,
                    "name": ["!=", self.name]  # exclude current record
                },
                ["name", "odometer_end"],
                order_by="creation desc"
            )

            if last_ride and last_ride[1] is not None:
                last_ride_name, last_odometer_end = last_ride
                if self.odometer_start < last_odometer_end:
                    frappe.throw(
                        _("Odometer Start ({}) must be greater than or equal to last Odometer End ({}) from previous ride: {}").format(
                            self.odometer_start, last_odometer_end, last_ride_name
                        )
                    )
    def set_info_field(self):
        lines = []

        if self.customer_name:
            lines.append(self.customer_name)

        if self.customer_number:
            lines.append(str(self.customer_number))

        if self.date:
            lines.append(f"Start Date: {self.date}")

        if self.trip_end_date:
            lines.append(f"End Date: {self.trip_end_date}")

        if self.vehicle:
            lines.append(f"{self.vehicle_title}")

        if self.driver:
            lines.append(f"Driver: {self.assigned_driver}")

        self.info = "\n".join(lines)


    def check_vehicle_assignment(self):
        if self.vehicle and self.ride_status != "Completed":
            existing = frappe.get_all(
                "Ride Booking",  # ✅ Use correct Doctype
                filters={
                    "name": ["!=", self.name],
                    "vehicle": self.vehicle,
                    "ride_status": ["!=", "Completed"]
                },
                fields=["name"]
            )

            if existing:
                frappe.throw(f"Vehicle is already assigned in Ride Booking {existing[0].name} which is not completed.")

