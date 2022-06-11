// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Call Template', {
	refresh: function(frm) {
		frm.add_custom_button(__("Create Grant Call Template Parameters"), function() {
			frappe.call({
				method: "create_grant_parameters",
				doc: frm.doc,
				callback: function (r) {
					refresh_field("parameters");
				}
			});
		}, __("Tools"));
	}
});