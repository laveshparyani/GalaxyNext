# GalaxyERP Logo Override Implementation

This document describes the comprehensive logo override implementation in the `galaxyerp` custom app that replaces all instances of the default Frappe/ERPNext logos with the custom GalaxyNext logo.

## Overview

The implementation uses a clean, non-intrusive approach by creating a custom app (`galaxyerp`) that overrides all logo-related assets and templates without modifying the core Frappe or ERPNext files. This ensures that the changes can be easily reverted by simply disabling or removing the custom app.

## Logo File Location

The GalaxyNext logo is stored at:
```
frappe-bench/apps/galaxyerp/galaxyerp/public/images/galaxynext_logo.png
```

## Implementation Components

### 1. Hooks Configuration (`hooks.py`)

The main configuration file that defines all logo overrides:

- **app_logo_url**: Overrides the main application logo
- **website_context**: Provides logo URLs for various contexts (favicon, splash_image, brand_logo, footer_logo)
- **email_brand_logo**: Overrides email branding logo
- **favicon**: Overrides favicon across all contexts
- **override_whitelisted_methods**: Overrides core functions to return GalaxyNext logo
- **app_include_css/js**: Includes custom CSS and JavaScript for logo styling and dynamic replacement

### 2. Template Overrides

#### Core Templates
- **`templates/base.html`**: Overrides favicon in base template
- **`templates/emails/standard.html`**: Overrides email branding logo
- **`templates/includes/splash_screen.html`**: Overrides splash screen logo
- **`templates/includes/footer/footer_logo_extension.html`**: Overrides footer logo

#### Page Templates
- **`www/login.html`**: Overrides login page logo
- **`www/app.html`**: Overrides app interface favicon
- **`www/apps.html`**: Overrides apps page logos
- **`www/update-password.html`**: Overrides password update page logo

#### JavaScript Templates
- **`public/js/frappe/ui/toolbar/navbar.html`**: Overrides navbar logo

### 3. Python Method Overrides

#### `utils/email_branding.py`
Overrides the `get_brand_logo()` function to return GalaxyNext logo for emails.

#### `utils/app_logo.py`
Overrides the `get_app_logo()` function to return GalaxyNext logo for all app contexts.

### 4. Asset Files

#### CSS (`public/css/galaxyerp.css`)
Provides consistent styling for the GalaxyNext logo across all contexts:
- App logo styling
- Navbar logo styling
- Login page logo styling
- Splash screen logo styling
- Email logo styling
- Footer logo styling
- Apps page logo styling

#### JavaScript (`public/js/galaxyerp.js`)
Provides dynamic logo replacement:
- Overrides logos in navbar, login page, apps page
- Updates favicon dynamically
- Overrides splash screen and footer logos
- Ensures logo replacement when DOM changes
- Overrides boot.app_logo_url

## Logo Contexts Covered

1. **Application Logo**: Main app logo in navbar and headers
2. **Login Page**: Logo displayed on login/signup pages
3. **Splash Screen**: Loading screen logo
4. **Favicon**: Browser tab and bookmark icon
5. **Email Branding**: Logo in email templates
6. **Footer Logo**: Logo in website footer
7. **Apps Page**: Logo on the apps selection page
8. **Password Update**: Logo on password update page

## Installation and Usage

### Prerequisites
- GalaxyNext logo file must be present at the specified location
- Custom app `galaxyerp` must be installed on the site

### Installation Steps
1. Ensure the logo file is in place
2. Install the custom app: `bench --site <site-name> install-app galaxyerp`
3. Build assets: `bench build`
4. Clear cache: `bench clear-cache`
5. Restart the server: `bench restart`

### Verification
After installation, verify that the GalaxyNext logo appears in:
- Login page
- Application navbar
- Browser favicon
- Email templates
- Splash screen
- Apps page
- Footer (if enabled)

## Reverting Changes

To revert to default logos:
1. Uninstall the custom app: `bench --site <site-name> uninstall-app galaxyerp`
2. Build assets: `bench build`
3. Clear cache: `bench clear-cache`
4. Restart the server: `bench restart`

## Technical Details

### Hook Priority
The custom app uses Frappe's hook system to override logo-related configurations. The app's hooks are processed after core Frappe hooks, ensuring that custom configurations take precedence.

### Template Override Mechanism
Frappe's template override system allows the custom app to provide alternative templates that replace the default ones without modifying core files.

### Method Override Mechanism
The `override_whitelisted_methods` hook allows the custom app to replace core functions with custom implementations that return the GalaxyNext logo.

### Asset Management
Custom CSS and JavaScript files are automatically included in all pages through the `app_include_css` and `app_include_js` hooks.

## Maintenance

### Adding New Logo Contexts
To add logo overrides for new contexts:
1. Add the logo URL to `website_context` in `hooks.py`
2. Create template overrides if needed
3. Add CSS styling in `galaxyerp.css`
4. Add JavaScript replacement in `galaxyerp.js`

### Updating the Logo
To update the logo:
1. Replace the logo file at `public/images/galaxynext_logo.png`
2. Build assets: `bench build`
3. Clear cache: `bench clear-cache`

### Troubleshooting
If logos don't appear correctly:
1. Check file permissions on the logo file
2. Verify the logo file path in all templates
3. Clear browser cache
4. Check browser developer tools for 404 errors
5. Verify that the custom app is properly installed

## Security Considerations

- The custom app only overrides logo-related assets and does not modify core functionality
- All overrides are done through Frappe's official hook and template systems
- No core files are modified, ensuring system integrity
- The implementation is fully reversible

## Performance Impact

- Minimal performance impact as only logo assets are overridden
- CSS and JavaScript files are optimized and minified during build
- Logo file is cached by browsers for optimal loading
- No additional database queries or server-side processing required 