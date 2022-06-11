// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Call', {
	grant_application_template: function (frm) {
		frappe.call({
			method: "copy_grant_application_parameters_from_template",
			doc: frm.doc,
			callback: function (r) {
				refresh_field("grant_application_parameters");
			}
		});
	},
	grant_reporting_template: function (frm) {
		frappe.call({
			method: "copy_grant_application_report_parameters_from_template",
			doc: frm.doc,
			callback: function (r) {
				refresh_field("grant_reporting_parameters");
			}
		});
	}
});
