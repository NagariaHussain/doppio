import click
import subprocess
from .spa_generator import SPAGenerator


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
def add_frappe_ui_starter(name, app):
	from pathlib import Path

	if not app:
		click.echo("Please provide an app with --app")
		return

	click.echo(f"Adding Frappe UI starter to {app}...")
	subprocess.run(
		["npx", "degit", "netchampfaris/frappe-ui-starter", name], cwd=Path("../apps", app)
	)
	subprocess.run(["yarn"], cwd=Path("../apps", app, name))

	click.echo(f"🖥️  You can start the dev server by running 'yarn dev' in apps/{app}/{name}")
	click.echo("📄  Docs: https://frappeui.com")


commands = [generate_spa, add_frappe_ui_starter]
