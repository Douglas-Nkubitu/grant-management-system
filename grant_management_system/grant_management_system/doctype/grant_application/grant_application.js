// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Application', {
    onload: function (frm) {
        cur_frm.set_query("institution", function () {
            return {
                "filters": {
                    "membership_type": "Institution",
                }
            };
        });
    },
	refresh: function(frm) {
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Grant Application'};

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if(!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}

		if(frm.doc.status == 'Received' && !frm.doc.email_notification_sent){
			frm.add_custom_button(__("Send Grant Review Email"), function() {
				frappe.call({
					method: "erpnext.non_profit.doctype.grant_application.grant_application.send_grant_review_emails",
					args: {
						grant_application: frm.doc.name
					}
				});
			});
		}
	},
    //Get grant call parameters
    grant_call: function (frm) {
        if (frm.doc.grant_call) {
            frm.clear_table('details');
            frappe.model.with_doc('Grant Call', frm.doc.grant_call, function () {
                let source_doc = frappe.model.get_doc('Grant Call', frm.doc.grant_call);
                $.each(source_doc.grant_application_parameters, function (index, source_row) {
					const target_row = frm.add_child('details');
                    target_row.parameter = source_row.parameter;
                    target_row.item_description = source_row.item_description;
                    target_row.maximum_score = source_row.maximum_score;
                    target_row.required = source_row.required;
                    target_row.is_numeric = source_row.is_numeric;
                    frm.refresh_field('details');
                });
            });
        }
    },
    //Get grant budget_template items
    grant_budget_template: function (frm) {
        if (frm.doc.grant_budget_template) {
            frm.clear_table('grant_application_budget_item');
            frappe.model.with_doc('Grant Budget Template', frm.doc.grant_budget_template, function () {
                let source_doc = frappe.model.get_doc('Grant Budget Template', frm.doc.grant_budget_template);
                $.each(source_doc.budget_items, function (index, source_row) {
					const target_row = frm.add_child('grant_application_budget_item');
                    target_row.budget_item = source_row.budget_item;
                    frm.refresh_field('grant_application_budget_item');
                });
            });
        }
    },
    //Calculate total budget
    validate: function (frm) {
		//Work Plan
		let total_cost_budget = 0;
		$.each(frm.doc.grant_application_work_plan, function (i, wpitem) {            
			total_cost_budget += flt(wpitem.cost_budget);
		});
		frm.doc.total_cost_budget = total_cost_budget;

        //Budget
		let total_budget_amt = 0;
		$.each(frm.doc.grant_application_budget_item, function (j, bitem) {
			total_budget_amt += flt(bitem.amount);
		});
		frm.doc.amount = total_budget_amt;
		
		//Deduction Items
		let total_deduction_items_amount = 0;
		$.each(frm.doc.grant_application_deduction_items, function (k, ditem) {
			total_deduction_items_amount += flt(ditem.amount);
		});
		frm.doc.total_deduction_items_amount = total_deduction_items_amount;
		
		//Other Sources of Funds
		let total_other_sources_of_fund_amount = 0;
		$.each(frm.doc.grant_application_other_sources_of_fund, function (l, sitem) {
			total_other_sources_of_fund_amount += flt(sitem.amount);
		});
		frm.doc.total_other_sources_of_fund_amount = total_other_sources_of_fund_amount;
	}
});

//Budget Amount Calculation
var amount_calculation = function (frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if ((row.qty) && (row.cost)) {
        frappe.model.set_value(cdt, cdn, 'amount', (row.qty * row.cost));
        frm.refresh_field("amount");
    }
}

//Budget child table amount calculation on qty change
frappe.ui.form.on("Grant Application Budget Item", "qty", function (frm, cdt, cdn) {
    //amount on qty change
    amount_calculation(frm, cdt, cdn);
})

//Budget child table amount calculation on cost change
frappe.ui.form.on("Grant Application Budget Item", "cost", function (frm, cdt, cdn) {
    //amount on cost change
    amount_calculation(frm, cdt, cdn);
})

//Deduction Items child table amount calculation on qty change
frappe.ui.form.on("Grant Application Deduction Items", "qty", function (frm, cdt, cdn) {
    //amount on qty change
    amount_calculation(frm, cdt, cdn);
})

//Deduction Items child table amount calculation on cost change
frappe.ui.form.on("Grant Application Deduction Items", "cost", function (frm, cdt, cdn) {
    //amount on cost change
    amount_calculation(frm, cdt, cdn);
})
