import frappe
from frappe import _

def get_context(context):
    """Get context for the Company Access Control dashboard"""
    context.title = "Company Access Control Dashboard"
    context.no_cache = 1
    
    # Check if user has permission to access this page
    if not frappe.has_permission("Company Access Control", "read"):
        frappe.throw(_("You don't have permission to access this page"), frappe.PermissionError)
    
    # Get current user's company access info
    user = frappe.session.user
    context.user_access = get_user_access_info(user)
    
    # Get summary statistics
    context.stats = get_dashboard_stats()
    
    # Get recent access records
    context.recent_access = get_recent_access_records()
    
    # Get company app status
    context.company_apps = get_company_app_status()
    
    return context

def get_user_access_info(user):
    """Get comprehensive user access information"""
    from galaxyerp.utils.company_access import get_user_company_access
    
    access = get_user_company_access(user)
    
    if not access["has_access"]:
        return {
            "has_access": False,
            "message": "No company access assigned",
            "company": None,
            "apps": [],
            "roles": []
        }
    
    return {
        "has_access": True,
        "company": access["company"],
        "apps": access["apps"],
        "roles": access["roles"],
        "is_admin": access["is_admin"],
        "valid_from": access["valid_from"],
        "valid_until": access["valid_until"]
    }

def get_dashboard_stats():
    """Get dashboard statistics"""
    stats = {}
    
    # Check if Company Access Control doctype exists
    if not frappe.db.exists("DocType", "Company Access Control"):
        stats["total_users"] = 0
        stats["total_companies"] = frappe.db.count("Company")
        stats["total_apps"] = 0
        stats["expiring_users"] = 0
        stats["users_without_access"] = 0
        return stats
    
    # Total users with company access
    stats["total_users"] = frappe.db.count("Company Access Control", {"access_status": "Active"})
    
    # Total companies
    stats["total_companies"] = frappe.db.count("Company")
    
    # Total company apps
    if frappe.db.exists("DocType", "Company App"):
        stats["total_apps"] = frappe.db.count("Company App", {"app_status": "Active"})
    else:
        stats["total_apps"] = 0
    
    # Users with expiring access (next 7 days)
    from frappe.utils import now_datetime, add_days
    expiring_users = frappe.get_all(
        "Company Access Control",
        filters={
            "access_status": "Active",
            "valid_until": ["between", [now_datetime(), add_days(now_datetime(), 7)]]
        },
        fields=["name"]
    )
    stats["expiring_users"] = len(expiring_users)
    
    # Users without company access
    system_users = frappe.get_all(
        "User",
        filters={"user_type": "System User", "enabled": 1},
        fields=["name"]
    )
    
    users_with_access = frappe.get_all(
        "Company Access Control",
        filters={"access_status": "Active"},
        fields=["user"]
    )
    
    users_with_access_set = set([u.user for u in users_with_access])
    users_without_access = [u for u in system_users if u.name not in users_with_access_set]
    stats["users_without_access"] = len(users_without_access)
    
    return stats

def get_recent_access_records():
    """Get recent company access records"""
    if not frappe.db.exists("DocType", "Company Access Control"):
        return []
    
    records = frappe.get_all(
        "Company Access Control",
        fields=["user", "company", "access_status", "valid_from", "valid_until", "modified"],
        order_by="modified desc",
        limit=10
    )
    
    # Add user details
    for record in records:
        try:
            user_doc = frappe.get_doc("User", record.user)
            record.user_full_name = user_doc.full_name or record.user
        except:
            record.user_full_name = record.user
    
    return records

def get_company_app_status():
    """Get status of company apps"""
    if not frappe.db.exists("DocType", "Company App"):
        return []
    
    apps = frappe.get_all(
        "Company App",
        fields=["name", "app_title", "app_status", "app_description"],
        order_by="app_title"
    )
    
    # Add usage statistics
    for app in apps:
        app["user_count"] = frappe.db.count(
            "Company App Assignment",
            {"company_app": app.name, "app_status": "Active"}
        )
    
    return apps

@frappe.whitelist()
def get_access_summary():
    """Get access summary for AJAX calls"""
    user = frappe.session.user
    return get_user_access_info(user)

@frappe.whitelist()
def get_dashboard_data():
    """Get dashboard data for AJAX calls"""
    return {
        "stats": get_dashboard_stats(),
        "recent_access": get_recent_access_records(),
        "company_apps": get_company_app_status()
    }

@frappe.whitelist()
def get_user_company_access_chart():
    """Get data for company access chart"""
    if not frappe.db.exists("DocType", "Company Access Control"):
        return []
    
    companies = frappe.get_all("Company", fields=["name", "company_name"])
    
    chart_data = []
    for company in companies:
        user_count = frappe.db.count(
            "Company Access Control",
            {"company": company.name, "access_status": "Active"}
        )
        chart_data.append({
            "company": company.company_name,
            "users": user_count
        })
    
    return chart_data

@frappe.whitelist()
def get_access_trends():
    """Get access trends for the last 30 days"""
    from frappe.utils import now_datetime, add_days
    
    trends = []
    for i in range(30):
        date = add_days(now_datetime(), -i)
        start_date = frappe.utils.get_datetime(date).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = frappe.utils.get_datetime(date).replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Count new access records created on this date
        new_access = frappe.db.count(
            "Company Access Control",
            {
                "creation": ["between", [start_date, end_date]]
            }
        )
        
        trends.append({
            "date": date.strftime("%Y-%m-%d"),
            "new_access": new_access
        })
    
    return trends[::-1]  # Reverse to show oldest first 