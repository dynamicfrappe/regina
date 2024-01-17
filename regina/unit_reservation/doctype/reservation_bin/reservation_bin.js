// Copyright (c) 2024, Dynamic Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reservation Bin', {
	// refresh: function(frm) {

	// }
	from_date:function(frm){
		frm.events.calculate_diff_days(frm)
	},
	to_date:function(frm){
		frm.events.calculate_diff_days(frm)
	},
	calculate_diff_days:function(frm){
		if(frm.doc.from_date && frm.doc.to_date){
			frm.call({
				method:"regina.unit_reservation.doctype.reservation_bin.reservation_bin.get_days_count",
				args:{
					from_date: frm.doc.from_date,
					 to_date: frm.doc.to_date,
				},
				callback:function(r){
					frm.set_value("days_count",r.message)
					frm.refresh_fields('days_count')
				}
			})
		}
	}
});
