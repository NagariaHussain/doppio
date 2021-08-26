import click
import subprocess

from pathlib import Path

APP_VUE_BOILERPLATE = """<template>
	<div>
		<button v-if="$auth.isLoggedIn">Logout</button>
		<router-view />
	</div>
</template>


<script>
export default {
	inject: ['$auth']
};
</script>
"""

HOME_VUE_BOILERPLATE = """<template>
	<h1>Home Page</h1>
	<button>Ping</button>
</template>
"""

LOGIN_VUE_BOILERPLATE = """<template>
  <div class="min-h-screen bg-white flex">
    <div class="mx-auto w-full max-w-sm lg:w-96">
      <form @submit.prevent="login" class="space-y-6">
        <label for="email"> Username: </label>
        <input type="text" v-model="email" />
        <br />
        <label for="password"> Password: </label>
        <input type="password" v-model="password" />

        <button
          class="bg-blue-500 block text-white p-2 hover:bg-blue-700"
          type="submit"
        >
          Sign in
        </button>
      </form>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      email: null,
      password: null,
    };
  },
  inject: ["$auth"],
  async mounted() {
    if (this.$route?.query?.route) {
      this.redirect_route = this.$route.query.route;
      this.$router.replace({ query: null });
    }
  },
  methods: {
    async login() {
      if (this.email && this.password) {
        let res = await this.$auth.login(this.email, this.password);
        if (res) {
          this.$router.push({ name: "Home" });
        }
      }
    },
  },
};
</script>
"""

VITE_CONFIG_BOILERPLATE = """import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 8080,
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

	setup_router(spa_path, name)
	setup_vue_files(spa_path)

	# Start the dev server
	subprocess.run(["yarn", "dev"], cwd=spa_path)


def setup_router(spa_path, spa_name):
	# Setup vue router
	router_dir_path: Path = spa_path / "src/router"

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


def setup_vue_files(spa_path: Path):
	app_vue = spa_path / "src/App.vue"

	with app_vue.open("w") as f:
		f.write(APP_VUE_BOILERPLATE)

	views_dir: Path = spa_path / "src/views"

	if not views_dir.exists():
		views_dir.mkdir()

	home_vue = views_dir / "Home.vue"
	login_vue = views_dir / "Login.vue"

	if not home_vue.exists():
		home_vue.touch()
	with home_vue.open("w") as f:
		f.write(HOME_VUE_BOILERPLATE)

	if not login_vue.exists():
		login_vue.touch()
	with login_vue.open("w") as f:
		f.write(LOGIN_VUE_BOILERPLATE)


commands = [generate_spa]
