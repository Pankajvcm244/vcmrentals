# # Copyright (c) 2024, Aman Soni and contributors
# # For license information, please see license.txt

# import frappe

# def execute(filters=None):
#     # Define the report columns
#     columns = [
#         {"label": "Vehicle Make", "fieldname": "vehicle_make", "fieldtype": "Data", "width": 150},
#         {"label": "Driver Name", "fieldname": "driver_name", "fieldtype": "Data", "width": 150},
#         {"label": "Odometer Start", "fieldname": "odometer_start", "fieldtype": "Int", "width": 100},
#         {"label": "Odometer End", "fieldname": "odometer_end", "fieldtype": "Int", "width": 100},
#         {"label": "Distance Moved (Km)", "fieldname": "distance_moved", "fieldtype": "Float", "width": 100}
#     ]

#     # Construct the query with joins to get vehicle make and driver full name
#     query = """
#         SELECT 
#             vcmvehicle.make AS vehicle_make,
#             CONCAT(cabdriver.first_name, ' ', cabdriver.last_name) AS driver_name,
#             ride_booking.odometer_start,
#             ride_booking.odometer_end,
#             (ride_booking.odometer_end - ride_booking.odometer_start) AS distance_moved
#         FROM 
#             `tabRide Booking` AS ride_booking
#         LEFT JOIN 
#             `tabVcmVehicle` AS vcmvehicle ON ride_booking.vehicle = vcmvehicle.name
#         LEFT JOIN 
#             `tabCabDriver` AS cabdriver ON ride_booking.driver = cabdriver.name
#         WHERE 
#             ride_booking.odometer_end IS NOT NULL 
#             AND ride_booking.odometer_start IS NOT NULL
#     """
    
#     # Execute the query and fetch the data
#     data = frappe.db.sql(query, as_dict=True)

#     return columns, data


import frappe

def execute(filters=None):
    # Define the report columns
    columns = [
        {"label": "Order", "fieldname": "order", "fieldtype": "Data", "width": 100},
        {"label": "Vehicle Make", "fieldname": "vehicle_make", "fieldtype": "Data", "width": 150},
        {"label": "Driver Name", "fieldname": "driver_name", "fieldtype": "Data", "width": 150},
        {"label": "Odometer Start", "fieldname": "odometer_start", "fieldtype": "Int", "width": 100},
        {"label": "Odometer End", "fieldname": "odometer_end", "fieldtype": "Int", "width": 100},
        {"label": "Distance Moved (Km)", "fieldname": "distance_moved", "fieldtype": "Float", "width": 100}
    ]

    # Construct the query with joins to get order, vehicle make, and driver full name
    query = """
        SELECT 
            ride_booking.order AS `order`,
            vcmvehicle.make AS vehicle_make,
            CONCAT(cabdriver.first_name, ' ', cabdriver.last_name) AS driver_name,
            ride_booking.odometer_start,
            ride_booking.odometer_end,
            (ride_booking.odometer_end - ride_booking.odometer_start) AS distance_moved
        FROM 
            `tabRide Booking` AS ride_booking
        LEFT JOIN 
            `tabVcmVehicle` AS vcmvehicle ON ride_booking.vehicle = vcmvehicle.name
        LEFT JOIN 
            `tabCabDriver` AS cabdriver ON ride_booking.driver = cabdriver.name
        WHERE 
            ride_booking.odometer_end IS NOT NULL 
            AND ride_booking.odometer_start IS NOT NULL
    """
    
    # Execute the query and fetch the data
    data = frappe.db.sql(query, as_dict=True)

    return columns, data






