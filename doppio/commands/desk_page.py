import os
import click
import frappe
import subprocess

from frappe import scrub
from pathlib import Path

from .boilerplates import (
	DESK_PAGE_JS_BUNDLE_TEMPLATE_VUE,
	DESK_PAGE_JS_TEMPLATE,
	DESK_PAGE_VUE_APP_COMPONENT_BOILERPLATE,
	DESK_PAGE_JSX_BUNDLE_TEMPLATE_REACT,
	DESK_PAGE_REACT_APP_COMPONENT_BOILERPLATE,
)


def setup_desk_page(site, app_name, page_name, starter):
	if not frappe.conf.developer_mode:
		click.echo("Please enable developer mode to add custom page")
		return

	page = create_page_doc(page_name, app_name, site)

	if starter == "vue":
		setup_vue_desk_page_starter(page, app_name)
	elif starter == "react":
		setup_react_desk_page_starter(page, app_name)
	else:
		click.echo("Please provide a valid starter")
		return

	launch_desk_page_in_browser(page, site)


def setup_vue_desk_page_starter(page_doc, app_name):
	setup_desk_page_for_framework("vue", page_doc, app_name)


def setup_react_desk_page_starter(page_doc, app_name):
	# check if package.json exists in app directory
	# if not, create package.json using npm init --yes
	app_path = Path("../apps") / app_name
	package_json_path = app_path / "package.json"
	if not package_json_path.exists():
		subprocess.run(["npm", "init", "--yes"], cwd=app_path)

	# install react and react-dom
	click.echo("Installing react and react-dom...")
	subprocess.run(
		["yarn", "add", "react", "react-dom"], cwd=app_path
	)

	setup_desk_page_for_framework("react", page_doc, app_name)


def setup_desk_page_for_framework(framework, page_doc, app_name):
	bundle_type = "js" if framework == "vue" else "jsx"
	context = {
		"pascal_cased_name": page_doc.name.replace("-", " ").title().replace(" ", ""),
		"scrubbed_name": page_doc.name.replace("-", "_"),
		"page_title": page_doc.title,
		"page_name": page_doc.name,
		"bundle_type": bundle_type,
	}

	desk_page_js_file_content = frappe.render_template(
		DESK_PAGE_JS_TEMPLATE, context
	)
	desk_page_js_bundle_file_content = frappe.render_template(
		DESK_PAGE_JS_BUNDLE_TEMPLATE_VUE
		if framework == "vue"
		else DESK_PAGE_JSX_BUNDLE_TEMPLATE_REACT,
		context,
	)

	# module
	module = frappe.get_module_list(app_name)[0]
	js_file_path = os.path.join(
		frappe.get_module_path(module),
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
		f.write(desk_page_js_file_content)

	# create dir if not exists
	Path(js_bundle_file_path).parent.mkdir(parents=True, exist_ok=True)
	with Path(js_bundle_file_path).open("w") as f:
		f.write(desk_page_js_bundle_file_content)

	app_component_file_name = "App.vue" if framework == "vue" else "App.jsx"
	app_component_path = os.path.join(
		frappe.get_app_path(app_name),
		"public",
		"js",
		scrub(page_doc.name),
		app_component_file_name,
	)

	app_component_path_relative = str(
		app_name / Path(app_component_path).relative_to(frappe.get_app_path(app_name))
	)

	app_component_template = None
	if framework == "vue":
		app_component_template = DESK_PAGE_VUE_APP_COMPONENT_BOILERPLATE
	else:
		app_component_template = DESK_PAGE_REACT_APP_COMPONENT_BOILERPLATE

	with Path(app_component_path).open("w") as f:
		app_component_template = frappe.render_template(app_component_template, {
			"app_component_path": app_component_path_relative,
		})
		f.write(app_component_template)

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


def launch_desk_page_in_browser(page, site):
	click.echo(f"Opening {page.title} in browser...")
	page_url = f"{frappe.utils.get_site_url(site)}/app/{page.name}"
	click.launch(page_url)
	click.echo(
		click.style(
			"Restart your bench to enable auto-reload of custom page on changes.",
			fg="yellow",
		)
	)
