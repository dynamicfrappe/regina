# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class Unitweek(Document):
    def validate(self):
        self.clear_child_table()
        days_list = get_dates_for_day(str(self.from_date), str(self.to_date), self.start_day, self.end_day)
        for day in days_list:
            self.append("unit_week_tool", {
                'start_day': day['start_day'],
                'end_day': day['end_day'],
                'desc1': day['start_day_name'],  
                'desc2': day['end_day_name'] 
            })

    def clear_child_table(self):
        self.set("unit_week_tool", [])

@frappe.whitelist()
def get_dates_for_day(from_date, to_date, start_day, end_day):
    from datetime import datetime, timedelta

    start = datetime.strptime(from_date, '%Y-%m-%d')
    end = datetime.strptime(to_date, '%Y-%m-%d')

    days_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    target_day_int = days_map[start_day]
    target_end_day_int = days_map[end_day]

    current_date = start + timedelta(days=(target_day_int - start.weekday()) % 7)
    end_date = start + timedelta(days=(target_end_day_int - start.weekday()) % 7)

    dates = []
    while current_date <= end:
        dates.append({  
            'start_day': current_date.strftime('%Y-%m-%d'), 
            'end_day': end_date.strftime('%Y-%m-%d'),
            'start_day_name': current_date.strftime('%A'),
            'end_day_name': end_date.strftime('%A')
        })
        current_date += timedelta(days=7)
        end_date += timedelta(days=7)

    return dates







