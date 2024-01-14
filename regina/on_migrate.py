import frappe 



#create main domain


def set_weeks():
   weeks_max_count  = frappe.db.get_single_value('Management Settings', 'weeks_count_for_sales')
   if weeks_max_count and int(weeks_max_count) > 0 :
      for i in range( 1 , ( int(weeks_max_count) + 1)) :
         if not frappe.db.exists("Week Number", {"name1": i }):
            week = frappe.new_doc("Week Number")
            week.name1 = i
            week.save()
            print(f"Week Created Success {i}")
# setup domain  

def initial_values(*args , **kwargs) :

   print("""
   this function run coz in Management Settings Init Data = True \n
   make it to false to ignore initial data  
   
   """)
   """
   #
    Initial Values  

   init Brand As resort location
   init Item Group as village name
   init Room View -- See the sea or not(Internal)
   init Room Type  Capacity -- (One Bed - Two Beds - Three Beds - four beds - five beds - six beds - seven beds - eight beds  )


   """
   #Create Brand Labels 
   brands =     ['العين السخنة' , 'الغردقة']
   room_views = ["See the Sea" , "Internal"] #key room_view
   room_types = ["One bed" , "Two beds" , 'Three beds' , 'Four beds' , 'Five beds' , 'Six beds' ,
                 'Seven beds' , 'Eight beds']
   for i in brands : 
      if not frappe.db.exists("Brand", {"brand": i }):
         brand = frappe.new_doc("Brand")
         brand.brand = i 
         brand.save()
         print("Brand Init Success")
   for v in room_views :
      if not frappe.db.exists("Room View", {"room_view": v }):
         view = frappe.new_doc("Room View")
         view.room_view = v 
         view.save()
         print("Room View Init Success")
   for t in room_types :
      if not frappe.db.exists("Room Type", {"room_name": t }):
         room = frappe.new_doc("Room Type")
         room.room_name = t
         room.save()
         print("Room Type Init Success")


   
def make_migrations(*args ,**kwargs) :
   setup_domain_time_share()
   init_data = frappe.db.get_single_value('Management Settings', 'init_data')
   if init_data :
      initial_values()
      set_weeks()
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



