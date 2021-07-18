import { createApp } from 'vue';
import App from './App.vue';
import './index.css';
import router from './router';
import call from './controllers/call';

const app = createApp(App);

app.use(router);
app.provide('$call', call);
app.mount('#app');
