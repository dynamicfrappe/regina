import frappe 
from frappe import _ ,throw 



def calculate_contract_service_payments(con) :
   """
   con : -- > string contract erpnext name required 
   
   """
   #check if contract is valid 
   if not  frappe.db.exists('Contract', con) :
      throw(_(f"Contract With name {con} Not Found !"))
   contract = frappe.get_doc("Contract" , con)
   #validate Contract Status 
   
   

   pass