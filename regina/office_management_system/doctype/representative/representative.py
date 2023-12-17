# Copyright (c) 2023, Dynamic Business Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Representative(Document):
	def validate(self) :
		#set Full name 
		self.full_name = f"""{self.first_name} {self.last_name}"""