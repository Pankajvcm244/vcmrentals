import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_employee():
    # Fetch records from the Employee Doctype where designation is 'Driver'
    records = frappe.get_all(
        'Vehicle Booking User',
        fields=[
            'name',
            'name1',
            'contact',
            'department',
            'email',
            'employee_type'
        ],
        # filters={
        #     'designation': 'Driver'
        # }
    )
    return records



@frappe.whitelist(allow_guest=True)
def get_ride_status_options():
    doctype = "Ride Booking"
    fieldname = "ride_status"
    
    """Fetches the options of a specific DocField from any Doctype."""
    try:
        meta = frappe.get_meta(doctype)  # Get/fetches the metadata about the "VcmTicketFacility" Doctype.
        field = meta.get_field(fieldname)  # Get the specific field details

        if field:
            if field.fieldtype == "Select":
                options = field.options.split("\n")  # Convert options to a list
                return options

            return {"message": "Field does not have selectable options"}

        return {"error": "Field not found"}

    except Exception as e:
        return {"error": str(e)}
    

@frappe.whitelist(allow_guest=True)
def get_ride_order_field_options(fieldname):
    """
    Fetches the selectable options for a field like 'ride_type' or 'vehicle_type' 
    from the 'Ride Order' Doctype.
    """
    doctype = "Ride Order"

    try:
        meta = frappe.get_meta(doctype)
        field = meta.get_field(fieldname)

        if field:
            if field.fieldtype == "Select":
                options = field.options.split("\n") if field.options else []
                return options
            else:
                return {"message": f"Field '{fieldname}' is not of type 'Select'"}
        else:
            return {"error": f"Field '{fieldname}' not found in '{doctype}'"}

    except Exception as e:
        return {"error": str(e)}



@frappe.whitelist(allow_guest=True)
def update_ride_order_status(ride_order_id, status):
    try:
        # Fetch the ride order document
        ride_order = frappe.get_doc("Ride Order", ride_order_id)
        
        # Validate status
        if status not in ["Accepted", "Rejected"]:
            return {
                "success": False, 
                "message": "Invalid status. Only 'Accepted' or 'Rejected' are allowed."
            }
        
        # Update status if current status is 'New' or 'Open'
        if ride_order.status in ["New", "Open"]:
            ride_order.status = status
            ride_order.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                "success": True, 
                "message": f"Ride order {ride_order_id} has been {status}."
            }
        else:
            return {
                "success": False, 
                "message": f"Ride order {ride_order_id} cannot be updated as it is already {ride_order.status}."
            }
    except Exception as e:
        frappe.log_error(message=str(e), title="Ride Order Status Update Failed")
        return {
            "success": False, 
            "message": "Failed to update the ride order status."
        }



@frappe.whitelist(allow_guest=True)
def update_ride_order_status(booking_id, status):
    """Update booking status (Approve or Cancel)"""

    # Check if the booking exists
    if not frappe.db.exists("Ride Order", booking_id):
        frappe.throw(_("Booking ID {} does not exist").format(booking_id))

    booking = frappe.get_doc("Ride Order", booking_id)
    
    # Only allow valid status updates
    if status not in ["Approved", "Cancelled"]:
        return {"status": "error", "message": _("Invalid status provided.")}

    if booking.status == status:
        return {"status": "error", "message": _(f"Booking is already {status}.")}

    # Update the booking status
    booking.status = status
    booking.save(ignore_permissions=True)  # Ignore permissions if needed
    frappe.db.commit()

    return {"status": "success", "message": _(f"Booking has been successfully {status.lower()}.")}