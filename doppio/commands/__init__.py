import click
from .spa_generator import SPAGenerator

@click.command("add-spa")
@click.option("--name", default="dashboard", prompt="Dashboard Name")
@click.option("--app", prompt='App Name')
@click.option('--framework', type=click.Choice(['vue', 'react']), default='vue', prompt='Which framework do you want to use?', help='The framework to use for the SPA')
@click.option(
	"--tailwindcss", default=False, is_flag=True, help="Configure tailwindCSS"
)
def generate_spa(framework, name, app, tailwindcss):
	if not app:
		click.echo("Please provide an app with --app")
		return

	generator = SPAGenerator(framework, name, app, tailwindcss)
	generator.generate_spa()


commands = [generate_spa]
