# import frappe
# from frappe import _
# from frappe.utils import get_datetime
# from frappe.model.document import Document

# class RideBooking(Document):
#     def validate(self):
#         self.check_vehicle_availability()

#     def on_submit(self):
#         # Get the linked Ride Order name from your link field (adjust fieldname accordingly)
#         ride_order_name = self.order  
#         if ride_order_name:
#             # Update the Ride Order state to 'Close'
#             frappe.db.set_value('Ride Order', ride_order_name, 'state', 'Close')
#             # Optionally commit changes immediately
#             frappe.db.commit()

#     def before_save(self):

#         self.starttime = f"{self.date}T{self.from_time}"
#         self.endtime = f"{self.date}T{self.to_time}"
#         #logging.debug(f"Before Save-2 {self.starttime} {self.endtime}")  
#         #logging.debug(f"Before Save-2 {self.docstatus} ")
    

#     def check_vehicle_availability(self):
#         if not self.vehicle or not self.date or not self.from_time or not self.to_time:
#             return

#         start_time = get_datetime(f"{self.date} {self.from_time}")
#         end_time = get_datetime(f"{self.date} {self.to_time}")

#         # Check for vehicle overlap
#         overlapping_vehicle = frappe.db.sql("""
#             SELECT name FROM `tabRide Booking`
#             WHERE name != %s
#             AND vehicle = %s
#             AND date = %s
#             AND (
#                 (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                 (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                 (CONCAT(date, ' ', from_time) BETWEEN %s AND %s)
#             )
#         """, (self.name, self.vehicle, self.date, start_time, end_time, start_time, end_time), as_dict=True)

#         if overlapping_vehicle:
#             frappe.throw(_("This vehicle is already booked for the selected date and time."))

#         # Check for driver overlap
#         if self.driver:
#             overlapping_driver = frappe.db.sql("""
#                 SELECT name FROM `tabRide Booking`
#                 WHERE name != %s
#                 AND driver = %s
#                 AND date = %s
#                 AND (
#                     (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                     (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                     (CONCAT(date, ' ', from_time) BETWEEN %s AND %s)
#                 )
#             """, (self.name, self.driver, self.date, start_time, end_time, start_time, end_time), as_dict=True)

#             if overlapping_driver:
#                 frappe.throw(_("This driver is already assigned to another ride during the selected date and time."))
   













# import frappe
# from frappe import _
# from frappe.utils import get_datetime
# from frappe.model.document import Document

# class RideBooking(Document):
#     def validate(self):
#         self.check_vehicle_availability()

#     def on_submit(self):
#         # Update linked Ride Order state to 'Close' if order linked
#         ride_order_name = self.order  
#         if ride_order_name:
#             frappe.db.set_value('Ride Order', ride_order_name, 'state', 'Close')
#             # Optional: commit if needed
#             # frappe.db.commit()

#     def before_save(self):
#         if self.docstatus == 0:  # draft
#             # Only send email if valid recipient email exists
#             if self.email:
#                 self.send_draft_email()
       
#         self.starttime = f"{self.date}T{self.from_time}"
#         self.endtime = f"{self.date}T{self.to_time}"

#     def check_vehicle_availability(self):
#         if not self.vehicle or not self.date or not self.from_time or not self.to_time:
#             return

#         start_time = get_datetime(f"{self.date} {self.from_time}")
#         end_time = get_datetime(f"{self.date} {self.to_time}")

#         # Check for vehicle overlap
#         overlapping_vehicle = frappe.db.sql("""
#             SELECT name FROM `tabRide Booking`
#             WHERE name != %s
#             AND vehicle = %s
#             AND date = %s
#             AND (
#                 (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                 (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                 (CONCAT(date, ' ', from_time) BETWEEN %s AND %s)
#             )
#         """, (self.name, self.vehicle, self.date, start_time, end_time, start_time, end_time), as_dict=True)

#         if overlapping_vehicle:
#             frappe.throw(_("This vehicle is already booked for the selected date and time."))

#         # Check for driver overlap
#         if self.driver:
#             overlapping_driver = frappe.db.sql("""
#                 SELECT name FROM `tabRide Booking`
#                 WHERE name != %s
#                 AND driver = %s
#                 AND date = %s
#                 AND (
#                     (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                     (%s BETWEEN CONCAT(date, ' ', from_time) AND CONCAT(date, ' ', to_time)) OR
#                     (CONCAT(date, ' ', from_time) BETWEEN %s AND %s)
#                 )
#             """, (self.name, self.driver, self.date, start_time, end_time, start_time, end_time), as_dict=True)

#             if overlapping_driver:
#                 frappe.throw(_("This driver is already assigned to another ride during the selected date and time."))

