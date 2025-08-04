// Copyright (c) 2024, Aman Soni and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Ride Booking", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Ride Booking", {
    odometer_start: function(frm) {
        if (frm.doc.odometer_start) {
            frm.set_value("odometer_start_time_stamp", frappe.datetime.now_datetime());
        }
    },
    odometer_end: function(frm) {
        if (frm.doc.odometer_end) {
            frm.set_value("odometer_end_time_stamp", frappe.datetime.now_datetime());
        }
    }
});
