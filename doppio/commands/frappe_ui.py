import subprocess
from pathlib import Path

import click

from .utils import add_commands_to_root_package_json, add_routing_rule_to_hooks


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
    click.echo("📄  Docs: https://ui.frappe.io")


def add_frappe_ui_starter(name, app):
    subprocess.run(
        ["npx", "degit", "NagariaHussain/doppio_frappeui_starter", name],
        cwd=Path("../apps", app),
    )
    subprocess.run(["yarn"], cwd=Path("../apps", app, name))

    add_commands_to_root_package_json(app, name)
    add_routing_rule_to_hooks(app, name)
    replace_placeholders_in_starter(app, name)


def replace_placeholders_in_starter(app, name):
    spa_path = Path("../apps", app, name)
    files = ("vite.config.js", "src/router.js")

    replacement_map = {
        "<app_name>": app,
        "frontend": name
    }

    for file in files:
        file_path = spa_path / file
        fixed_content = ""
        with file_path.open("r") as f:
            content = f.read()
            for placeholder, replacement in replacement_map.items():
                content = content.replace(placeholder, replacement)
            fixed_content = content
        with file_path.open("w") as f:
            f.write(fixed_content)
