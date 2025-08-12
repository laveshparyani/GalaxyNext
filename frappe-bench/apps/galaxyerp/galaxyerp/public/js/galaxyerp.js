// GalaxyERP Custom JavaScript

// Function to replace logos with GalaxyNext logo
function replaceLogos() {
	$('.navbar-brand .app-logo, .app-logo').each(function() {
		if ($(this).attr('src') && !$(this).attr('src').includes('galaxynext_logo')) {
			$(this).attr('src', '/assets/galaxyerp/images/galaxynext_logo.png');
		}
	});
	$('link[rel="shortcut icon"], link[rel="icon"]').each(function() {
		if ($(this).attr('href') && !$(this).attr('href').includes('galaxynext_logo')) {
			$(this).attr('href', '/assets/galaxyerp/images/galaxynext_logo.png');
		}
	});
	$('.splash img').each(function() {
		if ($(this).attr('src') && !$(this).attr('src').includes('galaxynext_logo')) {
			$(this).attr('src', '/assets/galaxyerp/images/galaxynext_logo.png');
		}
	});
	$('.footer-logo img').each(function() {
		if ($(this).attr('src') && !$(this).attr('src').includes('galaxynext_logo')) {
			$(this).attr('src', '/assets/galaxyerp/images/galaxynext_logo.png');
		}
	});
	$('img[src*="frappe-framework-logo"], img[src*="erpnext-logo"], img[src*="frappe-favicon"]').each(function() {
		$(this).attr('src', '/assets/galaxyerp/images/galaxynext_logo.png');
	});
}

