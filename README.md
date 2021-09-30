## Doppio

A Frappe App to setup and manage single page applications (using Vue 3) on any other custom Frappe App.

### Installation

In your bench directory:

```bash
$ bench get-app https://github.com/NagariaHussain/doppio
```

This will install the `Doppio` frappe app on your bench and enable some custom bench CLI commands
that will ease the process of attaching a SPA to your Frappe Application.

### Usage

Setting up a new Single Page Application

```bash
$ bench add-spa --app <app-name> [--tailwindcss]
```

You will be prompted to enter a name for your single page application, this will be the name of the directory and the URI path at which the application will be served. For instance, if you enter `dashboard` (default), then a folder named `dashboard` will be created inside your app's root directory and the application will be served at `/dashboard`.

You can optionally pass the `--tailwindcss` flag which will also setup tailwindCSS (who doesn't like tailwind!) along with the Vue 3 application.

The above command will do the follwing things:

1. Scaffold a new Vue 3 starter application (using [Vite](https://vitejs.dev/))

1. Add and configure Vue router

1. Link utility and controller files to make the connection with Frappe backend a breeze!

1. Configure Vite's proxy options (which will be helpful in development), check the `proxyOptions.js` file to see to what ports the Vite dev server proxies the requests (you frappe bench server).

1. Optionally, installs and set's up tailwindCSS.

1. Update the `website_route_rules` hook (in `hooks.py` of your app) to handle the routing of this SPA.

Once the setup is complete, you can `cd` into the SPA directory of your app (e.g. `dashboard`) and run:

```bash
$ yarn dev
```

This will start a development server at port `8080` by default (any other port if this port's already in use). You can view the running application at: `<site>:8080`.

## Building for Production

The below command builds the application and places it in the `www` directory of your frappe app:

```bash
$ cd <your-spa-name> && yarn build
```

Check the `package.json` file inside the Vue application directory to learn more about the dev server / build steps.

If you already have a package.json file with scripts in your app's root directory, you can add the following two scripts to your app's package.json file in order for the `bench build` command to work as expected:

```json
"dev": "cd <your-spa-folder> && yarn dev",
"build": "cd <your-spa-folder> && yarn build"
```

### License

Do whatever you want with the code. If you can sell it, go ahead an make some money!
