import frappe

def update_representative_status(login_manager):
   user = frappe.get_doc("User" , frappe.session.user )   
   if frappe.db.exists('Representative', {'email': user.name}) :
      representative =frappe.db.get_value("Representative" ,{'email': user.name} , "name")
      frappe.db.set_value("Representative" ,representative , {"status": "On Line"} )
  


def clear_session_defaults():
   user = frappe.get_doc("User" , frappe.session.user )   
   if frappe.db.exists('Representative', {'email': user.name}) :
      representative =frappe.db.get_value("Representative" ,{'email': user.name} , "name")
      frappe.db.set_value("Representative" ,representative , {"status": "Off Line"} )
      print("log Out")