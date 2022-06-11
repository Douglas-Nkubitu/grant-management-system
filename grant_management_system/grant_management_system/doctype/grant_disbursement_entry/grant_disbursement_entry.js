// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

//selecting and adding grant application in child table
frappe.ui.form.on('Grant Disbursement Entry', {

	get_grant_applications: function (frm) {
		frappe.call({
			method: "get_submitted_grant_applications",
			doc: frm.doc,
			callback: function (r) {
				refresh_field("grant_applications");
			}
		});
	}
});

// Action Button to create disbursement
frappe.ui.form.on("Grant Disbursement Entry", {
	refresh: function(frm){
		if(frm.doc.docstatus == 1) {			
			frappe.db.get_value("Loan", {"grant_disbursement_entry": frm.doc.name, "docstatus": 1}, "name", (r) => {
				if (Object.keys(r).length === 0) {
					frm.add_custom_button(__('Create Disbursement'), function() {
						frappe.model.open_mapped_doc({			
							method : "erpnext.non_profit.doctype.grant_disbursement_entry.grant_disbursement_entry.make_loan",
							frm : frm })
					},__('Action'))
					frm.page.set_inner_btn_group_as_primary(__('Action'));
				} else {
					frm.set_df_property('status', 'read_only', 1);
				}
			});
		}
    }
});