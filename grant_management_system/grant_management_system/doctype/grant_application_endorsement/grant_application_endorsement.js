// Copyright (c) 2022, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grant Application Endorsement', {
    email_id: function (frm) {
        get_user_details(frm);
    },
    validate: function (frm) {
        get_user_details(frm);
    },
    send_sms: function (frm) {
        send_sms(frm);
    }
});

//Begin of Functions
//Get user details
var get_user_details = function (frm) {
    if (frm.doc.email_id) {
        frappe.model.with_doc('User', frm.doc.email_id, function () {
            let user = frappe.model.get_doc('User', frm.doc.email_id);
            if (user['name']) {
                frm.set_value('user', user['name']);
                frm.set_value('mobile_no', user['mobile_no']);
                frm.set_value('first_name', user['first_name']);
                frm.set_value('middle_name', user['middle_name']);
                frm.set_value('last_name', user['last_name']);
            } else{
                frm.set_value('user', null);
                frm.set_value('mobile_no', null);
                frm.set_value('first_name', null);
                frm.set_value('middle_name', null);
                frm.set_value('last_name', null);
            }

            refresh_field('user');
            refresh_field('mobile_no');
            refresh_field('first_name');
            refresh_field('middle_name');
            refresh_field('last_name');
        });
    }
};

//Send SMS
var send_sms = function (frm) {
    if (frm.doc.first_name && frm.doc.send_sms === 1 && frm.doc.mobile_no) {
        var message = 'Dear, ' + frm.doc.first_name + ', Requesting for a Grant Application Endorsement at: ' + frm.doc.company + ', Sincerely: ' + frm.doc.applicant_name;
        frappe.call({
            method: "frappe.core.doctype.sms_settings.sms_settings.send_sms",
            args: {
                receiver_list: [frm.doc.mobile_no],
                msg: message,
            },
            callback: function (r) {
                if (r.exc) {
                    msgprint(r.exc);
                    return;
                }
            }
        });
    }
};
