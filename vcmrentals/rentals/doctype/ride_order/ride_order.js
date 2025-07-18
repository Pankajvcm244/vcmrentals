
// frappe.ui.form.on("Ride Order", {
// 	onload(frm) {
// 		console.log("running load...");
// 	},
// 	setup(frm) {
// 		console.log("setup...");
// 	},
// 	refresh(frm) {
// 		console.log("on refresh...")

// 		if (frm.doc.status === "Pending") {
// 			frm.add_custom_button("Accept", () => {
// 				// status => Accepted
// 				frm.set_value("status", "Accepted");
// 				// save the form
// 				frm.save();
// 			}, "Actions")

// 			frm.add_custom_button("Reject", () => {
// 				// status => Accepted
// 				frm.set_value("status", "Rejected");
// 				// save the form
// 				frm.save();
// 			}, "Actions")

// 			frm.add_custom_button("Cancel", () => {
// 				// status => Accepted
// 				frm.set_value("status", "Cancelled");
// 				// save the form
// 				frm.save();
// 			}, "Actions")
// 		}
// 	},
// 	status(frm) {
// 		console.log("status changed");
// 	}
// });

// frappe.ui.form.on('Ride Order', {
//     refresh: function(frm) {
//         if (!frm.doc.__islocal && frm.doc.status !== "Accepted") {

//             frm.add_custom_button('Accept Ride', function() {
//                 update_status(frm, 'Accepted');
//             }, 'Update Status');

//             frm.add_custom_button('Cancel Ride', function() {
//                 update_status(frm, 'Cancelled');
//             }, 'Update Status');

//             frm.add_custom_button('Reject Ride', function() {
//                 update_status(frm, 'Rejected');
//             }, 'Update Status');
//         }
//     }
// });

// function update_status(frm, new_status) {
//     frappe.call({
//         method: 'vcmrentals.rentals.doctype.ride_order.ride_order.update_ride_order_status',
//         args: {
//             order_name: frm.doc.name,
//             new_status: new_status
//         },
//         callback: function(r) {
//             if (!r.exc) {
//                 frappe.msgprint(r.message);
//                 frm.reload_doc();
//             }
//         }
//     });
// }
