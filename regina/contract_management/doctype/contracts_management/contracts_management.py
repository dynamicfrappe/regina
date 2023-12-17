# Copyright (c) 2023, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _


from frappe.model.document import Document

class ContractsManagement(Document):
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
						"recieve_date" :serial.receive_date } 

							)
