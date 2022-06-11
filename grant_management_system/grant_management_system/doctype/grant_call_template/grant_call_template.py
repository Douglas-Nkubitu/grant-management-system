# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class GrantCallTemplate(Document):

    # Get grant parameter types
    @frappe.whitelist()
    def create_grant_parameters(self):
        # Validations
        if not self.programme:
            frappe.throw(_("Please select the Grant Programme"),
                         title=_("Grant Programme Required"))
        # End Validations

        """ Pull non disabled grant parameter for the respective programme selected"""
        grant_parameters = get_grant_parameters(self)

        if grant_parameters:
            self.add_parameter_in_table(grant_parameters)
        else:
            frappe.msgprint(_("Grant Parameters are not available for the programme, please create them manually."), title=_(
                "Grant Parameter Missing"))

    # Add parameter types in the grant template parameters child table
    def add_parameter_in_table(self, grant_parameter_types):
        """ Add parameter types in the grant template parameters child table"""
        self.set('parameters', [])

        for data in grant_parameter_types:
            self.append('parameters', {
                'parameter': data.grant_parameter_name,
                'item_description': data.item_description,
                'required': data.required,
                'is_numeric': data.is_numeric
            })

# Get grant parameters from the list defined in tabGrant Parameter Type,
# these are to be used when creating grant templates
def get_grant_parameters(self):

    grant_parameters = frappe.db.sql("""
    	SELECT distinct gp.*
    	FROM `tabGrant Parameter` gp
    	WHERE gp.disabled = 0
        and gp.grant_parameter_name in (select parent 
                                         from `tabGrant Parameter Programme` gpp
                                         where gpp.programme = %(programme)s)
        and gp.grant_parameter_name not in(select parameter from `tabGrant Call Template Parameter` gctp
                                            where gctp.parent = %(parent)s)
		order by gp.parameter_sequence, gp.idx
		""".format(1), {
        "programme": self.programme,
        "parent": self.parent
    }, as_dict=1)
    return grant_parameters
