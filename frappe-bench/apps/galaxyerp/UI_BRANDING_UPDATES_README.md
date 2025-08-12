# GalaxyERP UI & Branding Updates

This document outlines the comprehensive UI and branding updates implemented in the `galaxyerp` custom app to replace ERPNext/Frappe branding with GalaxyNext branding across the entire system.

## 🎯 **Overview**

The `galaxyerp` app provides a clean, modular approach to override all branding elements without modifying core ERPNext or Frappe files. This ensures easy reversion to default configuration by simply disabling or removing the custom app.

## 📋 **Implemented Changes**

### 1. **Login Page Functionality & Design** ✅
- **File**: `galaxyerp/www/login.html`
- **Changes**:
  - ✅ **Login with Email Link**: Added "Login with Email Link" button with full functionality
  - ✅ **Preserved UX**: Maintained original ERPNext login page UX flow and styling
  - ✅ **Branding**: Updated branding from "GalaxyERP" to "GalaxyNext"
  - ✅ **Functionality**: Maintained all original functionality including social login, LDAP, etc.
  - ✅ **Configuration**: Enabled via `website_context.login_with_email_link = True`

### 2. **Onboarding Cards Branding** ✅
- **Files**: 
  - `galaxyerp/public/js/galaxyerp.js` (client-side)
  - `galaxyerp/utils/onboarding_branding.py` (server-side utilities)
  - `galaxyerp/utils/onboarding_override.py` (server-side overrides)
  - `galaxyerp/utils/onboarding_methods.py` (method overrides)
  - `galaxyerp/utils/onboarding_widget_override.py` (widget overrides)
- **Changes**:
  - ✅ **Dynamic Replacement**: "ERPNext" → "GalaxyNext" in all onboarding content
  - ✅ **Server-Side Overrides**: Method overrides for `get_module_onboarding` and `get_onboarding_step`
  - ✅ **Widget Overrides**: Custom widget data processing
  - ✅ **Content Preservation**: Original structure and logic maintained
  - ✅ **Specific Targeting**: Home module onboarding specifically handled

### 3. **Help → About Section Customization** ✅
- **File**: `galaxyerp/public/js/frappe/ui/toolbar/about.js`
- **Changes**:
  - ✅ **Title**: "Frappe Framework" → "GalaxyNext Framework"
  - ✅ **Links Updated**:
    - Website: `https://galaxyerpsoftware.com`
    - Source: `https://github.com/GalaxyERPSoftware/GalaxyNext`
    - Documentation: `https://docs.galaxyerpsoftware.com`
    - LinkedIn: `https://www.linkedin.com/company/galaxy-erp-software-private-limited`
    - Instagram: `https://www.instagram.com/galaxyerpsoftwarepvtltd`
  - ✅ **Commented Out**: Frappe School, Twitter, and YouTube entries
  - ✅ **Installed Apps**: ERPNext → GalaxyNext in the apps list
  - ✅ **Copyright**: "© GalaxyERP Software Pvt. Ltd. and contributors"

### 4. **Translation Overrides** ✅
- **File**: `galaxyerp/translations/en.csv`
- **Changes**:
  - ✅ **Hardcoded Strings**: Override all translatable strings containing "ERPNext"
  - ✅ **Comprehensive Coverage**: Login, onboarding, about modal, and general UI text
  - ✅ **Case Handling**: Both "ERPNext" and "erpnext" variations covered

## 🔧 **Technical Implementation**

### **Method Overrides** (`hooks.py`)
```python
override_whitelisted_methods = {
    "frappe.email.email_body.get_brand_logo": "galaxyerp.utils.email_branding.get_brand_logo",
    "frappe.core.doctype.navbar_settings.navbar_settings.get_app_logo": "galaxyerp.utils.app_logo.get_app_logo",
    "frappe.desk.page.setup_wizard.setup_wizard.get_module_onboarding": "galaxyerp.utils.onboarding_methods.get_module_onboarding",
    "frappe.desk.page.setup_wizard.setup_wizard.get_onboarding_step": "galaxyerp.utils.onboarding_methods.get_onboarding_step",
    "frappe.widgets.onboarding_widget.get_onboarding_data": "galaxyerp.utils.onboarding_widget_override.get_onboarding_widget_data_override",
    "frappe.widgets.onboarding_widget.get_step_data": "galaxyerp.utils.onboarding_widget_override.override_onboarding_step_data"
}
```

### **Website Context** (`hooks.py`)
```python
website_context = {
    "favicon": "/assets/galaxyerp/images/galaxynext_logo.png",
    "splash_image": "/assets/galaxyerp/images/galaxynext_logo.png",
    "app_logo_url": "/assets/galaxyerp/images/galaxynext_logo.png",
    "brand_logo": "/assets/galaxyerp/images/galaxynext_logo.png",
    "footer_logo": "/assets/galaxyerp/images/galaxynext_logo.png",
    "login_with_email_link": True  # Enable login with email link functionality
}
```

