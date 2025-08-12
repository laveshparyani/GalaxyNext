#!/usr/bin/env python3
"""
Test script for Company Access Control functionality
"""

import sys
import os

# Add the frappe-bench directory to Python path
sys.path.insert(0, '/mnt/c/Users/gi13/Desktop/GalaxyNext/frappe-bench')

def test_company_access():
    try:
        import frappe
        
        # Initialize Frappe
        frappe.init(site='galaxynext.com')
        frappe.connect()
        
        print("=== Company Access Control Test ===")
        
        # Check if all doctypes exist
        print("1. Checking doctype existence:")
        print(f"   Company Access Control: {frappe.db.exists('DocType', 'Company Access Control')}")
        print(f"   Company App: {frappe.db.exists('DocType', 'Company App')}")
        print(f"   Company App Assignment: {frappe.db.exists('DocType', 'Company App Assignment')}")
        print(f"   Company Role Assignment: {frappe.db.exists('DocType', 'Company Role Assignment')}")
        
        # Test the company access function
        print("\n2. Testing company access function:")
        try:
            result = frappe.call('galaxyerp.utils.company_access.get_user_company_access', 
                               {'user': 'admin@galaxyerpsoftware.com'})
            print(f"   Function result: {result}")
            print("   ✅ Company access function works!")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test getting available companies
        print("\n3. Testing available companies:")
        try:
            companies = frappe.call('galaxyerp.utils.company_access.get_available_companies')
            print(f"   Available companies: {companies}")
            print("   ✅ Available companies function works!")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test getting available company apps
        print("\n4. Testing available company apps:")
        try:
            apps = frappe.call('galaxyerp.utils.company_access.get_available_company_apps')
            print(f"   Available apps: {apps}")
            print("   ✅ Available apps function works!")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print("\n=== Test Complete ===")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_company_access() 