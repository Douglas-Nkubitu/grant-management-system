# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator

class GrantCall(WebsiteGenerator):
    website = frappe._dict(
        condition_field="published",
        page_title_field = "grant_call_name",
        template= "templates/generators/grant_call.html",
        no_cache=1
    )

    def get_context(self, context):
        context.parents = [{"name":frappe._("Home"), "route":"/"}]

        return context

    # Copy grant application parameters from template
    @frappe.whitelist()
    def copy_grant_application_parameters_from_template(self):

        if self.grant_application_template:
            # Validations
            if not self.programme:
                frappe.throw(_("Please select the Grant Programme"),
                             title=_("Grant Programme Required"))
            # End Validations
            # pull grant application parameters from the template
            template_parameters = get_grant_template_application_parameters(self)

            if template_parameters:
                self.add_parameter_in_grant_application_table(
                    template_parameters)
            else:
                frappe.msgprint(_("Grant Parameters are not available for the programme template."), title=_(
                    "Programme Template Parameters Missing"))

    # Add parameter types in the grant template parameters child table
    def add_parameter_in_grant_application_table(self, template_parameters):
        """ Add parameter in the grant application parameters child table"""
        self.set('grant_application_parameters', [])

        for data in template_parameters:
            self.append('grant_application_parameters', {
                'parameter': data.parameter,
                'item_description': data.item_description,
                'required': data.required,
                'is_numeric': data.is_numeric
            })

    # Copy grant application report parameters from template
    @frappe.whitelist()
    def copy_grant_application_report_parameters_from_template(self):

        if self.grant_reporting_template:
            # Validations
            if not self.programme:
                frappe.throw(_("Please select the Grant Programme"),
                             title=_("Grant Programme Required"))
            # End Validations
            # pull grant application parameters from the template
            template_parameters = get_grant_template_reporting_parameters(self)

            if template_parameters:
                self.add_parameter_in_grant_application_report_table(
                    template_parameters)
            else:
                frappe.msgprint(_("Grant Parameters are not available for the programme template."), title=_(
                    "Programme Template Parameters Missing"))

    # Add parameter types in the grant template parameters child table
    def add_parameter_in_grant_application_report_table(self, template_parameters):
        """ Add parameter in the grant application parameters child table"""
        self.set('grant_reporting_parameters', [])

        for data in template_parameters:
            self.append('grant_reporting_parameters', {
                'parameter': data.parameter,
                'item_description': data.item_description,
                'required': data.required,
                'is_numeric': data.is_numeric
            })

#Copy grant parameters from tabGrant Template,
#these are to be used when creating grants of the particular programme
def get_grant_template_application_parameters(self):

        template_parameters = frappe.db.sql("""
    	    SELECT distinct gct.name, gct.programme, gctp.*
    	    FROM `tabGrant Call Template` gct,
		         `tabGrant Call Template Parameter` gctp
    	    WHERE gct.name = %(grant_application_template)s
            and gct.programme = %(programme)s
            and gct.name = gctp.parent
		    and gct.disabled = 0
		    order by gctp.idx
		    """.format(1), {
            "grant_application_template": self.grant_application_template,
            "programme": self.programme
        }, as_dict=1)
        return template_parameters

#Copy grant parameters from tabGrant Template,
#these are to be used when creating grants of the particular programme
def get_grant_template_reporting_parameters(self):

        template_parameters = frappe.db.sql("""
    	    SELECT distinct gct.name, gct.programme, gctp.*
    	    FROM `tabGrant Call Template` gct,
		         `tabGrant Call Template Parameter` gctp
    	    WHERE gct.name = %(grant_reporting_template)s
            and gct.programme = %(programme)s
            and gct.name = gctp.parent
		    and gct.disabled = 0
		    order by gctp.idx
		    """.format(1), {
            "grant_reporting_template": self.grant_reporting_template,
            "programme": self.programme
        }, as_dict=1)

        return template_parameters

        
@frappe.whitelist(allow_guest=True)
def open_search_grant(text):
    filters = {"docstatus": 1,"published": 1,"closing_date":[">=", frappe.utils.nowdate()]}    

    active_grant_list = frappe.get_all("Grant Call",
                    filters = filters,
                    or_filters = {
                        "name": ["like", "%{0}%".format(text)],
                        "grant_call_name": ["like", "%{0}%".format(text)],
                        "programme": ["like", "%{0}%".format(text)],
                        "discipline": ["like", "%{0}%".format(text)],
                    },
                    fields = ["name", "grant_call_name","programme", "discipline","opening_date","closing_date","route"],
                    start=0)
    
    active_grant= []
    for grantcall in active_grant_list:
        active_grant.append(grantcall)

    return active_grant_list

@frappe.whitelist(allow_guest=True)
def closed_search_grant(text):
    filters = {"docstatus": 1,"published": 1,"closing_date":["<", frappe.utils.nowdate()]}    

    closed_grant_list = frappe.get_all("Grant Call",
                    filters = filters,
                    or_filters = {
                        "name": ["like", "%{0}%".format(text)],
                        "grant_call_name": ["like", "%{0}%".format(text)],
                        "programme": ["like", "%{0}%".format(text)],
                        "discipline": ["like", "%{0}%".format(text)],
                    },
                    fields = ["name", "grant_call_name", "programme", "discipline", "opening_date","closing_date","route"],
                    start=0)

    closed_grant = []
    for grantcall in closed_grant_list:
        closed_grant.append(grantcall)

    return closed_grant_list
