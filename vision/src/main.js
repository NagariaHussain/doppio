import { createApp, getCurrentInstance } from 'vue';
import App from './App.vue';
import './index.css';
import router from './router';
import call from './controllers/call';
import resourceManager from './resourceManager';

const app = createApp(App);

app.use(router);
app.use(resourceManager, {"test": "secret"});
app.mount('#app');
