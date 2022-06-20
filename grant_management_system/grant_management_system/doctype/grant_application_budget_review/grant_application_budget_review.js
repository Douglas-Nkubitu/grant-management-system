// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Application Budget Review', {
    grant_application: function (frm) {
        if (frm.doc.grant_application) {
            frm.clear_table('grant_application_budget_review_item');
            frappe.model.with_doc('Grant Application', frm.doc.grant_application, function () {
                let source_doc = frappe.model.get_doc('Grant Application', frm.doc.grant_application);
                $.each(source_doc.grant_application_budget_item, function (index, source_row) {
					const target_row = frm.add_child('grant_application_budget_review_item');
                    target_row.budget_item = source_row.budget_item;
                    target_row.unit_of_measure = source_row.unit_of_measure;
                    target_row.qty = source_row.qty;
                    target_row.rate = source_row.rate;
                    target_row.amount = source_row.amount;
                    target_row.item_description = source_row.item_description;
                     target_row.reviewed_rate = source_row.rate;
                    target_row.reviewed_amount = source_row.amount;
                    frm.refresh_field('grant_application_budget_review_item');
                });
            });
        }
    },
    //Calculate total score
    validate: function (frm) {
		// calculate total budget amount for each line budget item
		let total_requested_amount = 0;
		let total_reviewed_amount = 0;
		$.each(frm.doc.grant_application_budget_review_item, function (i, d) {
			total_requested_amount += flt(d.amount);
			total_reviewed_amount += flt(d.reviewed_amount);
		});
		frm.doc.requested_amount = total_requested_amount;
		frm.doc.reviewed_amount = total_reviewed_amount;
	},
    setup: function (frm) {
        frm.set_indicator_formatter('budget_item',
            function (doc) {
                return (doc.amount != doc.reviewed_amount) ? "green" : "white"
            })
    },
    on_submit: function (frm) {
        update_grant_app_average_reviewed_budget_amount(frm);
    },
    after_cancel: function (frm) {
        update_grant_app_average_reviewed_budget_amount(frm);
    }
});

//Update grant application
var update_grant_app_average_reviewed_budget_amount = function (frm) {
    
    let count_of_reviews = frappe.db.count('Grant Application Budget Review',
                                            {'grant_application': frm.doc.grant_application, 'docstatus': 1});
    
    let sum_of_reviews = frappe.db.get_list('Grant Application Budget Review',
                                            filters = {'grant_application': frm.doc.grant_application, 'docstatus': 1},
                                            fields = ['sum(reviewed_amount) as sum_rev_amt','grant_application'],
                                            group_by = 'grant_application');
    
    let average_reviewed_budget_amount = flt(sum_of_reviews / count_of_reviews, 2);
    
    frappe.db.set_value('Grant Application', frm.doc.grant_application, 'average_reviewed_budget_amount', average_reviewed_budget_amount);
};
