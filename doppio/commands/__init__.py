import click
import frappe

from .spa_generator import SPAGenerator
from frappe.commands import get_site, pass_context
from .frappe_ui import add_frappe_ui
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
