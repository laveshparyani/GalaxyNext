import frappe
import re
import json

def replace_erpnext_in_content(content):
	"""
	Replace ERPNext references with GalaxyNext in content
	"""
	if not content:
		return content
	
	# Comprehensive replacement patterns
	replacements = [
		(r'\bERPNext\b', 'GalaxyNext'),
		(r'\berpnext\b', 'galaxynext'),
		(r'Items are integral to everything you do in ERPNext', 'Items are integral to everything you do in GalaxyNext'),
		(r'ERPNext sets up a simple chart of accounts', 'GalaxyNext sets up a simple chart of accounts'),
		(r'ERPNext is optimized for itemized management', 'GalaxyNext is optimized for itemized management'),
		(r'Completing the Item Master is very essential for the successful implementation of ERPNext', 'Completing the Item Master is very essential for the successful implementation of GalaxyNext'),
		(r'In ERPNext, you can maintain a Warehouse in the tree structure', 'In GalaxyNext, you can maintain a Warehouse in the tree structure'),
		(r'Let\'s begin your journey with ERPNext', 'Let\'s begin your journey with GalaxyNext'),
		(r'You\'re ready to start your journey with ERPNext', 'You\'re ready to start your journey with GalaxyNext'),
		(r'Welcome to ERPNext', 'Welcome to GalaxyNext'),
		(r'Login to ERPNext', 'Login to GalaxyNext'),
		(r'Create a ERPNext Account', 'Create a GalaxyNext Account'),
		(r'ERPNext Setup', 'GalaxyNext Setup'),
		(r'ERPNext Setup Complete', 'GalaxyNext Setup Complete'),
		(r'ERPNext is ready to use', 'GalaxyNext is ready to use'),
		(r'Your ERPNext instance is now ready', 'Your GalaxyNext instance is now ready'),
		(r'ERPNext Dashboard', 'GalaxyNext Dashboard'),
		(r'ERPNext Workspace', 'GalaxyNext Workspace'),
		(r'ERPNext Modules', 'GalaxyNext Modules'),
		(r'ERPNext Features', 'GalaxyNext Features'),
		(r'ERPNext Documentation', 'GalaxyNext Documentation'),
		(r'ERPNext Community', 'GalaxyNext Community'),
		(r'ERPNext Support', 'GalaxyNext Support'),
		(r'ERPNext Training', 'GalaxyNext Training'),
		(r'ERPNext Certification', 'GalaxyNext Certification'),
		(r'ERPNext Partner', 'GalaxyNext Partner'),
		(r'ERPNext Developer', 'GalaxyNext Developer'),
		(r'ERPNext Consultant', 'GalaxyNext Consultant'),
		(r'ERPNext Implementation', 'GalaxyNext Implementation'),
		(r'ERPNext Migration', 'GalaxyNext Migration'),
		(r'ERPNext Customization', 'GalaxyNext Customization'),
		(r'ERPNext Integration', 'GalaxyNext Integration'),
		(r'ERPNext API', 'GalaxyNext API'),
		(r'ERPNext REST API', 'GalaxyNext REST API'),
		(r'ERPNext Webhook', 'GalaxyNext Webhook'),
		(r'ERPNext Workflow', 'GalaxyNext Workflow'),
		(r'ERPNext Report', 'GalaxyNext Report'),
		(r'ERPNext Print Format', 'GalaxyNext Print Format'),
		(r'ERPNext Letter Head', 'GalaxyNext Letter Head'),
		(r'ERPNext Print Style', 'GalaxyNext Print Style'),
		(r'ERPNext Email Template', 'GalaxyNext Email Template'),
		(r'ERPNext Notification', 'GalaxyNext Notification'),
		(r'ERPNext Calendar', 'GalaxyNext Calendar'),
		(r'ERPNext Task', 'GalaxyNext Task'),
		(r'ERPNext Project', 'GalaxyNext Project'),
		(r'ERPNext Issue', 'GalaxyNext Issue'),
		(r'ERPNext Timesheet', 'GalaxyNext Timesheet'),
		(r'ERPNext Activity', 'GalaxyNext Activity'),
		(r'ERPNext Event', 'GalaxyNext Event'),
		(r'ERPNext Meeting', 'GalaxyNext Meeting'),
		(r'ERPNext Contact', 'GalaxyNext Contact'),
		(r'ERPNext Address', 'GalaxyNext Address'),
		(r'ERPNext Lead', 'GalaxyNext Lead'),
		(r'ERPNext Opportunity', 'GalaxyNext Opportunity'),
		(r'ERPNext Quotation', 'GalaxyNext Quotation'),
		(r'ERPNext Sales Order', 'GalaxyNext Sales Order'),
		(r'ERPNext Delivery Note', 'GalaxyNext Delivery Note'),
		(r'ERPNext Sales Invoice', 'GalaxyNext Sales Invoice'),
		(r'ERPNext Payment Entry', 'GalaxyNext Payment Entry'),
		(r'ERPNext Journal Entry', 'GalaxyNext Journal Entry'),
		(r'ERPNext Purchase Order', 'GalaxyNext Purchase Order'),
		(r'ERPNext Purchase Receipt', 'GalaxyNext Purchase Receipt'),
		(r'ERPNext Purchase Invoice', 'GalaxyNext Purchase Invoice'),
		(r'ERPNext Stock Entry', 'GalaxyNext Stock Entry'),
		(r'ERPNext Material Request', 'GalaxyNext Material Request'),
		(r'ERPNext Request for Quotation', 'GalaxyNext Request for Quotation'),
		(r'ERPNext Supplier Quotation', 'GalaxyNext Supplier Quotation'),
		(r'ERPNext BOM', 'GalaxyNext BOM'),
		(r'ERPNext Work Order', 'GalaxyNext Work Order'),
		(r'ERPNext Job Card', 'GalaxyNext Job Card'),
		(r'ERPNext Maintenance Schedule', 'GalaxyNext Maintenance Schedule'),
		(r'ERPNext Maintenance Visit', 'GalaxyNext Maintenance Visit'),
		(r'ERPNext Asset', 'GalaxyNext Asset'),
		(r'ERPNext Asset Category', 'GalaxyNext Asset Category'),
		(r'ERPNext Asset Movement', 'GalaxyNext Asset Movement'),
		(r'ERPNext Asset Value Adjustment', 'GalaxyNext Asset Value Adjustment'),
		(r'ERPNext Asset Depreciation Schedule', 'GalaxyNext Asset Depreciation Schedule'),
		(r'ERPNext Asset Maintenance', 'GalaxyNext Asset Maintenance'),
		(r'ERPNext Asset Maintenance Log', 'GalaxyNext Asset Maintenance Log'),
		(r'ERPNext Asset Maintenance Team', 'GalaxyNext Asset Maintenance Team'),
		(r'ERPNext Asset Maintenance Task', 'GalaxyNext Asset Maintenance Task'),
		(r'ERPNext Asset Maintenance Schedule', 'GalaxyNext Asset Maintenance Schedule'),
		(r'ERPNext Asset Maintenance Visit', 'GalaxyNext Asset Maintenance Visit'),
		(r'ERPNext Asset Maintenance Schedule Template', 'GalaxyNext Asset Maintenance Schedule Template'),
		(r'ERPNext Asset Maintenance Visit Template', 'GalaxyNext Asset Maintenance Visit Template'),
		(r'ERPNext Asset Maintenance Task Template', 'GalaxyNext Asset Maintenance Task Template'),
		(r'ERPNext Asset Maintenance Team Template', 'GalaxyNext Asset Maintenance Team Template'),
		(r'ERPNext Asset Maintenance Log Template', 'GalaxyNext Asset Maintenance Log Template'),
	]
	
	for pattern, replacement in replacements:
		content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
	
	return content

