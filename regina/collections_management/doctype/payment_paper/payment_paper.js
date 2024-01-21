// Copyright (c) 2024, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Paper', {
	SecurityPolicyViolationEvent:function(frm){
		frm.add_fetch('customer', 'company', 'company');

	},
	refresh: function(frm) {
		frm.events.add_custom_btn(frm)
	},
	add_custom_btn:function(frm){
		if(frm.doc.status.includes("Pending","Partial Paid")){
			frm.add_custom_button("Make Payment",()=>{


				frappe.model.open_mapped_doc({

					method: "regina.collections_management.collection_management_api.make_payment_entry",
					frm:frm,
					args:{
						"dn":frm.doc.name,
					},
		
		
		
				})	
				
				// frm.call({
				// 	method:'regina.collections_management.collection_management_api.make_payment_entry',
				// 	args:{
				// 		dt:frm.doc.doctype,
				// 		dn:frm.doc.name,
				// 	},
				// 	callback:function(r){
				// 		frappe.set_route("Form", r.message.doctype, r.message.name);
				// 	}
				// })
			},(__("Utilies")))
		}
	}
});
