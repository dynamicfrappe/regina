import frappe 
from frappe import _ 


def send_to_agent(serial ,agent) :
		pass

#from contract_serial_number import regina.collections_management.contollers.contract_serial_number.receive_contract
@frappe.whitelist()
def receive_contract(serial , date , *args , **kwargs) :
		return 1


