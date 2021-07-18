<template>
	<div>
		<Navbar />
		<div class="font-sans antialiased text-gray-900">
			<div class="flex h-screen overflow-hidden">
				<div class="flex flex-1 overflow-y-auto" :class="'sm:bg-gray-50'">
					<div class="flex-1">
						<!-- <Navbar v-if="$auth.isLoggedIn" /> -->
						<div class="container mx-auto">
							<router-view />
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';

// This starter template is using Vue 3 experimental <script setup> SFCs
// Check out https://github.com/vuejs/rfcs/blob/master/active-rfcs/0040-script-setup.md
</script>
