# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Year(Document):
	
	
	def validate(self):
		if not(int(self.name) >= 1990 and int(self.name) <=2050):
			frappe.throw("Year Should Be in Range 1990 - 2050")

