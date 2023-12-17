frappe.ready(function() {
	// bind events here
	frappe.web_form.on( "item", (field, value) => {
	
		new frappe.ui.Scanner({
			dialog: true, // open camera scanner in a dialog
			multiple: false, // stop after scanning one value
			on_scan(data) {
			  console.log(data.decodedText);
			}
		 });
	
	})
	
	 
})