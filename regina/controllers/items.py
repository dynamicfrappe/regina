import frappe 
from frappe import _ 
from frappe.utils import getdate ,today , add_to_date




def get_reserved_weeks(item) :
   reserved_weeks = frappe.db.sql( f"""SELECT week FROM `tabWeek Ben Ledger` WHERE unit='{item}'"""  )
   return reserved_weeks



@frappe.whitelist()
#@frappe.validate_and_sanitize_search_inputs --later update 
def get_available_weeks_for_item(* args , **kwargs ) :
   print(f"+++++++++++++++++++++++ Got You +++++++++++++++++++++++++++ {args}")
   item = args[-1].get("item")
  
   """
   item  : item code As string 
   return All weeks number that item has no reservation 
   """
   reserved_weeks = frappe.db.sql(f"""
      SELECT name FROM `tabWeek Number` 
      where name not in (
       SELECT week FROM `tabWeek Ben Ledger` WHERE unit='{item}'
        ) 
       """ )
   
   
   return  reserved_weeks



@frappe.whitelist()
def get_item_reservation_data(year) :
   """
   params :
      year string year name 2024 
   function 
      create Unit Days Ledger for each Item with all data 
   
   """
   year_obj = frappe.get_doc("Year" , year) 
   start_date = getdate(year_obj.start_date )
   end_date  = getdate(year_obj.end_date )
   items = frappe.get_list("Item")  
   for item in items  :
      pro_date = start_date 
      while pro_date < end_date  :
         #chech if item with date has doc or not 
         if not frappe.db.exists("Unit Days Ledger" , {"date" :pro_date , 
                                                  "unit" :item.get("name")}) :
            ledger = frappe.new_doc("Unit Days Ledger")
            ledger.unit = item.get("name")
            ledger.date  = pro_date
            ledger.day_name    = pro_date.strftime("%A")
            ledger.year = year_obj.name
            ledger.save()
            frappe.db.commit()

         pro_date_update = add_to_date(pro_date , days =1 , as_string=True)
         pro_date = getdate(pro_date_update)


@frappe.whitelist()
def check_as_reserved(items=[] ,reserve = None ):
   print(items)