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
		
		# return all Grant Call, Grant Application, Grant Application Budget Review if group by is unselected
		if not group_by_field:
			return self.columns, data

		# handle grouping
		grant_application_budget_reviews_map, grouped_data = {}, []
		for d in data:
			grant_application_budget_reviews_map.setdefault(d[group_by_field], []).append(d)
		
		for key in grant_application_budget_reviews_map:
			applications = grant_application_budget_reviews_map[key]
			grouped_data += applications
			add_subtotal_row(grouped_data, applications, group_by_field, key)

		# move group by column to first position
		column_index = next((index for (index, d) in enumerate(self.columns) if d["fieldname"] == group_by_field), None)
		self.columns.insert(0, self.columns.pop(column_index))

		return self.columns, grouped_data, None, chart_data, None, skip_total_row
	
	# getting columns
	def get_columns(self):
		self.columns = [
			{
			'label': _('Grant Call Name'),
			'fieldname': 'grant_call_name',
			'fieldtype': 'Read Only',
			'options': 'Grant Application Budget Review',
			'width': 100
			},
			{
			'label': _('Grant Application'),
			'fieldname': 'grant_application',
			'fieldtype': 'Link',
			'options': 'Grant Application Budget Review',
			'width': 100
			},
			{
			'label': _('Applicant Name'),
			'fieldname': 'applicant_name',
			'fieldtype': 'Data',
			'options': 'Member',
			'width': 100
			},
			{
			'label': _('Grant Application Budget Review'),
			'fieldname': 'name',
			'fieldtype': 'Link',
			'options': 'Grant Application Budget Review',
			'width': 100
			},
			{
			'label': _('Budget Item'),
			'fieldname': 'budget_item',
			'fieldtype': 'Link',
			'options': 'Grant Application Budget Review Item',
			'width': 100
			},
			{
			'label': _('Amount'),
			'fieldname': 'amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Amount'),
			'fieldname': 'reviewed_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Difference of reviewed Amount'),
			'fieldname': 'difference',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 1 Amount'),
			'fieldname': 'year_1_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 1 Amount'),
			'fieldname': 'reviewed_year_1_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 1 Difference'),
			'fieldname': 'difference1',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 2 Amount'),
			'fieldname': 'year_2_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 2 Amount'),
			'fieldname': 'reviewed_year_2_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 2 Difference'),
			'fieldname': 'difference2',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 3 Amount'),
			'fieldname': 'year_3_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 3 Amount'),
			'fieldname': 'reviewed_year_3_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 3 Difference'),
			'fieldname': 'difference3',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 4 Amount'),
			'fieldname': 'year_4_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 4 Amount'),
			'fieldname': 'reviewed_year_4_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 4 Difference'),
			'fieldname': 'difference4',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 5 Amount'),
			'fieldname': 'year_5_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 5 Amount'),
			'fieldname': 'reviewed_year_5_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 5 Difference'),
			'fieldname': 'difference5',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 6 Amount'),
			'fieldname': 'year_6_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 6 Amount'),
			'fieldname': 'reviewed_year_6_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 6 Difference'),
			'fieldname': 'difference6',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 7 Amount'),
			'fieldname': 'year_7_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 7 Amount'),
			'fieldname': 'reviewed_year_7_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 7 Difference'),
			'fieldname': 'difference7',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 8 Amount'),
			'fieldname': 'year_8_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 8 Amount'),
			'fieldname': 'reviewed_year_8_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 8 Difference'),
			'fieldname': 'difference8',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 9 Amount'),
			'fieldname': 'year_9_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 9 Amount'),
			'fieldname': 'reviewed_year_9_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 9 Difference'),
			'fieldname': 'difference9',
			'fieldtype': "Currency",
			'width': 120
			},
			{
			'label': _('Year 10 Amount'),
			'fieldname': 'year_10_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Reviewed Year 10 Amount'),
			'fieldname': 'reviewed_year_10_amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
			},
			{
			'label': _('Year 10 Difference'),
			'fieldname': 'difference10',
			'fieldtype': "Currency",
			'width': 120
			}
		]

