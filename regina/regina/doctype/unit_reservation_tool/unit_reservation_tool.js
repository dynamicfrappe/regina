frappe.ui.form.on('Unit Reservation Tool', {
	onload: function(frm){
		erpnext.unit_reservation_tool.load_items(frm);
	},
	refresh: function(frm) {
		frm.disable_save();
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
	},
	get: function(frm) {
		erpnext.unit_reservation_tool.load_items(frm);
	} ,
	update: function(frm) {
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
				unit : frm.doc.unit  , 
				start_date : frm.doc.from_date , 
			    end_date	 : frm.doc.to_date		},
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
						console.log(item[i])
						// employee_present.push(item[i]);
					}
				});
				 frappe.call({
					method: "regina.controllers.items.check_as_reserved",
					args:{
						"items":employee_present,
						"reserve":frm.doc.unit_reservation,
						
					},

					callback: function(r) {
						erpnext.unit_reservation_tool.load_employees(frm);

					}
				});
			});

		// mark_employee_toolbar.find(".btn-mark-absent")
		// 	.html(__('Unreserve'))
		// 	.on("click", function() {
		// 		var employee_absent = [];
		// 		$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
		// 			if($(check).is(":checked")) {
		// 				console.log(item)
		// 				employee_absent.push(item[i]);
		// 			}
		// 		});
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
			// });


		

		var row;
		var row2 ;
		$.each(item, function(i,m ) {
			 row = $(`<div style = "justify-content: space-around;"class="row"></div>`).appendTo(me.wrapper);
			

			 $(repl(`<div class="col-sm-16 unmarked-item-checkbox" >\
			 <div class="checkbox">\
			 <label style="display: block;">\
			 <input type="checkbox" class="item-check"   item="item"/>\
			 <div > <div style="background-color:yellow"> <b >Room Number:&nbsp;</b>%(room_number)s &nbsp; </div><br>
			 <b>Unit:&nbsp;</b>%(item)s &nbsp; <br> \  \
			 <b>Group:&nbsp;</b>%(item_group)s &nbsp; <br> \
			 <b>Brand:&nbsp;</b>%(brand)s &nbsp; <br>  \
			 <b>Room View:&nbsp;</b>%(room_view)s &nbsp; <br>  \
			 <b>Room Type:&nbsp;</b>%(room_type)s &nbsp;<br>  \
			 <b>Resort:&nbsp;</b>%(resort)s &nbsp;<br>  \
			 <b>availadle:&nbsp;</b>%(availadle)s &nbsp;<br>  \
			 <b>busy:&nbsp;</b>%(busy)s &nbsp;<br>  \
			 </label> &nbsp; <br> </div> \
			 </div><br></div>`, {
				 item: m.item.name ,
				 item_group: m.item.item_group , 
				 brand: m.item.brand, 
				 room_number: m.item.room_number,
				 room_view: m.item.room_view,
				 room_type: m.item.room_type,
				 resort: m.item.resort,
				 availadle:m.available,
				 busy:m.busy	,
						

			 })).appendTo(row);


			 row = $(`<div style = "justify-content: space-around;"class="row"></div>`).appendTo(me.wrapper);
			 m.data.forEach(element => {
				$(`<div > 
				<div class="col-sm-12 unmarked-item-checkbox" >
				<label style="display: block;">\
				<div  style="background-color:yellow"> <b >Date:&nbsp;</b> ${element.date} &nbsp; / ${element.day}</div> <br> \
				<div style="background-color:${element.color}"> <b>status:&nbsp;</b> ${element.status} &nbsp; </div> <br>\
				</label>
				 </div></div><br>` ).appendTo(row);
			  });
			// $.each(m.data, function(e, f) {
			// 	item["oo"] = f.r_name ;
			// 	console.log( "Status " ,item)
			// 	if (e===0 || (e % 4) === 0) {
			// 		row2= $('<div style = "justify-content: space-around;"class="row"></div>').appendTo(row);
			// 	}
			// 	// var row2 = $('<div style = "justify-content: space-around;"class="row"></div>').appendTo(row)
			// 	$(repl('<div class="col-sm-16 unmarked-item-checkbox" >\
			// 	<div class="checkbox">\
			// 	<label style="display: block;">\
			// 	<input type="checkbox" checked=0 class="%(data_calss)s" %(disable)s item="%(r_name)s  "/>\
			// 	<div style="background-color:%(color)s;!important"> <div style="background-color:yellow"> \
			// 	<b >Room Number:&nbsp;</b>%(room_number)s &nbsp; </div><br>  \
			// 	<div><b>Day:&nbsp;</b>%(day)s &nbsp; </br> \
			// 	<b>Date:&nbsp;</b>%(date)s &nbsp; </br> \
			// 	<b>Group:&nbsp;</b>%(item_group)s &nbsp; <br> \
			// 	<b>Brand:&nbsp;</b>%(brand)s &nbsp; <br>  \
			// 	<b>Room View:&nbsp;</b>%(room_view)s &nbsp; <br>  \
			// 	<b>Room Type:&nbsp;</b>%(room_type)s &nbsp;<br>  \
			// 	<b>Resort:&nbsp;</b>%(resort)s &nbsp;<br>  \
			// 	</label> &nbsp; <br> </div> \
			// 	</div><br></div>', {
			// 		date : f.date ,
			// 		item: f.name ,
			// 		item_group: f.item_group , 
			// 		brand: f.brand, 
			// 		room_number: f.room_number,
			// 		room_view: f.room_view,
			// 		room_type: f.room_type,
			// 		resort: f.resort,
			// 		color : f.status === "Available" ?  "white" :"red" ,
			// 		disable :f.status === "Available" ?  "0" :"disabled" ,
			// 		data_type :f.status === "Available" ?  "checkbox" :"data" ,
			// 		data_calss :  f.status ===  "Available" ?  "item-check" :"data" ,
			// 		day :f.day ,
			// 		r_name:f.r_name

			// 	})).appendTo(row);
			

				
		});



		mark_employee_toolbar.appendTo($(this.wrapper));
	}
});



