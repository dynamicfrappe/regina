// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Contract", {
	onload: function(frm) {
		console.log ("Overide")
		frappe.db.get_value(
			"Selling Settings",
			"Selling Settings",
			"contract_naming_by",
			(r) => {
				frm.toggle_display("naming_series", r.contract_naming_by === "Naming Series");
			}
		);
	},

	unit:function(frm){
		if (frm.doc.unit) {
			
			frm.set_df_property("week" , "reqd" , 1)
		} else {

			frm.set_df_property("week" , "reqd" , 0)
		}
		
		// frm.refresh_field("week")
		frm.events.set_week_qey(frm)
		
	},
	set_week_qey:function(frm) {
		frm.set_query("Items" ,"week", function() {
			return {
				query: "regina.controllers.items.get_available_weeks_for_item",
				"filters": {"item": frm.doc.unit} 
		  };
		 }

		)
	
	} ,



	contract_template: function (frm) {
		if (frm.doc.contract_template) {
			frappe.call({
				method: 'erpnext.crm.doctype.contract_template.contract_template.get_contract_template',
				args: {
					template_name: frm.doc.contract_template,
					doc: frm.doc
				},
				callback: function(r) {
					if (r && r.message) {
						let contract_template = r.message.contract_template;
						frm.set_value("contract_terms", r.message.contract_terms);
						frm.set_value("requires_fulfilment", contract_template.requires_fulfilment);

						if (frm.doc.requires_fulfilment) {
							// Populate the fulfilment terms table from a contract template, if any
							r.message.contract_template.fulfilment_terms.forEach(element => {
								let d = frm.add_child("fulfilment_terms");
								d.requirement = element.requirement;
							});
							frm.refresh_field("fulfilment_terms");
						}
					}
				}
			});
		}
	}
});



frappe.ui.form.on('Items', {
	items_add:function(frm , cdt,cdn) {
			console.log("Catched")
	}



})