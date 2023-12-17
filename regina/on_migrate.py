import frappe 



#create main domain
# setup domain  

def make_migrations(*args ,**kwargs) :
   setup_domain_time_share()

def setup_domain_time_share(*ars , **kwargs):  
   domain = False
   if frappe.db.exists("Domain", {"domain": "Time Share"}): 
      domain = frappe.get_doc("Domain" ,"Time Share")
   if not frappe.db.exists("Domain", {"domain": "Time Share"}):
      print("++ Create domain Time Share ++")
      domain = frappe.new_doc("Domain")
      domain.domain ="Time Share"
      domain.save()
      frappe.db.commit()

   if domain :
      domain.setup_domain()