function replaceBranding() {
	// Replace text content in headings and titles
	$('h1, h2, h3, h4, h5, h6, .page-title, .card-title, .onboarding-title, .widget-title').each(function() {
		var $element = $(this);
		var text = $element.text();
		if (text && text.includes('ERPNext')) {
			text = text.replace(/erpnext/gi, 'GalaxyNext');
			text = text.replace(/ERPNext/g, 'GalaxyNext');
			$element.text(text);
		}
	});
	
	// Replace onboarding content specifically
	$('.onboarding-card, .onboarding-section, [data-onboarding], .module-onboarding').each(function() {
		var $element = $(this);
		var html = $element.html();
		if (html && html.includes('ERPNext')) {
			html = html.replace(/erpnext/gi, 'GalaxyNext');
			html = html.replace(/ERPNext/g, 'GalaxyNext');
			$element.html(html);
		}
	});
	
	// Replace onboarding widget content
	$('.onboarding-widget, .module-onboarding-widget').each(function() {
		var $widget = $(this);
		$widget.find('.onboarding-title, .widget-title, .onboarding-subtitle, .widget-subtitle, .onboarding-description, .widget-description, .onboarding-success, .widget-success').each(function() {
			var $element = $(this);
			var text = $element.text();
			if (text && text.includes('ERPNext')) {
				text = text.replace(/erpnext/gi, 'GalaxyNext');
				text = text.replace(/ERPNext/g, 'GalaxyNext');
				$element.text(text);
			}
		});
	});
	
	// Replace specific onboarding step content
	$('.onboarding-step, .step-content, .step-description').each(function() {
		var $element = $(this);
		var html = $element.html();
		if (html && html.includes('ERPNext')) {
			// Replace the specific problematic text
			html = html.replace(/Items are integral to everything you do in ERPNext/gi, 'Items are integral to everything you do in GalaxyNext');
			html = html.replace(/ERPNext sets up a simple chart of accounts/gi, 'GalaxyNext sets up a simple chart of accounts');
			html = html.replace(/ERPNext is optimized for itemized management/gi, 'GalaxyNext is optimized for itemized management');
			html = html.replace(/Completing the Item Master is very essential for the successful implementation of ERPNext/gi, 'Completing the Item Master is very essential for the successful implementation of GalaxyNext');
			html = html.replace(/In ERPNext, you can maintain a Warehouse in the tree structure/gi, 'In GalaxyNext, you can maintain a Warehouse in the tree structure');
			html = html.replace(/Let's begin your journey with ERPNext/gi, 'Let\'s begin your journey with GalaxyNext');
			html = html.replace(/You're ready to start your journey with ERPNext/gi, 'You\'re ready to start your journey with GalaxyNext');
			html = html.replace(/Welcome to ERPNext/gi, 'Welcome to GalaxyNext');
			html = html.replace(/Login to ERPNext/gi, 'Login to GalaxyNext');
			html = html.replace(/Create a ERPNext Account/gi, 'Create a GalaxyNext Account');
			html = html.replace(/ERPNext Setup/gi, 'GalaxyNext Setup');
			html = html.replace(/ERPNext Setup Complete/gi, 'GalaxyNext Setup Complete');
			html = html.replace(/ERPNext is ready to use/gi, 'GalaxyNext is ready to use');
			html = html.replace(/Your ERPNext instance is now ready/gi, 'Your GalaxyNext instance is now ready');
			html = html.replace(/ERPNext Dashboard/gi, 'GalaxyNext Dashboard');
			html = html.replace(/ERPNext Workspace/gi, 'GalaxyNext Workspace');
			html = html.replace(/ERPNext Modules/gi, 'GalaxyNext Modules');
			html = html.replace(/ERPNext Features/gi, 'GalaxyNext Features');
			html = html.replace(/ERPNext Documentation/gi, 'GalaxyNext Documentation');
			html = html.replace(/ERPNext Community/gi, 'GalaxyNext Community');
			html = html.replace(/ERPNext Support/gi, 'GalaxyNext Support');
			html = html.replace(/ERPNext Training/gi, 'GalaxyNext Training');
			html = html.replace(/ERPNext Certification/gi, 'GalaxyNext Certification');
			html = html.replace(/ERPNext Partner/gi, 'GalaxyNext Partner');
			html = html.replace(/ERPNext Developer/gi, 'GalaxyNext Developer');
			html = html.replace(/ERPNext Consultant/gi, 'GalaxyNext Consultant');
			html = html.replace(/ERPNext Implementation/gi, 'GalaxyNext Implementation');
			html = html.replace(/ERPNext Migration/gi, 'GalaxyNext Migration');
			html = html.replace(/ERPNext Customization/gi, 'GalaxyNext Customization');
			html = html.replace(/ERPNext Integration/gi, 'GalaxyNext Integration');
			html = html.replace(/ERPNext API/gi, 'GalaxyNext API');
			html = html.replace(/ERPNext REST API/gi, 'GalaxyNext REST API');
			html = html.replace(/ERPNext Webhook/gi, 'GalaxyNext Webhook');
			html = html.replace(/ERPNext Workflow/gi, 'GalaxyNext Workflow');
			html = html.replace(/ERPNext Report/gi, 'GalaxyNext Report');
			html = html.replace(/ERPNext Print Format/gi, 'GalaxyNext Print Format');
			html = html.replace(/ERPNext Letter Head/gi, 'GalaxyNext Letter Head');
			html = html.replace(/ERPNext Print Style/gi, 'GalaxyNext Print Style');
			html = html.replace(/ERPNext Email Template/gi, 'GalaxyNext Email Template');
			html = html.replace(/ERPNext Notification/gi, 'GalaxyNext Notification');
			html = html.replace(/ERPNext Calendar/gi, 'GalaxyNext Calendar');
			html = html.replace(/ERPNext Task/gi, 'GalaxyNext Task');
			html = html.replace(/ERPNext Project/gi, 'GalaxyNext Project');
			html = html.replace(/ERPNext Issue/gi, 'GalaxyNext Issue');
			html = html.replace(/ERPNext Timesheet/gi, 'GalaxyNext Timesheet');
			html = html.replace(/ERPNext Activity/gi, 'GalaxyNext Activity');
			html = html.replace(/ERPNext Event/gi, 'GalaxyNext Event');
			html = html.replace(/ERPNext Meeting/gi, 'GalaxyNext Meeting');
			html = html.replace(/ERPNext Contact/gi, 'GalaxyNext Contact');
			html = html.replace(/ERPNext Address/gi, 'GalaxyNext Address');
			html = html.replace(/ERPNext Lead/gi, 'GalaxyNext Lead');
			html = html.replace(/ERPNext Opportunity/gi, 'GalaxyNext Opportunity');
			html = html.replace(/ERPNext Quotation/gi, 'GalaxyNext Quotation');
			html = html.replace(/ERPNext Sales Order/gi, 'GalaxyNext Sales Order');
			html = html.replace(/ERPNext Delivery Note/gi, 'GalaxyNext Delivery Note');
			html = html.replace(/ERPNext Sales Invoice/gi, 'GalaxyNext Sales Invoice');
			html = html.replace(/ERPNext Payment Entry/gi, 'GalaxyNext Payment Entry');
			html = html.replace(/ERPNext Journal Entry/gi, 'GalaxyNext Journal Entry');
			html = html.replace(/ERPNext Purchase Order/gi, 'GalaxyNext Purchase Order');
			html = html.replace(/ERPNext Purchase Receipt/gi, 'GalaxyNext Purchase Receipt');
			html = html.replace(/ERPNext Purchase Invoice/gi, 'GalaxyNext Purchase Invoice');
			html = html.replace(/ERPNext Stock Entry/gi, 'GalaxyNext Stock Entry');
			html = html.replace(/ERPNext Material Request/gi, 'GalaxyNext Material Request');
			html = html.replace(/ERPNext Request for Quotation/gi, 'GalaxyNext Request for Quotation');
			html = html.replace(/ERPNext Supplier Quotation/gi, 'GalaxyNext Supplier Quotation');
			html = html.replace(/ERPNext BOM/gi, 'GalaxyNext BOM');
			html = html.replace(/ERPNext Work Order/gi, 'GalaxyNext Work Order');
			html = html.replace(/ERPNext Job Card/gi, 'GalaxyNext Job Card');
			html = html.replace(/ERPNext Maintenance Schedule/gi, 'GalaxyNext Maintenance Schedule');
			html = html.replace(/ERPNext Maintenance Visit/gi, 'GalaxyNext Maintenance Visit');
			html = html.replace(/ERPNext Asset/gi, 'GalaxyNext Asset');
			html = html.replace(/ERPNext Asset Category/gi, 'GalaxyNext Asset Category');
			html = html.replace(/ERPNext Asset Movement/gi, 'GalaxyNext Asset Movement');
			html = html.replace(/ERPNext Asset Value Adjustment/gi, 'GalaxyNext Asset Value Adjustment');
			html = html.replace(/ERPNext Asset Depreciation Schedule/gi, 'GalaxyNext Asset Depreciation Schedule');
			html = html.replace(/ERPNext Asset Maintenance/gi, 'GalaxyNext Asset Maintenance');
			html = html.replace(/ERPNext Asset Maintenance Log/gi, 'GalaxyNext Asset Maintenance Log');
			html = html.replace(/ERPNext Asset Maintenance Team/gi, 'GalaxyNext Asset Maintenance Team');
			html = html.replace(/ERPNext Asset Maintenance Task/gi, 'GalaxyNext Asset Maintenance Task');
			html = html.replace(/ERPNext Asset Maintenance Schedule/gi, 'GalaxyNext Asset Maintenance Schedule');
			html = html.replace(/ERPNext Asset Maintenance Visit/gi, 'GalaxyNext Asset Maintenance Visit');
			html = html.replace(/ERPNext Asset Maintenance Schedule Template/gi, 'GalaxyNext Asset Maintenance Schedule Template');
			html = html.replace(/ERPNext Asset Maintenance Visit Template/gi, 'GalaxyNext Asset Maintenance Visit Template');
			html = html.replace(/ERPNext Asset Maintenance Task Template/gi, 'GalaxyNext Asset Maintenance Task Template');
			html = html.replace(/ERPNext Asset Maintenance Team Template/gi, 'GalaxyNext Asset Maintenance Team Template');
			html = html.replace(/ERPNext Asset Maintenance Log Template/gi, 'GalaxyNext Asset Maintenance Log Template');
			$element.html(html);
		}
	});
	
	// Replace text in all text nodes that contain ERPNext
	$('*').contents().filter(function() {
		return this.nodeType === 3; // Text nodes only
	}).each(function() {
		if (this.textContent && this.textContent.includes('ERPNext')) {
			this.textContent = this.textContent.replace(/erpnext/gi, 'GalaxyNext');
			this.textContent = this.textContent.replace(/ERPNext/g, 'GalaxyNext');
		}
	});
}

