// Copyright (c) 2025, Aman Soni and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Ride Management"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "ride_type",
            "label": "Ride Type",
            "fieldtype": "Select",
            "options": "\nLocal\nIntercity\nOutstation"
        },
        {
            "fieldname": "vehicle",
            "label": "Vehicle",
            "fieldtype": "Link",
            "options": "VcmVehicle"
        },
        {
            "fieldname": "driver",
            "label": "Driver",
            "fieldtype": "Link",
            "options": "Vehicle Driver"
        }
    ]
}
