import frappe 
from frappe import _ 




@frappe.whitelist()
def receive_contract(doc, *args , **kwargs) :
   name ,agent , contract_type ,item_group= frappe.db.get_value("Contract Serial Number" , doc ,
                     ['name' ,'agent' , 'contract_type','item_group'])
   document = frappe.get_doc("Contract Serial Number" ,doc)
   terms = frappe.db.get_value("Contract Type" ,contract_type , "contract_terms")
   contract = frappe.new_doc("Contract") 
   contract.party_type = "Agent"
   contract.party_name = agent
   contract.serial_number = name
   contract.agent = agent
   contract.item_group = item_group
   contract.contract_type = contract_type
   contract.contract_terms = terms
   contract.brand = document.brand
   contract.room_type = document.room_type
   #add cash payment
   contract.append("contract_payments" , {
      "due_date" :document.recieve_date ,
      "type" :"Cash" ,
      "amount" :document.total_cash ,
      "descreption" : "Cash" 

   })

   #get payment dates from  valid receive payment papers
   payment_paper_doc = frappe.get_doc("Payment Paper Receive", {"contract_serial_number":doc})
   for item in payment_paper_doc.payment_paper_receive_item :
      contract.append("contract_payments" ,
                      {
                        "due_date" :item.date ,
                        "type" :"Payment Paper" ,
                        "amount" :item.amount ,
                        "descreption" : "Payment Paper" 

            })
      

   agent = frappe.get_doc("Agent" , agent)
   for i in agent.annual_services :
      if i.contract_type == document.contract_type and i.capacity == document.room_type and i.company_name ==document.item_group:
         contract.append("annual_services" ,{
            "contract_type" : document.contract_type ,
              "company_name" : document.item_group ,
              "capacity" :document.room_type ,
              "annual_cost" :i.annual_cost ,
              "service_type" : i.service_type

         })


   contract.save()
   return contract.name 





