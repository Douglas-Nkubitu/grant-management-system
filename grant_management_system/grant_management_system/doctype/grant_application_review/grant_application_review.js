// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Application Review', {
    grant_application: function (frm) {
        if (frm.doc.grant_application) {
            frm.clear_table('grant_application_review_item');
            frappe.model.with_doc('Grant Application', frm.doc.grant_application, function () {
                let source_doc = frappe.model.get_doc('Grant Application', frm.doc.grant_application);
                $.each(source_doc.details, function (index, source_row) {
					const target_row = frm.add_child('grant_application_review_item');
                    target_row.parameter = source_row.parameter;
                    target_row.item_description = source_row.item_description;
                    target_row.response = source_row.response;
                    target_row.response_description = source_row.response_description;
                    target_row.maximum_score = source_row.maximum_score;
                    frm.refresh_field('grant_application_review_item');
                });
            });
        }
    },
    //Calculate total score
    validate: function (frm) {
		// calculate total budget amount for each line budget item
		let total_maximum_score = 0;
		let total_score = 0;
		$.each(frm.doc.grant_application_review_item, function (i, d) {
			total_maximum_score += flt(d.maximum_score);
			if (d.score >= 0) {
			 total_score += flt(d.score);
			}
		});
		frm.doc.maximum_score = total_maximum_score;
		frm.doc.score = total_score;
	},
    setup: function (frm) {
        frm.set_indicator_formatter('parameter',
            function (doc) {
                if (doc.score >= 0){
                    return "green"
                } else if(doc.skip){
                    return "orange"
                }else{
                    return "white"
                }
            }
        )
    }
});

//Score Validation against Maximum Score
var maximum_score_validation = function (frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.score && d.maximum_score) {
        if (d.score > d.maximum_score) {
            msgprint('Score is greater than Maximum Score for the Parameter, please amend to continue');
            frappe.validated = false;
        }
    }
}

frappe.ui.form.on("Grant Application Review Item", "score", function (frm, cdt, cdn) {
    //Score Validation against Maximum Score
    maximum_score_validation(frm, cdt, cdn);
})
