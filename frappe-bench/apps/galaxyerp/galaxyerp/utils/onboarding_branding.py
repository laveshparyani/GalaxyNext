import frappe
import re

def replace_erpnext_with_galaxynext(text):
	"""
	Replace ERPNext branding with GalaxyNext in text content
	"""
	if not text:
		return text
	
	# Replace ERPNext with GalaxyNext (case insensitive)
	text = re.sub(r'erpnext', 'GalaxyNext', text, flags=re.IGNORECASE)
	text = re.sub(r'ERPNext', 'GalaxyNext', text)
	
	return text

def get_onboarding_content():
	"""
	Override onboarding content to replace ERPNext with GalaxyNext
	"""
	# This function can be extended to override specific onboarding content
	pass 