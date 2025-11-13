# Doppio

A Frappe App to setup and manage single page applications and custom desk pages (using Vue 3 or React) on your custom Frappe App.

## Installation

In your bench directory:

```bash
bench get-app https://github.com/NagariaHussain/doppio
```

This will install the `Doppio` frappe app on your bench and enable some custom bench CLI commands
that will ease the process of attaching a SPA to your Frappe Application.

## Setting Up React/Vue SPA

To set up a new Single Page Application, you can run the following command in your bench directory:

```bash
bench add-spa --app <app-name> [--tailwindcss] [--typescript] [--shadcn]

# or just, and answer the prompts
bench add-spa
```

You will be prompted to enter a name for your single page application, this will be the name of the directory and the URI path at which the application will be served. For instance, if you enter `dashboard` (default), then a folder named `dashboard` will be created inside your app's root directory and the application will be served at `/dashboard`.

You will then be asked to select the framework you prefer: React or Vue.

You can also select whether you want to use Typescript or Javascript.

You can optionally pass the following flags:
- `--tailwindcss` - Sets up Tailwind CSS v4 with the new `@tailwindcss/vite` plugin
- `--typescript` - Configures the project with TypeScript support and path aliases
- `--shadcn` - **The full package!** Sets up Shadcn UI with:
  - Pre-installed Button and Card components
  - Dark mode support with theme toggle (React) or system preference (Vue)
  - Beautiful starter template with card-based layout
  - All CSS variables for theming
  - Ready-to-use component library (requires `--typescript` and `--tailwindcss`)

The above command will do the following things:

### For Vue 3

1. Scaffold a new Vue 3 starter application (using [Vite](https://vitejs.dev/))

2. Add and configure Vue router

3. Link utility and controller files to make the connection with Frappe backend a breeze!

4. Configure Vite's proxy options (which will be helpful in development), check the `proxyOptions.js` file to see to what ports the Vite dev server proxies the requests (you frappe bench server).

5. Optionally, installs and set up Tailwind CSS v4.

6. Optionally, sets up TypeScript path aliases for cleaner imports (`@/components`, etc.)

7. Optionally, sets up Shadcn UI with pre-configured component library.

8. Update the `website_route_rules` hook (in `hooks.py` of your app) to handle the routing of this SPA.

### For React

1. Scaffold a new React starter application (using [Vite](https://vitejs.dev/))

2. Add and configure [frappe-react-sdk](https://github.com/nikkothari22/frappe-react-sdk) to make the connection with Frappe backend a breeze!

3. Configure Vite's proxy options (which will be helpful in development), check the `proxyOptions.js` file to see to what ports the Vite dev server proxies the requests (you frappe bench server).

4. Optionally, installs and set up Tailwind CSS v4.

5. Optionally, sets up TypeScript path aliases for cleaner imports (`@/components`, etc.)

6. Optionally, sets up Shadcn UI with pre-configured component library.

7. Update the `website_route_rules` hook (in `hooks.py` of your app) to handle the routing of this SPA.

Once the setup is complete, you can `cd` into the SPA directory of your app (e.g. `dashboard`) and run:

```bash
yarn dev
```

This will start a development server at port `8080` by default (any other port if this port's already in use). You can view the running application at: `<site>:8080`.

### 🎨 Shadcn UI - Beautiful Frontends in Seconds

When you use the `--shadcn` flag, your SPA comes with:

**Out of the box:**
- ✨ **Beautiful UI** - Professional card-based layout with proper spacing and typography
- 🌓 **Dark Mode** - Full dark mode support with theme toggle (React) or system preference
- 🎯 **Pre-installed Components** - Button and Card components ready to use
- 🎨 **Theme Variables** - Complete CSS variable system for customization
- 📦 **Component Library** - Access to 50+ Shadcn components

**Example usage:**
```bash
# Create a beautiful SPA with all the bells and whistles
bench add-spa --app myapp --typescript --tailwindcss --shadcn

# Then add more components as needed
cd myapp/dashboard
npx shadcn@latest add form input label select
```

**What you get:**
- React apps get a theme provider with light/dark/system modes
- Vue apps get Shadcn-Vue with full component support
- Both get a beautiful welcome screen showcasing the features
- All components use Tailwind CSS v4 with proper theming

## Adding FrappeUI

If you want to add a [frappe-ui](https://github.com/frappe/frappe-ui) starter project to your custom app, you can do that using just a single command:

```bash
bench add-frappe-ui
```

## Creating Desk Pages

If you want to setup Vue 3 or React powered custom desk pages, you can do that with just a single command:

```bash
bench --site <site-name> add-desk-page --app <app-name>
```

Follow the prompt to select the framework of your choice and **everything will be setup for you auto-magically**! Once the setup is done, the page will be opened up in the browser.

> Note: Restart your bench to get auto-reload on file changes for your custom app

## Building for Production

The below command builds the application and places it in the `www` directory of your frappe app:

```bash
cd <your-spa-name> && yarn build
```

Check the `package.json` file inside the Vue application directory to learn more about the dev server / build steps.

If you already have a package.json file with scripts in your app's root directory, you can add the following two scripts to your app's package.json file in order for the `bench build` command to work as expected:

```json
"dev": "cd <your-spa-folder> && yarn dev",
"build": "cd <your-spa-folder> && yarn build"
```

### License

[MIT](./license.txt)
