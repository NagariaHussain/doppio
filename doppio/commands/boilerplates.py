APP_VUE_BOILERPLATE = """<template>
	<div>
		<button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout</button>
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
  <div>
	<h1>Home Page</h1>
	<!-- Fetch the resource on click -->
	<button @click="$resources.ping.fetch()">Ping</button>
  </div>
</template>

<script>
export default {
  resources: {
	ping() {
	  return {
		method: "frappe.ping", // Method to call on backend
		onSuccess(d) {
		  alert(d);
		},
	  };
	},
  },
};
</script>
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

VUE_VITE_CONFIG_BOILERPLATE = """import path from "path"
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import tailwindcss from "@tailwindcss/vite"
import proxyOptions from "./proxyOptions"

// https://vite.dev/config/
export default defineConfig({
	plugins: [vue(), tailwindcss()],
	server: {
		port: 8080,
		host: "0.0.0.0",
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "./src"),
		}
	},
	build: {
		outDir: "../{{app}}/public/{{name}}",
		emptyOutDir: true,
		target: "es2015",
	},
})
"""

PROXY_OPTIONS_BOILERPLATE = """const common_site_config = require('../../../sites/common_site_config.json');
const { webserver_port } = common_site_config;

export default {
	'^/(app|api|assets|files|private)': {
		target: `http://127.0.0.1:${webserver_port}`,
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
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";

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


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: 'Login', query: { route: to.path } });
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

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

REACT_VITE_CONFIG_BOILERPLATE = """import path from "path"
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"
import proxyOptions from "./proxyOptions"

// https://vite.dev/config/
export default defineConfig({
	plugins: [react(), tailwindcss()],
	server: {
		port: 8080,
		host: "0.0.0.0",
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "./src"),
		}
	},
	build: {
		outDir: "../{{app}}/public/{{name}}",
		emptyOutDir: true,
		target: "es2015",
	},
})
"""

APP_REACT_BOILERPLATE = """import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { FrappeProvider } from 'frappe-react-sdk'
function App() {
  const [count, setCount] = useState(0)

  return (
	<div className="App">
	  <FrappeProvider>
		<div>
	  <div>
		<a href="https://vitejs.dev" target="_blank">
		  <img src="/vite.svg" className="logo" alt="Vite logo" />
		</a>
		<a href="https://reactjs.org" target="_blank">
		  <img src={reactLogo} className="logo react" alt="React logo" />
		</a>
	  </div>
	  <h1>Vite + React + Frappe</h1>
	  <div className="card">
		<button onClick={() => setCount((count) => count + 1)}>
		  count is {count}
		</button>
		<p>
		  Edit <code>src/App.jsx</code> and save to test HMR
		</p>
	  </div>
	  <p className="read-the-docs">
		Click on the Vite and React logos to learn more
	  </p>
	  </div>
	  </FrappeProvider>
	</div>
  )
}

export default App
"""

DESK_PAGE_JS_TEMPLATE = """frappe.pages["{{ page_name }}"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("{{ page_title }}"),
		single_column: true,
	});
};

frappe.pages["{{ page_name }}"].on_page_show = function (wrapper) {
	load_desk_page(wrapper);
};

function load_desk_page(wrapper) {
	let $parent = $(wrapper).find(".layout-main-section");
	$parent.empty();

	frappe.require("{{ scrubbed_name }}.bundle.{{ bundle_type }}").then(() => {
		frappe.{{ scrubbed_name }} = new frappe.ui.{{ pascal_cased_name }}({
			wrapper: $parent,
			page: wrapper.page,
		});
	});
}
"""

DESK_PAGE_JS_BUNDLE_TEMPLATE_VUE = """import { createApp } from "vue";
import App from "./App.vue";


class {{ pascal_cased_name }} {
	constructor({ page, wrapper }) {
		this.$wrapper = $(wrapper);
		this.page = page;

		this.init();
	}

	init() {
		this.setup_page_actions();
		this.setup_app();
	}

	setup_page_actions() {
		// setup page actions
		this.primary_btn = this.page.set_primary_action(__("Print Message"), () =>
	  frappe.msgprint("Hello My Page!")
		);
	}

	setup_app() {
		// create a vue instance
		let app = createApp(App);
		// mount the app
		this.${{ scrubbed_name }} = app.mount(this.$wrapper.get(0));
	}
}

frappe.provide("frappe.ui");
frappe.ui.{{ pascal_cased_name }} = {{ pascal_cased_name }};
export default {{ pascal_cased_name }};
"""

DESK_PAGE_VUE_APP_COMPONENT_BOILERPLATE = """<script setup>
import { ref } from "vue";

const dynamicMessage = ref("Hello from App.vue");
</script>
<template>
  <div>
	<h3>{{ dynamicMessage }}</h3>
    <h4>Start editing at {{ app_component_path }}</h4>
  </div>
</template>"""

DESK_PAGE_REACT_APP_COMPONENT_BOILERPLATE = """import * as React from "react";

export function App() {
  const dynamicMessage = React.useState("Hello from App.jsx");
  return (
    <div className="m-4">
      <h3>{dynamicMessage}</h3>
      <h4>Start editing at {{ app_component_path }}</h4>
    </div>
  );
}"""