#     def send_draft_email(self):
#         recipient = self.email
#         cc_emails = ["aman.soni@vcm.org.in", "amansonimtr@gmail.com"]

#         subject = f"Ride Booking Assign Vehicle: {self.name}"

#         message = f"""
#         <h2>Ride Booking Draft Saved - {self.name}</h2>
#         <p>Dear User,</p>
#         <p>Your ride booking draft has been saved successfully with the following details:</p>
#         <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; width: 600px;">
#             <tr><th align="left">Order</th><td>{self.order or '-'}</td></tr>
#             <tr><th align="left">Customer Name</th><td>{self.customer_name or '-'}</td></tr>
#             <tr><th align="left">Customer Number</th><td>{self.customer_number or '-'}</td></tr>
#             <tr><th align="left">Ride Type</th><td>{self.ride or '-'}</td></tr>
#             <tr><th align="left">Seating Capacity</th><td>{self.seating_capacity or '-'}</td></tr>
#             <tr><th align="left">Date</th><td>{self.date or '-'}</td></tr>
#             <tr><th align="left">From Time</th><td>{self.from_time or '-'}</td></tr>
#             <tr><th align="left">To Time</th><td>{self.to_time or '-'}</td></tr>
#             <tr><th align="left">PickUp Address</th><td>{self.pickup_address or '-'}</td></tr>
#             <tr><th align="left">Drop Address</th><td>{self.drop_address or '-'}</td></tr>
#             <tr><th align="left">Color</th><td>{self.color or '-'}</td></tr>
#             <tr><th align="left">Assign Vehicle Number</th><td>{self.assign_vehicle_number or '-'}</td></tr>
#             <tr><th align="left">Driver</th><td>{self.driver or '-'}</td></tr>
#             <tr><th align="left">Driver Email</th><td>{self.email or '-'}</td></tr>
#             <tr><th align="left">Driver Mobile Number</th><td>{self.driver_mobile_number or '-'}</td></tr>
#         </table>
#         <p>Regards,<br>VCM RENTAL Team</p>
#         """

#         frappe.sendmail(
#             recipients=[recipient],
#             cc=cc_emails,
#             subject=subject,
#             message=message,
#             reference_doctype=self.doctype,
#             reference_name=self.name
#         )







import frappe
from frappe import _
from frappe.utils import get_datetime
from frappe.model.document import Document

class RideBooking(Document):
    def validate(self):
        self.set_start_and_end()
        self.check_vehicle_availability()

    def on_update(self):
        # if self.booking_status == "Closed":
        #     self.close_linked_ride_order()
        self.send_draft_email()

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
        recipient = self.email
        cc_emails = ["aman.soni@vcm.org.in", "amansonimtr@gmail.com"]

        subject = f"Ride Booking Assign Vehicle: {self.name}"

        message = f"""
        <h2>Ride Booking Draft Saved - {self.name}</h2>
        <p>Dear User,</p>
        <p>Your ride booking draft has been saved successfully with the following details:</p>
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; width: 600px;">
            <tr><th align="left">Order</th><td>{self.order or '-'}</td></tr>
            <tr><th align="left">Customer Name</th><td>{self.customer_name or '-'}</td></tr>
            <tr><th align="left">Customer Number</th><td>{self.customer_number or '-'}</td></tr>
            <tr><th align="left">Ride Type</th><td>{self.ride or '-'}</td></tr>
            <tr><th align="left">Seating Capacity</th><td>{self.seating_capacity or '-'}</td></tr>
            <tr><th align="left">Date</th><td>{self.date or '-'}</td></tr>
            <tr><th align="left">From Time</th><td>{self.from_time or '-'}</td></tr>
            <tr><th align="left">To Time</th><td>{self.to_time or '-'}</td></tr>
            <tr><th align="left">PickUp Address</th><td>{self.pickup_address or '-'}</td></tr>
            <tr><th align="left">Drop Address</th><td>{self.drop_address or '-'}</td></tr>
            <tr><th align="left">Color</th><td>{self.color or '-'}</td></tr>
            <tr><th align="left">Assign Vehicle Number</th><td>{self.assign_vehicle_number or '-'}</td></tr>
            <tr><th align="left">Driver</th><td>{self.driver or '-'}</td></tr>
            <tr><th align="left">Driver Email</th><td>{self.email or '-'}</td></tr>
            <tr><th align="left">Driver Mobile Number</th><td>{self.driver_mobile_number or '-'}</td></tr>
        </table>
        <p>Regards,<br>VCM RENTAL Team</p>
        """

        frappe.sendmail(
            recipients=[recipient],
            cc=cc_emails,
            subject=subject,
            message=message,
            reference_doctype=self.doctype,
            reference_name=self.name
        )
