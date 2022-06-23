# Copyright (c) 2022, Navari Limited and contributors
# For license information, please see license.txt

from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.model.document import Document


class Donor(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def validate(self):
		from frappe.utils import validate_email_address

		if self.email:
			validate_email_address(self.email.strip(), True)
