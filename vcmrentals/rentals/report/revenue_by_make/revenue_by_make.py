import frappe

def execute(filters=None):

    frappe.errprint(filters)  # For debugging purposes, prints filters to log

    # Defining the columns of the report
    columns = [
        {"fieldname": "make", "label": "Make", "fieldtype": "Data"},
        {"fieldname": "total_revenue", "label": "Total Revenue", "fieldtype": "Currency", "options": "AED"},
    ]

    # Fetching the data from your VcmVehicle DocType
    data = frappe.get_all(
        "Ride Booking",  # Make sure this matches the DocType where revenue info is stored
        fields=["SUM(total_amount) AS total_revenue", "vehicle.make"],  # Adjust this based on your fields
        filters={"docstatus": 1},  # Add any necessary filters if applicable
        group_by="make"
    )

    # Defining the chart
    chart = {
        "data": {
            "labels": [x.make for x in data],
            "datasets": [{"values": [x.total_revenue for x in data]}],
        },
        "type": "pie"
    }

    # Returning the columns, data, message, and chart
    return columns, data, "Revenue by Make", chart
