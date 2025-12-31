# Copyright (c) 2025, Aman Soni and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Ride Order", "fieldname": "ride_order", "fieldtype": "Link", "options": "Ride Order", "width": 150},
        {"label": "Booking User", "fieldname": "user_name", "width": 150},
        {"label": "Department", "fieldname": "department", "width": 120},
        {"label": "Trip Start Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Trip End Date", "fieldname": "trip_end_date", "fieldtype": "Date", "width": 120},
        {"label": "Ride Type", "fieldname": "ride_type", "width": 120},
        {"label": "Vehicle Number", "fieldname": "vehicle_number", "width": 180},
        {"label": "Driver Name", "fieldname": "driver_name", "width": 150},
        {"label": "Meter Start", "fieldname": "odometer_start", "fieldtype": "Int", "width": 110},
		{"label": "Meter End", "fieldname": "odometer_end", "fieldtype": "Int", "width": 110},
		{"label": "Total KM", "fieldname": "total_km", "fieldtype": "Int", "width": 100},
        {"label": "Meter Start Time", "fieldname": "odometer_start_timestamp", "fieldtype": "Datetime", "width": 170},
        {"label": "Meter End Time", "fieldname": "odometer_end_timestamp", "fieldtype": "Datetime", "width": 170},
        {"label": "Running Hours", "fieldname": "running_hours", "fieldtype": "Float", "precision": 2, "width": 120},
        {"label": "Driver Feedback", "fieldname": "driver_feedback", "width": 200},
        {"label": "Ride Status", "fieldname": "ride_status", "width": 120},
  
    ]


def get_data(filters):
    conditions = []
    values = {}

    # Filter by date range
    if filters.get("from_date"):
        conditions.append("ro.date >= %(from_date)s")
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions.append("ro.date <= %(to_date)s")
        values["to_date"] = filters.get("to_date")

    # Filter by ride_type
    if filters.get("ride_type"):
        conditions.append("ro.ride_type = %(ride_type)s")
        values["ride_type"] = filters.get("ride_type")

    # Filter by vehicle (vehicle ID)
    if filters.get("vehicle"):
        conditions.append("rb.vehicle = %(vehicle)s")
        values["vehicle"] = filters.get("vehicle")

    # Filter by driver (driver ID)
    if filters.get("driver"):
        conditions.append("rb.driver = %(driver)s")
        values["driver"] = filters.get("driver")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
    SELECT
        ro.name AS ride_order,
        ro.user_name,
        ro.department,
        ro.date,
        ro.trip_end_date,
        ro.ride_type,
        v.title AS vehicle_number,
        d.driver_name AS driver_name,
        rb.odometer_start,
        rb.odometer_start_time_stamp AS odometer_start_timestamp,
        rb.odometer_end,
        rb.odometer_end_time_stamp AS odometer_end_timestamp,
        (rb.odometer_end - rb.odometer_start) AS total_km,
        TIMESTAMPDIFF(SECOND, rb.odometer_start_time_stamp, rb.odometer_end_time_stamp)/3600 AS running_hours,
        rb.driver_feedback,
        rb.ride_status,
        ro.workflow_state,
        rb.amount
    FROM `tabRide Order` ro
    LEFT JOIN `tabRide Booking` rb
        ON rb.`order` = ro.name
    LEFT JOIN `tabVcmVehicle` v
        ON rb.vehicle = v.name
    LEFT JOIN `tabVehicle Driver` d
        ON rb.driver = d.name
    {where_clause}
    ORDER BY ro.creation DESC
    """

    return frappe.db.sql(query, values, as_dict=1)
