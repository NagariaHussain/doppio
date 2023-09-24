import os
import click
import frappe

from frappe import scrub
from pathlib import Path

from .boilerplates import (
	CUSTOM_PAGE_APP_COMPONENT_BOILERPLATE,
	CUSTOM_PAGE_JS_TEMPLATE,
	CUSTOM_PAGE_JS_BUNDLE_TEMPLATE,
)


def setup_custom_page(site, app_name, page_name, starter):
	if not frappe.conf.developer_mode:
		click.echo("Please enable developer mode to add custom page")
		return

	module_name = frappe.get_all(
		"Module Def",
		filters={"app_name": app_name},
		limit=1,
		pluck="name",
		order_by="creation",
	)[0]

	# create page doc
	page = frappe.new_doc("Page")
	page.module = module_name
	page.standard = "Yes"
	page.page_name = page_name
	page.title = page_name
	page.insert()
	frappe.db.commit()

	if starter == "vue":
		setup_vue_custom_page_starter(page, app_name)

	click.echo(f"Opening {page.title} in browser...")
	page_url = f"{frappe.utils.get_site_url(site)}/app/{page.name}"
	click.launch(page_url)
	click.echo(click.style("Restart your bench to enable auto-reload of custom page on changes.", fg="yellow"))


def setup_vue_custom_page_starter(page_doc, app_name):
	context = {
		"pascal_cased_name": page_doc.name.replace("-", " ").title().replace(" ", ""),
		"scrubbed_name": page_doc.name.replace("-", "_"),
		"page_title": page_doc.title,
		"page_name": page_doc.name,
	}

	custom_page_js_file_content = frappe.render_template(CUSTOM_PAGE_JS_TEMPLATE, context)
	custom_page_js_bundle_file_content = frappe.render_template(
		CUSTOM_PAGE_JS_BUNDLE_TEMPLATE, context
	)

	js_file_path = os.path.join(
		frappe.get_module_path(app_name),
		scrub(page_doc.doctype),
		scrub(page_doc.name),
		scrub(page_doc.name) + ".js",
	)
	js_bundle_file_path = os.path.join(
		frappe.get_app_path(app_name),
		"public",
		"js",
		scrub(page_doc.name),
		scrub(page_doc.name) + ".bundle.js",
	)

	with Path(js_file_path).open("w") as f:
		f.write(custom_page_js_file_content)

	# create dir if not exists
	Path(js_bundle_file_path).parent.mkdir(parents=True, exist_ok=True)
	with Path(js_bundle_file_path).open("w") as f:
		f.write(custom_page_js_bundle_file_content)

	app_component_path = os.path.join(
		frappe.get_app_path(app_name), "public", "js", scrub(page_doc.name), "App.vue"
	)

	with Path(app_component_path).open("w") as f:
		f.write(CUSTOM_PAGE_APP_COMPONENT_BOILERPLATE)
	
	from frappe.build import bundle
	bundle("development", apps=app_name)

