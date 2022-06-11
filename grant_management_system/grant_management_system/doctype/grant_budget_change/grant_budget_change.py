# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from six import iteritems
from email_reply_parser import EmailReplyParser
from frappe.utils import (flt, getdate, get_url, now,
                          nowtime, get_time, today, get_datetime, add_days)
from erpnext.controllers.queries import get_filters_cond
from frappe.desk.reportview import get_match_cond
from frappe.model.document import Document

class GrantBudgetChange(Document):

    # Copy grant application budget items
    @frappe.whitelist()
    def copy_grant_application_budget_items(self):

        if self.grant_application:

            # pull grant application budget items
            budget_items = get_grant_application_budget_items(self)

            if budget_items:
                self.add_grant_budget_change_item(budget_items)
            else:
                frappe.msgprint(_("Budget items are not available for the Grant Application."), title=_(
                    "Grant Application Budget Missing"))

    # Add budget items to budget change item
    def add_grant_budget_change_item(self, budget_items):
        """ Add budget items in the child table"""
        self.set('items', [])

        for data in budget_items:
            self.append('items', {
				'budget_item': data.budget_item,
                'unit_of_measure': data.unit_of_measure,
                'qty': data.qty,
                'cost': data.cost,
                'amount': data.amount,
                'year_1_amount': data.year_1_amount,
                'year_2_amount': data.year_2_amount,
                'year_3_amount': data.year_3_amount,
                'year_4_amount': data.year_4_amount,
                'year_5_amount': data.year_5_amount,
                'year_6_amount': data.year_6_amount,
                'year_7_amount': data.year_7_amount,
                'year_8_amount': data.year_8_amount,
                'year_9_amount': data.year_9_amount,
                'year_10_amount': data.year_10_amount,
                'item_description': data.item_description
            })

#get_grant_application_budget_items
def get_grant_application_budget_items(self):

        grant_application_budget_items = frappe.db.sql("""
    	    SELECT gabi.*
    	    FROM `tabGrant Application Budget Item` gabi
    	    WHERE gabi.parent = %(grant_application)s
		    order by gabi.idx
		    """.format(1), {
            "grant_application": self.grant_application
        }, as_dict=1)
        return grant_application_budget_items