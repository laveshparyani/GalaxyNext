import frappe
from frappe.model.document import Document
from frappe import _
from galaxyerp.utils.company_access import update_user_permissions, get_user_company_access

class CompanyAccessControl(Document):
    def validate(self):
        self.validate_user_access()
        self.validate_company_assignment()
        self.validate_access_period()
        self.validate_app_assignments()
    
    def before_save(self):
        self.update_company_apps()
    
    def after_insert(self):
        self.update_user_permissions()
        self.create_audit_log("created")
    
    def after_update(self):
        self.update_user_permissions()
        self.create_audit_log("updated")
    
    def on_trash(self):
        self.create_audit_log("deleted")
        # Remove user permissions when access is deleted
        if self.user and self.company:
            frappe.db.delete("User Permission", {
                "user": self.user,
                "allow": "Company",
                "for_value": self.company
            })
    
    def validate_user_access(self):
        """Validate user access permissions"""
        if not frappe.has_permission("Company Access Control", "write"):
            frappe.throw(_("You don't have permission to modify company access"))
        
        # Check if user exists
        if not frappe.db.exists("User", self.user):
            frappe.throw(_("User {0} does not exist").format(self.user))
    
    def validate_company_assignment(self):
        """Validate company assignment"""
        if self.company:
            company_exists = frappe.db.exists("Company", self.company)
            if not company_exists:
                frappe.throw(_("Company {0} does not exist").format(self.company))
    
    def validate_access_period(self):
        """Validate access period"""
        if self.valid_until and self.valid_from:
            if self.valid_until <= self.valid_from:
                frappe.throw(_("Valid Until must be after Valid From"))
    
    def validate_app_assignments(self):
        """Validate company app assignments"""
        for app_assignment in self.assigned_company_apps:
            if app_assignment.company_app:
                app_exists = frappe.db.exists("Company App", app_assignment.company_app)
                if not app_exists:
                    frappe.throw(_("Company App {0} does not exist").format(app_assignment.company_app))
    
    def update_company_apps(self):
        """Update available company apps based on company"""
        if self.company and not self.assigned_company_apps:
            # Get available apps for this company
            available_apps = frappe.get_all(
                "Company App",
                filters={"app_status": "Active"},
                fields=["name", "app_title"]
            )
            
            for app in available_apps:
                self.append("assigned_company_apps", {
                    "company_app": app.name,
                    "app_status": "Active"
                })
    
    def update_user_permissions(self):
        """Update user permissions based on company access"""
        if self.user and self.company:
            apps = [app.company_app for app in self.assigned_company_apps if app.app_status == "Active"]
            update_user_permissions(self.user, self.company, apps)
    
    def create_audit_log(self, action):
        """Create audit log for access changes"""
        frappe.get_doc({
            "doctype": "Comment",
            "comment_type": "Updated",
            "reference_doctype": "Company Access Control",
            "reference_name": self.name,
            "content": f"Company access {action} for user {self.user} in company {self.company}",
            "comment_by": frappe.session.user
        }).insert(ignore_permissions=True)
    
    def get_user_access_info(self):
        """Get detailed access information for this user"""
        access_info = {
            "user": self.user,
            "company": self.company,
            "access_status": self.access_status,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "apps": [],
            "roles": []
        }
        
        for app_assignment in self.assigned_company_apps:
            if app_assignment.app_status == "Active":
                access_info["apps"].append({
                    "app": app_assignment.company_app,
                    "status": app_assignment.app_status
                })
        
        for role_assignment in self.company_roles:
            access_info["roles"].append({
                "role": role_assignment.role,
                "role_type": role_assignment.role_type,
                "permission_level": role_assignment.permission_level
            })
        
        return access_info

