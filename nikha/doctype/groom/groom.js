// Copyright (c) 2025, Saad and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Groom", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Groom', {
    refresh: function(frm) {
        // Add "Scan ID" button
        frm.add_custom_button(__('Scan ID Card'), function() {
            let uploader = new frappe.ui.FileUploader({
                restrictions: {
                    allowed_file_types: ['image/*','.pdf']
                },
                on_success: function(file) {
                    frappe.call({
                        method: "nikha.nikha.doctype.groom.groom.scan_groom_id",
                        args: { file_url: file.file_url },
                        callback: function(r) {
                            if (r.message && !r.message.error) {
                                console.log(r.message);
                                // Auto-fill the form fields
                                frm.set_value("name1", r.message.name);
                                frm.set_value("age", r.message.age);
                                frm.set_value("father_name", r.message.father_name);
                                frappe.show_alert(__("Fields auto-filled from scan!"));
                            } else {
                                frappe.msgprint(__("Scan failed. Please try again or enter manually."));
                            }
                        }
                    });
                }
            });
        }, __("Actions"));
    }
});