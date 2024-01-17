# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class UnitReservation(Document):
	
	
	def validate(self):
		dt_from = datetime.strptime(self.from_date, '%Y-%m-%d')
		dt_to = datetime.strptime(self.to_date, '%Y-%m-%d')
		if str(dt_from.year) != self.year or str(dt_to.year) != self.year:
			frappe.throw("Year in Date Should Be Same in Year")
