
import frappe

from erpnext.accounts.utils import get_account_currency
from frappe.utils import nowdate

@frappe.whitelist()
def make_payment_entry(dn):
	source_doc = frappe.get_doc("Payment Paper",dn)
	party_type = "Customer"
	company = frappe.defaults.get_user_default("Company")
	company_doc = frappe.get_doc('Company',company)
	party_account = company_doc.get("default_receivable_account") 
	party_account_currency = get_account_currency(party_account)
	account_paid_to = company_doc.get("default_bank_account")  

	get_advance_paid = f"""
	SELECT sum(paid_amount) as paid_amount FROM `tabPayment Entry` WHERE payment_paper='{dn}' AND docstatus=1 
	"""
	get_advance_paid = frappe.db.sql(get_advance_paid,as_dict=1)[0]

	pe = frappe.new_doc("Payment Entry")
	pe.company = company
	pe.payment_type = 'Receive'
	pe.paid_from_account_currency = party_account_currency
	pe.cost_center = company_doc.get("round_off_cost_center")  
	pe.posting_date = nowdate()
	pe.paid_from = party_account
	pe.paid_to = account_paid_to
	pe.paid_from_account_currency = party_account_currency
	pe.paid_to_account_currency = get_account_currency(account_paid_to)
	pe.reference_date = nowdate()
	pe.party_type = party_type
	pe.party = source_doc.customer
	pe.payment_paper = dn
	pe.paid_amount = source_doc.total_amount - (get_advance_paid.get('paid_amount') or 0)

	
	# print(f'\n\n\n==>\n\n\n=={pe.name}')
	return pe