# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Resort(Document):
    def validate(self):
        if self.unit_reservation_template:
            unit_week_set = set()
            for row in self.unit_reservation_template:
                if row.unit_week in unit_week_set:
                    frappe.throw("Duplicated Unit week {0}".format(row.unit_week), title="Validation Error")
                unit_week_set.add(row.unit_week)