function replaceOnboardingWidget() {
	$('.onboarding-widget, .module-onboarding-widget').each(function() {
		var $widget = $(this);
		$widget.find('.onboarding-title, .widget-title').each(function() {
			var $title = $(this);
			var text = $title.text();
			if (text && text.includes('ERPNext')) {
				text = text.replace(/erpnext/gi, 'GalaxyNext');
				text = text.replace(/ERPNext/g, 'GalaxyNext');
				$title.text(text);
			}
		});
		$widget.find('.onboarding-subtitle, .widget-subtitle').each(function() {
			var $subtitle = $(this);
			var text = $subtitle.text();
			if (text && text.includes('ERPNext')) {
				text = text.replace(/erpnext/gi, 'GalaxyNext');
				text = text.replace(/ERPNext/g, 'GalaxyNext');
				$subtitle.text(text);
			}
		});
		$widget.find('.onboarding-description, .widget-description').each(function() {
			var $desc = $(this);
			var html = $desc.html();
			if (html && html.includes('ERPNext')) {
				html = html.replace(/erpnext/gi, 'GalaxyNext');
				html = html.replace(/ERPNext/g, 'GalaxyNext');
				$desc.html(html);
			}
		});
		$widget.find('.onboarding-success, .widget-success').each(function() {
			var $success = $(this);
			var text = $success.text();
			if (text && text.includes('ERPNext')) {
				text = text.replace(/erpnext/gi, 'GalaxyNext');
				text = text.replace(/ERPNext/g, 'GalaxyNext');
				$success.text(text);
			}
		});
	});
}

