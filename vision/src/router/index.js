import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Courses from '../views/Courses.vue';

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home,
	},
	{
		path: '/courses',
		name: 'Course',
		component: Courses,
	}
];

const router = createRouter({
	base: '/',
	history: createWebHistory(),
	routes,
});

export default router;
