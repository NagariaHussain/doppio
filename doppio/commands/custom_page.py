import os
import click
import frappe
import subprocess

from frappe import scrub
from pathlib import Path

from .boilerplates import (
	CUSTOM_PAGE_JS_BUNDLE_TEMPLATE_VUE,
	CUSTOM_PAGE_JS_TEMPLATE,
	CUSTOM_PAGE_VUE_APP_COMPONENT_BOILERPLATE,
	CUSTOM_PAGE_JSX_BUNDLE_TEMPLATE_REACT,
	CUSTOM_PAGE_REACT_APP_COMPONENT_BOILERPLATE,
)


def setup_custom_page(site, app_name, page_name, starter):
	if not frappe.conf.developer_mode:
		click.echo("Please enable developer mode to add custom page")
		return

	page = create_page_doc(page_name, app_name, site)

	if starter == "vue":
		setup_vue_custom_page_starter(page, app_name)
	elif starter == "react":
		setup_react_custom_page_starter(page, app_name)
	else:
		click.echo("Please provide a valid starter")
		return

	launch_custom_page_in_browser(page, site)


def setup_vue_custom_page_starter(page_doc, app_name):
	setup_custom_page_for_framework("vue", page_doc, app_name)


def setup_react_custom_page_starter(page_doc, app_name):
	# check if package.json exists in app directory
	# if not, create package.json using npm init --yes
	package_json_path = Path(frappe.get_app_path(app_name)) / "package.json"
	if not package_json_path.exists():
		subprocess.run(["npm", "init", "--yes"], cwd=frappe.get_app_path(app_name))

	# install react and react-dom
	click.echo("Installing react and react-dom...")
	subprocess.run(
		["yarn", "add", "react", "react-dom"], cwd=frappe.get_app_path(app_name)
	)

	setup_custom_page_for_framework("react", page_doc, app_name)


def setup_custom_page_for_framework(framework, page_doc, app_name):
	bundle_type = "js" if framework == "vue" else "jsx"
	context = {
		"pascal_cased_name": page_doc.name.replace("-", " ").title().replace(" ", ""),
		"scrubbed_name": page_doc.name.replace("-", "_"),
		"page_title": page_doc.title,
		"page_name": page_doc.name,
		"bundle_type": bundle_type,
	}

	custom_page_js_file_content = frappe.render_template(
		CUSTOM_PAGE_JS_TEMPLATE, context
	)
	custom_page_js_bundle_file_content = frappe.render_template(
		CUSTOM_PAGE_JS_BUNDLE_TEMPLATE_VUE
		if framework == "vue"
		else CUSTOM_PAGE_JSX_BUNDLE_TEMPLATE_REACT,
		context,
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
		scrub(page_doc.name) + f".bundle.{bundle_type}",
	)

	with Path(js_file_path).open("w") as f:
		f.write(custom_page_js_file_content)

	# create dir if not exists
	Path(js_bundle_file_path).parent.mkdir(parents=True, exist_ok=True)
	with Path(js_bundle_file_path).open("w") as f:
		f.write(custom_page_js_bundle_file_content)

	app_component_file_name = "App.vue" if framework == "vue" else "App.jsx"
	app_component_path = os.path.join(
		frappe.get_app_path(app_name),
		"public",
		"js",
		scrub(page_doc.name),
		app_component_file_name,
	)

	with Path(app_component_path).open("w") as f:
		if framework == "vue":
			f.write(CUSTOM_PAGE_VUE_APP_COMPONENT_BOILERPLATE)
		else:
			f.write(CUSTOM_PAGE_REACT_APP_COMPONENT_BOILERPLATE)

	from frappe.build import bundle

	bundle("development", apps=app_name)


def create_page_doc(page_name, app_name, site):
	module_name = frappe.get_all(
		"Module Def",
		filters={"app_name": app_name},
		limit=1,
		pluck="name",
		order_by="creation",
	)

	if module_name:
		module_name = module_name[0]
	else:
		message = click.style(
			f"Make sure {app_name} is installed on the site {site}", fg="yellow"
		)
		click.echo(message)
		return

	# create page doc
	page = frappe.new_doc("Page")
	page.module = module_name
	page.standard = "Yes"
	page.page_name = page_name
	page.title = page_name
	page.insert()

	frappe.db.commit()
	return page


def launch_custom_page_in_browser(page, site):
	click.echo(f"Opening {page.title} in browser...")
	page_url = f"{frappe.utils.get_site_url(site)}/app/{page.name}"
	click.launch(page_url)
	click.echo(
		click.style(
			"Restart your bench to enable auto-reload of custom page on changes.",
			fg="yellow",
		)
	)