// ========================================
// WORKSPACE LAYOUT RESTORATION FUNCTIONS
// ========================================

function restoreWorkspaceLayout() {
	// Ensure proper layout structure
	var $mainWrapper = $('.layout-main-section-wrapper');
	var $sidebar = $('.layout-side-section');
	var $mainSection = $('.layout-main-section');
	
	// Set proper flex layout
	if ($mainWrapper.length && !$mainWrapper.hasClass('galaxyerp-layout-restored')) {
		$mainWrapper.addClass('galaxyerp-layout-restored');
		$mainWrapper.css({
			'display': 'flex',
			'min-height': 'calc(100vh - var(--navbar-height))',
			'background': 'var(--bg-color)'
		});
	}
	
	// Restore sidebar behavior
	if ($sidebar.length) {
		$sidebar.css({
			'width': '280px',
			'min-width': '280px',
			'background': 'var(--bg-color)',
			'border-right': '1px solid var(--border-color)',
			'transition': 'all 0.3s ease',
			'overflow-y': 'auto',
			'overflow-x': 'hidden',
			'position': 'relative',
			'z-index': '5'
		});
		
		// Handle hidden state
		if ($sidebar.hasClass('hidden')) {
			$sidebar.css({
				'width': '0',
				'min-width': '0',
				'overflow': 'hidden'
			});
		}
	}
	
	// Restore main section behavior
	if ($mainSection.length) {
		$mainSection.css({
			'flex': '1',
			'min-width': '0',
			'display': 'flex',
			'flex-direction': 'column',
			'background': 'var(--bg-color)',
			'transition': 'all 0.3s ease'
		});
	}
}

