# Copyright (c) 2024, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

# class Unitweek(Document):
# 	def validate(self):
# 		self.append("unit_week_tool", {})
# 		days1 = get_dates_for_day(self)

# 		for day in days1:
# 			self.append("unit_week_tool" , {
# 				'start_day':day.start_day,
# 				'end_day':day.end_day
# 			})
	# pass
	# def on_update(self):
	#     self.update_child_table_dates()

	# def update_child_table_dates(self):
	#     from_date = self.from_date
	#     to_date = self.to_date

	#     if from_date and to_date:
	#         for row in self.get('unit_week_tool'):
	#             row.start_day = from_date
	#             row.end_day = to_date

	#         self.save()  
	#     else:
	#         frappe.throw("From date and to date are required.")




# from frappe.utils import cint, formatdate, getdate, today

# @frappe.whitelist()
# def get_weekly_off_date_list(self , day):
# 	start_date, end_date = getdate(self.from_date), getdate(self.to_date)

# 	import calendar
# 	from datetime import timedelta

# 	from dateutil import relativedelta

# 	date_list = []
# 	existing_date_list = []
# 	week_1st_day = getattr(calendar, (day).upper())
# 	# week_2st_day = getattr(calendar, (self.end_day).upper())
# 	reference_date = start_date + relativedelta.relativedelta(weekday=week_1st_day)
# 	# existing_date_list = [getdate(holiday.holiday_date) for holiday in self.get("holidays")]

# 	while reference_date <= end_date:
# 		# if reference_date not in existing_date_list:
# 		date_list.append(reference_date)
# 		reference_date += timedelta(days=7)
# 	return date_list


from datetime import datetime, timedelta
import frappe

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









		

from datetime import datetime, timedelta


@frappe.whitelist()
def baio(self):
    # Convert start_date and end_date strings to datetime objects
    start = datetime.strptime(str(self.from_date), '%Y-%m-%d')
    end = datetime.strptime(str(self.to_date), '%Y-%m-%d')

    target_day = self.start_day
    day = self.end_day

    days_map1 = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

    target_day_int = days_map1[target_day]
    target_sec_day = days_map1[day]

    matching_dates = {}

    current_date = start
    # while current_date <= end:
    #     if current_date.weekday() == target_day_int:
    #         key = current_date.strftime('%A')  
    #         if key not in matching_dates:
    #             matching_dates[key] = []
    #         matching_dates[key].append(current_date.strftime('%Y-%m-%d'))
    #     elif current_date.weekday() == target_sec_day:
    #         key = current_date.strftime('%A')  
    #         if key not in matching_dates:
    #             matching_dates[key] = []
    #         matching_dates[key].append(current_date.strftime('%Y-%m-%d'))

        # current_date += timedelta(days=1)
    return matching_dates




