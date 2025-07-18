from __future__ import unicode_literals
from frappe import _



# def get_data():
#     return {
#         'fieldname': 'vehicle',  # field in Vehicle Challan that links to VcmVehicle
#         'transactions': [
#             {
#                 'label': 'Vehicle Records',
#                 'items': ['Vehicle Challan']
#             }
#         ]
#     }

def get_data():
    return {
        'fieldname': 'vehicle',  # field linking to VcmVehicle
        'transactions': [
            {
                'label': 'Vehicle Records',
                'items': ['Vehicle Challan', 'Vehicle Maintenance']
            }
        ]
    }




