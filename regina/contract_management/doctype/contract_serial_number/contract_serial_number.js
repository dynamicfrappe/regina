// Copyright (c) 2023, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contract Serial Number', {
	refresh: function(frm) {
		frm.events.setup_buttons(frm)
	}	,

	onload:function(frm){
		frm.events.setup_buttons(frm)
	},
	rejected:function(frm){
		frm.events.setup_buttons(frm)
	},
	// setup_buttons:function(frm){
	// 	if (!frm.doc.contract && frm.doc.status == "On Progress" && !frm.doc.rejected) {
	// 		frm.add_custom_button(__('Create Contract'), function(){
	// 			frm.events.create_contract(frm)
	// 	  }, __("Contracts"));
	// 	} else {

	// 	frm.remove_custom_button("Create Contract" ,"Contracts")
	// 			}
		
		

	// },
	setup_buttons: function(frm) {
		if (!frm.doc.contract && frm.doc.status == "On Progress" && !frm.doc.rejected) {
			frm.add_custom_button(__('Create Contract'), function() {
				frappe.call({
					method: 'regina.contract_management.doctype.contract_serial_number.contract_serial_number.process_contract_serial_number',
					args: {
						contract_serial_number: frm.doc.contract_serial_number
					},
					callback: function(r) {
						if(r.message) {
							frappe.msgprint(r.message);
						} else {
						}
					}
				});
			}, __("Contracts"));
		} else {
			frm.remove_custom_button("Create Contract", "Contracts");
		}
	},
	
	create_contract:function(frm){
		frappe.call({
			"method" : "regina.controllers.contract.receive_contract" , 
			"args": {
				"doc" :frm.doc.name
			},
		callback:function(e){
			console.log(e)
			frappe.set_route("Form", "Contract", e.message);
			},})
	}
});