### **Asset Inclusion** (`hooks.py`)
```python
app_include_js = [
    "/assets/galaxyerp/js/galaxyerp.js",
    "/assets/galaxyerp/js/frappe/ui/toolbar/about.js"
]
```

## 📁 **File Structure**

```
galaxyerp/
├── hooks.py                                    # Main configuration and overrides
├── www/
│   └── login.html                             # Login page override with email link
├── public/
│   ├── js/
│   │   ├── galaxyerp.js                       # Main branding JavaScript
│   │   └── frappe/ui/toolbar/about.js         # About modal override
│   ├── css/
│   │   └── galaxyerp.css                      # Custom styling
│   └── images/
│       └── galaxynext_logo.png                # GalaxyNext logo
├── templates/
│   ├── includes/
│   │   ├── splash_screen.html                 # Splash screen override
│   │   └── footer/footer_logo_extension.html  # Footer logo override
│   └── emails/
│       └── standard.html                      # Email template override
├── translations/
│   └── en.csv                                 # Translation overrides
└── utils/
    ├── app_logo.py                            # App logo override
    ├── email_branding.py                      # Email branding override
    ├── onboarding_branding.py                 # Onboarding utilities
    ├── onboarding_override.py                 # Server-side overrides
    ├── onboarding_methods.py                  # Method overrides
    └── onboarding_widget_override.py          # Widget overrides
```

## 🚀 **Installation & Usage**

### **Prerequisites**
- GalaxyNext logo file must be present at: `/assets/galaxyerp/images/galaxynext_logo.png`

### **Activation**
1. Ensure the `galaxyerp` app is installed and enabled
2. Run: `bench build`
3. Run: `bench clear-cache`
4. Run: `bench restart`

### **Verification**
1. **Login Page**: Visit `/login` - should show:
   - ✅ GalaxyNext logo
   - ✅ "Login with Email Link" button (functional)
   - ✅ "Login to GalaxyNext" branding
2. **Home Page**: Onboarding cards should display:
   - ✅ "Let's begin your journey with GalaxyNext"
   - ✅ All descriptions with "GalaxyNext" instead of "ERPNext"
3. **About Modal**: Help → About should show:
   - ✅ "GalaxyNext Framework" title
   - ✅ Updated links and company information
4. **All Pages**: GalaxyNext logo should appear in navbar, favicon, and footer

### **Reversion**
To revert to default ERPNext/Frappe branding:
1. Disable the `galaxyerp` app: `bench --site [site] disable-app galaxyerp`
2. Or remove the app entirely
3. Run: `bench build && bench clear-cache && bench restart`

## 🎨 **Branding Elements Covered**

### **Logos & Icons**
- ✅ Application logo in navbar
- ✅ Login page logo
- ✅ Splash screen logo
- ✅ Email template logos
- ✅ Footer logo
- ✅ Favicon

### **Text Content**
- ✅ Login page titles and branding
- ✅ Onboarding card text (comprehensive)
- ✅ About modal content
- ✅ Page titles and headings
- ✅ Dynamic content loaded via JavaScript
- ✅ Server-side content via method overrides

### **Links & References**
- ✅ About modal links
- ✅ Documentation links
- ✅ Social media links
- ✅ Company information

### **Functionality**
- ✅ Login with Email Link (fully functional)
- ✅ Onboarding widget data processing
- ✅ Translation overrides
- ✅ Method overrides for content replacement

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Login with Email Link Not Appearing**
   - Verify `login_with_email_link: True` in `website_context`
   - Check browser console for JavaScript errors
   - Clear browser cache

2. **Onboarding Content Not Updating**
   - Ensure method overrides are properly configured in `hooks.py`
   - Run `bench clear-cache` and `bench restart`
   - Check server logs for method override errors

3. **Logo Not Appearing**
   - Verify logo file exists at correct path
   - Check file permissions
   - Clear browser cache

4. **Branding Not Updating**
   - Ensure `galaxyerp` app is enabled
   - Run `bench build` and `bench clear-cache`
   - Check browser console for JavaScript errors

### **Debug Mode**
Enable debug mode to see detailed information:
```python
# In site_config.json
"debug": 1
```

## 📝 **Future Enhancements**

The modular design allows for easy extension:

1. **Additional Branding Elements**: Add more logo contexts or text replacements
2. **Custom Themes**: Extend CSS for custom color schemes
3. **Localization**: Add support for multiple languages
4. **Configuration**: Make branding elements configurable via UI
5. **Additional Modules**: Extend onboarding overrides to other modules

## 🤝 **Support**

For issues or questions regarding the GalaxyERP branding implementation:
- Check the troubleshooting section above
- Review the file structure and configuration
- Ensure all prerequisites are met
- Verify method overrides are working correctly

---

**Note**: This implementation maintains full compatibility with ERPNext/Frappe updates while providing complete branding customization through the modular `galaxyerp` app approach. All changes are reversible and non-destructive to the core system. 