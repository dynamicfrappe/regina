# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import throw , _ 
class PaymentPaperReceive(Document):

	"""
	on submit this document will create payment paper for each valid record 
	
	
	"""
	def validate(self):
		self.create_payments()
		self.create_payment_paper()

	def create_payments(self) :
		if not self.payment_paper_receive_item :
			for i in range(0 , int(self.total_paper_count)) :
				self.append("payment_paper_receive_item" ,{
					"date" :self.date ,
					"amount":0
				})
		if len(self.payment_paper_receive_item) > 0 :
		
			self.calculate_totals()

	def calculate_totals(self):
		
		self.total_count = 0 
		self.total_amount = 0 

		for i in self.payment_paper_receive_item :
			
			if i.status =="Valid" :
				print("valid")
				self.total_count = int(self.total_count or 0) + 1
				self.total_amount = float(self.total_amount) + float(i.amount)


	def on_submit(self) :
		pass

	def create_payment_paper(self) :
		for paper in self.payment_paper_receive_item :	
			if paper.status == "Valid" and not paper.payment_paper :
				payment_paper = frappe.new_doc("Payment Paper")
				payment_paper.due_date = paper.date 
				payment_paper.total_amount = paper.amount 
				payment_paper.outstanding_amount = paper.amount
				payment_paper.serial_number = self.contract_serial_number
				payment_paper.agent = self.agent
				payment_paper.location_status = "On Site"
				payment_paper.save()

				paper.payment_paper = payment_paper.name
