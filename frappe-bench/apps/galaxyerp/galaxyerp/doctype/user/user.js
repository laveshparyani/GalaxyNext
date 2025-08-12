frappe.provide('galaxyerp.user');

galaxyerp.user = {
    init: function() {
        this.setup_company_access_section();
        this.bind_events();
    },
    
    setup_company_access_section: function() {
        // Add company access section to user form
        if (frappe.model.has_perm('Company Access Control', 'write')) {
            this.add_company_access_section();
        }
    },
    
    add_company_access_section: function() {
        const company_section = $(`
            <div class="form-section">
                <div class="section-head">
                    <h3>Company Access Control</h3>
                </div>
                <div class="section-body">
                    <div class="row">
                        <div class="col-sm-6">
                            <div class="form-group">
                                <label>Company</label>
                                <select class="form-control" id="company_select">
                                    <option value="">Select Company</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-6">
                            <div class="form-group">
                                <label>Access Status</label>
                                <select class="form-control" id="access_status">
                                    <option value="Active">Active</option>
                                    <option value="Inactive">Inactive</option>
                                    <option value="Suspended">Suspended</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-12">
                            <div class="form-group">
                                <label>Assigned Apps</label>
                                <div id="assigned_apps"></div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-12">
                            <button class="btn btn-primary" id="save_company_access">
                                Save Company Access
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        $('.form-dashboard').append(company_section);
        this.load_companies();
    },
    
    load_companies: function() {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Company',
                fields: ['name', 'company_name']
            },
            callback: (r) => {
                const select = $('#company_select');
                r.message.forEach(company => {
                    select.append(`<option value="${company.name}">${company.company_name}</option>`);
                });
            }
        });
    },
    
    bind_events: function() {
        $('#company_select').on('change', () => {
            this.load_company_apps();
        });
        
        $('#save_company_access').on('click', () => {
            this.save_company_access();
        });
    },
    
    load_company_apps: function() {
        const company = $('#company_select').val();
        if (!company) return;
        
        frappe.call({
            method: 'galaxyerp.utils.company_access.get_company_apps',
            args: { company: company },
            callback: (r) => {
                this.render_assigned_apps(r.message);
            }
        });
    },
    
    render_assigned_apps: function(apps) {
        const container = $('#assigned_apps');
        container.empty();
        
        apps.forEach(app => {
            const app_html = $(`
                <div class="checkbox">
                    <label>
                        <input type="checkbox" value="${app.name}" ${app.assigned ? 'checked' : ''}>
                        ${app.app_title}
                    </label>
                </div>
            `);
            container.append(app_html);
        });
    },
    
    save_company_access: function() {
        const user = cur_frm.doc.name;
        const company = $('#company_select').val();
        const status = $('#access_status').val();
        const apps = [];
        
        $('#assigned_apps input:checked').each(function() {
            apps.push($(this).val());
        });
        
        frappe.call({
            method: 'galaxyerp.doctype.company_access_control.company_access_control.assign_company_to_user',
            args: {
                user: user,
                company: company,
                apps: apps
            },
            callback: (r) => {
                frappe.show_alert('Company access updated successfully');
            }
        });
    }
};

// Initialize when user form loads
$(document).ready(function() {
    if (cur_frm && cur_frm.doctype === 'User') {
        galaxyerp.user.init();
    }
});