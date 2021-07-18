import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home,
	},
];

const router = createRouter({
	base: '/vision/',
	history: createWebHashHistory(),
	routes,
});

export default router;