def get_onboarding_content_override():
	"""
	Override onboarding content to replace ERPNext with GalaxyNext
	"""
	pass

def override_onboarding_data(data):
	"""
	Override onboarding data to replace ERPNext branding
	"""
	if not data:
		return data
	
	if isinstance(data, dict):
		for key, value in data.items():
			if isinstance(value, str):
				data[key] = replace_erpnext_in_content(value)
			elif isinstance(value, dict):
				data[key] = override_onboarding_data(value)
			elif isinstance(value, list):
				data[key] = [override_onboarding_data(item) if isinstance(item, (dict, str)) else item for item in value]
	elif isinstance(data, str):
		return replace_erpnext_in_content(data)
	elif isinstance(data, list):
		return [override_onboarding_data(item) if isinstance(item, (dict, str)) else item for item in data]
	
	return data

def get_module_onboarding_override(module_name):
	"""
	Override module onboarding content specifically for the Home module
	"""
	if module_name == "Setup" or module_name == "Home":
		# Return custom onboarding data for Home module
		return {
			"title": "Let's begin your journey with GalaxyNext",
			"subtitle": "Item, Customer, Supplier and Quotation",
			"success_message": "You're ready to start your journey with GalaxyNext",
			"steps": [
				{"step": "Create an Item"},
				{"step": "Create a Customer"},
				{"step": "Create Your First Sales Invoice"}
			]
		}
	return None

