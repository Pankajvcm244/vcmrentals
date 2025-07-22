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
    

@frappe.whitelist()
def ride_order_mobile_approval(docname):
    
    doctype = "Ride Order"  

    if not docname:
        frappe.throw(_("Document name is required."))

    if not frappe.db.exists(doctype, docname):
        frappe.throw(_("Document {0} ({1}) does not exist.").format(doctype, docname))

    # Fetch the document
    doc = frappe.get_doc(doctype, docname)

    if not hasattr(doc, "workflow_state"):
        frappe.throw(_("Workflow state is missing in this document."))
    
    # get the next workflow action from get_next_action_methd returns like Recommended/First Approve
    next_action = get_next_action(doc)

    if not next_action:
        frappe.throw(_("No valid action found for the current workflow state."))

    # pass next action based on that it changes state and docstatus
    next_workflow_state, new_docstatus = get_next_workflow_state(next_action)

    if not next_workflow_state:
        frappe.throw(_("No valid next workflow state found."))

    # Ensure user has permission
    if not frappe.has_permission(doctype, "write", doc=doc):
        frappe.throw(_("You do not have permission to approve this document."))

    prev_workflow_state = doc.workflow_state

    # Apply workflow state update
    doc.workflow_state = next_workflow_state

    # Use standard ERPNext methods for state change
    if new_docstatus == 1:
        doc.submit()  # Submitting the document
    else:
        doc.save(ignore_permissions=True)  # Save as draft or update state

    if doc.workflow_state != next_workflow_state:
        frappe.throw(_("Failed to update workflow state. Expected: {0}, Found: {1}").format(next_workflow_state, doc.workflow_state))

    if doc.docstatus != new_docstatus:
        frappe.throw(_("Failed to update document status. Expected: {0}, Found: {1}").format(new_docstatus, doc.docstatus))



    doc.add_comment("Workflow", _('{0}').format(next_workflow_state))


    return {
        "status": "success",
        "message": _("Document {0} is now in '{1}' state.").format(docname, next_workflow_state),
        "previous_state": prev_workflow_state,
        "current_state": next_workflow_state,
        "next_action": next_action
    }

def get_next_action(doc):

    workflow_state = doc.workflow_state
    action = ""

    if workflow_state == "Pending":
        if doc.get("l1_approving_authority"):
            action = "L1 Approve"
        elif doc.get("l2_approving_authority"):
            action = "L2 Approve"
        elif doc.get("l3_approving_authority"):
            action = "L3 Approve"
        else:
            action = "Final Approve"

    elif workflow_state == "L1 Approved":
        if doc.get("l2_approving_authority"):
            action = "L2 Approve"
        elif doc.get("l3_approving_authority"):
            action = "L3 Approve"
        else:
            action = "Final Approve"

    elif workflow_state == "L2 Approved":
        if doc.get("l3_approving_authority"):
            action = "L3 Approve"
        else:
            action = "Final Approve"

    elif workflow_state == "L3 Approved":
        action = "Final Approve"

    return action

def get_next_workflow_state(action):
    """Returns the next workflow state and docstatus based on the action taken"""
    workflow_mapping = {
        "L1 Approve": ("L1 Approved", 0),
        "L2 Approve": ("L2 Approved", 0),
        "L3 Approve": ("L3 Approved", 0),
        "Final Approve": ("Final Level Approved", 1)  # Submitted state
    }
    return workflow_mapping.get(action, (None, None))

# def get_next_action(doc):

#     workflow_state = doc.workflow_state
#     action = ""

#     if workflow_state == "Checked":
#         if doc.get("recommended_by"):
#             action = "Recommend"
#         elif doc.get("first_approving_authority"):
#             action = "First Approve"
#         elif doc.get("second_approving_authority"):
#             action = "Second Approve"
#         else:
#             action = "Final Approve"

#     elif workflow_state == "Recommended":
#         if doc.get("first_approving_authority"):
#             action = "First Approve"
#         elif doc.get("second_approving_authority"):
#             action = "Second Approve"
#         else:
#             action = "Final Approve"
    

#     elif workflow_state == "First Level Approved":
#         if doc.get("second_approving_authority"):
#             action = "Second Approve"
#         else:
#             action = "Final Approve"

#     elif workflow_state == "Second Level Approved":
#         action = "Final Approve"

#     return action

# def get_next_workflow_state(action):
#     """Returns the next workflow state and docstatus based on the action taken"""
#     workflow_mapping = {
#         "Recommend": ("Recommended", 0),
#         "First Approve": ("First Level Approved", 0),
#         "Second Approve": ("Second Level Approved", 0),  # Draft state
#         "Final Approve": ("Final Level Approved", 1)  # Submitted state
#     }
#     return workflow_mapping.get(action, (None, None))



@frappe.whitelist()
def budgetAmendment_mobile_rejection(docname=None):
    
    """Apply workflow action on a document and delete the ToDo"""

    doctype = "VCM Budget Amendment" 

    # Validate API access
    if not frappe.request:
        frappe.throw(_("API not hit."))

    # Validate input parameters
    if not doctype or not docname:
        frappe.throw(_(f"Doctype and docname is required"))

    if not frappe.db.exists(doctype, docname):
        frappe.throw(_("Document {0} ({1}) does not exist.").format(doctype, docname))


    doc = frappe.get_doc(doctype, docname)

    # Ensure the document has a workflow state
    if not hasattr(doc, "workflow_state"):
        frappe.throw(_("Workflow state is missing in this document."))

    doc.workflow_state = "Prepared"
    doc.save(ignore_permissions=True)


    if doc.workflow_state != "Prepared":
        frappe.throw(_("Workflow state update failed."))


    # Log the workflow change for tracking
    doc.add_comment("Workflow", _("Prepared"))
       

    return {
        "status": "success",
        "message": _(f"Document {docname} is now in '{doc.workflow_state}' state."),
    }











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