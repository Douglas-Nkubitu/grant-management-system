// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Application Activity', {
    //Get grant budget_template items
    grant_budget_template: function (frm) {
        if (frm.doc.grant_budget_template) {
            frm.clear_table('grant_application_activity_budget_item');
            frappe.model.with_doc('Grant Budget Template', frm.doc.grant_budget_template, function () {
                let source_doc = frappe.model.get_doc('Grant Budget Template', frm.doc.grant_budget_template);
                $.each(source_doc.budget_items, function (index, source_row) {
					const target_row = frm.add_child('grant_application_activity_budget_item');
                    target_row.budget_item = source_row.budget_item;
                    target_row.budget_category = source_row.budget_category;
                    frm.refresh_field('grant_application_activity_budget_item');
                });
            });
        }
    },
    //Calculate total budget
    validate: function (frm) {
        //Budget
		let total_budget_amt = 0;
		$.each(frm.doc.grant_application_activity_budget_item, function (j, bitem) {
			total_budget_amt += flt(bitem.amount);
		});
		frm.doc.activity_budget = total_budget_amt;
	}
});

//Budget Amount Calculation
var amount_calculation = function (frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if ((row.qty) && (row.rate)) {
        frappe.model.set_value(cdt, cdn, 'amount', (row.qty * row.rate));
        frm.refresh_field("amount");
    }
}

//Budget child table amount calculation on qty change
frappe.ui.form.on("Grant Application Activity Budget Item", "qty", function (frm, cdt, cdn) {
    //amount on qty change
    amount_calculation(frm, cdt, cdn);
})

//Budget child table amount calculation on rate change
frappe.ui.form.on("Grant Application Activity Budget Item", "rate", function (frm, cdt, cdn) {
    //amount on rate change
    amount_calculation(frm, cdt, cdn);
})
