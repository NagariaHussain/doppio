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

app.mount('#app');
