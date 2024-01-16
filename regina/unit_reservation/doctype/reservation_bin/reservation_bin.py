# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class ReservationBin(Document):
	
	def validate(self):
		self.get_diff_days_count()
	

	def get_diff_days_count(self):
		dt_from = datetime.strptime(self.from_date, '%Y-%m-%d')
		dt_to = datetime.strptime(self.to_date, '%Y-%m-%d')
		if str(dt_from.year) != self.year or str(dt_to.year) != self.year:
			frappe.throw("Year in Date Should Be Same in Year")
		self.days_count = (dt_to - dt_from).days

	
	def after_insert(self):
		self.create_or_update_unit_bin_reservation()
	

	def create_or_update_unit_bin_reservation(self):
		if not frappe.db.exists("Unit Reservation Bin", {"unit":self.unit,"year":self.year}):
			new_bin = frappe.new_doc("Unit Reservation Bin")
			new_bin.unit = self.unit
			new_bin.year = self.year
			new_bin.available_unit = 366
			new_bin.reserved_days = self.days_count
			new_bin.valid_days = new_bin.available_unit - new_bin.reserved_days
			new_bin.insert(ignore_permissions=True)
			frappe.db.commit()
			#create new unit bin 
		else:
			# update curent bin
			unit_bi_name = frappe.db.get_value('Unit Reservation Bin', {"unit":self.unit,"year":self.year},'name')
			unit_bin_doc = frappe.get_doc('Unit Reservation Bin',unit_bi_name)
			unit_bin_doc.reserved_days +=  self.days_count
			unit_bin_doc.valid_days =   unit_bin_doc.available_unit - unit_bin_doc.reserved_days
			if unit_bin_doc.reserved_days  > 366:
				frappe.db.rollback()
				frappe.throw("Valid Days Count < Days Needed")
			unit_bin_doc.save(ignore_permissions=True)


@frappe.whitelist()
def get_days_count(from_date, to_date):
	dt_from = datetime.strptime(from_date, '%Y-%m-%d')
	dt_to = datetime.strptime(to_date, '%Y-%m-%d')
	return  (dt_to - dt_from).days