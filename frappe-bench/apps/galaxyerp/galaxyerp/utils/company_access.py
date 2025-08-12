import frappe
from frappe import _
from frappe.permissions import get_roles
from frappe.utils import now_datetime
import json

@frappe.whitelist()
def get_user_company_access(user=None):
    """Get company access information for user"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return {
            "has_access": True, 
            "is_admin": True,
            "company": None,
            "apps": [],
            "roles": []
        }
    
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        return {
            "has_access": False, 
            "is_admin": False,
            "company": None,
            "apps": [],
            "roles": [],
            "message": "Company Access Control module not installed"
        }
    
    # Check if user has company access control record
    try:
        access_records = frappe.get_all("Company Access Control", 
                                      filters={"user": user}, 
                                      fields=["*"], 
                                      limit=1)
        if not access_records:
            return {
                "has_access": False, 
                "is_admin": False,
                "company": None,
                "apps": [],
                "roles": []
            }
        access = frappe.get_doc("Company Access Control", access_records[0].name)
    except Exception as e:
        return {
            "has_access": False, 
            "is_admin": False,
            "company": None,
            "apps": [],
            "roles": [],
            "message": "Error accessing company access control"
        }
    
    # Check if access is active and not expired
    if access.access_status != "Active":
        return {
            "has_access": False, 
            "is_admin": False,
            "company": access.company,
            "apps": [],
            "roles": []
        }
    
    # Check expiry
    if access.valid_until and access.valid_until < now_datetime():
        return {
            "has_access": False, 
            "is_admin": False,
            "company": access.company,
            "apps": [],
            "roles": []
        }
    
    # Get assigned apps
    apps = []
    for app_assignment in access.assigned_company_apps:
        if app_assignment.app_status == "Active":
            apps.append(app_assignment.company_app)
    
    # Get assigned roles
    roles = []
    is_admin = False
    for role_assignment in access.company_roles:
        roles.append(role_assignment.role)
        if role_assignment.role_type == "Company Admin":
            is_admin = True
    
    return {
        "has_access": True,
        "is_admin": is_admin,
        "company": access.company,
        "apps": apps,
        "roles": roles,
        "valid_from": access.valid_from,
        "valid_until": access.valid_until
    }

def has_company_permission(user=None, company=None, permission="read"):
    """Check if user has permission for specific company"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return False
    
    if company and access["company"] != company:
        return False
    
    return True

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

def update_user_permissions(user, company, apps):
    """Update user permissions based on company access"""
    # Clear existing user permissions for other companies
    frappe.db.delete("User Permission", {
        "user": user,
        "allow": "Company",
        "for_value": ["!=", company]
    })
    
    # Add user permission for assigned company
    if not frappe.db.exists("User Permission", {
        "user": user,
        "allow": "Company",
        "for_value": company
    }):
        frappe.get_doc({
            "doctype": "User Permission",
            "user": user,
            "allow": "Company",
            "for_value": company,
            "apply_to_all_doctypes": 1
        }).insert()

def get_company_app_workspaces(company_app):
    """Get workspaces for a company app"""
    app_config = frappe.get_doc("Company App", company_app)
    if not app_config:
        return []
    
    # Return company-specific workspaces
    return [
        {
            "name": f"{app_config.app_name}_workspace",
            "title": f"{app_config.app_title} Workspace",
            "icon": app_config.app_icon or "fa fa-cube",
            "cards": []
        }
    ]

def filter_workspaces_for_user(workspaces, user=None):
    """Filter workspaces based on user company access"""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return workspaces
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        # Return only core workspaces
        return [w for w in workspaces if w.get("module") in ["Setup", "Tools"]]
    
    # Filter based on user's company apps
    user_apps = access.get("apps", [])
    filtered_workspaces = []
    
    for workspace in workspaces:
        # Always include core workspaces
        if workspace.get("module") in ["Setup", "Tools", "Integrations"]:
            filtered_workspaces.append(workspace)
            continue
        
        # Check if workspace belongs to user's company apps
        workspace_app = workspace.get("app")
        if workspace_app in user_apps:
            filtered_workspaces.append(workspace)
    
    return filtered_workspaces

@frappe.whitelist()
def get_company_data(company):
    """Get company data with permission check"""
    if not has_company_permission(company=company):
        frappe.throw(_("You do not have access to this company"))
    
    # Proceed to fetch and return data
    company_doc = frappe.get_doc("Company", company)
    return company_doc.as_dict()

@frappe.whitelist()
def get_user_company_apps(user=None):
    """Get company apps available for user"""
    if not user:
        user = frappe.session.user
    
    access = get_user_company_access(user)
    if not access["has_access"]:
        return []
    
    apps = []
    for app_name in access["apps"]:
        app_config = frappe.get_doc("Company App", app_name)
        if app_config and app_config.app_status == "Active":
            apps.append({
                "name": app_config.app_name,
                "title": app_config.app_title,
                "description": app_config.app_description,
                "assigned": True
            })
    
    return apps

