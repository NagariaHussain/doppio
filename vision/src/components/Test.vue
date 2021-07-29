<template>
	<div class="bg-white shadow-lg rounded-lg p-5 m-5">
		<h2 class="font-semibold text-lg">Hello, {{ userName }}</h2>

		<h2 class="font-semibold text-lg mt-3">Your ToDos:</h2>
		<Todos />

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
import Todos from './Todos.vue';

export default {
	props: {
		userName: {
			type: String,
			required: true,
		},
	},
	components: {
		Todos,
	},
	data() {
		return {
			email: 'Administrator',
			password: 'admin',
		};
	},
	setup(props) {
		// will remove reactivity
		// let { userName } = props;
		let { userName } = toRefs(props);

		let { user, numbers, secretMessage, insertNewNumber, encryptedMessage } =
			useComposeTest(userName);

		return { user, numbers, secretMessage, insertNewNumber, encryptedMessage };
	},
};
</script>
