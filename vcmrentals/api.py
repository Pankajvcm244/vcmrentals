import frappe


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

