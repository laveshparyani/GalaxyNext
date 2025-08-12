app_name = "galaxyerp"
app_title = "GalaxyERP"
app_publisher = "GalaxyERP Software Private Limited"
app_description = "GalaxyERP App"
app_email = "admin@galaxyerpsoftware.com"
app_license = "mit"

# Override ERPNext/Frappe logo assets
app_logo_url = "/assets/galaxyerp/images/galaxynext_logo.png"

# Website context for logo overrides
website_context = {
    "favicon": "/assets/galaxyerp/images/galaxynext_logo.png",
    "splash_image": "/assets/galaxyerp/images/galaxynext_logo.png",
    "app_logo_url": "/assets/galaxyerp/images/galaxynext_logo.png",
    "brand_logo": "/assets/galaxyerp/images/galaxynext_logo.png",
    "footer_logo": "/assets/galaxyerp/images/galaxynext_logo.png",
    "login_with_email_link": True  # Enable login with email link functionality
}

# Override favicon for all contexts
favicon = "/assets/galaxyerp/images/galaxynext_logo.png"

# Override Methods
# ------------------------------
override_whitelisted_methods = {
	"frappe.email.email_body.get_brand_logo": "galaxyerp.utils.email_branding.get_brand_logo",
	"frappe.core.doctype.navbar_settings.navbar_settings.get_app_logo": "galaxyerp.utils.app_logo.get_app_logo",
	"frappe.desk.page.setup_wizard.setup_wizard.get_module_onboarding": "galaxyerp.utils.onboarding_methods.get_module_onboarding",
	"frappe.desk.page.setup_wizard.setup_wizard.get_onboarding_step": "galaxyerp.utils.onboarding_methods.get_onboarding_step",
	"frappe.widgets.onboarding_widget.get_onboarding_data": "galaxyerp.utils.onboarding_widget_override.get_onboarding_widget_data_override",
	"frappe.widgets.onboarding_widget.get_step_data": "galaxyerp.utils.onboarding_widget_override.override_onboarding_step_data"
}

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "galaxyerp",
# 		"logo": "/assets/galaxyerp/logo.png",
# 		"title": "GalaxyERP",
# 		"route": "/galaxyerp",
# 		"has_permission": "galaxyerp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/galaxyerp/css/galaxyerp.css",
    "/assets/galaxyerp/css/company_access.css"
]
app_include_js = [
    "/assets/galaxyerp/js/galaxyerp.js",
    "/assets/galaxyerp/js/permissions.js",
    "/assets/galaxyerp/js/frappe/ui/toolbar/about.js"
]

# Template overrides
# ------------------
doc_events = {
    "Workspace": {
        "onload": "galaxyerp.utils.workspace_override.setup_workspace"
    },
    "User": {
        "after_insert": "galaxyerp.utils.user_events.after_user_insert",
        "on_update": "galaxyerp.utils.user_events.after_user_update"
    }
}

# Permission query conditions
# ---------------------------
permission_query_conditions = {
    "Company": "galaxyerp.utils.permissions.get_company_permission_query",
    "Sales Order": "galaxyerp.utils.permissions.get_company_permission_query",
    "Purchase Order": "galaxyerp.utils.permissions.get_company_permission_query",
    "Delivery Note": "galaxyerp.utils.permissions.get_company_permission_query",
    "Purchase Receipt": "galaxyerp.utils.permissions.get_company_permission_query",
    "Sales Invoice": "galaxyerp.utils.permissions.get_company_permission_query",
    "Purchase Invoice": "galaxyerp.utils.permissions.get_company_permission_query",
    "Journal Entry": "galaxyerp.utils.permissions.get_company_permission_query",
    "Payment Entry": "galaxyerp.utils.permissions.get_company_permission_query",
    "Customer": "galaxyerp.utils.permissions.get_company_permission_query",
    "Supplier": "galaxyerp.utils.permissions.get_company_permission_query",
    "Warehouse": "galaxyerp.utils.permissions.get_company_permission_query"
}

# Has permission
# --------------
has_permission = {
    "Company": "galaxyerp.utils.permissions.has_company_permission",
    "Sales Order": "galaxyerp.utils.permissions.has_company_permission",
    "Purchase Order": "galaxyerp.utils.permissions.has_company_permission",
    "Delivery Note": "galaxyerp.utils.permissions.has_company_permission",
    "Purchase Receipt": "galaxyerp.utils.permissions.has_company_permission",
    "Sales Invoice": "galaxyerp.utils.permissions.has_company_permission",
    "Purchase Invoice": "galaxyerp.utils.permissions.has_company_permission",
    "Journal Entry": "galaxyerp.utils.permissions.has_company_permission",
    "Payment Entry": "galaxyerp.utils.permissions.has_company_permission",
    "Customer": "galaxyerp.utils.permissions.has_company_permission",
    "Supplier": "galaxyerp.utils.permissions.has_company_permission",
    "Warehouse": "galaxyerp.utils.permissions.has_company_permission"
}

# Website pages
# -------------
website_route_rules = [
    {"from_route": "/company-access-dashboard", "to_route": "galaxyerp/www/company_access_dashboard"}
]

# include js, css files in header of web template
web_include_css = [
    "/assets/galaxyerp/css/galaxyerp.css",
    "/assets/galaxyerp/css/company_access.css"
]
web_include_js = [
    "/assets/galaxyerp/js/galaxyerp.js",
    "/assets/galaxyerp/js/permissions.js",
    "/assets/galaxyerp/js/frappe/ui/toolbar/about.js"
]

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "galaxyerp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "galaxyerp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "galaxyerp.utils.jinja_methods",
# 	"filters": "galaxyerp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "galaxyerp.install.before_install"
# after_install = "galaxyerp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "galaxyerp.uninstall.before_uninstall"
# after_uninstall = "galaxyerp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "galaxyerp.utils.before_app_install"
# after_app_install = "galaxyerp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "galaxyerp.utils.before_app_uninstall"
# after_app_uninstall = "galaxyerp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "galaxyerp.notifications.get_notification_config"

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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"galaxyerp.tasks.all"
# 	],
# 	"daily": [
# 		"galaxyerp.tasks.daily"
# 	],
# 	"hourly": [
# 		"galaxyerp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"galaxyerp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"galaxyerp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "galaxyerp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "galaxyerp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "galaxyerp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["galaxyerp.utils.before_request"]
# after_request = ["galaxyerp.utils.after_request"]

# Job Events
# ----------
# before_job = ["galaxyerp.utils.before_job"]
# after_job = ["galaxyerp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"galaxyerp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

