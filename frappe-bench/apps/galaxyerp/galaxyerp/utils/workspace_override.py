import frappe

def setup_workspace(doc, method):
	"""
	Setup proper workspace layout and functionality
	"""
	# This function will be called when a workspace document is loaded
	# We can add any workspace-specific setup here if needed
	pass

def get_workspace_title(workspace_name):
	"""
	Get the proper title for a workspace
	"""
	# Map workspace names to proper titles
	title_mapping = {
		"Home": "Home",
		"Accounting": "Accounting",
		"Selling": "Selling",
		"Buying": "Buying",
		"Stock": "Stock",
		"Manufacturing": "Manufacturing",
		"Quality": "Quality",
		"Asset": "Asset",
		"Projects": "Projects",
		"CRM": "CRM",
		"Support": "Support",
		"HR": "HR",
		"Payroll": "Payroll",
		"Asset": "Asset",
		"Website": "Website",
		"Setup": "Setup",
		"Tools": "Tools",
		"Integrations": "Integrations",
		"Settings": "Settings"
	}
	
	return title_mapping.get(workspace_name, workspace_name)

def ensure_workspace_structure():
	"""
	Ensure proper workspace structure exists
	"""
	# This function can be called to ensure workspace structure is correct
	pass 