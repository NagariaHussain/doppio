import click
import subprocess

from pathlib import Path

VITE_CONFIG_BOILERPLATE = """
import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 3000,
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../{{app}}/public/{{name}}',
		emptyOutDir: true,
		target: 'es2015',
	},
});
"""

PROXY_OPTIONS_BOILERPLATE = """const common_site_config = require('../../../sites/common_site_config.json');
const { webserver_port } = common_site_config;

module.exports = {
	'^/(app|api|assets|files)': {
		target: `http://localhost:${webserver_port}`,
		ws: true,
		router: function(req) {
			const site_name = req.headers.host.split(':')[0];
			return `http://${site_name}:${webserver_port}`;
		}
	}
};
"""

MAIN_JS_BOILERPLATE = """import { createApp, reactive } from "vue";
import App from "./App.vue";

import router from './router';
import resourceManager from "../../../doppio/vision/src/resourceManager";
import call from "../../../doppio/vision/src/controllers/call";
import socket from "../../../doppio/vision/src/controllers/socket";
import Auth from "../../../doppio/vision/src/controllers/auth";

const app = createApp(App);
const auth = reactive(new Auth());

// Plugins
app.use(router);
app.use(resourceManager);

// Global Properties,
// components can inject this
app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);

app.mount("#app");
"""

ROUTER_INDEX_BOILERPLATE = """import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  ...authRoutes,
];

const router = createRouter({
  base: "/{{name}}/",
  history: createWebHistory(),
  routes,
});

export default router;
"""


AUTH_ROUTES_BOILERPLATE = """export default [
    {
		path: '/login',
		name: 'Login',
		component: () =>
			import(/* webpackChunkName: "login" */ '../views/Login.vue'),
		meta: {
			isLoginPage: true
		},
		props: true
	}
]
"""


@click.command("add-spa")
@click.option("--name", default="dashboard", prompt="Dashboard Name")
@click.option("--app")
def generate_spa(name, app):
	if not app:
		click.echo("Please provide an app with --app")
		return

	click.echo("Generating spa...")
	app_path = Path("../apps") / app

	# Tasks
	# Run "yarn create vite {name} --template vue"
	print("Scafolding vue project...")
	subprocess.run(["yarn", "create", "vite", name, "--template", "vue"], cwd=app_path)

	# Install router and other npm packages
	# yarn add vue-router@4 socket.io-client@2.4.0
	print("Installing dependencies...")
	spa_path = app_path / name
	subprocess.run(
		["yarn", "add", "vue-router@^4", "socket.io-client@^2.4.0"], cwd=spa_path
	)

	# Link controller files in main.js
	print("Linking controller files...")
	main_js: Path = app_path / f"{name}/src/main.js"

	if main_js.exists():
		with main_js.open("w") as f:
			f.write(MAIN_JS_BOILERPLATE)
	else:
		click.echo("src/main.js not found!")
		return

	setup_router(spa_path, name)

	# Setup proxy options file
	proxy_options_file: Path = spa_path / "proxyOptions.js"
	proxy_options_file.touch()
	with proxy_options_file.open("w") as f:
		f.write(PROXY_OPTIONS_BOILERPLATE)

	vite_config_file: Path = spa_path / "vite.config.js"
	if not vite_config_file.exists():
		vite_config_file.touch()
	with vite_config_file.open("w") as f:
		boilerplate = VITE_CONFIG_BOILERPLATE.replace("{{app}}", app)
		boilerplate = boilerplate.replace("{{name}}", name)
		f.write(boilerplate)


def setup_router(spa_path, spa_name):
	# Setup vue router
	router_dir_path: Path = spa_path / "router"

	# Create router directory
	router_dir_path.mkdir()

	# Create files
	router_index_file = router_dir_path / "index.js"
	router_index_file.touch()
	with router_index_file.open("w") as f:
		boilerplate = ROUTER_INDEX_BOILERPLATE.replace("{{name}}", spa_name)
		f.write(boilerplate)

	auth_routes_file = router_dir_path / "auth.js"
	auth_routes_file.touch()
	with auth_routes_file.open("w") as f:
		f.write(AUTH_ROUTES_BOILERPLATE)


commands = [generate_spa]
