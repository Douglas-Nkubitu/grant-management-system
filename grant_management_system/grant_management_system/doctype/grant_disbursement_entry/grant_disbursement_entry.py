# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class GrantDisbursementEntry(Document):

	# Get submitted grant Application
	def get_submitted_grant_applications(self):
		#Validations
		if not self.grant_call:
			frappe.throw(_("Please select the Grant Call"),title=_("Grant Call Required"))

		if not self.institution:
			frappe.throw(_("Please select the Institution"),title=_("Institution Required"))

		if not self.from_date:
			frappe.throw(_("Please select the From Date Filter"),title=_("From Date Required"))

		if not self.to_date:
			frappe.throw(_("Please select the To Date Filter"),title=_("To Date Required"))
		#End Validations


		""" Pull grant applications which are submitted based on criteria selected"""
		submitted_ga = get_grant_applications(self)

		if submitted_ga:
			self.add_si_in_table(submitted_ga)
			self.get_items()
			frappe.msgprint(_("Grant Applications selection completed"),title=_("Grant Application Selection"))
		else:
			frappe.msgprint(_("Grant Applications are not available for Grant Disbursement Entry"))

	# Add submitted grant applications in table
	def add_ga_in_table(self, submitted_ga): 
		""" Add grant applications in the table"""
		self.set('grant_applications', [])
		for data in submitted_ga:
			self.append('grant_applications', {
				'grant_application': data.name,
				'applicant': data.applicant,
				'applicant_name':data.applicant_name,
				'amount': data.amount                       
			})

	# Get Items
	def get_items(self):
		self.get_ga_items()

	# Get list of Grant Application query
	def get_ga_items(self):
		# Check for empty table or empty rows
		if not self.get("grant_applications"):
			frappe.throw(_("Please fill the Items Details table"),
							title=_("Grant Applications Items Required"))

# Get submitted grant application query
def get_grant_applications(self):
    si_filter = ""
    if self.grant_call:
        si_filter += " and ga.grant_call = %(grant_call)s"
    if self.institution:
        si_filter += " and ga.institution = %(institution)s"
    if self.from_date:
        si_filter += " and ga.date >= %(from_date)s"
    if self.to_date:
        si_filter += " and ga.date <= %(to_date)s"


    submitted_ga = frappe.db.sql("""
        select distinct ga.name, ga.applicant, ga.applicant_name, ga.institution, ga.grant_call, ga.amount, ga.date
        from `tabGrant Application` ga
        where ga.docstatus = 1
            and ga.company = %(company)s {0}
			and (ga.name not in (select gdei.grant_application from `tabGrant Disbursement Entry Item` gdei,
                            `tabGrant Disbursement Entry` gde where gdei.parent = gde.name and gde.docstatus != 2))
            
        order by ga.name
        """.format(si_filter), {
        "grant_call": self.grant_call,
		"institution":self.institution,
        "from_date": self.from_date,
        "to_date": self.to_date,
        "company": self.company
    }, as_dict=1)
    return submitted_ga


@frappe.whitelist()
def make_loan(source_name, target_doc=None):
	def postprocess(source, doc):
		doc.loan_name = source.name

	doc = get_mapped_doc("Grant Disbursement Entry", source_name, {
		"Grant Disbursement Entry": {
			"doctype": "Loan",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map":{
				"name" : "grant_disbursement_entry"
			}
		},
	}, target_doc, postprocess)

	return doc
