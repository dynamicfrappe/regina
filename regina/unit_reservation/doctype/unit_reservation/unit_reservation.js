// Copyright (c) 2024, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unit Reservation', {
	refresh: function(frm) {
		frm.events.event_add_custom_btns(frm)
	},


	event_add_custom_btns:function(frm){
		frm.add_custom_button('Show History',()=>{

		},__("View")),
		frm.add_custom_button('Reservation History',()=>{

		},__("View"))
	}
});
