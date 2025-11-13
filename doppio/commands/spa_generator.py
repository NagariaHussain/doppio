import click
import subprocess

from pathlib import Path
from .boilerplates import *
from .utils import (
	create_file,
	add_commands_to_root_package_json,
	add_routing_rule_to_hooks,
)


class SPAGenerator:
	def __init__(self, framework, spa_name, app, add_tailwindcss, typescript, add_shadcn):
		"""Initialize a new SPAGenerator instance"""
		self.framework = framework
		self.app = app
		self.app_path = Path("../apps") / app
		self.spa_name = spa_name
		self.spa_path: Path = self.app_path / self.spa_name
		self.add_tailwindcss = add_tailwindcss
		self.use_typescript = typescript
		self.add_shadcn = add_shadcn

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
		add_commands_to_root_package_json(self.app, self.spa_name)
		self.create_www_directory()
		self.add_csrf_to_html()

		if self.add_tailwindcss:
			self.setup_tailwindcss()

		# Setup TypeScript path aliases if using TypeScript
		if self.use_typescript:
			self.setup_typescript_paths()

		# Setup Shadcn if requested (requires TypeScript and Tailwind)
		if self.add_shadcn:
			if not self.use_typescript:
				click.echo("⚠️  Shadcn requires TypeScript. Adding --typescript flag.", fg="yellow")
			if not self.add_tailwindcss:
				click.echo("⚠️  Shadcn requires Tailwind CSS. Adding --tailwindcss flag.", fg="yellow")
			self.setup_shadcn()

		add_routing_rule_to_hooks(self.app, self.spa_name)

		click.echo(f"Run: cd {self.spa_path.absolute().resolve()} && npm run dev")
		click.echo("to start the development server and visit: http://<site>:8080")

	def setup_tailwindcss(self):
		"""Setup Tailwind CSS v4 with @tailwindcss/vite plugin"""
		# Install Tailwind CSS v4 and the Vite plugin
		subprocess.run(
			[
				"npm",
				"install",
				"-D",
				"tailwindcss@latest",
				"@tailwindcss/vite@latest",
			],
			cwd=self.spa_path,
		)

		# Create an index.css file with the new v4 import syntax
		index_css_path: Path = self.spa_path / "src/index.css"

		# Add Tailwind CSS v4 import with Shadcn variables if enabled
		if self.add_shadcn:
			INDEX_CSS_BOILERPLATE = """@import "tailwindcss";

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.269 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.371 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.439 0 0);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""
		else:
			INDEX_CSS_BOILERPLATE = """@import "tailwindcss";
