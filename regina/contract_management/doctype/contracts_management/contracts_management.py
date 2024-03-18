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
		if self.document_method == "Receive" :
			self.validate_received_serials()
			self.calculate_totals_values()
	def on_submit(self) :
		self.set_serial_number_values()


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
					 is {float(item.total_cash or 0 ) + float(item.total_payment_papers or 0)}"""))
					



# def on_change(self):
# 	if self.docstatus == 2:
# 		items = frappe.get_all(
#          		"Contract Management Items",
#          		filters={"parent": self.name},
#          		fields=["contract_serial_number", "total_cash" , "contract_status" , "item_group" , "contract_type" , "receive_date" , "room_type" , "agent_contract_price" , "document_method"]
#       		)
# 		if self.document_method == "Receive":
# 			for item in items:
# 				temp = frappe.get_doc("Contract Serial Number" , item.contract_serial_number)
# 				if temp.status == "On Progress":
# 					temp.status = "With Agent"
# 					temp.recieve_date = None
# 					temp.save()
# 				elif temp.status == "Completed":
# 						frappe.throw("")
# 						return False
# 		elif self.document_method == "Send":
# 			for item in items:
# 				temp = frappe.get_doc("Contract Serial Number" , item.contract_serial_number)
# 				if temp.status != "With Agent":




			


			
	

