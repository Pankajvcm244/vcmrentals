// // // Copyright (c) 2025, Aman Soni and contributors
// // // For license information, please see license.txt

// // // frappe.ui.form.on("Vehicle Booking Settings", {
// // // 	refresh(frm) {

// // // 	},
// // // });


//     frappe.ui.form.on('Vehicle Booking Settings', {
//         refresh: function(frm) {
//             // Add Insurance reminder button
//             frm.add_custom_button(__('Send Insurance Expiry Reminders'), function() {
//                 frappe.call({
//                     method: "vcmrentals.reminder_utils.send_insurance_expiry_reminders",
//                     callback: function(r) {
//                         if (r.message) {
//                             frappe.msgprint(r.message);
//                         }
//                     }
//                 });
//             });

            
//             frm.add_custom_button(__('Send Pollution Expiry Reminders'), function() {
//                 frappe.call({
//                     method: "vcmrentals.reminder_utils.send_pollution_expiry_reminders",
//                     callback: function(r) {
//                         if(r.message) {
//                             frappe.msgprint(r.message);
//                         }
//                     }
//                 });
//             });

//             frm.add_custom_button(__('Send Driver License Expiry Reminders'), function() {
//                 frappe.call({
//                     method: "vcmrentals.reminder_utils.send_driver_license_expiry_reminders",
//                     callback: function(r) {
//                         if(r.message){
//                             frappe.msgprint(r.message);
//                         }
//                     }
//                 });
//             });
//         }
//     });

