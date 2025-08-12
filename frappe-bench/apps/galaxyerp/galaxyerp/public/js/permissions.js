// GalaxyERP Company Access Control - Client Side Logic

frappe.provide('galaxyerp.permissions');

galaxyerp.permissions = {
    user_access: null,
    company_apps: [],
    is_admin: false,
    
    init: function() {
        this.load_user_access();
        this.setup_workspace_restrictions();
        this.setup_company_access_ui();
    },
    
    load_user_access: function() {
        // Get user access from server
        frappe.call({
            method: 'galaxyerp.utils.company_access.get_user_company_access',
            args: { user: frappe.session.user },
            callback: (r) => {
                this.user_access = r.message;
                this.company_apps = this.user_access.apps || [];
                this.is_admin = this.user_access.is_admin || false;
                
                // Store in frappe.boot for global access
                frappe.boot.user.company_access = this.user_access;
                
                // Apply restrictions after loading
                this.apply_workspace_restrictions();
                this.apply_company_access_restrictions();
            }
        });
    },
    
    setup_workspace_restrictions: function() {
        // Override workspace page load to apply restrictions
        const original_workspace_load = frappe.pages['workspace'];
        if (original_workspace_load && original_workspace_load.on_page_load) {
            const original_on_load = original_workspace_load.on_page_load;
            frappe.pages['workspace'].on_page_load = function(wrapper) {
                original_on_load(wrapper);
                galaxyerp.permissions.apply_workspace_restrictions();
            };
        }
        
        // Override workspace sidebar loading
        const original_get_sidebar = frappe.workspace.get_workspace_sidebar_items;
        if (original_get_sidebar) {
            frappe.workspace.get_workspace_sidebar_items = function() {
                const items = original_get_sidebar();
                return galaxyerp.permissions.filter_workspace_items(items);
            };
        }
    },
    
    apply_workspace_restrictions: function() {
        if (!this.user_access || !this.user_access.has_access) {
            // Hide all company-specific workspaces
            $('.workspace-company-specific, [data-company-app]').hide();
            $('.workspace-card[data-module*="company"]').hide();
            
            // Show only core workspaces
            $('.workspace-card').each(function() {
                const module = $(this).data('module');
                const is_core = ['Setup', 'Tools', 'Integrations', 'Settings'].includes(module);
                if (!is_core) {
                    $(this).hide();
                }
            });
        } else {
            // Show only workspaces for assigned company apps
            $('.workspace-card, .workspace-company-specific, [data-company-app]').each(function() {
                const $element = $(this);
                const app = $element.data('company-app') || $element.data('app');
                const module = $element.data('module');
                
                // Always show core modules
                const is_core = ['Setup', 'Tools', 'Integrations', 'Settings'].includes(module);
                if (is_core) {
                    $element.show();
                    return;
                }
                
                // Show only if user has access to this company app
                if (app && this.company_apps.includes(app)) {
                    $element.show();
                } else {
                    $element.hide();
                }
            });
        }
    },
    
    filter_workspace_items: function(items) {
        if (!this.user_access || !this.user_access.has_access) {
            // Return only core items
            return items.filter(item => {
                const module = item.module;
                return ['Setup', 'Tools', 'Integrations', 'Settings'].includes(module);
            });
        }
        
        // Filter based on user's company apps
        return items.filter(item => {
            const module = item.module;
            const app = item.app || item.company_app;
            
            // Always include core modules
            const is_core = ['Setup', 'Tools', 'Integrations', 'Settings'].includes(module);
            if (is_core) return true;
            
            // Include only if user has access to this company app
            if (app && this.company_apps.includes(app)) {
                return true;
            }
            
            return false;
        });
    },
    
    setup_company_access_ui: function() {
        // Add company access indicator to header
        this.add_company_access_indicator();
        
        // Override user menu to show company info
        this.override_user_menu();
        
        // Add company switcher if user has multiple companies
        this.add_company_switcher();
    },
    
    add_company_access_indicator: function() {
        if (!this.user_access || !this.user_access.has_access) return;
        
        const indicator = $(`
            <div class="company-access-indicator" style="
                position: fixed;
                top: 60px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <i class="fa fa-building"></i> ${this.user_access.company}
            </div>
        `);
        
        $('body').append(indicator);
    },
    
    override_user_menu: function() {
        // Add company info to user menu
        const user_menu = $('.navbar .dropdown-menu');
        if (user_menu.length && this.user_access && this.user_access.has_access) {
            const company_info = $(`
                <li class="dropdown-header">
                    <i class="fa fa-building"></i> Company: ${this.user_access.company}
                </li>
                <li class="divider"></li>
            `);
            user_menu.prepend(company_info);
        }
    },
    
    add_company_switcher: function() {
        // This would be implemented if user has access to multiple companies
        // For now, we'll keep it simple with single company access
    },
    
    apply_company_access_restrictions: function() {
        // Hide company-specific elements based on access
        if (!this.user_access || !this.user_access.has_access) {
            $('[data-company-specific]').hide();
            $('.company-specific-feature').hide();
        } else {
            // Show only elements for user's company
            $('[data-company-specific]').each(function() {
                const $element = $(this);
                const company = $element.data('company');
                if (company === this.user_access.company) {
                    $element.show();
                } else {
                    $element.hide();
                }
            });
        }
    },
    
    // Utility functions
    has_company_access: function(company) {
        if (!this.user_access || !this.user_access.has_access) return false;
        return this.user_access.company === company;
    },
    
    has_app_access: function(app) {
        if (!this.user_access || !this.user_access.has_access) return false;
        return this.company_apps.includes(app);
    },
    
    is_company_admin: function() {
        return this.is_admin;
    }
};

// Initialize when page loads
$(document).ready(function() {
    galaxyerp.permissions.init();
});

// Override frappe workspace loading
frappe.pages['workspace'] = frappe.pages['workspace'] || {};
frappe.pages['workspace'].on_page_load = function(wrapper) {
    // Apply workspace restrictions
    galaxyerp.permissions.apply_workspace_restrictions();
};

// Override desk page loading
frappe.pages['desk'] = frappe.pages['desk'] || {};
frappe.pages['desk'].on_page_load = function(wrapper) {
    // Apply company access restrictions
    galaxyerp.permissions.apply_company_access_restrictions();
}; 