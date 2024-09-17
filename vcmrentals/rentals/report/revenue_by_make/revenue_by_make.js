
frappe.query_reports["Revenue by Make"] = {
    "filters": [
        {
            "fieldname": "my_filter",
            "label": "Vehicle Make",
            "fieldtype": "Link",
            "options": "VcmVehicle"
        }
    ]
};
