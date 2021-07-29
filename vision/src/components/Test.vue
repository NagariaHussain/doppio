<template>
	<div class="bg-white shadow-lg rounded-lg p-5 m-5">
		<h2 v-if="this.$auth.isLoggedIn">Secret for user</h2>
		<button
			@click="this.$auth.isLoggedIn ? this.$auth.logout() : login()"
			class="text-white bg-indigo-700 p-2 rounded mt-3 hover:bg-indigo-800"
		>
			{{ this.$auth.isLoggedIn ? 'Log Out' : 'Log in' }}
		</button>
		<h2 class="font-semibold text-lg">
			Hello, {{ userName }}, logged in: {{ this.$auth.isLoggedIn }}
		</h2>
		<button
			@click="insertNewNumber()"
			class="text-white bg-indigo-700 p-2 rounded mt-3 hover:bg-indigo-800"
		>
			Add number
		</button>
		<ul class="mt-3">
			<li v-for="n of numbers" :key="n">{{ n }}</li>
		</ul>
		<hr />

		<h2 class="font-semibold text-lg mt-3">Watching changes</h2>

		<p>Current User: {{ user.name }}</p>
		<button
			@click="user.setName('Hussain')"
			class="text-white bg-indigo-700 p-2 rounded mt-3 hover:bg-indigo-800"
		>
			Switch User
		</button>

		<h2 class="font-semibold text-lg mt-3">Playing with computed</h2>
		<input type="text" v-model="secretMessage" />
		<p>Secret Message: {{ encryptedMessage || 'None yet' }}</p>
	</div>
</template>

<script>
import { toRefs } from 'vue';
import useComposeTest from '../composables/useComposeTest';

export default {
	inject: ['$auth'],
	props: {
		userName: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			email: 'Administrator',
			password: 'admin'
		}
	},
	setup(props) {
		// will remove reactivity
		// let { userName } = props;
		let { userName } = toRefs(props);

		let { user, numbers, secretMessage, insertNewNumber, encryptedMessage } =
			useComposeTest(userName);

		return { user, numbers, secretMessage, insertNewNumber, encryptedMessage };
	},
	methods: {
		async login() {
			if (this.email && this.password) {
				let res = await this.$auth.login(this.email, this.password);
				if (res) {
					console.log('logged in successfully, redirecting...');
				}
			}
		},
	},
};
</script>
