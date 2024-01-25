import re
import json
import subprocess
from pathlib import Path


def create_file(path: Path, content: str = None):
	# Create the file if not exists
	if not path.exists():
		path.touch()

	# Write the contents (if any)
	if content:
		with path.open("w") as f:
			f.write(content)


def add_commands_to_root_package_json(app, spa_name):
	app_path = Path("../apps") / app
	spa_path: Path = app_path / spa_name
	package_json_path: Path = spa_path / "package.json"

	if not package_json_path.exists():
		print("package.json not found. Please manually update the build command.")
		return

	data = {}
	with package_json_path.open("r") as f:
		data = json.load(f)

	data["scripts"][
		"build"
	] = f"vite build --base=/assets/{app}/{spa_name}/ && yarn copy-html-entry"

	data["scripts"]["copy-html-entry"] = (
		f"cp ../{app}/public/{spa_name}/index.html" f" ../{app}/www/{spa_name}.html"
	)

	with package_json_path.open("w") as f:
		json.dump(data, f, indent=2)

	# Update app's package.json
	app_package_json_path: Path = app_path / "package.json"

	if not app_package_json_path.exists():
		subprocess.run(["npm", "init", "--yes"], cwd=app_path)

		data = {}
		with app_package_json_path.open("r") as f:
			data = json.load(f)

		data["scripts"]["postinstall"] = f"cd {spa_name} && yarn install"
		data["scripts"]["dev"] = f"cd {spa_name} && yarn dev"
		data["scripts"]["build"] = f"cd {spa_name} && yarn build"

		with app_package_json_path.open("w") as f:
			json.dump(data, f, indent=2)


def add_routing_rule_to_hooks(app, spa_name):
	hooks_py = Path(f"../apps/{app}/{app}") / "hooks.py"
	hooks = ""
	with hooks_py.open("r") as f:
		hooks = f.read()

	pattern = re.compile(r"website_route_rules\s?=\s?\[(.+)\]")

	rule = (
		"{" + f"'from_route': '/{spa_name}/<path:app_path>', 'to_route': '{spa_name}'" + "}"
	)

	rules = pattern.sub(r"website_route_rules = [{rule}, \1]", hooks)

	# If rule is not already defined
	if not pattern.search(hooks):
		rules = hooks + "\nwebsite_route_rules = [{rule},]"

	updates_hooks = rules.replace("{rule}", rule)
	with hooks_py.open("w") as f:
		f.write(updates_hooks)
