# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class UnitReservation(Document):
	
	
	def validate(self):
		dt = datetime.strptime(self.from_date, '%Y-%m-%d')
		if dt.year == self.year:
			...
