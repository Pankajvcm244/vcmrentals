# Copyright (c) 2024, Aman Soni and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class RideBooking(Document):
    
    def validate(self):
        # If rate is not provided, set it to the standard rate from Rentals Settings
        if not self.rate:
            self.rate = frappe.db.get_single_value("Rentals Settings", "standard_rate")

        # Calculate the total distance and amount
        total_distance = 0
        for item in self.items:
            total_distance += item.distance

        self.total_amount = total_distance * self.rate

    def after_insert(self):
        # Send email after the Ride Booking is saved
        self.send_ride_booking_email()

    def send_ride_booking_email(self):
        # Fetch recipient email from the Ride Booking document
        recipient_email = self.email

        # Fetch driver's details
        driver_details = frappe.db.get_value('CabDriver', self.driver, ['first_name', 'last_name', 'phone_number'], as_dict=True)

        # Fetch vehicle title
        vehicle_title = frappe.db.get_value('VcmVehicle', self.vehicle, 'title')

        if recipient_email and driver_details and vehicle_title:
            driver_full_name = f"{driver_details.get('first_name')} {driver_details.get('last_name')}"
            driver_contact = driver_details.get('phone_number')

            # Prepare the items list for the email
            item_details = ""
            for item in self.items:
                item_details += f"""
                <tr>
                    <td>{item.idx}</td>
                    <td>{item.source}</td>
                    <td>{item.distance}</td>
                    <td>{item.destination}</td>
                </tr>
                """

            subject = f"Ride Booking Confirmation - Order {self.order}"
            message = f"""
            <p>Dear Customer,</p>

            <p>Your ride booking has been confirmed. Here are the details:</p>

            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; max-width: 600px;">
                <tr>
                    <th style="background-color: #f2f2f2;">Order</th>
                    <td>{self.order}</td>
                </tr>
                <tr>
                    <th style="background-color: #f2f2f2;">Vehicle</th>
                    <td>{vehicle_title}</td>
                </tr>
                <tr>
                    <th style="background-color: #f2f2f2;">Driver</th>
                    <td>{driver_full_name} ({driver_contact})</td>
                </tr>
                <tr>
                    <th style="background-color: #f2f2f2;">Email</th>
                    <td>{recipient_email}</td>
                </tr>
            </table>

            <p><strong>Ride Details:</strong></p>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; max-width: 600px;">
                <thead>
                    <tr>
                        <th style="background-color: #f2f2f2;">No.</th>
                        <th style="background-color: #f2f2f2;">Source</th>
                        <th style="background-color: #f2f2f2;">Distance</th>
                        <th style="background-color: #f2f2f2;">Destination</th>
                    </tr>
                </thead>
                <tbody>
                    {item_details}
                </tbody>
            </table>

            <p><strong>Rate per Km:</strong> {self.rate}</p>
            <p><strong>Total Amount:</strong> ₹ {self.total_amount}</p>

            <p>Thank you for choosing our service.</p>

            <p>Best Regards,<br>Your Company Name</p>
            """

            # Send email using frappe's sendmail function
            frappe.sendmail(
                recipients=recipient_email,
                subject=subject,
                message=message,
                cc=["amansoniofficial20@gmail.com"]  # Add CC recipient
            )
