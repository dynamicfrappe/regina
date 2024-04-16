# Copyright (c) 2023, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _


from frappe.model.document import Document

class ContractsManagement(Document):

	def on_cancel(self):
		self.valide_befor_cancel()
		self.change_status()

		
	def valide_befor_cancel(self):
		for item in self.items:
			temp = frappe.get_doc("Contract Serial Number" , item.contract_serial_number)

			if self.document_method == "Receive" and temp.status == "Completed":
				frappe.throw("This Serial number {} has status completed".format(temp.name))
				return False
		
			if self.document_method == "Send" and temp.status == "With Agent":
				frappe.throw("This Serial number {} has status With Agent".format(temp.name))
				return False



	def change_status(self):
		for item in self.items:
			if self.document_method == "Receive":
				temp = frappe.get_doc("Contract Serial Number" , item.contract_serial_number)
				if temp.status == "On Progress":
					temp.status = "With Agent"
					temp.recieve_date = None
					temp.save()





	"""
	On Submit this document 
	   change serial number status and set agent --
	
	
	"""
	def validate(self) :
		"""
		validate status 
		  if status send -- check if contract is on site if not throw validation error 
		  if status receive check if contract serial number is with current agent 
		"""
		if self.document_method == "Send" :
			self.validate_send_serials()
			self.validate_payment_details()
		if self.document_method == "Receive" :
			self.validate_received_serials()
			self.validate_items_values()
			self.calculate_totals_values()
			self.validate_payment_details()
			#for test remove it in production 
			#self.create_payment_paper()
	def on_submit(self) :
		self.set_serial_number_values()
		self.create_payment_paper()

	def validate_payment_details(self) :
		#get agent accepted contract Type 
		agent = frappe.get_doc("Agent" , self.agent)
		for serial in self.items :
			accepted_type = False
			serial_number = frappe.get_doc("Contract Serial Number" , serial.contract_serial_number)
			if not serial_number.item_group :
				frappe.throw(_(f""" Please set Company name to serial number { serial.contract_serial_number}""") )
			if not serial_number.room_type: 
				frappe.throw(_(f""" Please set Room  Type  to serial number { serial.contract_serial_number}""") )
			for accepted in agent.agent_price_list  :
				if accepted.contract_type == serial_number.contract_type and accepted.capacity == serial_number.room_type:
					serial.agent_contract_price = accepted.total_payment_amount
					accepted_type  = True 
			if accepted_type == False:
				frappe.throw(_(f""" Please set value for room type and contract type in agent data  """))
			print(accepted_type  , "accepted")	

				 
	def validate_send_serials(self) :
		for serial in self.items  :
			if not serial.send_date :
				serial.send_date = self.date
			serial.contract_status = "Send"
			serial.document_method == "Send"
			#CHECK SERIAL OLD AGENT 
			contract  = frappe.db.get_value('Contract Serial Number',
					 serial.contract_serial_number,['agent' , 'status'] , as_dict=1)
			if contract.agent :
				frappe.throw(_(f"Contract {serial.contract_serial_number}  already with agent {contract.agent}"))
			if contract.status != "On Site" :
				frappe.throw(_(f"Contract {serial.contract_serial_number} has invalid status {contract.status}"))

	
	def validate_received_serials(self):
		for serial in self.items  :
			if not serial.receive_date :
				serial.receive_date = self.date
			if not serial.contract_status or serial.contract_status =="Send" :
				serial.contract_status = "Completed"
			serial.document_method == "Receive"
			contract  = frappe.db.get_value('Contract Serial Number',
					 serial.contract_serial_number,['agent' , 'status'] , as_dict=1)
			if not contract.agent :
				frappe.throw(_(f"Contract {serial.contract_serial_number}  is not associated with {contract.agent}"))
			if contract.status == "On Site" :
				frappe.throw(_(f"Contract {serial.contract_serial_number} is on Site !"))

	# def get_agent_contract_amount(self) :
	# 	pass

	def set_serial_number_values(self) :
		if self.document_method == "Send" :
			for serial in self.items  :
				#Update Serial Number Values 
				frappe.db.set_value('Contract Serial Number', serial.contract_serial_number, {
						'agent': self.agent , 
						'status': 'With Agent' ,
						"send_date" :serial.send_date } 
						
									)
		if self.document_method == "Receive" :	
			agent = frappe.get_doc("Agent" , self.agent )
			for serial in self.items  :
				frappe.db.set_value('Contract Serial Number', serial.contract_serial_number, {
						'agent': self.agent , 
						'status': 'On Progress' ,
						"recieve_date" :serial.receive_date , 
						"total_cash" : serial.total_cash ,
						"total_payment_document_amount" : serial.total_payment_papers , 
						"total_payment_documentcount" : serial.total_payment_papers_count ,
						"grand_total" : serial.total_amount
						}
							)
				for item in agent.agent_price_list :
					for i in self.items :

						if item.capacity == i.room_type  and item.company_name == i.item_group:
							serial.agent_contract_price = item.total_payment_amount 

	def validate_items_values(self) :
		for item in self.items :
			if float(item.total_cash or 0) + float(item.total_payment_papers or 0) != float(item.total_amount or 0) :
				total_payments = float(item.total_cash or 0 ) + float(item.total_payment_papers or 0)
				frappe.throw(_(f""" Total Amount is {item.total_amount}
		                     and total cash is {item.total_cash} 
									and total payment paper amount is {item.total_payment_papers }
									Please validate amounts
									  difference is {total_payments - float(item.total_amount)} """))

	#calculate collection and validate amounts 
	def calculate_totals_values(self) :
		if self.document_method == "Receive" :
			self.total_cash = 0 
			self.total_payment_paper_amount = 0 
			self.total_payment_paper_count = 0 
			self.grand_total = 0 
			#validate totals 
			for item in  self.items :
				self.total_cash = self.total_cash + float( item.total_cash or 0)
				self.total_payment_paper_amount = self.total_payment_paper_amount + float( item.total_payment_papers or 0 )
				self.total_payment_paper_count = self.total_payment_paper_count + float( item.total_payment_papers_count or 0 )
				self.grand_total = self.grand_total + float(item.total_amount or 0)
				if float(item.total_cash or 0 ) + float(item.total_payment_papers or 0) != (float(item.total_amount or 0)) :
					
					frappe.msgprint(_(f""" in Contract {item.contract_serial_number}You have difference Value Between Collected Mony And Contract Total \n
		          Your Total Collection is {item.total_amount} and your collection mony and paper 
					 is {float(item.total_cash or 0 ) + float(item.total_payment_papers or 0)}
					
					 """))


	@frappe.whitelist()				
	def create_payment_paper(self) :
		for item in self.items :
			#create payment and payment paper 
			paper = frappe.new_doc("Payment Paper Receive")
			paper.date = item.receive_date 
			paper.contract_serial_number = item.contract_serial_number 
			paper.total_paper_count = item.total_payment_papers_count
			paper.total_paper_amount = item.total_payment_papers	
			paper.agent = self.agent	
			paper.save()


	@frappe.whitelist()
	def get_agent_amount(agent , room_type ,group) :
		pass
					








			


			
	

