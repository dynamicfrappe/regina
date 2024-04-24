frappe.ui.form.on('Unit Reservation Tool', {
	onload: function(frm){
		erpnext.unit_reservation_tool.load_items(frm);
	},
	refresh: function(frm) {
		// frm.disable_save();
	},
	item_group: function(frm) {
		erpnext.unit_reservation_tool.load_items(frm);
	},

	brand: function(frm) {
		erpnext.unit_reservation_tool.load_items(frm);
	},

	room_type: function(frm) {
		erpnext.unit_reservation_tool.load_items(frm);
	},

	unit: function(frm) {
		erpnext.unit_reservation_tool.load_items(frm);
	},
	room_view: function(frm) {
		erpnext.unit_reservation_tool.load_items(frm);
	}

});

erpnext.unit_reservation_tool = {
	load_items: function(frm) {
		frappe.call({
			method: "regina.regina.doctype.unit_reservation_tool.unit_reservation_tool.get_items",
			args: {
				item_group : frm.doc.item_group , 
				brand : frm.doc.brand , 
				room_view : frm.doc.room_view , 
				room_type : frm.doc.room_type, 
				unit : frm.doc.unit 
			},
			callback: function(r) {
				if(r.message.length > 0) {
					// frm.form_wrapper.empty();
					unhide_field('marked_items_section')
					if(!frm.fields_dict.marked_item_html.wrapper.innerHTML) {
						frm.form_wrapper = $('<div>')
						.appendTo(frm.fields_dict.marked_item_html.wrapper);
					}
					
					frm.Items_Sellector = new erpnext.Items_Sellector(frm, frm.form_wrapper, r.message)
				}
				else{
					hide_field('marked_items_section')
				}
			}
		});
	}
}


erpnext.Items_Sellector = Class.extend({
	init: function(frm, wrapper, item) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.make(frm, item);
	},
	make: function(frm, item) {
		var me = this;

		$(this.wrapper).empty();

		
		var employee_toolbar = $('<div class="col-sm-12 top-toolbar">\
			<button class="btn btn-default btn-add btn-xs"></button>\
			<button class="btn btn-xs btn-default btn-remove"></button>\
			</div><br>').appendTo($(this.wrapper));

		var mark_employee_toolbar = $('<div class="col-sm-12 bottom-toolbar">\
			<button class="btn btn-primary btn-mark-present btn-xs"></button>\
			<button class="btn btn-danger btn-mark-absent btn-xs"></button>\
			</div><br>');

		employee_toolbar.find(".btn-add")
			.html(__('Check all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if(!$(check).is(":checked")) {
						check.checked = true;
					}
				});
			});

		employee_toolbar.find(".btn-remove")
			.html(__('Uncheck all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						check.checked = false;
					}
				});
			});

		mark_employee_toolbar.find(".btn-mark-present")
			.html(__('Reserve'))
			.on("click", function() {
				var employee_present = [];
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						employee_present.push(item[i]);
					}
				});
				// frappe.call({
				// 	method: "erpnext.hr.doctype.employee_attendance_tool.employee_attendance_tool.mark_employee_attendance",
				// 	args:{
				// 		"employee_list":employee_present,
				// 		"status":"Present",
				// 		"date":frm.doc.date,
				// 		"company":frm.doc.company
				// 	},

				// 	callback: function(r) {
				// 		erpnext.employee_attendance_tool.load_employees(frm);

				// 	}
				// });
			});

		mark_employee_toolbar.find(".btn-mark-absent")
			.html(__('Unreserve'))
			.on("click", function() {
				var employee_absent = [];
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						employee_absent.push(item[i]);
					}
				});
				// frappe.call({
				// 	method: "erpnext.hr.doctype.employee_attendance_tool.employee_attendance_tool.mark_employee_attendance",
				// 	args:{
				// 		"employee_list":employee_absent,
				// 		"status":"Absent",
				// 		"date":frm.doc.date,
				// 		"company":frm.doc.company
				// 	},

				// 	callback: function(r) {
				// 		erpnext.employee_attendance_tool.load_employees(frm);

				// 	}
				// });
			});


		

		var row;
		$.each(item, function(i, m) {
			if (i===0 || (i % 4) === 0) {
				row = $('<div style = "justify-content: space-around;"class="row"></div>').appendTo(me.wrapper);
			}

			$(repl('<div class="col-sm-16 unmarked-item-checkbox">\
				<div class="checkbox">\
				<label style="display: block;"><input type="checkbox" class="item-check" item="%(item)s"/>\
				<div><b>Room:&nbsp;</b>%(item)s &nbsp; </br> \
				<b>Group:&nbsp;</b>%(item_group)s &nbsp; <br> \
				<b>Brand:&nbsp;</b>%(brand)s &nbsp; <br>  \
				<b>Room Number:&nbsp;</b>%(room_number)s &nbsp; <br>  \
				<b>Room View:&nbsp;</b>%(room_view)s &nbsp; <br>  \
				<b>Room Type:&nbsp;</b>%(room_type)s &nbsp;<br>  \
				<b>Resort:&nbsp;</b>%(resort)s &nbsp;<br>  \
				</label> &nbsp; <br> </div> \
				</div><br></div>', {
					item: m.name ,
					item_group: m.item_group , 
					brand: m.brand, 
					room_number: m.room_number,
					room_view: m.room_view,
					room_type: m.room_type,
					resort: m.resort,

				})).appendTo(row);
				
		});



		mark_employee_toolbar.appendTo($(this.wrapper));
	}
});


