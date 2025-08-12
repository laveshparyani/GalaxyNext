import frappe
from frappe import _
from galaxyerp.utils.company_access import get_user_company_access, has_company_permission

def get_company_permission_query(user, doctype):
    """Get permission query condition for company-restricted doctypes"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    # Check if the doctype has a company field
    try:
        meta = frappe.get_meta(doctype)
        if not meta.has_field("company"):
            # If doctype doesn't have company field, return empty string (no restriction)
            return ""
    except Exception:
        # If we can't get meta, return empty string to avoid errors
        return ""
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        # User has no company access, return condition that will show no results
        return "`tab{0}`.company = 'NON_EXISTENT'".format(doctype)
    
    # Return condition to filter by user's company
    return "`tab{0}`.company = '{1}'".format(doctype, access["company"])

def has_company_permission(user, doctype, ptype, doc=None):
    """Check if user has permission for company-restricted doctype"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return False
    
    # If document is provided, check if it belongs to user's company
    if doc and hasattr(doc, 'company'):
        if doc.company != access["company"]:
            return False
    
    return True

def get_company_restricted_doctypes():
    """Get list of doctypes that should be company-restricted"""
    # Only include doctypes that actually have a company field
    return [
        "Sales Order",
        "Purchase Order", 
        "Delivery Note",
        "Purchase Receipt",
        "Sales Invoice",
        "Purchase Invoice",
        "Journal Entry",
        "Payment Entry",
        "Customer",
        "Supplier",
        "Warehouse"
        # Note: "Item" removed as it doesn't have a company field
    ]

def apply_company_filters_to_query(doctype, filters=None):
    """Apply company filters to query filters"""
    if not filters:
        filters = {}
    
    user = frappe.session.user
    if user == "Administrator":
        return filters
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        # Return filter that will show no results
        filters["company"] = "NON_EXISTENT"
        return filters
    
    # Add company filter
    filters["company"] = access["company"]
    return filters

def get_user_accessible_companies(user=None):
    """Get list of companies user can access"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return frappe.get_all("Company", pluck="name")
    
    access = get_user_company_access(user)
    if access["has_access"] and access["company"]:
        return [access["company"]]
    
    return []

def check_company_access_for_doc(doc, user=None):
    """Check if user has access to a specific document based on company"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return False
    
    # Check if document has company field and if it matches user's company
    if hasattr(doc, 'company') and doc.company:
        return doc.company == access["company"]
    
    return True

def get_company_permission_conditions(doctype, user=None):
    """Get permission conditions for company-restricted doctypes"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return "`tab{0}`.company = 'NON_EXISTENT'".format(doctype)
    
    return "`tab{0}`.company = '{1}'".format(doctype, access["company"])

def filter_company_data(data, user=None):
    """Filter data based on user's company access"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return data
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return []
    
    # Filter data to only include user's company
    filtered_data = []
    for item in data:
        if isinstance(item, dict) and item.get('company') == access["company"]:
            filtered_data.append(item)
        elif hasattr(item, 'company') and item.company == access["company"]:
            filtered_data.append(item)
    
    return filtered_data

def get_company_restricted_modules():
    """Get list of modules that should be company-restricted"""
    return [
        "Selling",
        "Buying",
        "Stock",
        "Accounts",
        "Manufacturing",
        "Quality",
        "Asset",
        "Projects",
        "CRM",
        "Support"
    ]

def check_module_access(module, user=None):
    """Check if user has access to a specific module"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        # User has no company access, only allow core modules
        core_modules = ["Setup", "Tools", "Integrations", "Settings"]
        return module in core_modules
    
    # User has company access, allow all modules
    return True

def get_user_company_roles(user=None):
    """Get company-specific roles for user"""
    if not user:
        user = frappe.session.user
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return []
    
    return access.get("roles", [])

def is_company_admin(user=None):
    """Check if user is a company admin"""
    if not user:
        user = frappe.session.user
    
    access = get_user_company_access(user)
    return access.get("is_admin", False)

def get_company_admin_users(company):
    """Get all admin users for a specific company"""
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        return []
    
    admin_users = []
    
    company_access_records = frappe.get_all(
        "Company Access Control",
        filters={"company": company, "access_status": "Active"},
        fields=["user"]
    )
    
    for record in company_access_records:
        access = get_user_company_access(record.user)
        if access.get("is_admin", False):
            admin_users.append(record.user)
    
    return admin_users

def validate_company_access_for_action(doctype, action, user=None):
    """Validate company access for specific actions"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        frappe.throw(_("You do not have company access to perform this action"))
    
    # Additional validation for admin-only actions
    if action in ["create", "delete", "submit", "cancel"]:
        if not access.get("is_admin", False):
            frappe.throw(_("Only company administrators can perform this action"))
    
    return True

@frappe.whitelist()
def get_company_permission_summary(user=None):
    """Get summary of user's company permissions"""
    if not user:
        user = frappe.session.user
    
    access = get_user_company_access(user)
    
    summary = {
        "has_access": access["has_access"],
        "company": access["company"],
        "is_admin": access.get("is_admin", False),
        "apps_count": len(access.get("apps", [])),
        "roles_count": len(access.get("roles", [])),
        "accessible_doctypes": get_company_restricted_doctypes() if access["has_access"] else [],
        "accessible_modules": get_company_restricted_modules() if access["has_access"] else []
    }
    
    return summary 