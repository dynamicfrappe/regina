

import frappe

from frappe.utils import nowdate
DOMAINS = frappe.get_active_domains()



def submit_payment_entry_regina(doc,*args,**kwargs):
    if "Time Share" in DOMAINS:
        if doc.payment_paper:
            payment_paper_doc = frappe.get_doc('Payment Paper', doc.payment_paper)
            paid_amount = (payment_paper_doc.paid_amount or 0) + doc.paid_amount
            outstanding_amount = (payment_paper_doc.total_amount ) - paid_amount
            payment_paper_doc.db_set('paid_amount',paid_amount)
            payment_paper_doc.db_set('outstanding_amount',outstanding_amount)

            #update customer payment date
            frappe.db.set_value('Customer',payment_paper_doc.customer,'last_payment_date',nowdate())
            frappe.db.commit()

            # create papeer payment log
            create_paper_payment_log(doc)
            


def cancel_payment_entry_regina(doc,*args,**kwargs):
    if "Time Share" in DOMAINS:
        if doc.payment_paper:
            payment_paper_doc = frappe.get_doc('Payment Paper', doc.payment_paper)
            paid_amount = (payment_paper_doc.paid_amount or 0)  -  doc.paid_amount
            outstanding_amount = (payment_paper_doc.outstanding_amount ) + doc.paid_amount
            payment_paper_doc.db_set('paid_amount',paid_amount)
            payment_paper_doc.db_set('outstanding_amount',outstanding_amount)


def create_paper_payment_log(doc):
    payment_log = frappe.new_doc('Payment Paper Log')
    payment_log.payment_paper = doc.payment_paper
    payment_log.payment_entry = doc.name
    payment_log.paid_amount = doc.paid_amount
    payment_log.payment_date = doc.posting_date
    payment_log.insert(ignore_permissions=1)