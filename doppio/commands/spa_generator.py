import re
import json
import click
import subprocess

from pathlib import Path
from .boilerplates import *
from .utils import create_file


class SPAGenerator:
	def __init__(self, framework, spa_name, app, add_tailwindcss, typescript):
		"""Initialize a new SPAGenerator instance"""
		self.framework = framework
		self.app = app
		self.app_path = Path("../apps") / app
		self.spa_name = spa_name
		self.spa_path: Path = self.app_path / self.spa_name
		self.add_tailwindcss = add_tailwindcss
		self.use_typescript = typescript

		self.validate_spa_name()

	def validate_spa_name(self):
		if self.spa_name == self.app:
			click.echo("Dashboard name must not be same as app name", err=True, color=True)
			exit(1)

	def generate_spa(self):
		click.echo("Generating spa...")
		if self.framework == "vue":
			self.initialize_vue_vite_project()
			self.link_controller_files()
			self.setup_proxy_options()
			self.setup_vue_vite_config()
			self.setup_vue_router()
			self.create_vue_files()

		elif self.framework == "react":
			self.initialize_react_vite_project()
			self.setup_proxy_options()
			self.setup_react_vite_config()
			self.create_react_files()

		# Common to all frameworks
		self.update_package_json()
		self.create_www_directory()
		self.add_csrf_to_html()

		if self.add_tailwindcss:
			self.setup_tailwindcss()

		self.add_routing_rule_to_hooks()

		click.echo(f"Run: cd {self.spa_path.absolute().resolve()} && npm run dev")
		click.echo("to start the development server and visit: http://<site>:8080")

	def setup_tailwindcss(self):
		# TODO: Convert to yarn command
		# npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
		subprocess.run(
			[
				"npm",
				"install",
				"-D",
				"tailwindcss@latest",
				"postcss@latest",
				"autoprefixer@latest",
			],
			cwd=self.spa_path,
		)

		# npx tailwindcss init -p
		subprocess.run(["npx", "tailwindcss", "init", "-p"], cwd=self.spa_path)

		# Create an index.css file
		index_css_path: Path = self.spa_path / "src/index.css"

		# Add boilerplate code
		INDEX_CSS_BOILERPLATE = """@tailwind base;
@tailwind components;
@tailwind utilities;
	"""

		create_file(index_css_path, INDEX_CSS_BOILERPLATE)

	def create_vue_files(self):
		app_vue = self.spa_path / "src/App.vue"
		create_file(app_vue, APP_VUE_BOILERPLATE)

		views_dir: Path = self.spa_path / "src/views"
		if not views_dir.exists():
			views_dir.mkdir()

		home_vue = views_dir / "Home.vue"
		login_vue = views_dir / "Login.vue"

		create_file(home_vue, HOME_VUE_BOILERPLATE)
		create_file(login_vue, LOGIN_VUE_BOILERPLATE)

	def setup_vue_router(self):
		# Setup vue router
		router_dir_path: Path = self.spa_path / "src/router"

		# Create router directory
		router_dir_path.mkdir()

		# Create files
		router_index_file = router_dir_path / "index.js"
		create_file(
			router_index_file, ROUTER_INDEX_BOILERPLATE.replace("{{name}}", self.spa_name)
		)

		auth_routes_file = router_dir_path / "auth.js"
		create_file(auth_routes_file, AUTH_ROUTES_BOILERPLATE)

	def initialize_vue_vite_project(self):
		# Run "yarn create vite {name} --template vue"
		print("Scafolding vue project...")
		if self.use_typescript:
			subprocess.run(
				["yarn", "create", "vite", self.spa_name, "--template", "vue-ts"], cwd=self.app_path
			)
		else:
			subprocess.run(
				["yarn", "create", "vite", self.spa_name, "--template", "vue"], cwd=self.app_path
			)

		# Install router and other npm packages
		# yarn add vue-router@4 socket.io-client@2.4.0
		print("Installing dependencies...")
		subprocess.run(
			["yarn", "add", "vue-router@^4", "socket.io-client@^2.4.0"], cwd=self.spa_path
		)

	def link_controller_files(self):
		# Link controller files in main.js/main.ts
		print("Linking controller files...")
		main_js: Path = self.app_path / (f"{self.spa_name}/src/main.ts" if self.use_typescript else f"{self.spa_name}/src/main.js")

		if main_js.exists():
			with main_js.open("w") as f:
				boilerplate = MAIN_JS_BOILERPLATE

				# Add css import
				if self.add_tailwindcss:
					boilerplate = "import './index.css';\n" + boilerplate

				f.write(boilerplate)
		else:
			click.echo("src/main.js not found!")
			return

	def setup_proxy_options(self):
		# Setup proxy options file
		proxy_options_file: Path = self.spa_path / "proxyOptions.js"
		create_file(proxy_options_file, PROXY_OPTIONS_BOILERPLATE)

	def setup_vue_vite_config(self):
		vite_config_file: Path = self.spa_path / ("vite.config.ts" if self.use_typescript else "vite.config.js")
		if not vite_config_file.exists():
			vite_config_file.touch()
		with vite_config_file.open("w") as f:
			boilerplate = VUE_VITE_CONFIG_BOILERPLATE.replace("{{app}}", self.app)
			boilerplate = boilerplate.replace("{{name}}", self.spa_name)
			f.write(boilerplate)

	def add_routing_rule_to_hooks(self):
		hooks_py = Path(f"../apps/{self.app}/{self.app}") / "hooks.py"
		hooks = ""
		with hooks_py.open("r") as f:
			hooks = f.read()

		pattern = re.compile(r"website_route_rules\s?=\s?\[(.+)\]")

		rule = (
			"{"
			+ f"'from_route': '/{self.spa_name}/<path:app_path>', 'to_route': '{self.spa_name}'"
			+ "}"
		)

		rules = pattern.sub(r"website_route_rules = [{rule}, \1]", hooks)

		# If rule is not already defined
		if not pattern.search(hooks):
			rules = hooks + "\nwebsite_route_rules = [{rule},]"

		updates_hooks = rules.replace("{rule}", rule)
		with hooks_py.open("w") as f:
			f.write(updates_hooks)

	def update_package_json(self):
		package_json_path: Path = self.spa_path / "package.json"

		if not package_json_path.exists():
			print("package.json not found. Please manually update the build command.")
			return

		data = {}
		with package_json_path.open("r") as f:
			data = json.load(f)

		data["scripts"][
			"build"
		] = f"vite build --base=/assets/{self.app}/{self.spa_name}/ && yarn copy-html-entry"

		data["scripts"]["copy-html-entry"] = (
			f"cp ../{self.app}/public/{self.spa_name}/index.html"
			f" ../{self.app}/www/{self.spa_name}.html"
		)

		with package_json_path.open("w") as f:
			json.dump(data, f, indent=2)

		# Update app's package.json
		app_package_json_path: Path = self.app_path / "package.json"

		if not app_package_json_path.exists():
			subprocess.run(["npm", "init", "--yes"], cwd=self.app_path)

			data = {}
			with app_package_json_path.open("r") as f:
				data = json.load(f)

			data["scripts"]["dev"] = f"cd {self.spa_name} && yarn dev"
			data["scripts"]["build"] = f"cd {self.spa_name} && yarn build"

			with app_package_json_path.open("w") as f:
				json.dump(data, f, indent=2)

	def create_www_directory(self):
		www_dir_path: Path = self.app_path / f"{self.app}/www"

		if not www_dir_path.exists():
			www_dir_path.mkdir()

	def add_csrf_to_html(self):
		index_html_file_path = self.spa_path / "index.html"
		with index_html_file_path.open("r") as f:
			current_html = f.read()

		# For attaching CSRF Token
		updated_html = current_html.replace(
			"</div>", "</div>\n\t\t<script>window.csrf_token = '{{ csrf_token }}';</script>"
		)

		with index_html_file_path.open("w") as f:
			f.write(updated_html)

	def initialize_react_vite_project(self):
		# Run "yarn create vite {name} --template react"
		print("Scaffolding React project...")
		if self.use_typescript:
			subprocess.run(
				["yarn", "create", "vite", self.spa_name, "--template", "react-ts"], cwd=self.app_path
			)
		else:
			subprocess.run(
				["yarn", "create", "vite", self.spa_name, "--template", "react"], cwd=self.app_path
			)

		# Install router and other npm packages
		# yarn add frappe-react-sdk socket.io-client@2.4.0
		print("Installing dependencies...")
		subprocess.run(
			["yarn", "add", "frappe-react-sdk", "socket.io-client@^2.4.0"], cwd=self.spa_path
		)

	def setup_react_vite_config(self):
		vite_config_file: Path = self.spa_path / ("vite.config.ts" if self.use_typescript else "vite.config.js")
		if not vite_config_file.exists():
			vite_config_file.touch()
		with vite_config_file.open("w") as f:
			boilerplate = REACT_VITE_CONFIG_BOILERPLATE.replace("{{app}}", self.app)
			boilerplate = boilerplate.replace("{{name}}", self.spa_name)
			f.write(boilerplate)

	def create_react_files(self):
		app_react = self.spa_path / ("src/App.tsx" if self.use_typescript else "src/App.jsx")
		create_file(app_react, APP_REACT_BOILERPLATE)
