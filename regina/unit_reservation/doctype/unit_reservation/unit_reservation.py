# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

from frappe.utils import date_diff , today ,getdate

from dateutil.relativedelta import relativedelta

class UnitReservation(WebsiteGenerator):
	
	
	def validate(self):
		self.calculate_days_count()
		dt_from = datetime.strptime(str(self.from_date), '%Y-%m-%d')
		dt_to = datetime.strptime(str(self.to_date), '%Y-%m-%d')
		if str(dt_from.year) != self.year or str(dt_to.year) != self.year:
			frappe.throw("Year in Date Should Be Same in Year")

		self.calculate_customer_days_credit()
		self.calculate_totals()
		

		
	def calculate_days_count(self):
		df = date_diff( self.to_date ,self.from_date )
		self.days = df


	
	def calculate_customer_days_credit(self) :
		if not self.contract :
			frappe.throw(_("Please Select customer Contract "))
		
		contract = frappe.get_doc("Contract" , self.contract )
		if contract.party_name != self.customer  and  contract.partner_name != self.customer :
			frappe.throw(_(f"Customer {self.customer} Is not in this contract"))
		years= relativedelta(  getdate(today()) ,getdate(contract.start_date))
		years_actual = int(years.years) +1

		#set actual credit days 
		if years_actual >= 3 :
			self.available_days = int(contract.yearly_days) * 3 
		if years_actual < 3 :
			self.available_days = int(contract.yearly_days) * years_actual 

		self.unit_reservation_services = []
		cr_year = int(self.year) - years_actual 
		last_amount = 0
		service_last_amount = {}
		for i in range(0,int(years_actual)) :
			cr_year = int(cr_year) + 1
			
			for service in contract.annual_services :
			
				#check service last payment day 
				print(cr_year)
				print("last amount" ,service_last_amount)
				last_payemnet_day = frappe.db.sql(f""" SELECT a.name FROM `tabAnnual Services Payments` a 
				INNER JOIN `tabAnnual Services Type` b
				ON a.annual_services_type =b.name
				WHERE a.contract='{self.contract}'
				AND a.annual_services_type='{service.service_type}'  and a.year='{cr_year}' and b.is_upgrade='0'  and b.is_eachange='0' """)
				if not last_payemnet_day :
					ser = frappe.get_doc("Annual Services Type" ,service.service_type )
					if not ser.is_upgrade and not ser.is_eachange :
						cost = service.annual_cost
						if service_last_amount.get(f"{service.service_type}") :
							cost = float(service_last_amount.get(f"{service.service_type}")) + ( float(service_last_amount.get(f"{service.service_type}"))*(10/100))
						self.append("unit_reservation_services" , {"service" :service.service_type,"year":cr_year ,"amount":cost })
						service_last_amount[service.service_type] = cost
				

	def calculate_payment_paper_details(self):

		total_paper = 0
		total_paid = 0 
		total_unpaid = 0
		#get paper 
		contract = frappe.get_doc("Contract" , self.contract )
		payment_papers = frappe.get_list("Payment Paper" , {"serial_number" : contract.serial_number} , {"due_date" , "total_amount" , "name" , "status"})
		self.reservation_payment_paper =[]
		for paper in payment_papers :
			if paper.status in ["Partial Paid" , "Completed" ,"Pending"]:
				total_paper = total_paper +1
			if paper.status == "Completed" :
				total_paid = total_paid +1
			if paper.status in ["Pending" ,"Partial Paid"] :
				if getdate(paper.due_date) < getdate(self.from_date) :
					total_unpaid = total_unpaid +1 
					self.append("reservation_payment_paper" ,{
						"payment_paper" : paper.name ,
						"status"  : paper.status , 
						"amount" : paper.total_amount ,
						"due_date" :paper.due_date
					})

		if total_unpaid > 1 :
			self.status = "Payment paper Unpaid"
		self.total_payment_paper = total_paper
		self.total_payed = total_paid 
		self.total_unpaid = total_unpaid
			
	def calculate_totals(self):
		total_unpayment_paper = 0
		total_unpaid_services = 0
		total_unpaid_other_services = 0
		total_paid_services = 0
		total_paid_other_services = 0

		for payment in self.reservation_payment_paper:
			if payment.status == "Pending" and payment.amount is not None:
				total_unpayment_paper += float(payment.amount)

		for service in self.unit_reservation_services:
			if service.amount is not None:
				total_unpaid_services += float(service.amount)
			if service.payed_amount is not None:
				total_paid_services += float(service.payed_amount)
		for added_service in self.unit_reservation_added_services:
			if added_service.amount is not None:
				total_unpaid_other_services += float(added_service.amount)
			if added_service.payed_amount is not None:
				total_paid_other_services += float(added_service.payed_amount)
		total_unpaid_all = total_unpayment_paper + total_unpaid_services + total_unpaid_other_services
		total_paid_all = total_paid_services + total_paid_other_services
		self.total_unpayment_paper = total_unpayment_paper
		self.total_unpaid_services = total_unpaid_services
		self.total_unpaid_other_services = total_unpaid_other_services
		self.total_unpaid_all = total_unpaid_all
		self.total_paid_services = total_paid_services
		self.total_paid_other_services = total_paid_other_services
		self.total_paid_all = total_paid_all
	


from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_reservation(source_name , target_doc=None):
	doclist = get_mapped_doc(
		"Unit Reservation",
		source_name,
		{
			"Unit Reservation": {
				"doctype": "Unit Reservation Tool",
				"field_map": {
					"unit": "unit",
					# "payment_terms_template": "payment_terms_template",
				},

			},
		},
		target_doc,
		ignore_permissions=True,
	)
	return doclist