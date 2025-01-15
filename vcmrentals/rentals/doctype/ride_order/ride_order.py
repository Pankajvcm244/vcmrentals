# # import frappe
# # from frappe.model.document import Document

# # class RideOrder(Document):
# #     def validate(self):
# #         # Check if the document is new and send the approval email to the manager
# #         if self.is_new():
# #             self.send_approval_email_to_manager()
# #         elif self.has_status_changed():
# #             self.send_status_update_email()

# #     def has_status_changed(self):
# #         # Fetch the old status from the database
# #         old_status = frappe.db.get_value("Ride Order", self.name, "status")
# #         return old_status != self.status

# #     def send_approval_email_to_manager(self):
# #         # Fetch the email address from the linked Manager Email DocType
# #         if self.manager_email:
# #             manager_email_address = frappe.db.get_value("Manager Email", self.manager_email, "Email")

# #             if not manager_email_address:
# #                 frappe.log_error(message="Manager Email address not found", title="Email Sending Failed")
# #                 return
            
# #             subject = f"Approval Required for Ride Order {self.name}"
# #             message = f"""
# #                 <html>
# #                 <body>
# #                     <table width="100%" cellpadding="10" cellspacing="0" border="0">
# #                         <tr>
# #                             <td>
# #                                 <h2>Ride Order Approval Needed</h2>
# #                                 <p>Dear Manager,</p>
# #                                 <p>A new ride order has been created and requires your approval. Below are the details:</p>
# #                                 <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
# #                                     <tr>
# #                                         <td><b>Customer Name:</b></td>
# #                                         <td>{self.customer_name}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Contact Number:</b></td>
# #                                         <td>{self.contact_number}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Pickup Time:</b></td>
# #                                         <td>{self.pickup_time}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Drop Time:</b></td>
# #                                         <td>{self.drop_time}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Pickup Address:</b></td>
# #                                         <td>{self.pickup_address}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Drop Address:</b></td>
# #                                         <td>{self.drop_address}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Vehicle Type:</b></td>
# #                                         <td>{self.vehicle_type}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Ride Type:</b></td>
# #                                         <td>{self.ride_type}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Remarks:</b></td>
# #                                         <td>{self.comment}</td>
# #                                     </tr>
                                    
# #                                 </table>
# #                                 <p>Please review the details and approve or reject the ride order.</p>
# #                                 <p>
# #                                     <a href="http://13.200.187.97:8000/api/method/vcmrentals.api.update_ride_order_status?ride_order_id={self.name}&status=Accepted">Accept</a>
# #                                     <a href="http://13.200.187.97:8000/api/method/vcmrentals.api.update_ride_order_status?ride_order_id={self.name}&status=Rejected">Reject</a>

# #                                 </p>
# #                                 <p>Best regards,<br>Your Ride Booking Team</p>
# #                             </td>
# #                         </tr>
# #                     </table>
# #                 </body>
# #                 </html>
                
# #             """

# #             try:
# #                 frappe.sendmail(
# #                     recipients=[manager_email_address],
# #                     subject=subject,
# #                     message=message
# #                 )
# #             except Exception as e:
# #                 frappe.log_error(message=str(e), title="Approval Email Sending Failed")
# #         else:
# #             frappe.log_error(message="Manager Email field is empty", title="Email Sending Failed")

# #     def send_status_update_email(self):
# #         submitter_email = self.email  # Email field in Ride Order DocType
# #         cc_email = "amansoniofficial20@gmail.com,amansonimtr@gmail.com"  # CC Emails

# #         if self.status == "Accepted":
# #             subject = f"Confirmation of Your Ride Order {self.name}"
# #             message = f"""
# #                 <html>
# #                 <body>
# #                     <table width="100%" cellpadding="10" cellspacing="0" border="0">
# #                         <tr>
# #                             <td>
# #                                 <h2>Ride Order Confirmation</h2>
# #                                 <p>Dear {self.customer_name},</p>
# #                                 <p>Your ride order has been confirmed. Below are the details:</p>
# #                                 <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
# #                                     <tr>
# #                                         <td><b>Order Number:</b></td>
# #                                         <td>{self.name}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Pickup Time:</b></td>
# #                                         <td>{self.pickup_time}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Drop Time:</b></td>
# #                                         <td>{self.drop_time}</td>
# #                                     </tr>

# #                                     <tr>
# #                                         <td><b>Pickup Address:</b></td>
# #                                         <td>{self.pickup_address}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Drop Address:</b></td>
# #                                         <td>{self.drop_address}</td>
# #                                     </tr>
                                   
