frappe.provide("frappe.ui.misc");
frappe.ui.misc.about = function () {
	if (!frappe.ui.misc.about_dialog) {
		var d = new frappe.ui.Dialog({ title: __("GalaxyNext Framework") });

		$(d.body).html(
			repl(
				`<div>
					<p>${__("Open Source Applications for the Web")}</p>
					<p><i class='fa fa-globe fa-fw'></i>
						${__("Website")}:
						<a href='https://galaxyerpsoftware.com' target='_blank'>https://galaxyerpsoftware.com</a></p>
					<p><i class='fa fa-github fa-fw'></i>
						${__("Source")}:
						<a href='https://github.com/GalaxyERPSoftware/GalaxyNext' target='_blank'>https://github.com/GalaxyERPSoftware/GalaxyNext</a></p>
					<p><i class='fa fa-book fa-fw'></i>
						Documentation: <a href='https://docs.galaxyerpsoftware.com' target='_blank'>https://docs.galaxyerpsoftware.com</a></p>
					<p><i class='fa fa-linkedin fa-fw'></i>
						LinkedIn: <a href='https://www.linkedin.com/company/galaxy-erp-software-private-limited' target='_blank'>https://www.linkedin.com/company/galaxy-erp-software-private-limited</a></p>
					<p><i class='fa fa-instagram fa-fw'></i>
						Instagram: <a href='https://www.instagram.com/galaxyerpsoftwarepvtltd' target='_blank'>https://www.instagram.com/galaxyerpsoftwarepvtltd</a></p>
					<!-- Commented out entries for Frappe School, Twitter, and YouTube -->
					<!-- <p><i class='fa fa-graduation-cap fa-fw'></i>
						Frappe School: <a href='https://frappe.school' target='_blank'>https://frappe.school</a></p> -->
					<!-- <p><i class='fa fa-twitter fa-fw'></i>
						Twitter: <a href='https://twitter.com/frappetech' target='_blank'>https://twitter.com/frappetech</a></p> -->
					<!-- <p><i class='fa fa-youtube fa-fw'></i>
						YouTube: <a href='https://www.youtube.com/@frappetech' target='_blank'>https://www.youtube.com/@frappetech</a></p> -->
					<hr>
					<h4>${__("Installed Apps")}</h4>
					<div id='about-app-versions'>${__("Loading versions...")}</div>
					<hr>
					<p class='text-muted'>${__("&copy; GalaxyERP Software Pvt. Ltd. and contributors")} </p>
					</div>`,
				frappe.app
			)
		);

		frappe.ui.misc.about_dialog = d;

		frappe.ui.misc.about_dialog.on_page_show = function () {
			if (!frappe.versions) {
				frappe.call({
					method: "frappe.utils.change_log.get_versions",
					callback: function (r) {
						show_versions(r.message);
					},
				});
			} else {
				show_versions(frappe.versions);
			}
		};

		var show_versions = function (versions) {
			var $wrap = $("#about-app-versions").empty();
			$.each(Object.keys(versions).sort(), function (i, key) {
				var v = versions[key];
				let text;
				
				// Override ERPNext title with GalaxyNext
				var displayTitle = v.title;
				if (v.title === "ERPNext") {
					displayTitle = "GalaxyNext";
				}
				
				if (v.branch) {
					text = $.format("<p><b>{0}:</b> v{1} ({2})<br></p>", [
						displayTitle,
						v.branch_version || v.version,
						v.branch,
					]);
				} else {
					text = $.format("<p><b>{0}:</b> v{1}<br></p>", [displayTitle, v.version]);
				}
				$(text).appendTo($wrap);
			});

			frappe.versions = versions;
		};
	}

	frappe.ui.misc.about_dialog.show();
}; 