"""

		create_file(index_css_path, INDEX_CSS_BOILERPLATE)

	def create_vue_files(self):
		app_vue = self.spa_path / "src/App.vue"

		# Use Shadcn boilerplate if enabled
		if self.add_shadcn:
			create_file(app_vue, SHADCN_VUE_APP_BOILERPLATE)
		else:
			create_file(app_vue, APP_VUE_BOILERPLATE)

		views_dir: Path = self.spa_path / "src/views"
		if not views_dir.exists():
			views_dir.mkdir()

		home_vue = views_dir / "Home.vue"
		login_vue = views_dir / "Login.vue"

		# Use Shadcn home boilerplate if enabled
		if self.add_shadcn:
			create_file(home_vue, SHADCN_VUE_HOME_BOILERPLATE)
		else:
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
		# yarn add vue-router@4 socket.io-client@4.5.1
		print("Installing dependencies...")
		subprocess.run(
			["yarn", "add", "vue-router@^4", "socket.io-client@^4.5.1"], cwd=self.spa_path
		)

	def link_controller_files(self):
		# Link controller files in main.js/main.ts
		print("Linking controller files...")
		main_js: Path = self.app_path / (
			f"{self.spa_name}/src/main.ts"
			if self.use_typescript
			else f"{self.spa_name}/src/main.js"
		)

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
		proxy_options_file: Path = self.spa_path / (
			"proxyOptions.ts" if self.use_typescript else "proxyOptions.js"
		)
		create_file(proxy_options_file, PROXY_OPTIONS_BOILERPLATE)

	def setup_vue_vite_config(self):
		vite_config_file: Path = self.spa_path / (
			"vite.config.ts" if self.use_typescript else "vite.config.js"
		)
		if not vite_config_file.exists():
			vite_config_file.touch()
		with vite_config_file.open("w") as f:
			boilerplate = VUE_VITE_CONFIG_BOILERPLATE.replace("{{app}}", self.app)
			boilerplate = boilerplate.replace("{{name}}", self.spa_name)
			f.write(boilerplate)

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
			"</div>", "</div>\n\t\t<script>window.csrf_token = '{{ frappe.session.csrf_token }}';</script>"
		)

		with index_html_file_path.open("w") as f:
			f.write(updated_html)

	def initialize_react_vite_project(self):
		# Run "yarn create vite {name} --template react"
		print("Scaffolding React project...")
		if self.use_typescript:
			subprocess.run(
				["yarn", "create", "vite", self.spa_name, "--template", "react-ts"],
				cwd=self.app_path,
			)
		else:
			subprocess.run(
				["yarn", "create", "vite", self.spa_name, "--template", "react"], cwd=self.app_path
			)

		# Install router and other npm packages
		# yarn add frappe-react-sdk socket.io-client@4.5.1
		print("Installing dependencies...")
		subprocess.run(
			["yarn", "add", "frappe-react-sdk"], cwd=self.spa_path
		)

	def setup_react_vite_config(self):
		vite_config_file: Path = self.spa_path / (
			"vite.config.ts" if self.use_typescript else "vite.config.js"
		)
		if not vite_config_file.exists():
			vite_config_file.touch()
		with vite_config_file.open("w") as f:
			boilerplate = REACT_VITE_CONFIG_BOILERPLATE.replace("{{app}}", self.app)
			boilerplate = boilerplate.replace("{{name}}", self.spa_name)
			f.write(boilerplate)

	def create_react_files(self):
		app_react = self.spa_path / ("src/App.tsx" if self.use_typescript else "src/App.jsx")

		# Use Shadcn boilerplate if enabled
		if self.add_shadcn:
			create_file(app_react, SHADCN_REACT_APP_BOILERPLATE)
			# Also create the theme provider
			components_dir = self.spa_path / "src/components"
			components_dir.mkdir(exist_ok=True)
			theme_provider = components_dir / "theme-provider.tsx"
			create_file(theme_provider, THEME_PROVIDER_BOILERPLATE)
		else:
			create_file(app_react, APP_REACT_BOILERPLATE)

	def setup_typescript_paths(self):
		"""Setup TypeScript path aliases for better imports"""
		click.echo("Setting up TypeScript path aliases...")

		# Update tsconfig.json with path aliases
		tsconfig_path: Path = self.spa_path / "tsconfig.json"
		if tsconfig_path.exists():
			# Replace the entire tsconfig.json with our boilerplate
			create_file(tsconfig_path, TSCONFIG_JSON_BOILERPLATE)

		# Update tsconfig.app.json with path aliases
		tsconfig_app_path: Path = self.spa_path / "tsconfig.app.json"
		if tsconfig_app_path.exists():
			content = tsconfig_app_path.read_text()
			# Add paths to compilerOptions if not already there
			if '"paths"' not in content and '"@/*"' not in content:
				# Find the compilerOptions section and add paths
				content = content.replace(
					'"compilerOptions": {',
					'"compilerOptions": {\n' + TSCONFIG_APP_JSON_PATHS
				)
				tsconfig_app_path.write_text(content)

	def setup_shadcn(self):
		"""Setup Shadcn UI for beautiful components"""
		click.echo("Setting up Shadcn UI...")

		# Install @types/node (required for path resolution)
		subprocess.run(
			["npm", "install", "-D", "@types/node"],
			cwd=self.spa_path,
		)

		# Run shadcn init with default options
		# Using environment variables to provide answers to the prompts
		import os
		env = os.environ.copy()

		# Create components.json directly instead of running init interactively
		components_json = {
			"$schema": "https://ui.shadcn.com/schema.json",
			"style": "new-york",
			"rsc": False,
			"tsx": True,
			"tailwind": {
				"config": "",
				"css": "src/index.css",
				"baseColor": "neutral",
				"cssVariables": True,
				"prefix": ""
			},
			"aliases": {
				"components": "@/components",
				"utils": "@/lib/utils",
				"ui": "@/components/ui",
				"lib": "@/lib",
				"hooks": "@/hooks"
			}
		}

		import json
		components_json_path = self.spa_path / "components.json"
		with components_json_path.open("w") as f:
			json.dump(components_json, f, indent=2)

		# Create lib directory and utils.ts
		lib_dir = self.spa_path / "src/lib"
		lib_dir.mkdir(exist_ok=True)

		utils_content = '''import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''
		create_file(lib_dir / "utils.ts", utils_content)

		# Install required dependencies
		subprocess.run(
			["npm", "install", "clsx", "tailwind-merge"],
			cwd=self.spa_path,
		)

		# Install starter components automatically
		click.echo("Installing starter components (button, card)...")

		if self.framework == "react":
			# Install radix icons for theme toggle
			subprocess.run(
				["npm", "install", "@radix-ui/react-icons"],
				cwd=self.spa_path,
			)

			# Install shadcn components
			subprocess.run(
				["npx", "shadcn@latest", "add", "button", "card", "-y"],
				cwd=self.spa_path,
			)
		elif self.framework == "vue":
			# Install radix-vue and icons
			subprocess.run(
				["npm", "install", "radix-vue", "@radix-ui/react-icons"],
				cwd=self.spa_path,
			)

			# Install shadcn-vue components
			subprocess.run(
				["npx", "shadcn-vue@latest", "add", "button", "card", "-y"],
				cwd=self.spa_path,
			)

		click.echo("✓ Shadcn UI configured with starter components!")
		click.echo(f"  Add more: npx shadcn{'- vue' if self.framework == 'vue' else ''}@latest add <component>")
