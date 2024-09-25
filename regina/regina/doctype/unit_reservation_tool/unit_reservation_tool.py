# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UnitReservationTool(Document):
	pass


@frappe.whitelist()
def get_items(item_group = None , brand=None , room_view=None , room_type=[] , 
	      				unit=None , start_date = None ,end_date =None ,check_in=None) :
	
	import json
	# item_marked = []
	# item_unmarked = []


	roomtype = [room.get("room_type") for room  in json.loads(room_type) ] if len(room_type) > 0 else []
	print(roomtype)
	item_filters = {
		"item_group" : item_group , 
		"brand"      : brand , 
		"room_view"  : room_view , 
		# "room_type"  : ["in" ,roomtype] , 
		"name"       : unit   ,
		"check_in_day":check_in
	}
	if len(roomtype) > 0  :
		item_filters["room_type"] = ["in"  , roomtype]

	ledger_filetrs = [] 
	if item_group :
		ledger_filetrs.append({"group" : item_group})
	if room_view :
		ledger_filetrs.append({"room_view" : room_view})
	# if room_type :
	# 	ledger_filetrs.append({"room_type" : ["in" ,roomtype]})
	if unit :
		ledger_filetrs.append({"unit" : unit})

	if start_date :
		ledger_filetrs.append({"date" : [">=" , start_date]})
	if end_date  :
		ledger_filetrs.append({"date" : ["<=" , end_date]})

	item_filters = {k: v for k, v in item_filters.items() if v not in (None, "")}
	
	# get items and date range 

	items = frappe.db.get_list("Item" ,filters=item_filters , fields =[ 'name' , 'item_name' ,
								    "room_number" , "item_group","room_type" ,"room_view","brand" , "check_in_day"])
	data = []
	pr_data = []
	for item in items :
		print("Item --- >>>>>>>> " ,item)
		obj= {"item" : item }
		available =0 
		busy= 0 
		data_list = []
		# get all item available dates 
		applyed_filters = ledger_filetrs.copy()
		applyed_filters.append ({"unit":item.name} )
		print("applyed_filters ---- >" , applyed_filters)
		ledger = frappe.get_list("Unit Days Ledger" , filters=applyed_filters ,
			    fields =[ "brand" , "unit" ,"room_type" , "room_view" , "resort" , "group" , "date" , "status" ,"day_name" ,"name","resort"],
				order_by='date', )
		print("Ledger --- > " ,ledger)
		for componant in ledger :
				color = "white"
				applyed_filters = ledger_filetrs
				print("ledger Filter" , ledger_filetrs)
				# data.append({
				# 	"date" : componant.date ,
				# 	"item_name" : item.item_name , 
				# 	"room_number" : item.room_number ,
				# 	"name" : componant.name , 
				# 	"brand" : componant.brand , 
				# 	"date" : componant.date  ,
				# 	"room_type" :componant.room_type , 
				# 	"room_view"  : componant.room_view ,
				# 	"resort" :componant.resort ,
				# 	"item_group" :componant.group
					
				# } )
				if componant.status == "Available" :
					available+=1
				if componant.status == "Busy" :
					busy+=1
					color = "red"


				data_list.append ({
			
					"date" : componant.date ,
					"item_name" : item.item_name , 
					"room_number" : item.room_number ,
					"name" : componant.name , 
					"brand" : componant.brand , 
					"date" : componant.date  ,
					"room_type" :componant.room_type , 
					"room_view"  : componant.room_view ,
					"resort" :componant.resort ,
					"item_group" :componant.group ,
					"status" : componant.status ,
					"day" :componant.day_name ,
					"r_name" :componant.name,
					"color" :color
 					
				})
		obj["data"] = data_list
		obj["busy"] = busy
		obj["available"] = available
		pr_data.append(obj)
				
		
	# items = frappe.db.get_list("Item" , fields =["item_name" , "name" , "brand" , "room_number" , "room_type" , "room_view" , "resort" , "item_group"] , filters=filters , order_by="item_name")
	print(pr_data)
	return pr_data