@frappe.whitelist()
def get_user_company_access(user):
    """Get company access for a user"""
    if not frappe.db.exists("DocType", "Company Access Control"):
        return None
    
    try:
        access = frappe.get_doc("Company Access Control", {"user": user})
        return access.get_user_access_info() if access else None
    except frappe.DoesNotExistError:
        return None
    except Exception as e:
        return None

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
    except frappe.DoesNotExistError:
        access = frappe.new_doc("Company Access Control")
        access.user = user
    except Exception as e:
        access = frappe.new_doc("Company Access Control")
        access.user = user
    
    access.company = company
    access.access_status = "Active"
    
    # Clear existing assignments
    access.assigned_company_apps = []
    access.company_roles = []
    
    # Assign apps
    if apps:
        if isinstance(apps, str):
            apps = frappe.parse_json(apps)
        for app in apps:
            access.append("assigned_company_apps", {
                "company_app": app,
                "app_status": "Active"
            })
    
    # Assign roles
    if roles:
        if isinstance(roles, str):
            roles = frappe.parse_json(roles)
        for role in roles:
            access.append("company_roles", {
                "role": role,
                "role_type": "Company User",
                "permission_level": "Limited Access"
            })
    
    access.save()
    return access.name

@frappe.whitelist()
def remove_company_access(user, company):
    """Remove company access from user"""
    if not frappe.has_permission("Company Access Control", "write"):
        frappe.throw(_("Permission denied"))
    
    try:
        access = frappe.get_doc("Company Access Control", {"user": user})
        if access.company == company:
            access.delete()
            return {"status": "success", "message": f"Access removed for user {user} from company {company}"}
        else:
            return {"status": "error", "message": f"User {user} is not assigned to company {company}"}
    except frappe.DoesNotExistError:
        return {"status": "error", "message": f"No access record found for user {user}"}

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
def get_user_access_summary(user=None):
    """Get summary of user access"""
    if not user:
        user = frappe.session.user
    
    access_info = get_user_company_access(user)
    if not access_info:
        return {
            "has_access": False,
            "company": None,
            "apps_count": 0,
            "roles_count": 0
        }
    
    return {
        "has_access": access_info["access_status"] == "Active",
        "company": access_info["company"],
        "apps_count": len(access_info["apps"]),
        "roles_count": len(access_info["roles"]),
        "valid_from": access_info["valid_from"],
        "valid_until": access_info["valid_until"]
    }

@frappe.whitelist()
def bulk_assign_company_access(users, company, apps=None, roles=None):
    """Bulk assign company access to multiple users"""
    if not frappe.has_permission("Company Access Control", "write"):
        frappe.throw(_("Permission denied"))
    
    if isinstance(users, str):
        users = frappe.parse_json(users)
    
    results = []
    for user in users:
        try:
            access_name = assign_company_to_user(user, company, apps, roles)
            results.append({"user": user, "status": "success", "access_name": access_name})
        except Exception as e:
            results.append({"user": user, "status": "error", "error": str(e)})
    
    return results

@frappe.whitelist()
def check_access_expiry():
    """Check and update expired access"""
    from frappe.utils import now_datetime

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
    
    results = []
    for access in expired_access:
        try:
            doc = frappe.get_doc("Company Access Control", access.name)
            doc.access_status = "Expired"
            doc.save()
            results.append({
                "user": access.user,
                "company": access.company,
                "status": "expired"
            })
        except Exception as e:
            results.append({
                "user": access.user,
                "company": access.company,
                "status": "error",
                "error": str(e)
            })
    
    return results

@frappe.whitelist()
def get_available_companies():
    """Get list of available companies"""
    companies = frappe.get_all(
        "Company",
        fields=["name", "company_name", "abbr"],
        order_by="company_name"
    )
    return companies

@frappe.whitelist()
def get_available_company_apps():
    """Get list of available company apps"""
    if not frappe.db.exists("DocType", "Company App"):
        return []
    
    apps = frappe.get_all(
        "Company App",
        filters={"app_status": "Active"},
        fields=["name", "app_title", "app_description"],
        order_by="app_title"
    )
    return apps