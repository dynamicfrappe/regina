import frappe 
from frappe import _ 
import json


@frappe.whitelist()
def create_lead(*args , **kwargs) :
   data = json.loads(kwargs.get("args"))
   
   lead = frappe.new_doc("Lead")
   lead.lead_name = data.get("lead_name") 
   # lead.company_name = kwargs.get("company_name")
   lead.status= "Lead"
   lead.email_id = data.get("email_id")
   lead.mobile_no = data.get("mobile_no")
   lead.gender = data.get("gender")
   lead.source = data.get("source")
   lead.save()
   frappe.db.commit()
   return {"name" :lead.name , "lead_name" :lead.lead_name }

@frappe.whitelist()
def get_name(document_type , document) :
   field = "customer_name" if document_type == "Customer" else "lead_name"
   name  = frappe.db.get_value(f"{document_type}" , document , f"{field}")
   return name