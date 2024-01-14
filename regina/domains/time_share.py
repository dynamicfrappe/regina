from __future__ import unicode_literals
import frappe
from frappe import _


data = {
    'custom_fields':{ 
        "Contract" :[{
            "label"        :_("Contract Type"),
            "insert_after" : "status" ,
            "fieldtype"    : "Link",
            "options"      : "Contract Type" ,
            "fieldname"    : "contract_type",
            "read_only"    : 0 ,
            "depends_on": None ,
            "default":None

        } ,
        {
            "label"        :_("Agent"),
            "insert_after":"contract_type", 
            "fieldtype"    : "Link",
            "options"      : "Agent" ,
            "fieldname"    : "agent",
            "read_only" : 1 

            
        } ,
        {
            "label"        :_("Contract Serial Number"),
            "insert_after"  :"agent", 
            "fieldtype"    : "Link",
            "options"      : "Contract Serial Number" ,
            "fieldname"    : "contract_serial_number",
            "read_only" : 1 

            
        } ,
       


        ],
        "Company":[
            {    
                "label"        :_("Commercial ID"),
                "insert_after" :"tax_id", 
                "fieldtype"    : "Data",
                "fieldname"    : "com_id",
                "read_only"    : 0

            
            } ,

        ],
        "Item":[
            {    
                "label"        :_("Room Number"),
                "fieldname" :"room_number", 
                "insert_after" :"brand", 
                "fieldtype"    : "Int",
                "read_only"    : 0

            
            } ,
            {    
                "label"        :_("Room Number"),
                "fieldname" :"room_number", 
                "insert_after" :"brand", 
                "fieldtype"    : "Int",
                "read_only"    : 0

            
            } ,
            {    
                "label"        :_("Room Type"),
                "fieldname" :"room_type", 
                "insert_after" :"room_number", 
                "fieldtype"    : "Link",
                "options"    : "Room Type",
                "read_only"    : 0

            
            } ,
            {    
                "label"        :_("Room View"),
                "fieldname" :"room_view", 
                "insert_after" :"room_type", 
                "fieldtype"    : "Link",
                "options"    : "Room View",
                "read_only"    : 0
            } ,
            {    
                "label"        :_("Location"),
                "fieldname" :"resort", 
                "insert_after" :"room_view", 
                "fieldtype"    : "Link",
                "options"    : "Resort",
                "read_only"    : 0
            } ,

        ],
       
          "Customer":[
              {    
                "label"        :_("Contract Info"),
                "fieldname" :"contract_info", 
                "insert_after" :"represents_company", 
                "fieldtype"    : "Section Break",
            } ,
            {    
                "label"        :_("Is Egyptian"),
                "fieldname" :"is_egyptian", 
                "insert_after" :"contract_info", 
                "fieldtype"    : "Check",
                "read_only"    : 0
            } ,
            {    
                "label"        :_("Nationality"),
                "fieldname" :"nationality", 
                "insert_after" :"is_egyptian", 
                "fieldtype"    : "Link",
                "options"    : "Nationality",
                "read_only"    : 0,
                "depends_on"    :"eval:doc.is_egyptian==0",
                "mandatory_depends_on"    :"eval:doc.is_egyptian==0",
                
            } ,
            {    
                "label"        :_("Occopation"),
                "fieldname" :"occopation", 
                "insert_after" :"nationality", 
                "fieldtype"    : "Data",
                "read_only"    : 0
            } ,
            {    
                "label"        :_("Age"),
                "fieldname" :"age", 
                "insert_after" :"occopation", 
                "fieldtype"    : "Int",
                "read_only"    : 0
            } ,
            {    
                "label"        :_("National ID"),
                "fieldname" :"national_id", 
                "insert_after" :"age", 
                "fieldtype"    : "Int",
                "read_only"    : 0,
                "depends_on"    :"eval:doc.is_egyptian",
                "mandatory_depends_on"    :"eval:doc.is_egyptian",
            } ,
            {    
                "label"        :_(""),
                "fieldname" :"column_contract", 
                "insert_after" :"national_id", 
                "fieldtype"    : "Column Break",
            } ,
            {    
                "label"        :_("Issued date"),
                "fieldname"    :"issued_date", 
                "insert_after" :"column_contract", 
                "fieldtype"    : "Date",
                "read_only"    : 0
            } ,
            {    
                "label"        :_("Passport No"),
                "fieldname"    :"passport_no", 
                "insert_after" :"issued_date", 
                "fieldtype"    : "Int",
                "read_only"    : 0,
                "depends_on"    :"eval:doc.is_egyptian==0",
                "mandatory_depends_on"    :"eval:doc.is_egyptian==0",
            } ,
            {    
                "label"        :_("Resident Permission"),
                "fieldname"    :"resident_Permission", 
                "insert_after" :"passport_no", 
                "fieldtype"    : "Data",
                "read_only"    : 0
            } ,
          ]           
      }
        
    ,
    "properties": [
    ] ,
     # 'on_setup': 'regina.regina.setup.setup_time_share'
    
    }