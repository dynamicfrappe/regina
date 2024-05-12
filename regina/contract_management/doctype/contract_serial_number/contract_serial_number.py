# Copyright (c) 2023, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today  



class ContractSerialNumber(Document):

	def validate(self):
		pass
	def send_to_agent(self ,agent) :
		pass

	def receive_contract(self , date) :
		pass





def send_to_agent(self ,agent) :
		pass

def receive_contract(self , date) :
	pass



@frappe.whitelist()
def check_agent_and_status(contract_serial_number):
    contract_agent = frappe.db.get_value("Contract Serial Number", contract_serial_number, "agent")
    payment_paper_receive = frappe.get_all("Payment Paper Receive", filters={"agent": contract_agent}, fields=["name"])
    
    for ppr in payment_paper_receive:
        valid_items = frappe.get_all("Payment Paper Receive Item", filters={"parent": ppr.name, "status": "Valid"}, fields=["name"])
        total_items = frappe.get_all("Payment Paper Receive Item", filters={"parent": ppr.name}, fields=["name"])
        
        if len(valid_items) != len(total_items):
            return False
    
    return True
 


@frappe.whitelist()
def compare_contract_serial_numbers(contract_serial_number):
    doc_name = get_document_name(contract_serial_number)

    if doc_name:
        payment_doc = frappe.get_value("Payment Paper Receive", {"contract_serial_number": contract_serial_number}, "name")
        
        if payment_doc:
            valid_child_record = frappe.db.exists(
                "Payment Paper Receive Item",
                {"parent": payment_doc, "status": "Valid"}
            )
            if valid_child_record:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def get_document_name(contract_serial_number):
    doc = frappe.get_doc("Contract Serial Number", contract_serial_number)
    
    if doc:
        return doc.name
    else:
        return None

          
     





