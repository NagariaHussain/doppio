import { createApp, reactive } from 'vue';
import App from './App.vue';
import './index.css';
import router from './router';
import resourceManager from './resourceManager';
import Auth from './controllers/auth';
import call from './controllers/call';
import socket from './controllers/socket';

const app = createApp(App);
const auth = reactive(new Auth());

// Plugins
app.use(router);
app.use(resourceManager);

// Global Properties,
// components can inject this
app.provide('$auth', auth);
app.provide('$call', call);
app.provide('$socket', socket);

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
		// if already logged in, route to /welcome
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

app.mount('#app');
