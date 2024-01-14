import frappe 
from frappe import _ 





def get_reserved_weeks(item) :
   reserved_weeks = frappe.db.sql( f"""SELECT week FROM `tabWeek Ben Ledger` WHERE unit='{item}'"""  )
   return reserved_weeks



@frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
def get_available_weeks_for_item(* args , **kwargs ) :

   item = args[-1].get("item")
   """
   item  : item code As string 
   return All weeks number that item has no reservation 
   """
   reserved_weeks = frappe.db.sql(f"""
      SELECT name FROM `tabWeek Number` 
      where name not in (
       SELECT week FROM `tabWeek Ben Ledger` WHERE unit='{item}'
       );
       """ )
   return reserved_weeks 