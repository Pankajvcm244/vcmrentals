
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime
from frappe.model.naming import make_autoname
from frappe.utils import getdate, nowdate

from vcmrentals.rentals.doctype.ride_order.ridealm.ride import (
    assign_and_notify_next_ride_authority,
    get_preq_ride_level,
)


class RideOrder(Document):
    def autoname(self):
        today = now_datetime()
        date_prefix = today.strftime("%y%m")  # e.g., 2507 for July 2025
        prefix = f"RIDE-REQ-{date_prefix}-"
        self.name = make_autoname(prefix + ".#####")

    def before_save(self):
        self.refresh_alm()

    def validate(self):
        if self.date:
            trip_start = getdate(self.date)
            today = getdate(nowdate())

            # Check if trip_start is before today
            if trip_start < today:
                frappe.throw("Trip Start Date cannot be before today")

        if self.date and self.trip_end_date:
            trip_start = getdate(self.date)
            trip_end = getdate(self.trip_end_date)

            if trip_end < trip_start:
                frappe.throw("Trip End Date cannot be before Trip Start Date")



    # def validate(self):
    #     if self.date and self.trip_end_date:
    #         trip_start = getdate(self.date)
    #         trip_end = getdate(self.trip_end_date)

    #         if trip_end < trip_start:
    #             frappe.throw("Trip End Date cannot be before Trip Start Date")

    def after_insert(self):
        self.send_draft_email()

    def on_update(self):
        if self.workflow_state == "Rejected":
            self.send_rejection_email()

        if self.workflow_state == "Trashed":
            self.send_cancellation_email()
            

        if self.workflow_state == "Pending":
            self.send_workflow_update_emails()
            

        if self.is_new():
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
            # If no ALM level is configured, set workflow state to Final Level Approved
            # self.workflow_state = "Final Level Approved"
            return

        self.l1_approving_authority = alm_level.l1_approver
        self.l2_approving_authority = alm_level.l2_approver
        self.l3_approving_authority = alm_level.l3_approver
        self.final_approving_authority = alm_level.final_approver


    # def refresh_alm(self):
    #     if not self.department:
    #         frappe.throw("Department is not set.")
    #     alm_level = get_preq_ride_level(self)
    #     if not alm_level:
    #         frappe.throw("ALM Levels are not set for this document.")
    #     self.l1_approving_authority = alm_level.l1_approver
    #     self.l2_approving_authority = alm_level.l2_approver
    #     self.l3_approving_authority = alm_level.l3_approver
    #     self.final_approving_authority = alm_level.final_approver



    def _build_cc_list(self):
        try:
            settings = frappe.get_cached_doc("Vehicle Booking Settings")
        except frappe.DoesNotExistError:
            return [self.email] if self.email else []

        cc = []
        if settings.enable_email == "Yes" and settings.ride_order_cc:
            cc = [email.strip() for email in settings.ride_order_cc.split(",") if email.strip()]

        if self.email:
            cc.append(self.email)

        return cc

    def send_draft_email(self):
        settings = frappe.get_cached_doc("Vehicle Booking Settings")
        if settings.enable_email != "Yes":
            return

        frappe.sendmail(
            recipients=[self.email] if self.email else [],
            cc=self._build_cc_list(),
            subject=f"Ride Request Received - {self.name}",
            message=frappe.render_template(
                """
                <div style="font-family: 'Segoe UI', sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                    <div style="background-color: #00bfa5; color: white; padding: 20px;">
                        <h2 style="margin: 0;">Ride Request 🚘</h2>
                        <p style="margin: 5px 0 0;">Hare Krishna {{ doc.user_name or "Guest" }},</p>
                    </div>

                    <div style="padding: 20px;">
                        <p>We’ve received your request for ride <strong>{{ doc.name }}</strong>. Our team will confirm your booking shortly.</p>

                        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                            <tr><td style="padding: 8px;">📅 <strong>Trip Start Date</strong></td><td>{{ doc.date }}</td></tr>
                            <tr><td style="padding: 8px;">📅 <strong>Trip End Date</strong></td><td>{{ doc.trip_end_date }}</td></tr>
                            <tr><td style="padding: 8px;">🕒 <strong>Pickup Time</strong></td><td>{{ doc.pickup_time }}</td></tr>
                            <tr><td style="padding: 8px;">🕒 <strong>Drop Time</strong></td><td>{{ doc.drop_time }}</td></tr>
                            <tr><td style="padding: 8px;">🏢 <strong>Department</strong></td><td>{{ doc.department }}</td></tr>
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
        settings = frappe.get_cached_doc("Vehicle Booking Settings")
        if settings.enable_email != "Yes":
            return

        frappe.sendmail(
            recipients=[self.email] if self.email else [],
            cc=self._build_cc_list(),
            subject=f"Ride {self.name} Confirmed - VCM Rentals",
            message=frappe.render_template(
                """
                <div style="font-family: 'Segoe UI', sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                    <div style="background-color: #00bfa5; color: white; padding: 20px;">
                        <h2 style="margin: 0;">Ride Confirmed ✅</h2>
                        <p style="margin: 5px 0 0;">Hare Krishna {{ doc.user_name or "Guest" }},</p>
                    </div>

                    <div style="padding: 20px;">
                        <p>Your ride <strong>{{ doc.name }}</strong> has been <span style="color: green;"><strong>CONFIRMED</strong></span>.</p>

                        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                            <tr><td style="padding: 8px;">📅 <strong>Trip Start Date</strong></td><td>{{ doc.date }}</td></tr>
                            <tr><td style="padding: 8px;">📅 <strong>Trip End Date:</strong></td><td>{{ doc.trip_end_date }}</td></tr>
                            <tr><td style="padding: 8px;">🕒 <strong>Pickup Time</strong></td><td>{{ doc.pickup_time }}</td></tr>
                            <tr><td style="padding: 8px;">🕓 <strong>Drop Time</strong></td><td>{{ doc.drop_time }}</td></tr>
                            <tr><td style="padding: 8px;">🏢 <strong>Department</strong></td><td>{{ doc.department }}</td></tr>
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
    def send_rejection_email(self):
            settings = frappe.get_cached_doc("Vehicle Booking Settings")
            if settings.enable_email != "Yes":
                return

            frappe.sendmail(
                recipients=[self.email] if self.email else [],
                cc=self._build_cc_list(),
                subject=f"Ride Request {self.name} - Rejected ❌",
                message=frappe.render_template(
                    """
                    <div style="font-family: 'Segoe UI', sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                        <div style="background-color: #d32f2f; color: white; padding: 20px;">
                            <h2 style="margin: 0;">Ride Request Rejected ❌</h2>
                            <p style="margin: 5px 0 0;">Hare Krishna {{ doc.user_name or "User" }},</p>
                        </div>

                        <div style="padding: 20px;">
                            <p>We're sorry to inform you that your ride request <strong>{{ doc.name }}</strong> has been <strong>rejected</strong>.</p>

                            {% if doc.rejection_reason %}
                                <p><strong>Reason:</strong> {{ doc.rejection_reason }}</p>
                            {% endif %}

                            <p style="margin-top: 20px;">Please contact support if you have any questions.<br><strong>— Team VCM Rentals</strong></p>
                        </div>

                        <div style="background-color: #f9f9f9; padding: 10px 20px; text-align: center; font-size: 12px; color: #999;">
                            © 2025 VCM Rentals • All rights reserved
                        </div>
                    </div>
                    """,
                    {"doc": self}
                )
            )
    def send_workflow_update_emails(self):
        """Send email to all non-empty approving authorities on workflow state change."""
        approvers = [
            self.l1_approving_authority,
            self.l2_approving_authority,
            self.l3_approving_authority,
            self.final_approving_authority,
        ]

        recipients = [email for email in approvers if email]

        if not recipients:
            return

        subject = f"Ride Order {self.name} – Workflow Updated to {self.workflow_state}"
        message = frappe.render_template(
            """
            <div style="font-family: 'Segoe UI', sans-serif; max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.06);">
                <div style="background-color: #00695c; color: white; padding: 20px;">
                    <h2 style="margin: 0;">Ride Order Update 🚘</h2>
                    <p style="margin: 4px 0 0;">Ride ID: <strong>{{ doc.name}}</strong></p>
                </div>

                <div style="padding: 20px; color: #333;">
                    <p>Dear Approver,</p>
                    <p>The workflow status for this ride has changed to:</p>
                    <p style="background-color: #e0f2f1; padding: 10px; border-left: 5px solid #00796b; font-weight: bold;">
                        {{ doc.workflow_state }}
                    </p>

                    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
                        <tr><td style="padding: 6px;"><strong>Trip Start Date:</strong></td><td>{{ doc.date }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Trip End Date:</strong></td><td>{{ doc.trip_end_date }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Pickup Time:</strong></td><td>{{ doc.pickup_time }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Pickup Address:</strong></td><td>{{ doc.pickup_address }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Drop Address:</strong></td><td>{{ doc.drop_address }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Vehicle Type:</strong></td><td>{{ doc.vehicle_type }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Ride Type:</strong></td><td>{{ doc.ride_type }}</td></tr>
                    </table>

                    <p style="margin-top: 20px;">Please log in to the system to take necessary action.</p>
                </div>

                <div style="background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                    © 2025 VCM Rentals • All Rights Reserved
                </div>
            </div>
            """,
            {"doc": self}
        )

        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message,
            # cc=self._build_cc_list()
        )

    def send_cancellation_email(self):
        """Send email when user cancels the ride (workflow_state = Trashed)."""
        if not self.email:
            return  # no recipient

        subject = f"Ride Booking {self.name} – Cancelled 🗑️"
        message = frappe.render_template(
            """
            <div style="font-family: 'Segoe UI', sans-serif; max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
                <div style="background-color: #b71c1c; color: white; padding: 20px;">
                    <h2 style="margin: 0;">Ride Cancelled 🚘</h2>
                    <p style="margin: 4px 0 0;">Ride ID: <strong>{{ doc.name }}</strong></p>
                </div>

                <div style="padding: 20px; color: #333;">
                    <p>Dear {{ doc.user_name or "User" }},</p>
                    <p>Your ride booking <strong>{{ doc.name }}</strong> has been successfully <strong>cancelled</strong>.</p>

                    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
                        <tr><td style="padding: 6px;"><strong>Trip Start Date:</strong></td><td>{{ doc.date }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Trip End Date:</strong></td><td>{{ doc.trip_end_date }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Pickup Time:</strong></td><td>{{ doc.pickup_time }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Drop Time:</strong></td><td>{{ doc.drop_time }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Department:</strong></td><td>{{ doc.department }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Pickup Address:</strong></td><td>{{ doc.pickup_address }}</td></tr>
                        <tr><td style="padding: 6px;"><strong>Drop Address:</strong></td><td>{{ doc.drop_address }}</td></tr>
                    </table>

                    <p style="margin-top: 20px;">If this was a mistake, please create a new booking.</p>
                </div>

                <div style="background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                    © 2025 VCM Rentals • All Rights Reserved
                </div>
            </div>
            """,
            {"doc": self}
        )

        frappe.sendmail(
            recipients=[self.email],
            cc=self._build_cc_list(),
            subject=subject,
            message=message
        )


