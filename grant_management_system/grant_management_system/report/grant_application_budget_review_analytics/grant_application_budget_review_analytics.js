// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Grant Application Budget Review Analytics"] = {
	"filters": [
		{
			"fieldname": "doc_type",
			"label": __("Grant Application Budget Review"),
			"fieldtype": "Read Only",
			"options": ["Grant Application Budget Review"],
			"width": "100",
			"default": "Grant Application Budget Review"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{ 
			"fieldname":"grant_call",
			"label": __("Grant Call"),
			"fieldtype": "Link",
			"options": "Grant Call",
			"width": "100"
		},
		{
			"fieldname":"grant_application",
			"label": __("Grant Application"),
			"fieldtype": "Link",
			"options": "Grant Application",
			"width": "100"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"institution",
			"label": __("Institution Name"),
			"fieldtype": "Link",
			"options": "Member",
			"width": "100"
		},
		{
			"label": __("Group By"),
			"fieldname": "group_by",
			"fieldtype": "Select",
			"options": ["","Grant Call", "Grant Application", "Grant Application Budget Review"],
			"default": "Grant Call"
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	}
};