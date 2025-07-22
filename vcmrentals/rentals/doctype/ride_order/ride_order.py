import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import now_datetime

from vcmrentals.rentals.doctype.ride_order.ridealm.ride import (
    assign_and_notify_next_ride_authority,
    get_preq_ride_level,
)

BOOKING_CC = ["aman.soni@vcm.org.in"]

class RideOrder(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # day-month, e.g., 2507 for 25 July
        prefix = f"ORDER-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")
    


    def before_save(self):
        self.refresh_alm()

    def after_insert(self):
        self.send_draft_email()

    def on_update(self):
        if self.is_new() and self.status == "Pending":
            self.send_approval_email_to_manager()
        assign_and_notify_next_ride_authority(self)

    def on_submit(self):
        if self.docstatus == 1:
            self.send_confirm_email()

    def refresh_alm(self):
        if not self.department:
            frappe.throw("Department is not set.")
        alm_level = get_preq_ride_level(self)
        if not alm_level:
            frappe.throw("ALM Levels are not set for this document.")
        self.l1_approving_authority = alm_level.l1_approver
        self.l2_approving_authority = alm_level.l2_approver
        self.l3_approving_authority = alm_level.l3_approver
        self.final_approving_authority = alm_level.final_approver

    def _build_cc_list(self):
        cc = BOOKING_CC.copy()
        if self.email:
            cc.append(self.email)
        return cc

    def send_draft_email(self):
        frappe.sendmail(
            recipients=[self.email] if self.email else BOOKING_CC,
            cc=self._build_cc_list(),
            subject=f"Ride Request Received - {self.name}",
            message=frappe.render_template(
                """
                <div style="font-family: 'Segoe UI', sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                    <div style="background-color: #00bfa5; color: white; padding: 20px;">
                        <h2 style="margin: 0;">Ride Request 📥</h2>
                        <p style="margin: 5px 0 0;">Hi {{ doc.user_name or "Guest" }},</p>
                    </div>

                    <div style="padding: 20px;">
                        <p>We’ve received your request for ride <strong>{{ doc.name }}</strong>. Our team will confirm your booking shortly.</p>

                        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                            <tr><td style="padding: 8px;">📅 <strong>Date</strong></td><td>{{ doc.date }}</td></tr>
                            <tr><td style="padding: 8px;">🕒 <strong>Pickup Time</strong></td><td>{{ doc.pickup_time }}</td></tr>
                            <tr><td style="padding: 8px;">🚘 <strong>Vehicle Type</strong></td><td>{{ doc.vehicle_type }}</td></tr>
                            <tr><td style="padding: 8px;">📍 <strong>Pickup Address</strong></td><td>{{ doc.pickup_address }}</td></tr>
                            <tr><td style="padding: 8px;">📌 <strong>Drop Address</strong></td><td>{{ doc.drop_address }}</td></tr>
                            {% if doc.intermediate_stop %}
                            <tr><td style="padding: 8px;">⏸️ <strong>Intermediate Stop</strong></td><td>{{ doc.intermediate_stop }}</td></tr>
                            {% endif %}
                            <tr><td style="padding: 8px;">🎯 <strong>Ride Type</strong></td><td>{{ doc.ride_type }}</td></tr>
                        </table>

                        <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">


                        <p style="margin-top: 20px;">You’ll receive another email once your ride is confirmed.<br><strong>— Team VCM Rentals</strong></p>
                    </div>

                    <div style="background-color: #f9f9f9; padding: 10px 20px; text-align: center; font-size: 12px; color: #999;">
                        © 2025 VCM Rentals • All rights reserved
                    </div>
                </div>
                """,
                {"doc": self}
            ),
        )

    def send_confirm_email(self):
        frappe.sendmail(
            recipients=[self.email] if self.email else BOOKING_CC,
            cc=self._build_cc_list(),
            subject=f"Ride {self.name} Confirmed - VCM Rentals",
            message=frappe.render_template(
                """
                <div style="font-family: 'Segoe UI', sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                    <div style="background-color: #00bfa5; color: white; padding: 20px;">
                        <h2 style="margin: 0;">Ride Confirmed ✅</h2>
                        <p style="margin: 5px 0 0;">Hi {{ doc.user_name or "Guest" }},</p>
                    </div>

                    <div style="padding: 20px;">
                        <p>Your ride <strong>{{ doc.name }}</strong> has been <span style="color: green;"><strong>CONFIRMED</strong></span>.</p>

                        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                            <tr><td style="padding: 8px;">📅 <strong>Date</strong></td><td>{{ doc.date }}</td></tr>
                            <tr><td style="padding: 8px;">🕒 <strong>Pickup Time</strong></td><td>{{ doc.pickup_time }}</td></tr>
                            <tr><td style="padding: 8px;">🕓 <strong>Drop Time</strong></td><td>{{ doc.drop_time }}</td></tr>
                            <tr><td style="padding: 8px;">🚘 <strong>Vehicle Type</strong></td><td>{{ doc.vehicle_type }}</td></tr>
                            <tr><td style="padding: 8px;">📍 <strong>Pickup Address</strong></td><td>{{ doc.pickup_address }}</td></tr>
                            <tr><td style="padding: 8px;">📌 <strong>Drop Address</strong></td><td>{{ doc.drop_address }}</td></tr>
                            {% if doc.intermediate_stop %}
                            <tr><td style="padding: 8px;">⏸️ <strong>Intermediate Stop</strong></td><td>{{ doc.intermediate_stop }}</td></tr>
                            {% endif %}
                            
                        </table>

                        <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">


                        <p style="margin-top: 20px;">Have a safe and pleasant journey!<br><strong>— Team VCM Rentals</strong></p>
                    </div>

                    <div style="background-color: #f9f9f9; padding: 10px 20px; text-align: center; font-size: 12px; color: #999;">
                        © 2025 VCM Rentals • All rights reserved
                    </div>
                </div>
                """,
                {"doc": self}
            ),
        )
