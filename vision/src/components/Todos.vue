<template>
	<p v-if="$resources.todos.loading">Loading todos...</p>
	<ul v-else>
		<li v-for="todo in todos" :key="todo.name">
			<div class="p-3 bg-gray-800 rounded-lg my-2 max-w-sm">
				<div class="flex flex-row justify-between mb-3">
					<p
						class="
							inline-flex
							items-center
							px-2.5
							py-0.5
							rounded-md
							text-sm
							font-medium
							bg-indigo-100
							text-indigo-800
						"
					>
						{{ todo.status }}
					</p>
					<span
						class="
							inline-flex
							items-center
							px-2.5
							py-0.5
							rounded-md
							text-sm
							font-medium
							bg-yellow-100
							text-yellow-800
						"
					>
						{{ todo.priority }}
					</span>
				</div>
				<div v-html="todo.description" class="text-white"></div>
			</div>
		</li>
	</ul>
</template>

<script>
export default {
	resources: {
		todos() {
			return {
				method: 'doppio.api.main.get_my_todos',
				auto: true,
			};
		},
	},
	computed: {
		todos() {
			return this.$resources.todos.data;
		},
	},
};
</script>
