// Copyright (c) 2023, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contracts Management', {

	clear_child_table:function(frm) {
		frm.set_value('items', [])
		frm.refresh_field("items")
	},
	onload:function(frm){
		console.log("Load")
		frm.events.clear_child_table(frm)
		frm.set_df_property("items", "read_only", 1);
	},
	agent:function(frm) {
		console.log("Agent")
		frm.events.clear_child_table(frm)
	} ,
	document_method:function(frm){
		frm.events.clear_child_table(frm)
		frm.set_df_property("items", "read_only", 0);
		frm.refresh_field("items")
		if (frm.doc.document_method =='Send' ){
			frm.events.setup_send(frm)
		}else {
			frm.events.setup_receive(frm)
		}
	},
	setup_send:function(frm){
		frm.set_query("contract_serial_number" ,"items", function() {
			return {
				"filters": {
					"status": "On Site",
					
				}}
		})
	},
	setup_receive:function(frm){
		frm.set_query("contract_serial_number" ,"items", function() {
			return {
				"filters": {
					"status": "With Agent",
				 	"agent": frm.doc.agent
					
				}}
		})
	}
})



frappe.ui.form.on("Contract Management Items" ,{
	contract_serial_number:function(frm ,cdt,cdn){
		console.log(locals[cdt][cdn])
	},
	items_add:function(frm  ,cdt,cdn){
		var row = frm.get_field('items').grid.get_row(cdn) 
		var df = frappe.meta.get_docfield("Contract Management Items","receive_date", frm.doc.name)
		df.read_only = 1;
		frm.refresh_field("items")
		console.log(row)
		if (frm.doc.document_method =='Send' ){
			locals[cdt][cdn].send_date=frm.doc.date
			row.toggle_editable("receive_date", 1);
			frm.set_df_property("receive_date", "items","read_only", 1);
			frm.refresh_field("items")
		}else {
			locals[cdt][cdn].receive_date=frm.doc.date
			frm.refresh_field("items")
		}
		
		
	} 
}

)