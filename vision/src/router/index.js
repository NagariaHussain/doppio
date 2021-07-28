import { createRouter, createWebHistory } from 'vue-router';
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
	history: createWebHistory(),
	routes,
});

export default router;