def override_onboarding_step_content(step_name, content):
	"""
	Override specific onboarding step content
	"""
	if not content:
		return content
	
	# Replace ERPNext references in step content
	content = replace_erpnext_in_content(content)
	
	# Specific replacements for common onboarding steps
	replacements = {
		"Create an Item": {
			"description": content.replace(
				"Items are integral to everything you do in ERPNext",
				"Items are integral to everything you do in GalaxyNext"
			).replace(
				"Everything you buy or sell, whether it is a physical product or a service is an Item. Items can be stock, non-stock, variants, serialized, batched, assets, etc.",
				"Everything you buy or sell, whether it is a physical product or a service is an Item. Items can be stock, non-stock, variants, serialized, batched, assets, etc."
			)
		},
		"Create a Customer": {
			"description": content.replace(
				"Customers are linked in Quotations, Sales Orders, Invoices, and Payments",
				"Customers are linked in Quotations, Sales Orders, Invoices, and Payments"
			)
		},
		"Create Your First Sales Invoice": {
			"description": content.replace(
				"A Sales Invoice is a bill that you send to your Customers against which the Customer makes the payment",
				"A Sales Invoice is a bill that you send to your Customers against which the Customer makes the payment"
			)
		},
		"Create a Product": {
			"description": content.replace(
				"ERPNext is optimized for itemized management of your sales and purchase",
				"GalaxyNext is optimized for itemized management of your sales and purchase"
			).replace(
				"Completing the Item Master is very essential for the successful implementation of ERPNext",
				"Completing the Item Master is very essential for the successful implementation of GalaxyNext"
			)
		},
		"Create a Warehouse": {
			"description": content.replace(
				"In ERPNext, you can maintain a Warehouse in the tree structure",
				"In GalaxyNext, you can maintain a Warehouse in the tree structure"
			)
		},
		"Create a Quotation": {
			"description": content.replace(
				"Let's get started with business transactions by creating your first Quotation. You can create a Quotation for an existing customer or a prospect. It will be an approved document, with items you sell and the proposed price + taxes applied. After completing the instructions, you will get a Quotation in a ready to share print format.",
				"Let's get started with business transactions by creating your first Quotation. You can create a Quotation for an existing customer or a prospect. It will be an approved document, with items you sell and the proposed price + taxes applied. After completing the instructions, you will get a Quotation in a ready to share print format."
			)
		},
		"Create a Supplier": {
			"description": content.replace(
				"Also known as Vendor, is a master at the center of your purchase transactions. Suppliers are linked in Request for Quotation, Purchase Orders, Receipts, and Payments. Suppliers can be either numbered or identified by name.",
				"Also known as Vendor, is a master at the center of your purchase transactions. Suppliers are linked in Request for Quotation, Purchase Orders, Receipts, and Payments. Suppliers can be either numbered or identified by name."
			).replace(
				"Through Supplier's master, you can effectively track essentials like:",
				"Through Supplier's master, you can effectively track essentials like:"
			)
		},
		"Create a Material Request": {
			"description": content.replace(
				"Also known as Purchase Request or an Indent, is a document identifying a requirement of a set of items (products or services) for various purposes like procurement, transfer, issue, or manufacturing. Once the Material Request is validated, a purchase manager can take the next actions for purchasing items like requesting RFQ from a supplier or directly placing an order with an identified Supplier.",
				"Also known as Purchase Request or an Indent, is a document identifying a requirement of a set of items (products or services) for various purposes like procurement, transfer, issue, or manufacturing. Once the Material Request is validated, a purchase manager can take the next actions for purchasing items like requesting RFQ from a supplier or directly placing an order with an identified Supplier."
			)
		},
		"Create BOM": {
			"description": content.replace(
				"A Bill of Materials (BOM) is a list of items and sub-assemblies with quantities required to manufacture an Item.",
				"A Bill of Materials (BOM) is a list of items and sub-assemblies with quantities required to manufacture an Item."
			).replace(
				"BOM also provides cost estimation for the production of the item. It takes raw-materials cost based on valuation and operations to cost based on routing, which gives total costing for a BOM.",
				"BOM also provides cost estimation for the production of the item. It takes raw-materials cost based on valuation and operations to cost based on routing, which gives total costing for a BOM."
			)
		},
		"Work Order": {
			"description": content.replace(
				"A Work Order or a Job order is given to the manufacturing shop floor by the Production Manager to initiate the manufacturing of a certain quantity of an item. Work Order carriers details of production Item, its BOM, quantities to be manufactured, and operations.",
				"A Work Order or a Job order is given to the manufacturing shop floor by the Production Manager to initiate the manufacturing of a certain quantity of an item. Work Order carriers details of production Item, its BOM, quantities to be manufactured, and operations."
			).replace(
				"Through Work Order, you can track various production status like:",
				"Through Work Order, you can track various production status like:"
			)
		},
		"Asset Item": {
			"description": content.replace(
				"Asset items are created based on Asset Category. You can create one or multiple items against once Asset Category. The sales and purchase transaction for Asset is done via Asset Item.",
				"Asset items are created based on Asset Category. You can create one or multiple items against once Asset Category. The sales and purchase transaction for Asset is done via Asset Item."
			)
		},
		"Create Product": {
			"description": content.replace(
				"One of the prerequisites of a BOM is the creation of raw materials, sub-assembly, and finished items. Once these items are created, you will be able to proceed to the Bill of Materials master, which is composed of items and routing.",
				"One of the prerequisites of a BOM is the creation of raw materials, sub-assembly, and finished items. Once these items are created, you will be able to proceed to the Bill of Materials master, which is composed of items and routing."
			)
		}
	}
	
	if step_name in replacements:
		return replacements[step_name]["description"]
	
	return content 