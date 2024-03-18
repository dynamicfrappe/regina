# Copyright (c) 2023, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 
from frappe.model.document import Document

class Agent(Document):
	def validate(self) :
		#run validate method here 
		# 1 calculate annuel fees
		self.calculate_tax()
		self.set_annual_table_services()

	def calculate_item_tax(self , template , fees) :
		tax_template = frappe.get_doc("Sales Taxes and Charges Template" , template )
		
		tax  ,discount = 0 , 0 
		for i in tax_template.taxes : 
			if i.rate > 0 :
				tax+= float(fees ) * (i.rate / 100)
			if i.rate < 0 :
				discount += float(fees) * ((i.rate * -1) / 100)

		return (tax ,discount)
	def calculate_tax(self) :
		tax_template = frappe.db.get_single_value("Management Settings" , "agent_default_tax_template")
		if not tax_template :
			frappe.throw(_(""" Please Set default tax template in Management Settings"""))
      #get default tax template 
		

		#calculate tax values 
		for item in  self.agent_price_list :
			tax_fees = self.calculate_item_tax(tax_template , item.agent__fees)
			item.agent__fees_tax  = tax_fees[0]
			item.agent_fee_discount_tax = tax_fees[1]

	def set_annual_table_services(self) :
		self.annual_services = []
		for fee in self.agent_price_list :
			if fee.annual_services  :
				#set annual services base on template
				#service Template 
				
				# if not self.annual_services  or len(self.annual_services) == 0 :
				template = frappe.get_doc("Annual Services Template" , fee.annual_services)
				for service in template.services :
					raw = self.append("annual_services")
					# main info
					raw.capacity = fee.capacity 
					raw.company_name =fee.company_name 
					raw.contract_type = fee.contract_type 
					# service info
					raw.service_type = service.service_type 
					raw.annual_cost= service.annual_cost
		