import os
import click
import frappe
import subprocess
from .spa_generator import SPAGenerator
from frappe.commands import get_site, pass_context
from frappe import get_module_path, scrub
from .utils import add_build_command_to_package_json, add_routing_rule_to_hooks
from .boilerplates import (
	CUSTOM_PAGE_APP_COMPONENT_BOILERPLATE,
	CUSTOM_PAGE_JS_TEMPLATE,
	CUSTOM_PAGE_JS_BUNDLE_TEMPLATE,
)
from pathlib import Path


@click.command("add-spa")
@click.option("--name", default="dashboard", prompt="Dashboard Name")
@click.option("--app", prompt="App Name")
@click.option(
	"--framework",
	type=click.Choice(["vue", "react"]),
	default="vue",
	prompt="Which framework do you want to use?",
	help="The framework to use for the SPA",
)
@click.option(
	"--typescript",
	default=False,
	prompt="Configure TypeScript?",
	is_flag=True,
	help="Configure with TypeScript",
)
@click.option(
	"--tailwindcss", default=False, is_flag=True, help="Configure tailwindCSS"
)
def generate_spa(framework, name, app, typescript, tailwindcss):
	if not app:
		click.echo("Please provide an app with --app")
		return
	generator = SPAGenerator(framework, name, app, tailwindcss, typescript)
	generator.generate_spa()


@click.command("add-frappe-ui")
@click.option("--name", default="frontend", prompt="Dashboard Name")
@click.option("--app", prompt="App Name")
def add_frappe_ui(name, app):
	if not app:
		click.echo("Please provide an app with --app")
		return

	click.echo(f"Adding Frappe UI starter to {app}...")
	add_frappe_ui_starter(name, app)

	click.echo(
		f"🖥️  You can start the dev server by running 'yarn dev' in apps/{app}/{name}"
	)
	click.echo("📄  Docs: https://frappeui.com")


def add_frappe_ui_starter(name, app):
	from pathlib import Path

	subprocess.run(
		["npx", "degit", "NagariaHussain/doppio_frappeui_starter", name],
		cwd=Path("../apps", app),
	)
	subprocess.run(["yarn"], cwd=Path("../apps", app, name))

	add_build_command_to_package_json(app, name)
	add_routing_rule_to_hooks(app, name)


@click.command("add-custom-page")
@click.option("--page-name", prompt="Custom Page Name")
@click.option("--app", prompt="App Name")
@click.option(
	"--starter",
	type=click.Choice(["vue", "simple"]),
	default="vue",
	prompt="Which framework do you want to use?",
	help="Setup a custom page with the framework of your choice",
)
@pass_context
def add_custom_page(context, app, page_name, starter):
	site = get_site(context)
	frappe.init(site=site)

	try:
		frappe.connect()
		setup_custom_page(site, app, page_name, starter)
	finally:
		frappe.destroy()


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


commands = [generate_spa, add_frappe_ui, add_custom_page]
