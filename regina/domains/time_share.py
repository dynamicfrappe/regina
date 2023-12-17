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
       
       

    
                     
      }
        
    ,
    "properties": [
    ] ,
     # 'on_setup': 'regina.regina.setup.setup_time_share'
    
    }