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


# import frappe

# def execute(filters=None):
#     # Define the report columns
#     columns = [
#         {"label": "Order", "fieldname": "order", "fieldtype": "Data", "width": 100},
#         {"label": "Vehicle Make", "fieldname": "vehicle_make", "fieldtype": "Data", "width": 150},
#         {"label": "Driver Name", "fieldname": "driver_name", "fieldtype": "Data", "width": 150},
#         {"label": "Odometer Start", "fieldname": "odometer_start", "fieldtype": "Int", "width": 100},
#         {"label": "Odometer End", "fieldname": "odometer_end", "fieldtype": "Int", "width": 100},
#         {"label": "Distance Moved (Km)", "fieldname": "distance_moved", "fieldtype": "Float", "width": 100}
#     ]

#     # Construct the query with joins to get order, vehicle make, and driver full name
#     query = """
#         SELECT 
#             ride_booking.order AS `order`,
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

# import frappe

# def execute(filters=None):
#     # Define the report columns
#     columns = [
#         {"label": "Order", "fieldname": "order", "fieldtype": "Data", "width": 100},
#         {"label": "Vehicle Make", "fieldname": "vehicle_make", "fieldtype": "Data", "width": 150},
#         {"label": "Driver Name", "fieldname": "driver_name", "fieldtype": "Data", "width": 150},
#         {"label": "Odometer Start", "fieldname": "odometer_start", "fieldtype": "Int", "width": 100},
#         {"label": "Odometer End", "fieldname": "odometer_end", "fieldtype": "Int", "width": 100},
#         {"label": "Distance Moved (Km)", "fieldname": "distance_moved", "fieldtype": "Float", "width": 100},
#         {"label": "Source", "fieldname": "source", "fieldtype": "Data", "width": 150},
#         {"label": "Distance (KM)", "fieldname": "item_distance", "fieldtype": "Float", "width": 100},
#         {"label": "Destination", "fieldname": "destination", "fieldtype": "Data", "width": 150},
#     ]

#     # Construct the query with joins to get ride booking, vehicle, driver, and items (Source, Distance, Destination)
#     query = """
#         SELECT 
#             ride_booking.order AS `order`,
#             vcmvehicle.make AS vehicle_make,
#             CONCAT(cabdriver.first_name, ' ', cabdriver.last_name) AS driver_name,
#             ride_booking.odometer_start,
#             ride_booking.odometer_end,
#             (ride_booking.odometer_end - ride_booking.odometer_start) AS distance_moved,
#             ride_item.source AS source,
#             ride_item.distance AS item_distance,
#             ride_item.destination AS destination
#         FROM 
#             `tabRide Booking` AS ride_booking
#         LEFT JOIN 
#             `tabVcmVehicle` AS vcmvehicle ON ride_booking.vehicle = vcmvehicle.name
#         LEFT JOIN 
#             `tabCabDriver` AS cabdriver ON ride_booking.driver = cabdriver.name
#         LEFT JOIN
#             `tabRide Booking Item` AS ride_item ON ride_booking.name = ride_item.parent
#         WHERE 
#             ride_booking.odometer_end IS NOT NULL 
#             AND ride_booking.odometer_start IS NOT NULL
#     """
    
#     # Execute the query and fetch the data
#     data = frappe.db.sql(query, as_dict=True)

#     return columns, data

import frappe

def execute(filters=None):
    # Define the report columns for the table
    columns = [
        {"label": "Order", "fieldname": "order", "fieldtype": "Data", "width": 100},
        {"label": "Vehicle Make", "fieldname": "vehicle_make", "fieldtype": "Data", "width": 150},
        {"label": "Driver Name", "fieldname": "driver_name", "fieldtype": "Data", "width": 150},
        {"label": "Odometer Start", "fieldname": "odometer_start", "fieldtype": "Int", "width": 100},
        {"label": "Odometer End", "fieldname": "odometer_end", "fieldtype": "Int", "width": 100},
        {"label": "Distance Moved (Km)", "fieldname": "distance_moved", "fieldtype": "Float", "width": 100},
        {"label": "Source", "fieldname": "source", "fieldtype": "Data", "width": 150},
        {"label": "Distance (KM)", "fieldname": "item_distance", "fieldtype": "Float", "width": 100},
        {"label": "Destination", "fieldname": "destination", "fieldtype": "Data", "width": 150},
        {"label": "Created On", "fieldname": "created_on", "fieldtype": "Datetime", "width": 150}  # New column for Created On
    ]

    # Construct the query to get data from ride booking, vehicle, driver, and items
    query = """
        SELECT 
            ride_booking.order AS `order`,
            vcmvehicle.make AS vehicle_make,
            CONCAT(cabdriver.first_name, ' ', cabdriver.last_name) AS driver_name,
            ride_booking.odometer_start,
            ride_booking.odometer_end,
            (ride_booking.odometer_end - ride_booking.odometer_start) AS distance_moved,
            ride_item.source AS source,
            ride_item.distance AS item_distance,
            ride_item.destination AS destination,
            ride_booking.creation AS created_on  # Added field for Created On
        FROM 
            `tabRide Booking` AS ride_booking
        LEFT JOIN 
            `tabVcmVehicle` AS vcmvehicle ON ride_booking.vehicle = vcmvehicle.name
        LEFT JOIN 
            `tabCabDriver` AS cabdriver ON ride_booking.driver = cabdriver.name
        LEFT JOIN
            `tabRide Booking Item` AS ride_item ON ride_booking.name = ride_item.parent
        WHERE 
            ride_booking.odometer_end IS NOT NULL 
            AND ride_booking.odometer_start IS NOT NULL
    """
    
    # Execute the query and fetch the data
    data = frappe.db.sql(query, as_dict=True)

    # Preparing data for the chart (group by vehicle make)
    vehicle_data = {}
    for row in data:
        vehicle_make = row['vehicle_make']
        distance_moved = row['distance_moved']
        if vehicle_make not in vehicle_data:
            vehicle_data[vehicle_make] = 0
        vehicle_data[vehicle_make] += distance_moved

    # Create pie chart data
    chart = {
        "data": {
            "labels": list(vehicle_data.keys()),  # Vehicle make as labels
            "datasets": [{"values": list(vehicle_data.values())}]  # Distance moved as values
        },
        "type": "pie"  # Type of chart is pie
    }

    # Return columns, data, and chart
    return columns, data, None, chart



