import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import set_name_by_naming_series
from frappe.utils import getdate, nowdate


from regina.controllers.items import get_reserved_weeks

class Contract(Document):
	def validate_week_with_item(self) :
		if not self.week and self.unit :
			frappe.throw(_(f"Please Set week for unit {self.unit}"))
		reserved_weeks = get_reserved_weeks(self.unit)
		if len(reserved_weeks) > 0  :
			for item in self.items :
				if item.week in reserved_weeks[0] :
					frappe.throw(_(f""" Unit number {self.unit} Week {item.week} is Reserved for other Contract"""))
	def create_week_ben_ledger(self) :
		# create ledger 
		ledger = frappe.new_doc("Week Ben Ledger") 
		ledger.unit = self.unit
		ledger.week = self.week
		ledger.contract = self.name
		ledger.customer = self.party_name
		ledger.save()
		#check if item has Week Ben List 
		
		if frappe.db.exists("Week Ben List", {"unit": self.unit }):
			# update unit available weeks 
			# We need to update this function  
			item_ben = frappe.get_doc("Week Ben List", {"unit": self.unit })
			item_ben.reserved_weeks = int(item_ben.reserved_weeks) +1
			item_ben.available_weeks = int(item_ben.available_weeks) -1
			item_ben.save()
		if not frappe.db.exists("Week Ben List", {"unit": self.unit }):
			#create  
			item_ben = frappe.new_doc("Week Ben List") 
			item_ben.unit = self.unit 
			item_ben.total_weeks = frappe.db.get_single_value('Management Settings', 'weeks_count_for_sales')
			item_ben.reserved_weeks = 1 
			item_ben.available_weeks= int(item_ben.total_weeks) - 1 
			item_ben.save()

		
	def on_submit(self) :

		"""
		submit functions 
		1 - validate week number 
		2 - Create Week Ben Ledger
		3 - Update or create Week Ben List
		
		
		
		
		"""
		self.validate_week_with_item()
		self.create_week_ben_ledger()
		# frappe.throw("submit Functions ")
	def autoname(self):
		if frappe.db.get_single_value("Selling Settings", "contract_naming_by") == "Naming Series":
			set_name_by_naming_series(self)
		else:
			name = self.party_name

			if self.contract_template:
				name = f"{name} - {self.contract_template} Agreement"

			# If identical, append contract name with the next number in the iteration
			if frappe.db.exists("Contract", name):
				count = frappe.db.count(
					"Contract",
					filters={
						"name": ("like", f"%{name}%"),
					},
				)
				name = f"{name} - {count}"

			self.name = _(name)

	def validate(self):
		self.validate_dates()
		self.update_contract_status()
		self.update_fulfilment_status()
		self.validate_serial_number()
		self.validate_week_with_item()
		
	def validate_serial_number(self):
		if self.serial_number :
			agent , status , contract = frappe.db.get_value("Contract Serial Number" ,self.serial_number ,
					["agent" ,"status" ,"contract"] )
			if contract :
				frappe.throw(_(f""" Serial Number {self.serial_number} already  Have a Contract :{contract} """))
			if status != "On Progress" :
				frappe.throw(_(f""" serial number has invalid status {self.serial_number} - {status}"""))
			if agent != self.agent :
				frappe.throw(_(f""" {self.serial_number} -is assosiated with {agent} not {self.agent}"""))
	def before_submit(self):
		if self.serial_number :
			self.validate_serial_number()
			frappe.db.set_value("Contract Serial Number" ,self.serial_number , {
				"contract"  : self.name ,
				"status" : "Completed"
			} )
		self.signed_by_company = frappe.session.user

	def before_update_after_submit(self):
		self.update_contract_status()
		self.update_fulfilment_status()

	def validate_dates(self):
		if self.end_date and self.end_date < self.start_date:
			frappe.throw(_("End Date cannot be before Start Date."))

	def update_contract_status(self):
		if self.is_signed:
			self.status = get_status(self.start_date, self.end_date)
		else:
			self.status = "Unsigned"

	def update_fulfilment_status(self):
		fulfilment_status = "N/A"

		if self.requires_fulfilment:
			fulfilment_progress = self.get_fulfilment_progress()

			if not fulfilment_progress:
				fulfilment_status = "Unfulfilled"
			elif fulfilment_progress < len(self.fulfilment_terms):
				fulfilment_status = "Partially Fulfilled"
			elif fulfilment_progress == len(self.fulfilment_terms):
				fulfilment_status = "Fulfilled"

			if fulfilment_status != "Fulfilled" and self.fulfilment_deadline:
				now_date = getdate(nowdate())
				deadline_date = getdate(self.fulfilment_deadline)

				if now_date > deadline_date:
					fulfilment_status = "Lapsed"

		self.fulfilment_status = fulfilment_status

	def get_fulfilment_progress(self):
		return len([term for term in self.fulfilment_terms if term.fulfilled])

	def on_cancel(self) :
		#re Set serial Status 
		if self.serial_number :
			
			frappe.db.set_value("Contract Serial Number" ,self.serial_number , {
				"contract"  :None ,
				"status" : "On Progress"
			} )
def get_status(start_date, end_date):
	"""
	Get a Contract's status based on the start, current and end dates

	Args:
	        start_date (str): The start date of the contract
	        end_date (str): The end date of the contract

	Returns:
	        str: 'Active' if within range, otherwise 'Inactive'
	"""

	if not end_date:
		return "Active"

	start_date = getdate(start_date)
	end_date = getdate(end_date)
	now_date = getdate(nowdate())

	return "Active" if start_date <= now_date <= end_date else "Inactive"

	
def update_status_for_contracts():
	"""
	Run the daily hook to update the statuses for all signed
	and submitted Contracts
	"""

	contracts = frappe.get_all(
		"Contract",
		filters={"is_signed": True, "docstatus": 1},
		fields=["name", "start_date", "end_date"],
	)

	for contract in contracts:
		status = get_status(contract.get("start_date"), contract.get("end_date"))
		frappe.db.set_value("Contract", contract.get("name"), "status", status)