function restoreHeaderLayout() {
	// Ensure proper header structure
	var $pageHead = $('.page-head');
	var $pageTitle = $('.page-title');
	var $sidebarToggle = $('.sidebar-toggle-btn');
	var $titleText = $('.title-text');
	
	// Restore page head
	if ($pageHead.length) {
		$pageHead.css({
			'background': 'var(--bg-color)',
			'border-bottom': '1px solid var(--border-color)',
			'position': 'sticky',
			'top': 'var(--navbar-height)',
			'z-index': '6',
			'transition': '0.5s top'
		});
	}
	
	// Restore page title section
	if ($pageTitle.length) {
		$pageTitle.css({
			'display': 'flex',
			'align-items': 'center',
			'flex': '1'
		});
	}
	
	// Restore sidebar toggle button
	if ($sidebarToggle.length) {
		$sidebarToggle.css({
			'display': 'flex',
			'align-items': 'center',
			'justify-content': 'center',
			'width': '32px',
			'height': '32px',
			'margin-right': '12px',
			'cursor': 'pointer',
			'background': 'transparent',
			'border': 'none',
			'border-radius': '4px',
			'transition': 'all 0.2s ease'
		});
	}
	
	// Restore title text
	if ($titleText.length) {
		$titleText.css({
			'font-size': '1.5rem',
			'font-weight': '700',
			'color': 'var(--text-color)',
			'margin': '0',
			'padding': '0',
			'line-height': '1.2',
			'max-width': '25vw',
			'overflow': 'hidden',
			'text-overflow': 'ellipsis',
			'white-space': 'nowrap'
		});
	}
}

function setupSidebarToggle() {
	// Ensure sidebar toggle functionality works
	$(document).on('click', '.sidebar-toggle-btn', function(e) {
		e.preventDefault();
		e.stopPropagation();
		
		var $sidebar = $('.layout-side-section');
		var $body = $('body');
		
		if ($sidebar.length) {
			if ($sidebar.hasClass('hidden')) {
				// Show sidebar
				$sidebar.removeClass('hidden');
				$body.attr('data-sidebar', '1');
				$sidebar.css({
					'width': '280px',
					'min-width': '280px'
				});
			} else {
				// Hide sidebar
				$sidebar.addClass('hidden');
				$body.attr('data-sidebar', '0');
				$sidebar.css({
					'width': '0',
					'min-width': '0'
				});
			}
			
			// Trigger resize event for any responsive components
			$(window).trigger('resize');
		}
	});
}

function ensureProperWorkspaceStructure() {
	// Ensure workspace has proper structure
	var $body = $('body');
	var $mainWrapper = $('.layout-main-section-wrapper');
	
	// Set proper body attributes
	if ($body.length) {
		$body.attr('data-sidebar', '1');
	}
	
	// Ensure main wrapper exists and has proper structure
	if ($mainWrapper.length === 0) {
		// Create main wrapper if it doesn't exist
		var $content = $('.content');
		if ($content.length) {
			$content.wrap('<div class="layout-main-section-wrapper"></div>');
		}
	}
	
	// Ensure proper page container structure
	var $pageContainer = $('.page-container');
	if ($pageContainer.length === 0) {
		var $mainSection = $('.layout-main-section');
		if ($mainSection.length) {
			$mainSection.wrap('<div class="page-container"></div>');
		}
	}
}

function fixWorkspaceTitle() {
	// Fix workspace title to show module-specific title instead of generic "Workspace"
	var $titleText = $('.title-text');
	if ($titleText.length) {
		var currentTitle = $titleText.text().trim();
		
		// If it's a generic title, try to find the actual module title
		if (currentTitle === 'Workspace' || currentTitle === '{{ _("Workspace") }}' || currentTitle === '') {
			// Try multiple selectors to find the actual module title
			var moduleTitle = $('.module-title').text() || 
							 $('.page-title').text() || 
							 $('h1').first().text() ||
							 $('.breadcrumb-item:last').text() ||
							 $('.nav-item.active').text() ||
							 $('.sidebar-item.selected').text() ||
							 frappe.get_route()[1] || // Get from route
							 'Workspace';
			
			// Clean up the title
			moduleTitle = moduleTitle.trim();
			if (moduleTitle && moduleTitle !== currentTitle) {
				$titleText.text(moduleTitle);
			}
		}
	}
}

