# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today
class PaymentPaper(Document):
	def validate(self) :
	
		if self.location_status == "On Site" and self.collector :
			
			# frappe.throw("Va")
			self.location_status= "With Collector"
		print("DD Date" ,self.deliverd_to_collector_date)	
		if not self.deliverd_to_collector_date   and self.collector :
			self.deliverd_to_collector_date = today()
		#update payment status
		self.validate_status()

	def validate_status(self) :
		if float(self.paid_amount or 0) > 0  and float(self.paid_amount or 0) < float(self.total_amount or 0) :
			self.status = "Partial Paid"	
		if float(self.paid_amount or 0) > 0  and float(self.paid_amount or 0) >= float(self.total_amount or 0) :
			self.status = "Completed"