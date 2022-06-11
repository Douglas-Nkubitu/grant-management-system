// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Budget Change', {
	grant_project: function (frm) {
		frappe.call({
			method: "copy_grant_application_budget_items",
			doc: frm.doc,
			callback: function (r) {
				refresh_field("items");
			}
		});
	}
});
