// Copyright (c) 2023, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Agent', {
	refresh: function(frm) {
		//
	},
	get_row_tax:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		frappe.call({
			method:"regina.collections_management.collection_management_api.get_row_tax_regina_agent",
			args:{
				// 'capacity':row.capacity,
			},
			callback:function(r){
				if(r.message){
					let rate = r.message
					if(rate > 0){
						row.agent__fees_tax = row.toal_payment_amount + (rate/100 * row.toal_payment_amount)
						row.agent_fee_discount_tax = 0
					}else if(rate < 0){
						row.agent_fee_discount_tax = row.toal_payment_amount - (rate/100 * row.toal_payment_amount)
						row.agent__fees_tax = 0
					}
					frm.refresh_field("agent_price_list")
				}
			}
		})
	}
});





frappe.ui.form.on('Agent Price List', {
	capacity: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn]
		if (row.capacity){
			frm.events.get_row_tax(frm,cdt,cdn)
			
		}
	}
});