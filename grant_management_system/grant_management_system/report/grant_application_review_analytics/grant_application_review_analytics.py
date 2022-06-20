# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import flt

def execute(filters=None):
	return Report(filters).run()

class Report(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
					

	def run(self):
		self.get_columns()
		group_by_field = get_group_by_field(self.filters.get("group_by"))
		data = get_data(self.filters, group_by_field)
		chart_data = get_chart_data(data)
		skip_total_row = 0
		
		# return all Grant Call, Grant Application, Grant Application Review if group by is unselected
		if not group_by_field:
			return self.columns, data

		# handle grouping
		grant_application_reviews_map, grouped_data = {}, []
		for d in data:
			grant_application_reviews_map.setdefault(d[group_by_field], []).append(d)
		
		for key in grant_application_reviews_map:
			applications = grant_application_reviews_map[key]
			grouped_data += applications
			add_subtotal_row(grouped_data, applications, group_by_field, key)

		# move group by column to first position
		column_index = next((index for (index, d) in enumerate(self.columns) if d["fieldname"] == group_by_field), None)
		self.columns.insert(0, self.columns.pop(column_index))

		return self.columns, grouped_data, None, chart_data, None, skip_total_row

	# getings columns
	def get_columns(self):
		self.columns = [
			{
			'label': _('Grant Call Name'),
			'fieldname': 'grant_call_name',
			'fieldtype': 'Read Only',
			'options': 'Grant Application Review',
			'width': 300
			},
			{
			'label': _('Grant Application'),
			'fieldname': 'grant_application',
			'fieldtype': 'Link',
			'options': 'Grant Application Review',
			'width': 170
			},
			{
			'label': _('Applicant Name'),
			'fieldname': 'applicant_name',
			'fieldtype': 'Data',
			'options': 'Member',
			'width': 130
			},
			{
			'label': _('Grant Application Review'),
			'fieldname': 'name',
			'fieldtype': 'Link',
			'options': 'Grant Application Review',
			'width': 200
			},			
			{
			'label': _('Parameter'),
			'fieldname': 'parameter',
			'fieldtype': 'Link',
			'options': 'Grant Application Review Item',
			'width': 300
			},
			{
			'label': _('Score'),
			'fieldname': 'score',
			'fieldtype': 'Float',		
			'width': 80
			}
		]

def get_data(filters,conditions=""):
	conditions = get_conditions(filters)
	data = frappe.db.sql("""
	SELECT 	
			ga.applicant_name,ga.institution,
			gar.name, gar.date, gar.grant_call_name, 
			gar.grant_application, gar.company, gari.parameter, gari.score
			
	FROM `tabGrant Application Review Item` gari,`tabGrant Application Review` gar 

	LEFT JOIN `tabGrant Application` ga 
		ON gar.grant_application = ga.name
	WHERE 
		gar.name = gari.parent 
		and gar.docstatus=1 %s 

	""" % conditions, filters, as_dict=1)

	return data

# add subtotal of rows based on grouping by
def add_subtotal_row(data, grouped_applications, group_by_field, group_by_value):
	score = sum(d.score for d in grouped_applications)
	data.append({
		group_by_field: group_by_value,
		"score": score,
		"bold": 1
	})
	data.append({})

# generate graphs
def get_chart_data(data):
	grant_application_review_map = {}
	labels, datapoints = [], []

	for row in data:
		column_key = row.get("grant_application")

		if not column_key in grant_application_review_map:
			grant_application_review_map[column_key] = 0

		grant_application_review_map[column_key] = flt(grant_application_review_map[column_key]) + flt(row.get("score"))

	grant_application_review_map = { item: value for item, value in (sorted(grant_application_review_map.items(), key = lambda i: i[1], reverse=True))}

	for key in grant_application_review_map:
		labels.append(key)
		datapoints.append(grant_application_review_map[key])

	return {
		"data" : {
			"labels" : labels[:30], # show max of 30 items in chart
			"datasets" : [
				{
					"name" : _(" Total Score"),
					"values" : datapoints[:30]
				}
			]
		},
		"type" : "bar"
	}

# filters conditions
def get_conditions(filters):
	conditions = ""
	
	if	filters.get("from_date"):
			conditions += " and gar.date >= %(from_date)s"

	if filters.get("to_date"):
			conditions += " and gar.date <= %(to_date)s"

	if filters.get("grant_call"): 
			conditions += " and gar.grant_call = %(grant_call)s"

	if filters.get("grant_application"):
			conditions += " and gar.grant_application = %(grant_application)s"

	if filters.get("company"):
			conditions += " and gar.company = %(company)s"

	if filters.get("institution"):
			conditions += " and ga.institution = %(institution)s"

	if not filters.get("group_by"):
		conditions += "ORDER BY gar.name, gari.parameter asc"
	else:
		conditions += get_group_by_field(filters)

	return conditions

#grouping by selected fields
def get_group_by_field(group_by):
	group_by_field = ""

	if group_by == "Grant Call":
		group_by_field = "grant_call_name"
	elif group_by == "Grant Application":
		group_by_field = "grant_application"
	elif group_by == "Grant Application Review":
		group_by_field = "name"
	
	return group_by_field
