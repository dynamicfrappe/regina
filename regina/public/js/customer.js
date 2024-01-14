








frappe.ui.form.on("Customer", {

    national_id: function (frm) {
        if(frm.doc.national_id && frm.doc.is_egyptian ){
            if(!$.isNumeric(frm.doc.national_id) || String((frm.doc.national_id)).length!=14){
               frappe.throw(__('National Id Must Be Number And 14 Digits'))
            }
        }

    }
})