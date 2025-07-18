# import frappe
# from frappe.model.document import Document
# from frappe.utils import get_url, nowdate
# import os

# class RideOrder(Document):
#     # def validate(self):
#     #     if self.is_new():
#     #         self.send_approval_email_to_manager()
#     #     elif self.has_status_changed():
#     #         self.send_status_update_email()
#     def validate(self):
#         if self.is_new() and self.status == "Pending":
#             self.send_approval_email_to_manager()
#         elif self.has_status_changed():
#             self.send_status_update_email()


#     def has_status_changed(self):
#         old_status = frappe.db.get_value("Ride Order", self.name, "status")
#         return old_status != self.status

#     def send_approval_email_to_manager(self):
#         try:
#             #  Load HTML from your path
#             html_path = os.path.join(
#                 frappe.get_app_path("vcmrentals"),
#                 "rentals", "doctype", "ride_order", "ride_order.html"
#             )
#             with open(html_path, "r") as f:
#                 html_template = f.read()

#             # accept_link = f"{get_url()}/api/method/vcmrentals.api.update_ride_order_status?ride_order_id={self.name}&status=Accepted"
#             # reject_link = f"{get_url()}/api/method/vcmrentals.api.update_ride_order_status?ride_order_id={self.name}&status=Rejected"

#             html = html_template\
#                 .replace("{{ name }}", self.name)\
#                 .replace("{{ employee_name }}", self.employee_name or "")\
#                 .replace("{{ employee_code }}", self.employee_code or "")\
#                 .replace("{{ contact_number }}", self.contact_number or "")\
#                 .replace("{{ emp_department }}", self.emp_department or "")\
#                 .replace("{{ email }}", self.email or "")\
#                 .replace("{{ date }}", str(self.date) or "")\
#                 .replace("{{ pickup_time }}", self.pickup_time or "")\
#                 .replace("{{ drop_time }}", self.drop_time or "")\
#                 .replace("{{ ride_type }}", self.ride_type or "")\
#                 .replace("{{ vehicle_type }}", self.vehicle_type or "")\
#                 .replace("{{ pickup_address }}", self.pickup_address or "")\
#                 .replace("{{ drop_address }}", self.drop_address or "")\
#                 .replace("{{ current_year }}", str(nowdate().split("-")[0]))

#             frappe.sendmail(
#                 recipients=[self.manager_email],
#                 cc=["amansonimtr@gmail.com"],
#                 subject=f"Approval Required: Ride Order {self.name}",
#                 message=html
#             )
#         except Exception as e:
#             frappe.log_error(message=str(e), title="Approval Email Sending Failed")

#     def send_status_update_email(self):
#         status_message = f"Your ride order <b>{self.name}</b> has been <b>{self.status}</b>."
#         try:
#             frappe.sendmail(
#                 recipients=[self.email],
#                 cc=["aman.soni@vcm.org.in", "amansonimtr@gmail.com"],
#                 subject=f"Ride Order {self.status}: {self.name}",
#                 message=status_message
#             )
#         except Exception as e:
#             frappe.log_error(message=str(e), title="Status Update Email Failed")











# # Copyright (c) 2025, pankaj.sharma@vcm.org.in and contributors
# # For license information, please see license.txt

# import frappe
# import datetime
# from frappe.model.document import Document
# from frappe.model.naming import getseries
# from frappe.utils import nowdate, getdate


# from vcmrentals.rentals.doctype.ride_order.ridealm.ride import (
#     assign_and_notify_next_ride_authority,
#     get_preq_ride_level,
# )

# from frappe.workflow.doctype.workflow_action.workflow_action import (
#     get_doc_workflow_state,
# )


# class RideOrder(Document):

#     def before_save(self):
#         #self.update_extra_description_from_mrn()
#         self.refresh_alm()
        

#     def on_update(self):
#         assign_and_notify_next_ride_authority(self)

#     def refresh_alm(self):
#         #logging.debug(f"in PREQ refresh_preq_alm")
#         if hasattr(self, "department") and self.department == "":
#             frappe.throw("Department is not set.")
#         alm_level = get_preq_ride_level(self)
#         if alm_level is not None:
#             self.l1_approving_authority = alm_level.l1_approver
#             self.l2_approving_authority = alm_level.l2_approver
#             self.l3_approving_authority = alm_level.l3_approver
#             self.final_approving_authority = alm_level.final_approver
#             #logging.debug(f"in PREQ refresh_preq_alm {self.name}, {self.l1_approving_authority}, {self.l2_approving_authority}, {self.l3_approving_authority}, {self.final_approving_authority}")
#         else:
#             frappe.throw("ALM Levels are not set for Payment Req in this document")



    


import frappe
from frappe.model.document import Document

import frappe
import datetime
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils import nowdate, getdate


from vcmrentals.rentals.doctype.ride_order.ridealm.ride import (
    assign_and_notify_next_ride_authority,
    get_preq_ride_level,
)

from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
)


BOOKING_CC = ["aman.soni@vcm.org.in"]

class RideOrder(Document):
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
        if self.status == "Approved":
            self.send_final_approval_email()

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
            subject=f"Thanks for booking {self.name}",
            message=frappe.render_template(
                """
                Hi {{ doc.employee_name or "Guest" }},

                Thank you for booking ride {{ doc.name }}.
                We will confirm your request shortly.

                — VCM Rental
                """,
                {"doc": self}
            ),
        )

    def send_confirm_email(self):
        frappe.sendmail(
            recipients=[self.email] if self.email else BOOKING_CC,
            cc=self._build_cc_list(),
            subject=f"Ride {self.name} confirmed",
            message=frappe.render_template(
                """
                Hi {{ doc.employee_name or "Guest" }},

                Your ride {{ doc.name }} on {{ doc.date }}
                ({{ doc.pickup_time }}–{{ doc.drop_time }}) is CONFIRMED.

                Safe travels!
                — VCM Rental
                """,
                {"doc": self}
            ),
        )
