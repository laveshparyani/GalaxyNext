import frappe
from frappe import _
from galaxyerp.utils.company_access import get_user_company_access

def after_user_insert(doc, method):
    """Handle events after user is inserted"""
    # Check if user should have default company access
    if doc.user_type == "System User":
        setup_default_company_access(doc)

def after_user_update(doc, method):
    """Handle events after user is updated"""
    # Update company access if user type changed
    if doc.has_value_changed("user_type"):
        if doc.user_type == "System User":
            setup_default_company_access(doc)
        else:
            # Remove company access for non-system users
            remove_company_access(doc)

def setup_default_company_access(doc):
    """Setup default company access for new system users"""
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        return
    
    # Check if user already has company access
    existing_access = frappe.db.exists("Company Access Control", {"user": doc.name})
    if existing_access:
        return
    
    # Get default company from system settings
    default_company = frappe.db.get_single_value("System Settings", "default_company")
    if not default_company:
        # Get first available company
        companies = frappe.get_all("Company", limit=1)
        if companies:
            default_company = companies[0].name
    
    if default_company:
        # Create default company access
        try:
            frappe.get_doc({
                "doctype": "Company Access Control",
                "user": doc.name,
                "company": default_company,
                "access_status": "Active"
            }).insert()
            
            frappe.msgprint(
                f"Default company access ({default_company}) has been assigned to user {doc.name}",
                title="Company Access Assigned"
            )
        except Exception as e:
            frappe.log_error(f"Failed to setup default company access for user {doc.name}: {str(e)}")

def remove_company_access(doc):
    """Remove company access for user"""
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        return
    
    try:
        existing_access = frappe.get_doc("Company Access Control", {"user": doc.name})
        existing_access.delete()

        frappe.msgprint(
            f"Company access has been removed for user {doc.name}",
            title="Company Access Removed"
        )
    except frappe.DoesNotExistError:
        # No company access exists, nothing to remove
        pass
    except Exception as e:
        frappe.log_error(f"Failed to remove company access for user {doc.name}: {str(e)}")

def validate_user_company_access(doc, method):
    """Validate user has proper company access"""
    if doc.user_type == "System User":
        # Check if user has company access
        access = get_user_company_access(doc.name)
        if not access["has_access"]:
            frappe.msgprint(
                f"User {doc.name} does not have company access assigned. Please assign company access.",
                title="Company Access Required",
                indicator="orange"
            )

def setup_user_company_roles(doc, company, roles=None):
    """Setup company-specific roles for user"""
    if not roles:
        roles = ["Company User"]
    
    # Get or create company access record
    try:
        access = frappe.get_doc("Company Access Control", {"user": doc.name})
    except frappe.DoesNotExistError:
        access = frappe.new_doc("Company Access Control")
        access.user = doc.name
        access.company = company
        access.access_status = "Active"
    
    # Clear existing roles
    access.company_roles = []
    
    # Add new roles
    for role in roles:
        access.append("company_roles", {
            "role": role,
            "role_type": "Company Admin" if role == "Company Admin" else "Company User",
            "permission_level": "Full Access" if role == "Company Admin" else "Limited Access"
        })
    
    access.save()
    return access.name

def get_user_company_info(user):
    """Get comprehensive company information for user"""
    access = get_user_company_access(user)
    
    if not access["has_access"]:
        return {
            "has_access": False,
            "message": "No company access assigned"
        }
    
    company_info = {
        "has_access": True,
        "company": access["company"],
        "apps": access["apps"],
        "roles": access["roles"],
        "is_admin": access["is_admin"],
        "valid_from": access["valid_from"],
        "valid_until": access["valid_until"]
    }
    
    # Get company details
    if access["company"]:
        try:
            company_doc = frappe.get_doc("Company", access["company"])
            company_info["company_name"] = company_doc.company_name
            company_info["company_abbr"] = company_doc.abbr
            company_info["company_country"] = company_doc.country
        except frappe.DoesNotExistError:
            company_info["company_name"] = access["company"]
    
    return company_info

def bulk_setup_company_access(users, company, apps=None, roles=None):
    """Bulk setup company access for multiple users"""
    results = []
    
    for user in users:
        try:
            # Get user doc
            user_doc = frappe.get_doc("User", user)
            
            # Setup company access
            access_name = setup_user_company_roles(user_doc, company, roles)
            
            results.append({
                "user": user,
                "status": "success",
                "access_name": access_name
            })
        except Exception as e:
            results.append({
                "user": user,
                "status": "error",
                "error": str(e)
            })
    
    return results

def check_user_access_expiry():
    """Check and notify about user access expiry"""
    from frappe.utils import now_datetime, add_days
    
    # Get users with access expiring in next 7 days
    expiring_access = frappe.get_all(
        "Company Access Control",
        filters={
            "access_status": "Active",
            "valid_until": ["between", [now_datetime(), add_days(now_datetime(), 7)]]
        },
        fields=["user", "company", "valid_until"]
    )
    
    for access in expiring_access:
        # Send notification to user
        frappe.sendmail(
            recipients=[access.user],
            subject="Company Access Expiring Soon",
            message=f"""
            Your company access for {access.company} will expire on {access.valid_until}.
            Please contact your administrator to renew your access.
            """
        )
    
    return len(expiring_access)

def get_users_without_company_access():
    """Get list of system users without company access"""
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        return []
    
    users_without_access = []
    
    system_users = frappe.get_all(
        "User",
        filters={"user_type": "System User", "enabled": 1},
        fields=["name", "full_name", "email"]
    )
    
    for user in system_users:
        access = get_user_company_access(user.name)
        if not access["has_access"]:
            users_without_access.append(user)
    
    return users_without_access

@frappe.whitelist()
def auto_assign_company_access():
    """Automatically assign company access to users without access"""
    users_without_access = get_users_without_company_access()
    
    if not users_without_access:
        return {"message": "All users have company access assigned"}
    
    # Get default company
    default_company = frappe.db.get_single_value("System Settings", "default_company")
    if not default_company:
        companies = frappe.get_all("Company", limit=1)
        if companies:
            default_company = companies[0].name
    
    if not default_company:
        return {"error": "No company available for assignment"}
    
    results = []
    for user in users_without_access:
        try:
            user_doc = frappe.get_doc("User", user.name)
            access_name = setup_user_company_roles(user_doc, default_company)
            results.append({
                "user": user.name,
                "status": "success",
                "access_name": access_name
            })
        except Exception as e:
            results.append({
                "user": user.name,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "message": f"Company access assigned to {len([r for r in results if r['status'] == 'success'])} users",
        "results": results
    } 