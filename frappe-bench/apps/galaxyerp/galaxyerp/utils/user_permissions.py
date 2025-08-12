import frappe
from frappe import _

def has_galaxyerp_access(user=None):
    """Check if user has access to galaxyerp features via roles"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    # Get user's roles
    user_roles = frappe.get_roles(user)
    galaxyerp_roles = ["GalaxyERP User", "GalaxyERP Admin"]
    
    # Check if user has any galaxyerp roles
    return any(role in user_roles for role in galaxyerp_roles)

def is_galaxyerp_admin(user=None):
    """Check if user has GalaxyERP Admin role"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    return "GalaxyERP Admin" in user_roles

def get_galaxyerp_user_company(user=None):
    """Get the company app associated with the user"""
    if not user:
        user = frappe.session.user
    
    # Check user permissions for company-specific access
    user_permissions = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Company",
            "for_value": ["in", ["Packedge Industries", "Patodia Exports"]]
        },
        fields=["for_value"]
    )
    
    if user_permissions:
        return user_permissions[0].for_value
    
    return None

def should_load_galaxyerp_assets():
    """Determine if galaxyerp assets should be loaded"""
    return has_galaxyerp_access()

def should_load_company_assets(company_name):
    """Determine if company-specific assets should be loaded"""
    if not has_galaxyerp_access():
        return False
    
    user_company = get_galaxyerp_user_company()
    return user_company == company_name

def get_user_galaxyerp_profile(user=None):
    """Get the GalaxyERP role profile assigned to user"""
    if not user:
        user = frappe.session.user
    
    # Get user's role profiles
    user_profiles = frappe.get_all(
        "User Role Profile",
        filters={"parent": user},
        fields=["role_profile"]
    )
    
    for profile in user_profiles:
        if "GalaxyERP" in profile.role_profile:
            return profile.role_profile
    
    return None