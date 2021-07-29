import { createApp, reactive } from 'vue';
import App from './App.vue';
import './index.css';
import router from './router';
import resourceManager from './resourceManager';
import Auth from './controllers/auth';
import call from './controllers/call';

const app = createApp(App);
const auth = reactive(new Auth());

app.use(router);
app.use(resourceManager);

app.config.globalProperties.$call = call;
app.config.globalProperties.$auth = auth;

app.provide('$auth', auth);
app.mount('#app');