def get_data(filters, conditions=""):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
	SELECT
			ga.applicant_name,ga.institution,
			gabr.name, gabr.date, 
			gabr.grant_call_name, gabr.grant_application,
			gabri.budget_item, gabri.amount, gabri.reviewed_amount,
			(gabri.amount - gabri.reviewed_amount) as difference, 
			gabri.year_1_amount, gabri.reviewed_year_1_amount,
			(gabri.year_1_amount - gabri.reviewed_year_1_amount) as difference1,
			gabri.year_2_amount, gabri.reviewed_year_2_amount,
			(gabri.year_2_amount - gabri.reviewed_year_2_amount) as difference2,
			gabri.year_3_amount, gabri.reviewed_year_3_amount,
			(gabri.year_3_amount - gabri.reviewed_year_3_amount) as difference3,
			gabri.year_4_amount, gabri.reviewed_year_4_amount,
			(gabri.year_4_amount - gabri.reviewed_year_4_amount) as difference4,
			gabri.year_5_amount, gabri.reviewed_year_5_amount,
			(gabri.year_5_amount - gabri.reviewed_year_5_amount) as difference5,
			gabri.year_6_amount, gabri.reviewed_year_6_amount,
			(gabri.year_6_amount - gabri.reviewed_year_6_amount) as difference6,
			gabri.year_7_amount, gabri.reviewed_year_7_amount,
			(gabri.year_7_amount - gabri.reviewed_year_7_amount) as difference7,
			gabri.year_8_amount, gabri.reviewed_year_8_amount,
			(gabri.year_8_amount - gabri.reviewed_year_8_amount) as difference8,
			gabri.year_9_amount, gabri.reviewed_year_9_amount,
			(gabri.year_9_amount - gabri.reviewed_year_9_amount) as difference9,
			gabri.year_10_amount, gabri.reviewed_year_10_amount,
			(gabri.year_10_amount - gabri.reviewed_year_10_amount) as difference10, 
			gabr.company 
	FROM `tabGrant Application Budget Review Item` gabri, `tabGrant Application Budget Review` gabr 

	LEFT JOIN `tabGrant Application` ga 
		ON gabr.grant_application = ga.name
	WHERE 
		gabr.name = gabri.parent
		and gabr.docstatus=1 %s
	""" % conditions, filters, as_dict=1)

	return data

# add subtotal of rows based on grouping by
def add_subtotal_row(data, grouped_applications, group_by_field, group_by_value):
	amount = sum(d.amount for d in grouped_applications)
	reviewed_amount = sum(d.reviewed_amount for d in grouped_applications)
	difference = sum(d.difference for d in grouped_applications)
	year_1_amount = sum(d.year_1_amount for d in grouped_applications)
	reviewed_year_1_amount = sum(d.reviewed_year_1_amount for d in grouped_applications)
	difference1 = sum(d.difference1 for d in grouped_applications)
	year_2_amount = sum(d.year_2_amount for d in grouped_applications)
	reviewed_year_2_amount = sum(d.reviewed_year_2_amount for d in grouped_applications)
	difference2 = sum(d.difference2 for d in grouped_applications)
	year_3_amount = sum(d.year_3_amount for d in grouped_applications)
	reviewed_year_3_amount = sum(d.reviewed_year_3_amount for d in grouped_applications)
	difference3 = sum(d.difference3 for d in grouped_applications)
	year_4_amount = sum(d.year_4_amount for d in grouped_applications)
	reviewed_year_4_amount = sum(d.reviewed_year_4_amount for d in grouped_applications)
	difference4 = sum(d.difference4 for d in grouped_applications)
	year_5_amount = sum(d.year_5_amount for d in grouped_applications)
	reviewed_year_5_amount = sum(d.reviewed_year_5_amount for d in grouped_applications)
	difference5 = sum(d.difference5 for d in grouped_applications)
	year_6_amount = sum(d.year_6_amount for d in grouped_applications)
	reviewed_year_6_amount = sum(d.reviewed_year_6_amount for d in grouped_applications)
	difference6 = sum(d.difference6 for d in grouped_applications)
	year_7_amount = sum(d.year_7_amount for d in grouped_applications)
	reviewed_year_7_amount = sum(d.reviewed_year_7_amount for d in grouped_applications)
	difference7 = sum(d.difference7 for d in grouped_applications)
	year_8_amount = sum(d.year_8_amount for d in grouped_applications)
	reviewed_year_8_amount = sum(d.reviewed_year_8_amount for d in grouped_applications)
	difference8 = sum(d.difference8 for d in grouped_applications)
	year_9_amount = sum(d.year_9_amount for d in grouped_applications)
	reviewed_year_9_amount = sum(d.reviewed_year_9_amount for d in grouped_applications)
	difference9 = sum(d.difference9 for d in grouped_applications)
	year_10_amount = sum(d.year_10_amount for d in grouped_applications)
	reviewed_year_10_amount = sum(d.reviewed_year_10_amount for d in grouped_applications)
	difference10 = sum(d.difference10 for d in grouped_applications)

	data.append({
		group_by_field: group_by_value,
		"amount": amount,
		"reviewed_amount":reviewed_amount,
		"difference":difference,
		"year_1_amount":year_1_amount,
		"reviewed_year_1_amount":reviewed_year_1_amount,
		"difference1":difference1,
		"year_2_amount":year_2_amount,
		"reviewed_year_2_amount":reviewed_year_2_amount,
		"difference2":difference2,
		"year_3_amount":year_3_amount,
		"reviewed_year_3_amount":reviewed_year_3_amount,
		"difference3":difference3,
		"year_4_amount":year_4_amount,
		"reviewed_year_4_amount":reviewed_year_4_amount,
		"difference4":difference4,
		"year_5_amount":year_5_amount,
		"reviewed_year_5_amount":reviewed_year_5_amount,
		"difference5":difference5,
		"year_6_amount":year_6_amount,
		"reviewed_year_6_amount":reviewed_year_6_amount,
		"difference6":difference6,
		"year_7_amount":year_7_amount,
		"reviewed_year_7_amount":reviewed_year_7_amount,
		"difference7":difference7,
		"year_8_amount":year_8_amount,
		"reviewed_year_8_amount":reviewed_year_8_amount,
		"difference8":difference8,
		"year_9_amount":year_9_amount,
		"reviewed_year_9_amount":reviewed_year_9_amount,
		"difference9":difference9,
		"year_10_amount":year_10_amount,
		"reviewed_year_10_amount":reviewed_year_10_amount,
		"difference10":difference10,
		"bold": 1
	})
	data.append({})


# generate graphs
def get_chart_data(data):
	grant_application_budget_map = {}
	labels, datapoints = [], []

	for row in data:
		column_key = row.get("grant_application")

		if not column_key in grant_application_budget_map:
			grant_application_budget_map[column_key] = 0

		grant_application_budget_map[column_key] = flt(grant_application_budget_map[column_key]) + flt(row.get("amount"))

	grant_application_budget_map = { item: value for item, value in (sorted(grant_application_budget_map.items(), key = lambda i: i[1], reverse=True))}

	for key in grant_application_budget_map:
		labels.append(key)
		datapoints.append(grant_application_budget_map[key])

	return {
		"data" : {
			"labels" : labels[:30], # show max of 30 items in chart
			"datasets" : [
				{
					"name" : _(" Total Amount"),
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
			conditions += " and gabr.date >= %(from_date)s"

	if filters.get("to_date"):
			conditions += " and gabr.date <= %(to_date)s"

	if filters.get("grant_call"): 
			conditions += " and gabr.grant_call = %(grant_call)s"

	if filters.get("grant_application"):
			conditions += " and gabr.grant_application = %(grant_application)s"

	if filters.get("company"):
			conditions += " and gabr.company = %(company)s"

	if filters.get("institution"):
			conditions += " and ga.institution = %(institution)s"

	if not filters.get("group_by"):
		conditions += "ORDER BY gabr.name desc"
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
	elif group_by == "Grant Application Budget Review":
		group_by_field = "name"
	
	return group_by_field
	
