import frappe 
from frappe import _ 




@frappe.whitelist()
def receive_contract(doc, *args , **kwargs) :
   name ,agent , contract_type = frappe.db.get_value("Contract Serial Number" , doc ,
                     ['name' ,'agent' , 'contract_type'])

   terms = frappe.db.get_value("Contract Type" ,contract_type , "contract_terms")
   contract = frappe.new_doc("Contract") 
   contract.party_type = "Agent"
   contract.party_name = agent
   contract.contract_serial_number = name
   contract.agent = agent
   contract.contract_type = contract_type
   contract.contract_terms = terms
   contract.save()
   return contract.name 





