import click
from .spa_generator import SPAGenerator

@click.command("add-spa")
@click.option("--name", default="dashboard", prompt="Dashboard Name")
@click.option("--app")
@click.option(
	"--tailwindcss", default=False, is_flag=True, help="Configure tailwindCSS"
)
def generate_spa(name, app, tailwindcss):
	if not app:
		click.echo("Please provide an app with --app")
		return

	generator = SPAGenerator(name, app, tailwindcss)
	generator.generate_spa()


commands = [generate_spa]