@frappe.whitelist()
def assign_company_to_user(user, company, apps=None, roles=None):
    """Assign company access to user"""
    if not frappe.has_permission("Company Access Control", "write"):
        frappe.throw(_("Permission denied"))
    
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        frappe.throw(_("Company Access Control module not installed. Please run bench migrate first."))
    
    # Create or update access control
    try:
        access = frappe.get_doc("Company Access Control", {"user": user})
        if not access:
            access = frappe.new_doc("Company Access Control")
            access.user = user
    except Exception as e:
        access = frappe.new_doc("Company Access Control")
        access.user = user
    
    access.company = company
    access.access_status = "Active"
    access.valid_from = now_datetime()
    
    # Clear existing assignments
    access.assigned_company_apps = []
    access.company_roles = []
    
    # Assign apps
    if apps:
        for app in apps:
            access.append("assigned_company_apps", {
                "company_app": app,
                "app_status": "Active"
            })
    
    # Assign roles
    if roles:
        for role in roles:
            access.append("company_roles", {
                "role": role,
                "role_type": "Company User",
                "permission_level": "Limited Access"
            })
    
    access.save()
    
    # Update user permissions
    update_user_permissions(user, company, apps or [])
    
    return access.name

@frappe.whitelist()
def create_company_admin_role(company):
    """Create company admin role for a specific company"""
    role_name = f"{company}_Admin"
    
    if not frappe.db.exists("Role", role_name):
        role = frappe.new_doc("Role")
        role.role_name = role_name
        role.desk_access = 1
        role.save()
    
    return role_name

@frappe.whitelist()
def get_company_users(company):
    """Get all users assigned to a specific company"""
    if not frappe.db.exists("DocType", "Company Access Control"):
        return []
    
    users = frappe.get_all(
        "Company Access Control",
        filters={"company": company, "access_status": "Active"},
        fields=["user", "access_status", "valid_from", "valid_until"]
    )
    return users

@frappe.whitelist()
def check_access_expiry():
    """Check and update expired access"""
    if not frappe.db.exists("DocType", "Company Access Control"):
        return []
    
    expired_access = frappe.get_all(
        "Company Access Control",
        filters={
            "access_status": "Active",
            "valid_until": ["<", now_datetime()]
        },
        fields=["name", "user", "company"]
    )
    
    for access in expired_access:
        doc = frappe.get_doc("Company Access Control", access.name)
        doc.access_status = "Expired"
        doc.save()
        
        # Notify user about expired access
        frappe.msgprint(
            f"Access expired for user {access.user} in company {access.company}",
            title="Access Expired"
        )

@frappe.whitelist()
def get_user_access_summary():
    """Get summary of user access for dashboard"""
    user = frappe.session.user
    access = get_user_company_access(user)
    
    summary = {
        "has_access": access["has_access"],
        "company": access["company"],
        "apps_count": len(access["apps"]),
        "roles_count": len(access["roles"]),
        "is_admin": access["is_admin"]
    }
    
    if access["has_access"]:
        summary["apps"] = access["apps"]
        summary["roles"] = access["roles"]
    
    return summary

@frappe.whitelist()
def bulk_assign_company_access(users, company, apps=None, roles=None):
    """Bulk assign company access to multiple users"""
    if not frappe.has_permission("Company Access Control", "write"):
        frappe.throw(_("Permission denied"))
    
    results = []
    for user in users:
        try:
            access_name = assign_company_to_user(user, company, apps, roles)
            results.append({"user": user, "status": "success", "access_name": access_name})
        except Exception as e:
            results.append({"user": user, "status": "error", "error": str(e)})
    
    return results

def apply_company_filters(doctype, filters=None):
    """Apply company filters to queries"""
    user = frappe.session.user
    access = get_user_company_access(user)
    
    if not access["has_access"]:
        # User has no company access, return empty result
        return {"company": ["=", "NON_EXISTENT"]}
    
    if filters is None:
        filters = {}
    
    # Add company filter
    filters["company"] = access["company"]
    
    return filters

def get_company_restricted_doctypes():
    """Get list of doctypes that should be company-restricted"""
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
        "Item",
        "Warehouse"
    ]

def setup_company_permissions():
    """Setup company permissions for restricted doctypes"""
    restricted_doctypes = get_company_restricted_doctypes()
    
    for doctype in restricted_doctypes:
        # Add permission query condition
        frappe.db.set_value(
            "Custom DocPerm",
            {
                "parent": doctype,
                "role": "Company User"
            },
            {
                "permlevel": 0,
                "select": 1,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 1,
                "cancel": 1,
                "amend": 1,
                "report": 1,
                "export": 1,
                "share": 1,
                "print": 1,
                "email": 1,
                "set_user_permissions": 1,
                "apply_user_permissions": 1
            }
        )