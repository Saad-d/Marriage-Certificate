// Copyright (c) 2025, Saad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Marriage Certificate", {
	refresh(frm) {

	},
    dob(frm) {
        set_age(frm, frm.doc.dob, 'groom_age');
    },
    bride_dob(frm) {
        set_age(frm, frm.doc.bride_dob, 'age');
    }
});


function set_age(frm, dob_value, target_fieldname) {
    if (dob_value) {
        const dob = new Date(dob_value);
        const today = new Date();

        let age = today.getFullYear() - dob.getFullYear();
        const m = today.getMonth() - dob.getMonth();

        if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
            age--;
        }

        frm.set_value(target_fieldname, age.toString());
    }
}