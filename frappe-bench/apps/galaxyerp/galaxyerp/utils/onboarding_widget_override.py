import frappe
from .onboarding_override import replace_erpnext_in_content

def override_onboarding_widget_data(data):
	"""
	Override onboarding widget data to replace ERPNext with GalaxyNext
	"""
	if not data:
		return data
	
	# Handle different data structures
	if isinstance(data, dict):
		for key, value in data.items():
			if isinstance(value, str):
				data[key] = replace_erpnext_in_content(value)
			elif isinstance(value, dict):
				data[key] = override_onboarding_widget_data(value)
			elif isinstance(value, list):
				data[key] = [override_onboarding_widget_data(item) if isinstance(item, (dict, str)) else item for item in value]
	elif isinstance(data, str):
		return replace_erpnext_in_content(data)
	elif isinstance(data, list):
		return [override_onboarding_widget_data(item) if isinstance(item, (dict, str)) else item for item in data]
	
	return data

def get_onboarding_widget_data_override(module_name):
	"""
	Override the onboarding widget data for specific modules
	"""
	# Get the original data
	original_data = frappe.get_doc("Module Onboarding", module_name)
	
	# Apply our custom override for Home module
	if module_name == "Home":
		original_data.title = "Let's begin your journey with GalaxyNext"
		original_data.subtitle = "Item, Customer, Supplier and Quotation"
		original_data.success_message = "You're ready to start your journey with GalaxyNext"
	
	# Replace any remaining ERPNext references
	original_data.title = replace_erpnext_in_content(original_data.title)
	original_data.subtitle = replace_erpnext_in_content(original_data.subtitle)
	original_data.success_message = replace_erpnext_in_content(original_data.success_message)
	
	return original_data

def override_onboarding_step_data(step_name):
	"""
	Override onboarding step data to replace ERPNext with GalaxyNext
	"""
	# Get the original step data
	original_data = frappe.get_doc("Onboarding Step", step_name)
	
	# Apply content replacement
	original_data.title = replace_erpnext_in_content(original_data.title)
	original_data.description = replace_erpnext_in_content(original_data.description)
	
	return original_data 