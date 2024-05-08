// Copyright (c) 2024, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unit Reservation', {
	refresh: function(frm) {
		frm.events.event_add_custom_btns(frm)
		frm.events.setup_query(frm)
	},


	event_add_custom_btns:function(frm){
		frm.add_custom_button('Show History',()=>{

		},__("View")),
		frm.add_custom_button('Reservation History',()=>{

		},__("View")),
		frm.add_custom_button('Reservation',()=>{
			create_reservation(frm);

		},__("Create"))
	},

	setup_query:function(frm) {
		frm.set_query('unit', () => {
			return {
				 filters: {
					  item_group: frm.doc.item_group ,
					  room_type : frm.doc.room_type ,
					  room_view :frm.doc.room_view
				 }
			}
	  })
	}
	
});


function create_reservation(frm){
	// let from_date = frm.doc.from_date ;
	// let to_date = frm.doc.to_date ;

	// let brand = frm.doc.brand ; 
	// let item_group = frm.doc.item_group ; 
	// let room_view = frm.doc.room_view ; 
	// let room_type = frm.doc.room_type ; 
	// let unit = frm.doc.unit ;

	frappe.model.open_mapped_doc({
		method: "regina.unit_reservation.doctype.unit_reservation.unit_reservation.create_reservation",
		frm: frm
	})


}