DESK_PAGE_JSX_BUNDLE_TEMPLATE_REACT = """import * as React from "react";
import { App } from "./App";
import { createRoot } from "react-dom/client";


class {{ pascal_cased_name }} {
	constructor({ page, wrapper }) {
		this.$wrapper = $(wrapper);
		this.page = page;

		this.init();
	}

	init() {
		this.setup_page_actions();
		this.setup_app();
	}

	setup_page_actions() {
		// setup page actions
		this.primary_btn = this.page.set_primary_action(__("Print Message"), () =>
	  		frappe.msgprint("Hello My Page!")
		);
	}

	setup_app() {
		// create and mount the react app
		const root = createRoot(this.$wrapper.get(0));
		root.render(<App />);
		this.${{ scrubbed_name }} = root;
	}
}

frappe.provide("frappe.ui");
frappe.ui.{{ pascal_cased_name }} = {{ pascal_cased_name }};
export default {{ pascal_cased_name }};
"""

TSCONFIG_JSON_BOILERPLATE = """{
  "files": [],
  "references": [
    {
      "path": "./tsconfig.app.json"
    },
    {
      "path": "./tsconfig.node.json"
    }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
"""

TSCONFIG_APP_JSON_PATHS = """    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },"""

# Shadcn-enabled beautiful boilerplates

SHADCN_REACT_APP_BOILERPLATE = """import { ThemeProvider } from "@/components/theme-provider"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MoonIcon, SunIcon } from "@radix-ui/react-icons"
import { useTheme } from "@/components/theme-provider"
import './App.css'

function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
    >
      <SunIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <MoonIcon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="ui-theme">
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-bold">Welcome to Your App</h1>
            <ThemeToggle />
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Getting Started</CardTitle>
                <CardDescription>Your beautiful frontend is ready!</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Edit <code className="bg-muted px-1 py-0.5 rounded">src/App.tsx</code> to get started.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Shadcn UI</CardTitle>
                <CardDescription>Beautiful components at your fingertips</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Add more components with:
                </p>
                <code className="bg-muted px-2 py-1 rounded text-xs">
                  npx shadcn@latest add [component]
                </code>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Dark Mode</CardTitle>
                <CardDescription>Toggle theme with one click</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Dark mode is enabled by default. Try clicking the theme toggle button!
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </ThemeProvider>
  )
}

export default App
"""

THEME_PROVIDER_BOILERPLATE = """import { createContext, useContext, useEffect, useState } from "react"

type Theme = "dark" | "light" | "system"

type ThemeProviderProps = {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

type ThemeProviderState = {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
}

const ThemeProviderContext = createContext<ThemeProviderState>(initialState)

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "vite-ui-theme",
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  )

  useEffect(() => {
    const root = window.document.documentElement

    root.classList.remove("light", "dark")

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
        ? "dark"
        : "light"

      root.classList.add(systemTheme)
      return
    }

    root.classList.add(theme)
  }, [theme])

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme)
      setTheme(theme)
    },
  }

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext)

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider")

  return context
}
"""

SHADCN_VUE_APP_BOILERPLATE = """<template>
  <div class="min-h-screen bg-background">
    <div class="container mx-auto p-8">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-bold">Welcome to Your App</h1>
        <Button
          v-if="$auth.isLoggedIn"
          variant="outline"
          @click="$auth.logout()"
        >
          Logout
        </Button>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script>

<script lang="ts">
export default {
  inject: ['$auth']
}
</script>
"""

SHADCN_VUE_HOME_BOILERPLATE = """<template>
  <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
    <Card>
      <CardHeader>
        <CardTitle>Getting Started</CardTitle>
        <CardDescription>Your beautiful frontend is ready!</CardDescription>
      </CardHeader>
      <CardContent>
        <p class="text-sm text-muted-foreground">
          Edit <code class="bg-muted px-1 py-0.5 rounded">src/views/Home.vue</code> to get started.
        </p>
      </CardContent>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle>Shadcn UI</CardTitle>
        <CardDescription>Beautiful components at your fingertips</CardDescription>
      </CardHeader>
      <CardContent>
        <p class="text-sm text-muted-foreground mb-4">
          Add more components with:
        </p>
        <code class="bg-muted px-2 py-1 rounded text-xs">
          npx shadcn-vue@latest add [component]
        </code>
      </CardContent>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle>Frappe Integration</CardTitle>
        <CardDescription>Connected to your Frappe backend</CardDescription>
      </CardHeader>
      <CardContent>
        <Button @click="$resources.ping.fetch()">
          Ping Server
        </Button>
        <p v-if="$resources.ping.data" class="text-sm text-muted-foreground mt-4">
          Response: {{ $resources.ping.data }}
        </p>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
</script>

<script lang="ts">
export default {
  resources: {
    ping() {
      return {
        method: "frappe.ping",
        onSuccess(d: any) {
          console.log("Ping successful:", d)
        },
      }
    },
  },
}
</script>
"""