# #                                     <tr>
# #                                         <td><b>Vehicle Type:</b></td>
# #                                         <td>{self.vehicle_type}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Ride Type:</b></td>
# #                                         <td>{self.ride_type}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Remarks:</b></td>
# #                                         <td>{self.comment}</td>
# #                                     </tr>
# #                                 </table>
# #                                 <p>Thank you for choosing our service.</p>
# #                                 <p>Best regards,<br>Your Ride Booking Team</p>
# #                             </td>
# #                         </tr>
# #                     </table>
# #                 </body>
# #                 </html>
# #             """
# #         elif self.status == "Rejected":
# #             subject = f"Notification: Your Ride Order {self.name} is Rejected"
# #             message = f"""
# #                 <html>
# #                 <body>
# #                     <table width="100%" cellpadding="10" cellspacing="0" border="0">
# #                         <tr>
# #                             <td>
# #                                 <h2>Ride Order Rejected</h2>
# #                                 <p>Dear {self.customer_name},</p>
# #                                 <p>We regret to inform you that your ride order has been rejected. Below are the details:</p>
# #                                 <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
# #                                     <tr>
# #                                         <td><b>Order Number:</b></td>
# #                                         <td>{self.name}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Pickup Time:</b></td>
# #                                         <td>{self.pickup_time}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Drop Time:</b></td>
# #                                         <td>{self.drop_time}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Pickup Address:</b></td>
# #                                         <td>{self.pickup_address}</td>
# #                                     </tr>
# #                                      <tr>
# #                                         <td><b>Drop Address:</b></td>
# #                                         <td>{self.drop_address}</td>
# #                                     </tr>
                                    
# #                                     <tr>
# #                                         <td><b>Vehicle Type:</b></td>
# #                                         <td>{self.vehicle_type}</td>
# #                                     </tr>
                                    
# #                                     <tr>
# #                                         <td><b>Ride Type:</b></td>
# #                                         <td>{self.ride_type}</td>
# #                                     </tr>
# #                                     <tr>
# #                                         <td><b>Remarks:</b></td>
# #                                         <td>{self.comment}</td>
# #                                     </tr>
# #                                 </table>
# #                                 <p>We apologize for any inconvenience this may have caused.</p>
# #                                 <p>Best regards,<br>Your Ride Booking Team</p>
# #                             </td>
# #                         </tr>
# #                     </table>
# #                 </body>
# #                 </html>
# #             """

# #         try:
# #             frappe.sendmail(
# #                 recipients=[submitter_email],
# #                 cc=cc_email.split(","),
# #                 subject=subject,
# #                 message=message
# #             )
# #         except Exception as e:
# #             frappe.log_error(message=str(e), title="Email Sending Failed")


# # @frappe.whitelist()
# # def update_ride_order_status(ride_order_id, status):
# #     try:
# #         ride_order = frappe.get_doc("Ride Order", ride_order_id)
# #         ride_order.status = status
# #         ride_order.save(ignore_permissions=True)
# #         frappe.db.commit()
# #         return {"success": True, "message": f"Ride order {ride_order_id} has been {status}."}
# #     except Exception as e:
# #         frappe.log_error(message=str(e), title="Ride Order Status Update Failed")
# #         return {"success": False, "message": "Failed to update the ride order status."}

# ///////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////



import frappe
from frappe.model.document import Document
from frappe.utils import get_url

