// Copyright (c) 2023, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contracts Management', {

	clear_child_table:function(frm) {
		frm.set_value('items', [])
		frm.refresh_field("items")
	},
	onload:function(frm){
		
		if (frm.doc.__unsaved) {
			frm.events.clear_child_table(frm)
			frm.set_df_property("items", "read_only", 1);
		}
		
	},
	agent:function(frm) {
	
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
	onload:function(frm) {
		var row = frm.get_field('items').grid.get_row(cdn) 
		// var df = frappe.meta.get_docfield("Contract Management Items","receive_date", frm.doc.name)
		var df = frappe.meta.get_docfield("Contract Management Items","receive_date", frm.doc.name)
		df.read_only = 1;
		var tppc = frappe.meta.get_docfield("Contract Management Items","total_payment_papers_count", frm.doc.name)
		tppc.read_only = 1;
		var tc = frappe.meta.get_docfield("Contract Management Items","total_cash", frm.doc.name)
		tc.read_only = 1;
		var tpp = frappe.meta.get_docfield("Contract Management Items","total_payment_papers", frm.doc.name)
		tpp.read_only = 1;
		frm.refresh_field("items") 
	},
	
	items_add:function(frm  ,cdt,cdn){
	
		// frm.refresh_field("items")
	
		if (frm.doc.document_method =='Send' ){
			locals[cdt][cdn].send_date=frm.doc.date
			// var rd = frappe.meta.get_docfield("Contract Management Items","receive_date", frm.doc.name)
			// rd.read_only = 1
			var tppc = frappe.meta.get_docfield("Contract Management Items","total_payment_papers_count", frm.doc.name)
			tppc.read_only = 1;
			var tc = frappe.meta.get_docfield("Contract Management Items","total_cash", frm.doc.name)
			tc.read_only = 1;
			var tpp = frappe.meta.get_docfield("Contract Management Items","total_payment_papers", frm.doc.name)
			tpp.read_only = 1;
			frm.refresh_field("items") 
		}else {
			locals[cdt][cdn].receive_date=frm.doc.date
			var rd = frappe.meta.get_docfield("Contract Management Items","receive_date", frm.doc.name)
			rd.read_only = 0
			var tppc = frappe.meta.get_docfield("Contract Management Items","total_payment_papers_count", frm.doc.name)
			tppc.read_only = 0;
			var tc = frappe.meta.get_docfield("Contract Management Items","total_cash", frm.doc.name)
			tc.read_only = 0;
			var tpp = frappe.meta.get_docfield("Contract Management Items","total_payment_papers", frm.doc.name)
			tpp.read_only = 0;
			frm.refresh_field("items")
		}
		
		
	} 
}

)