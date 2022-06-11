# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _
from frappe.utils import formatdate, format_datetime
from frappe.model.document import Document
from frappe.desk.form import assign_to


class DuplicateDeclarationError(frappe.ValidationError):
    pass


class NonProfitController(Document):
    '''
            Create the project and the task for the grant application
            Assign to the concerned person and roles as per the grant application
    '''

    def validate(self):
        # remove the task if linked before submitting the form
        if self.amended_from:
            for activity in self.activities:
                activity.task = ''

    # TODO
    # def on_submit(self):
        # create the project for the given grant application

    # TODO
    # def create_task_and_notify_user(self):
        # create the task for the given project and assign to the concerned person

    def assign_task_to_users(self, task, users):
        for user in users:
            args = {
                'assign_to': [user],
                'doctype': task.doctype,
                'name': task.name,
                'description': task.description or task.subject,
                'notify': self.notify_users_by_email
            }
            assign_to.add(args)

    # TODO
    # def on_cancel(self):
        # delete task project

    #Copy grant parameters from tabGrant Template,
	#these are to be used when creating grants of the particular programme
    def copy_grant_template_parameters(self):

        filters = ""
        if self.title:
            filters += " and gt.title = %(title)s"
        if self.programme:
            filters += " and gt.programme = %(programme)s"

        data = frappe.db.sql("""
    	    SELECT gt.title, gt.programme, gtp.parameter, gtp.description
    	    FROM `tabGrant Template` gt,
		         `tabGrant Template Parameter` gtp
    	    WHERE gt.title = gtp.parent
		    and gt.disabled = 0
		    order by gtp.idx
		    """.format(filters), {
            "title": self.title,
            "programme": self.programme
        }, as_dict=1)

@frappe.whitelist()
def get_grant_transfer_field_property(grant_application, fieldname):
	if grant_application and fieldname:
		field = frappe.get_meta("Grant Application").get_field(fieldname)
		value = frappe.db.get_value("Grant Application", grant_application, fieldname)
		options = field.options
		if field.fieldtype == "Date":
			value = formatdate(value)
		elif field.fieldtype == "Datetime":
			value = format_datetime(value)
		return {
			"value" : value,
			"datatype" : field.fieldtype,
			"label" : field.label,
			"options" : options
		}
	else:
		return False