class RideOrder(Document):
    def validate(self):
        # Check if the document is new and send the approval email to the manager
        if self.is_new():
            self.send_approval_email_to_manager()
        elif self.has_status_changed():
            self.send_status_update_email()

    def has_status_changed(self):
        # Fetch the old status from the database
        old_status = frappe.db.get_value("Ride Order", self.name, "status")
        return old_status != self.status

    def send_approval_email_to_manager(self):
        # Fetch the email address from the linked Manager Email DocType
        if self.manager_email:
            manager_email_address = frappe.db.get_value("Manager Email", self.manager_email, "Email")

            if not manager_email_address:
                frappe.log_error(message="Manager Email address not found", title="Email Sending Failed")
                return
            
            base_url = get_url()  # Dynamically fetch the base URL
            subject = f"Approval Required for Ride Order {self.name}"
            message = f"""
                <html>
                <body>
                    <table width="100%" cellpadding="10" cellspacing="0" border="0">
                        <tr>
                            <td>
                                <h2>Ride Order Approval Needed</h2>
                                <p>Dear Manager,</p>
                                <p>A new ride order has been created and requires your approval. Below are the details:</p>
                                <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
                                    <tr>
                                        <td><b>Customer Name:</b></td>
                                        <td>{self.customer_name}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Contact Number:</b></td>
                                        <td>{self.contact_number}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Pickup Time:</b></td>
                                        <td>{self.pickup_time}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Drop Time:</b></td>
                                        <td>{self.drop_time}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Pickup Address:</b></td>
                                        <td>{self.pickup_address}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Drop Address:</b></td>
                                        <td>{self.drop_address}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Vehicle Type:</b></td>
                                        <td>{self.vehicle_type}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Ride Type:</b></td>
                                        <td>{self.ride_type}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Remarks:</b></td>
                                        <td>{self.comment}</td>
                                    </tr>
                                </table>
                                <p>Please review the details and approve or reject the ride order.</p>
                                <p>
                                    <a href="{base_url}/api/method/vcmrentals.api.update_ride_order_status?ride_order_id={self.name}&status=Accepted">Accept</a>
                                    <a href="{base_url}/api/method/vcmrentals.api.update_ride_order_status?ride_order_id={self.name}&status=Rejected">Reject</a>
                                </p>
                                <p>Best regards,<br>Your Ride Booking Team</p>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
            """

            try:
                frappe.sendmail(
                    recipients=[manager_email_address],
                    subject=subject,
                    message=message
                )
            except Exception as e:
                frappe.log_error(message=str(e), title="Approval Email Sending Failed")
        else:
            frappe.log_error(message="Manager Email field is empty", title="Email Sending Failed")

    def send_status_update_email(self):
        submitter_email = self.email  # Email field in Ride Order DocType
        cc_email = "amansoniofficial20@gmail.com,amansonimtr@gmail.com"  # CC Emails

        if self.status == "Accepted":
            subject = f"Confirmation of Your Ride Order {self.name}"
            message = f"""
                <html>
                <body>
                    <table width="100%" cellpadding="10" cellspacing="0" border="0">
                        <tr>
                            <td>
                                <h2>Ride Order Confirmation</h2>
                                <p>Dear {self.customer_name},</p>
                                <p>Your ride order has been confirmed. Below are the details:</p>
                                <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
                                    <tr>
                                        <td><b>Order Number:</b></td>
                                        <td>{self.name}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Pickup Time:</b></td>
                                        <td>{self.pickup_time}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Drop Time:</b></td>
                                        <td>{self.drop_time}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Pickup Address:</b></td>
                                        <td>{self.pickup_address}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Drop Address:</b></td>
                                        <td>{self.drop_address}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Vehicle Type:</b></td>
                                        <td>{self.vehicle_type}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Ride Type:</b></td>
                                        <td>{self.ride_type}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Remarks:</b></td>
                                        <td>{self.comment}</td>
                                    </tr>
                                </table>
                                <p>Thank you for choosing our service.</p>
                                <p>Best regards,<br>Your Ride Booking Team</p>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
            """
        elif self.status == "Rejected":
            subject = f"Notification: Your Ride Order {self.name} is Rejected"
            message = f"""
                <html>
                <body>
                    <table width="100%" cellpadding="10" cellspacing="0" border="0">
                        <tr>
                            <td>
                                <h2>Ride Order Rejected</h2>
                                <p>Dear {self.customer_name},</p>
                                <p>We regret to inform you that your ride order has been rejected. Below are the details:</p>
                                <table width="100%" cellpadding="8" cellspacing="0" border="1" style="border-collapse: collapse;">
                                    <tr>
                                        <td><b>Order Number:</b></td>
                                        <td>{self.name}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Pickup Time:</b></td>
                                        <td>{self.pickup_time}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Drop Time:</b></td>
                                        <td>{self.drop_time}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Pickup Address:</b></td>
                                        <td>{self.pickup_address}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Drop Address:</b></td>
                                        <td>{self.drop_address}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Vehicle Type:</b></td>
                                        <td>{self.vehicle_type}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Ride Type:</b></td>
                                        <td>{self.ride_type}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Remarks:</b></td>
                                        <td>{self.comment}</td>
                                    </tr>
                                </table>
                                <p>We apologize for any inconvenience this may have caused.</p>
                                <p>Best regards,<br>Your Ride Booking Team</p>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
            """

        try:
            frappe.sendmail(
                recipients=[submitter_email],
                cc=cc_email.split(","),
                subject=subject,
                message=message
            )
        except Exception as e:
            frappe.log_error(message=str(e), title="Email Sending Failed")


@frappe.whitelist()
def update_ride_order_status(ride_order_id, status):
    try:
        ride_order = frappe.get_doc("Ride Order", ride_order_id)
        ride_order.status = status
        ride_order.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": f"Ride order {ride_order_id} has been {status}."}
    except Exception as e:
        frappe.log_error(message=str(e), title="Ride Order Status Update Failed")
        return {"success": False, "message": "Failed to update the ride order status."}





