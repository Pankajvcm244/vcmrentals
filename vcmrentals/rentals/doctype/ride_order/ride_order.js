frappe.ui.form.on('Ride Order', {
    
    onload: function(frm) {
        // Check if user has "Vehicle Agent" role
        if (frappe.user.has_role("Vehicle Agent")) {
            // Show all records
            frm.set_query("name1", function() {
                return {};
            });
        } else {
            // Only show record matching logged-in user's email
            frm.set_query("name1", function() {
                return {
                    filters: {
                        email: frappe.session.user
                    }
                };
            });
        }
    },
   
});

