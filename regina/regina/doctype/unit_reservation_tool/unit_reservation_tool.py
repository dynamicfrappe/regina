# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UnitReservationTool(Document):
	pass


@frappe.whitelist()
def get_items(item_group = None , brand=None , room_view=None , room_type=None , unit=None):
	# item_marked = []
	# item_unmarked = []

	filters = {
		"item_group":item_group , 
		"brand" : brand , 
		"room_view" : room_view , 
		"room_type":room_type , 
		"name":unit 
		}

	filters = {k: v for k, v in filters.items() if v not in (None, "")}

	items = frappe.db.get_list("Item" , fields =["item_name" , "name" , "brand" , "room_number" , "room_type" , "room_view" , "resort" , "item_group"] , filters=filters , order_by="item_name")
	print(items)
	return items

