// Copyright (c) 2024, Dynamic Business Solutions and contributors
// For license information, please see license.txt "regina.controllers.items.get_available_weeks_for_item"

frappe.ui.form.on('Year', {
	refresh: function(frm) {
		frm.add_custom_button(__('Set Custome rledger '), function(){
			frappe.call({
				"method" :"regina.controllers.items.get_item_reservation_data", 
				"args": {"year" : frm.doc.name }
			})
		}, __("Utilities"));
	}
});
