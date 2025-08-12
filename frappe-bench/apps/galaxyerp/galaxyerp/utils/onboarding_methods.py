import frappe
from .onboarding_override import replace_erpnext_in_content, get_module_onboarding_override, override_onboarding_step_content

def get_module_onboarding(module_name):
	"""
	Override the get_module_onboarding method to replace ERPNext with GalaxyNext
	"""
	# Get the original onboarding data
	original_data = frappe.get_doc("Module Onboarding", module_name)
	
	# Apply our custom override for Home module
	if module_name == "Home":
		custom_data = get_module_onboarding_override(module_name)
		if custom_data:
			# Update the document with custom data
			original_data.title = custom_data["title"]
			original_data.subtitle = custom_data["subtitle"]
			original_data.success_message = custom_data["success_message"]
			original_data.steps = custom_data["steps"]
	
	# Replace any remaining ERPNext references
	original_data.title = replace_erpnext_in_content(original_data.title)
	original_data.subtitle = replace_erpnext_in_content(original_data.subtitle)
	original_data.success_message = replace_erpnext_in_content(original_data.success_message)
	
	return original_data

def get_onboarding_step(step_name):
	"""
	Override the get_onboarding_step method to replace ERPNext with GalaxyNext
	"""
	# Get the original step data
	original_data = frappe.get_doc("Onboarding Step", step_name)
	
	# Apply content replacement
	original_data.title = replace_erpnext_in_content(original_data.title)
	original_data.description = override_onboarding_step_content(step_name, original_data.description)
	
	return original_data

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