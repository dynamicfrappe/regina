from . import __version__ as app_version

app_name = "regina"
app_title = "Regina"
app_publisher = "Dynamic Business Solutions"
app_description = "Regina Resort"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "beshoy.atef@dynamiceg.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/regina/css/regina.css"
# app_include_js = "/assets/regina/js/regina.js"

# include js, css files in header of web template
# web_include_css = "/assets/regina/css/regina.css"
# web_include_js = "/assets/regina/js/regina.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "regina/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# is_frappe_above_v13 = int(frappe_version.split('.')[0]) > 13

# Includes in <head>
# ------------------

# include js, css files in header of desk.html



# include js, css files in header of web template
# app_include_css = ['chat.bundle.css'] if is_frappe_above_v13 else [
#     '/assets/css/chat.css']
# app_include_js = ['chat.bundle.js'] if is_frappe_above_v13 else [
#     '/assets/js/chat.js']
# web_include_css = ['chat.bundle.css'] if is_frappe_above_v13 else [
#     '/assets/css/chat.css']
# web_include_js = ['chat.bundle.js'] if is_frappe_above_v13 else [
#     '/assets/js/chat.js']
# doctype_js =      {"Contract" :  "override/contract/contract.js"}
# doctype_list_js = {"Contract" :  "override/contract/contract_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "regina.install.before_install"
# after_install = "regina.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "regina.uninstall.before_uninstall"
# after_uninstall = "regina.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "regina.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Contract": "regina.override.contract.contract.Contract"
    
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"regina.tasks.all"
# 	],
# 	"daily": [
# 		"regina.tasks.daily"
# 	],
# 	"hourly": [
# 		"regina.tasks.hourly"
# 	],
# 	"weekly": [
# 		"regina.tasks.weekly"
# 	]
# 	"monthly": [
# 		"regina.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "regina.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "regina.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "regina.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"regina.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
on_session_creation = "regina.override.auth.update_representative_status"
on_logout = (
					"regina.override.auth.clear_session_defaults"
				)
after_migrate="regina.on_migrate.make_migrations"
domains = {
    "Time Share" : "regina.domains.time_share"
}