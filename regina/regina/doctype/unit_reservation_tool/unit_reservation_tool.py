# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UnitReservationTool(Document):
	pass


@frappe.whitelist()
def get_items(item_group = None , brand=None , room_view=None , room_type=None , 
	      				unit=None , start_date = None ,end_date =None):
	# item_marked = []
	# item_unmarked = []
	item_filters = {
		"item_group" : item_group , 
		"brand"      : brand , 
		"room_view"  : room_view , 
		"room_type"  : room_type , 
		"name"       : unit   ,
	}
	ledger_filetrs = [] 
	if item_group :
		ledger_filetrs.append({"group" : item_group})
	if room_view :
		ledger_filetrs.append({"room_view" : room_view})
	if room_type :
		ledger_filetrs.append({"room_type" : room_type})
	if unit :
		ledger_filetrs.append({"unit" : unit})

	if start_date :
		ledger_filetrs.append({"date" : [">=" , start_date]})
	if end_date  :
		ledger_filetrs.append({"date" : ["<=" , end_date]})

	item_filters = {k: v for k, v in item_filters.items() if v not in (None, "")}
	
	# get items and date range 

	items = frappe.db.get_list("Item" ,filters=item_filters , fields =[ 'name' , 'item_name' ,"room_number"])
	data = []
	applyed_filters = ledger_filetrs
	for item in items :
		print("Item --- >>>>>>>> " ,item)
		# get all item available dates 
		applyed_filters = ledger_filetrs
		
		applyed_filters.append ({"unit":item.name} )
		print("applyed_filters ---- >" , applyed_filters)
		ledger = frappe.get_list("Unit Days Ledger" , filters=applyed_filters ,
			    fields =[ "brand" ,  "room_type" , "room_view" , "resort" , "group" , "date"] )
		print("Ledger --- > " ,ledger)
		for componant in ledger :
				applyed_filters = ledger_filetrs
				print("ledger Filter" , ledger_filetrs)
				data.append({
					"date" : componant.date ,
					"item_name" : item.item_name , 
					"room_number" : item.room_number ,
					"name" : componant.name , 
					"brand" : componant.brand , 
					"date" : componant.date  ,
					"room_type" :componant.room_type , 
					"room_view"  : componant.room_view ,
					"resort" :componant.resort ,
					"item_group" :componant.group
			} )
		
	# items = frappe.db.get_list("Item" , fields =["item_name" , "name" , "brand" , "room_number" , "room_type" , "room_view" , "resort" , "item_group"] , filters=filters , order_by="item_name")
	print(data)
	return data

