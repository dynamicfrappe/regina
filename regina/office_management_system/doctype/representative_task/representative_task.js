// Copyright (c) 2023, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Representative Task', {
	setup:function(frm){
		frm.set_query("representative" , function() {
			return {
				"filters": {
					"status": "Available",
					
				}}
		})
	},



	new_lead:function(frm) {
		let d = new frappe.ui.Dialog({
			title: 'Lead Details',
			fields: [
				 {
					  label: 'Full Name',
					  fieldname: 'lead_name',
					  fieldtype: 'Data',
					  reqd:1
				 },
				 {
					  label: 'Company',
					  fieldname: 'company_name',
					  fieldtype: 'Data'
				 },
				 {
					  label: 'Email',
					  fieldname: 'email_id',
					  fieldtype: 'Data'
				 },
				 {
					label: 'Mobile No.',
					fieldname: 'mobile_no',
					fieldtype: 'Data'
			  },
				 {
					label: 'Gender',
					fieldname: 'gender',
					fieldtype: 'Link' ,
					options: "Gender"
			  },
			  {
				label: 'Source',
				fieldname: 'source',
				fieldtype: 'Link' ,
				options: "Lead Source"
		  },

			],
			size: 'small', // small, large, extra-large 
			primary_action_label: 'Submit',
			primary_action(values) {
				frappe.call({
					"method" :"regina.controllers.crm.create_lead" ,
					"args" :
						{"args": values } ,
						callback:function(r){
							if (r.message){
								frm.doc.customer = r.message.name
								frm.doc.customer_name = r.message.lead_name
								frm.set_df_property("customer_name","read_only", 1);
								frm.refresh_field("customer")
								frm.refresh_field("customer_name")
							}
						}
					
				})
				 d.hide();
			}
	  });
	  
	  d.show();
		} ,
   get_customer_name:function(frm){
		frappe.call({
			"method" :"regina.controllers.crm.get_name" ,
			"args" :{
				"document_type": frm.doc.agent_type ,
				"document" : frm.doc.customer
			},
			callback:function(r){
				frm.doc.customer_name = r.message
				frm.set_df_property("customer_name","read_only", 1);
				frm.refresh_field("customer_name")
			}
		
		})
	},
	customer:function(frm){
		frm.events.get_customer_name(frm)
	},
	agent_type:function(frm){
		frm.doc.customer_name  = "";
		frm.doc.customer = "";
		frm.refresh_field("customer")						
		frm.refresh_field("customer_name")
	}

	// refresh: function(frm) {

	// }
});