function applyGalaxyNextBranding() {
	replaceLogos();
	replaceBranding();
	replaceOnboardingWidget();
}

function initializeWorkspaceLayout() {
	// Initialize workspace layout restoration
	restoreWorkspaceLayout();
	restoreHeaderLayout();
	setupSidebarToggle();
	ensureProperWorkspaceStructure();
	fixWorkspaceTitle();
	applyGalaxyNextBranding();
}

// Initialize when document is ready
$(document).ready(function() {
	initializeWorkspaceLayout();
	
	// Apply branding after a short delay to catch dynamically loaded content
	setTimeout(function() {
		applyGalaxyNextBranding();
		restoreWorkspaceLayout();
		fixWorkspaceTitle();
	}, 100);
	
	setTimeout(function() {
		applyGalaxyNextBranding();
		restoreHeaderLayout();
		fixWorkspaceTitle();
	}, 500);
});

// Initialize when Frappe is ready
if (typeof frappe !== 'undefined') {
	frappe.ready(function() {
		initializeWorkspaceLayout();
	});
}

// Set app logo URL
if (typeof frappe !== 'undefined' && frappe.boot) {
	frappe.boot.app_logo_url = '/assets/galaxyerp/images/galaxynext_logo.png';
}

// Safe MutationObserver with throttling to prevent infinite loops
if (typeof MutationObserver !== 'undefined') {
	let observerTimeout;
	const observer = new MutationObserver(function(mutations) {
		// Throttle the observer to prevent excessive calls
		clearTimeout(observerTimeout);
		observerTimeout = setTimeout(function() {
			let shouldApply = false;
			mutations.forEach(function(mutation) {
				if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
					// Only apply branding if new nodes contain ERPNext text
					for (let i = 0; i < mutation.addedNodes.length; i++) {
						const node = mutation.addedNodes[i];
						if (node.nodeType === 1 && node.textContent && node.textContent.includes('ERPNext')) {
							shouldApply = true;
							break;
						}
					}
				}
			});
			if (shouldApply) {
				applyGalaxyNextBranding();
				restoreWorkspaceLayout();
				fixWorkspaceTitle();
			}
		}, 100);
	});
	
	observer.observe(document.body, {
		childList: true,
		subtree: true
	});
}

// Override Frappe UI methods for proper workspace behavior
if (typeof frappe !== 'undefined' && frappe.ui && frappe.ui.misc) {
	if (!frappe.ui.misc.original_about) {
		frappe.ui.misc.original_about = frappe.ui.misc.about;
	}
}

// Safe onboarding widget override
if (typeof frappe !== 'undefined' && frappe.widgets && frappe.widgets.OnboardingWidget) {
	var originalOnboardingWidget = frappe.widgets.OnboardingWidget;
	if (originalOnboardingWidget && originalOnboardingWidget.prototype) {
		var originalRefresh = originalOnboardingWidget.prototype.refresh;
		if (originalRefresh) {
			originalOnboardingWidget.prototype.refresh = function() {
				originalRefresh.call(this);
				// Apply branding after widget refresh with delay
				setTimeout(function() {
					replaceOnboardingWidget();
					restoreWorkspaceLayout();
					fixWorkspaceTitle();
				}, 100);
			};
		}
	}
}

// Override page setup for proper workspace behavior
if (typeof frappe !== 'undefined' && frappe.ui && frappe.ui.page) {
	var originalPageSetup = frappe.ui.page.Page.prototype.setup_sidebar_toggle;
	if (originalPageSetup) {
		frappe.ui.page.Page.prototype.setup_sidebar_toggle = function() {
			originalPageSetup.call(this);
			// Ensure our layout restoration is applied
			setTimeout(function() {
				restoreWorkspaceLayout();
				restoreHeaderLayout();
				fixWorkspaceTitle();
			}, 50);
		};
	}
} 



