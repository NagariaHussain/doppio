<template>
	<div>
		<!-- <header class="bg-white shadow-sm">
			<div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
				<h1 class="text-lg leading-6 font-semibold text-gray-900">Dashboard</h1>
			</div>
		</header> -->
		<div>
			<Test userName="@NagariaHussain" />
		</div>
		<main>
			<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
				<div class="px-4 py-4 sm:px-0">
					<div>
						<p>$resources.ping.loading: {{ $resources.ping.loading }}</p>
						<p>loading computed: {{ isLoading }}</p>
						<p>pong computed property: {{ pong }}</p>
						<p>this.$resources.ping.data: {{ this.$resources.ping.data }}</p>
					</div>
					<button
						class="bg-red-500 rounded px-2 py-2 text-white"
						@click="$resources.ping.reload()"
					>
						Click me
					</button>
				</div>

				<div>User is logged in: {{ this.$auth.isLoggedIn }}</div>
				<button>Ping</button>
			</div>
		</main>
	</div>
</template>

<script>
import Test from '../components/Test.vue';

export default {
	name: 'Home',
	inject: ['$auth', '$socket'],
	mounted() {
		this.$socket.on('hussain', (d) => {
			console.log('hussain event', d);
		});
	},
	data() {
		return {};
	},
	components: {
		Test,
	},
	resources: {
		ping() {
			return {
				method: 'doppio.api.main.ping',
				delay: 2,
				// auto: true,
			};
		},
	},
	computed: {
		pong() {
			console.log('Home.vue, computed', this.$resources);
			console.log('Home.vue, computed', this.$resources.ping);
			if (!this.$resources.ping.data) {
				return 'No data';
			}

			return this.$resources.ping.data;
		},
		isLoading() {
			return this.$resources.ping.loading;
		},
	},
};
</script>
