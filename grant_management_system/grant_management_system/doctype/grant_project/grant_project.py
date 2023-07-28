# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today

class GrantProject(Document):
	def validate(self):
		if not self.is_new():
			self.copy_from_grant_application()
        #self.update_costing()
		#self.update_percent_complete()

	def copy_from_grant_application(self):
		'''
		Copy grant application tasks from grant application
		'''
		if self.grant_application and not frappe.db.get_all('Grant Project Task', dict(grant_project = self.name), limit=1):

			# has a grant application, and no loaded grant application tasks, so lets create
			if not self.expected_start_date:
				# grant project starts today
				self.expected_start_date = today()

			# create grant project tasks from grant application tasks
			grant_application_tasks = get_grant_application_tasks(self)

			for grant_application_task in grant_application_tasks:
				self.create_grant_project_task_from_grant_application_task(grant_application_task)

	def create_grant_project_task_from_grant_application_task(self, grant_application_task):
		return frappe.get_doc(dict(
				doctype = 'Grant Project Task',
				key_action_steps_activities = grant_application_task.key_action_step_activity,
				type = grant_application_task.type,
				grant_project = self.name,
				owner = self.owner,
				applicant_name = self.applicant_name,
				grant_application = self.grant_application,
				grant_call = self.grant_call,
				company = self.company,
				status = 'Open',
				expected_start_date = grant_application_task.expected_start_date,
				expected_completion_date = grant_application_task.expected_completion_date,
				expected_time_in_days = grant_application_task.expected_time_in_days,
				expected_output = grant_application_task.expected_output,
				means_of_verification = grant_application_task.means_of_verification,
				grant_budget_template = grant_application_task.grant_budget_template,
				person_responsible = grant_application_task.person_responsible,
				institution_responsible = grant_application_task.institution_responsible,
				task_budget = grant_application_task.task_budget,
				comments = grant_application_task.comments
			)).insert()

	def after_insert(self):
		self.copy_from_grant_application()

def get_grant_application_tasks(self):

        grant_application_tasks = frappe.db.sql("""
    	    SELECT gat.*
    	    FROM `tabGrant Application Task` gat
    	    WHERE gat.grant_application = %(grant_application)s
		    order by gat.name
		    """.format(1), {
            "grant_application": self.grant_application
        }, as_dict=1)
        return grant_application_tasks