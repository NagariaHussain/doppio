import click
import frappe
import subprocess
from .spa_generator import SPAGenerator
from frappe.commands import get_site, pass_context
from .utils import add_build_command_to_package_json, add_routing_rule_to_hooks
from .desk_page import setup_desk_page


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


@click.command("add-desk-page")
@click.option("--page-name", prompt="Page Name")
@click.option("--app", prompt="App Name")
@click.option(
    "--starter",
    type=click.Choice(["vue", "react"]),
    default="vue",
    prompt="Which framework do you want to use?",
    help="Setup a desk page with the framework of your choice",
)
@pass_context
def add_desk_page(context, app, page_name, starter):
    site = get_site(context)
    frappe.init(site=site)

    try:
        frappe.connect()
        setup_desk_page(site, app, page_name, starter)
    finally:
        frappe.destroy()


commands = [generate_spa, add_frappe_ui, add_desk_page]
