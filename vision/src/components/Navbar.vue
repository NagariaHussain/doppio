<template>
	<Disclosure as="header" class="bg-white shadow" v-slot="{ open }">
		<div
			class="
				max-w-7xl
				mx-auto
				px-2
				sm:px-4
				lg:divide-y lg:divide-gray-200 lg:px-8
			"
		>
			<div class="relative h-16 flex justify-between">
				<div class="relative z-10 px-2 flex lg:px-0">
					<div class="flex-shrink-0 flex items-center">
						<img
							class="block h-8 w-auto"
							src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
							alt="Workflow"
						/>
					</div>
				</div>
				<div
					class="
						relative
						z-0
						flex-1
						px-2
						flex
						items-center
						justify-center
						sm:absolute sm:inset-0
					"
				>
					<div class="w-full sm:max-w-xs">
						<label for="search" class="sr-only">Search</label>
						<div class="relative">
							<div
								class="
									pointer-events-none
									absolute
									inset-y-0
									left-0
									pl-3
									flex
									items-center
								"
							>
								<SearchIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
							</div>
							<input
								id="search"
								name="search"
								class="
									block
									w-full
									bg-white
									border border-gray-300
									rounded-md
									py-2
									pl-10
									pr-3
									text-sm
									placeholder-gray-500
									focus:outline-none
									focus:text-gray-900
									focus:placeholder-gray-400
									focus:ring-1
									focus:ring-indigo-500
									focus:border-indigo-500
									sm:text-sm
								"
								placeholder="Search"
								type="search"
							/>
						</div>
					</div>
				</div>
				<div class="relative z-10 flex items-center lg:hidden">
					<!-- Mobile menu button -->
					<DisclosureButton
						class="
							rounded-md
							p-2
							inline-flex
							items-center
							justify-center
							text-gray-400
							hover:bg-gray-100 hover:text-gray-500
							focus:outline-none
							focus:ring-2
							focus:ring-inset
							focus:ring-indigo-500
						"
					>
						<span class="sr-only">Open menu</span>
						<MenuIcon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
						<XIcon v-else class="block h-6 w-6" aria-hidden="true" />
					</DisclosureButton>
				</div>
				<div class="hidden lg:relative lg:z-10 lg:ml-4 lg:flex lg:items-center">
					<button
						class="
							flex-shrink-0
							bg-white
							rounded-full
							p-1
							text-gray-400
							hover:text-gray-500
							focus:outline-none
							focus:ring-2
							focus:ring-offset-2
							focus:ring-indigo-500
						"
					>
						<span class="sr-only">View notifications</span>
						<BellIcon class="h-6 w-6" aria-hidden="true" />
					</button>

					<!-- Profile dropdown -->
					<Menu as="div" class="flex-shrink-0 relative ml-4">
						<div>
							<MenuButton
								class="
									bg-white
									rounded-full
									flex
									focus:outline-none
									focus:ring-2
									focus:ring-offset-2
									focus:ring-indigo-500
								"
							>
								<span class="sr-only">Open user menu</span>
								<img class="h-8 w-8 rounded-full" :src="user.imageUrl" alt="" />
							</MenuButton>
						</div>
						<transition
							enter-active-class="transition ease-out duration-100"
							enter-from-class="transform opacity-0 scale-95"
							enter-to-class="transform opacity-100 scale-100"
							leave-active-class="transition ease-in duration-75"
							leave-from-class="transform opacity-100 scale-100"
							leave-to-class="transform opacity-0 scale-95"
						>
							<MenuItems
								class="
									origin-top-right
									absolute
									right-0
									mt-2
									w-48
									rounded-md
									shadow-lg
									bg-white
									ring-1 ring-black ring-opacity-5
									py-1
									focus:outline-none
								"
							>
								<MenuItem
									v-for="item in userNavigation"
									:key="item.name"
									v-slot="{ active }"
								>
									<a
										@click="item.action"
										:class="[
											active ? 'bg-gray-100' : '',
											'block py-2 px-4 text-sm text-gray-700',
										]"
										class="cursor-pointer"
									>
										{{ item.name }}
									</a>
								</MenuItem>
							</MenuItems>
						</transition>
					</Menu>
				</div>
			</div>
			<nav class="hidden lg:py-2 lg:flex lg:space-x-8" aria-label="Global">
				<router-link
					v-for="item in navigation"
					:key="item.name"
					:to="item.href"
					v-slot="{ href, route, navigate, isActive, isExactActive }"
				>
					<a
						:class="[
							(
								item.highlight
									? item.highlight(route)
									: item.route == '/'
									? isExactActive
									: isActive
							)
								? 'bg-gray-100 text-gray-900'
								: 'text-gray-900 hover:bg-gray-50 hover:text-gray-900',
							'rounded-md py-2 px-3 inline-flex items-center text-sm font-medium',
						]"
						:href="href"
						@click="navigate"
						:aria-current="isActive ? 'page' : undefined"
					>
						{{ item.name }}
					</a>
				</router-link>
			</nav>
		</div>

		<DisclosurePanel as="nav" class="lg:hidden" aria-label="Global">
			<div class="pt-2 pb-3 px-2 space-y-1">
				<a
					v-for="item in navigation"
					:key="item.name"
					:href="item.href"
					:class="[
						item.current
							? 'bg-gray-100 text-gray-900'
							: 'text-gray-900 hover:bg-gray-50 hover:text-gray-900',
						'block rounded-md py-2 px-3 text-base font-medium',
					]"
					:aria-current="item.current ? 'page' : undefined"
					>{{ item.name }}</a
				>
			</div>
			<div class="border-t border-gray-200 pt-4 pb-3">
				<div class="px-4 flex items-center">
					<div class="flex-shrink-0">
						<img class="h-10 w-10 rounded-full" :src="user.imageUrl" alt="" />
					</div>
					<div class="ml-3">
						<div class="text-base font-medium text-gray-800">
							{{ user.name }}
						</div>
						<div class="text-sm font-medium text-gray-500">
							{{ user.email }}
						</div>
					</div>
					<button
						class="
							ml-auto
							flex-shrink-0
							bg-white
							rounded-full
							p-1
							text-gray-400
							hover:text-gray-500
							focus:outline-none
							focus:ring-2
							focus:ring-offset-2
							focus:ring-indigo-500
						"
					>
						<span class="sr-only">View notifications</span>
						<BellIcon class="h-6 w-6" aria-hidden="true" />
					</button>
				</div>
				<div class="mt-3 px-2 space-y-1">
					<a
						v-for="item in userNavigation"
						:key="item.name"
						:href="item.href"
						class="
							block
							rounded-md
							py-2
							px-3
							text-base
							font-medium
							text-gray-500
							hover:bg-gray-50 hover:text-gray-900
						"
						>{{ item.name }}</a
					>
				</div>
			</div>
		</DisclosurePanel>
	</Disclosure>
</template>

<script>
import { ref } from 'vue';
import {
	Disclosure,
	DisclosureButton,
	DisclosurePanel,
	Menu,
	MenuButton,
	MenuItem,
	MenuItems,
} from '@headlessui/vue';
import { SearchIcon } from '@heroicons/vue/solid';
import { BellIcon, MenuIcon, XIcon } from '@heroicons/vue/outline';

const user = {
	name: 'Tom Cook',
	email: 'tom@example.com',
	imageUrl:
		'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
};
const navigation = [
	{ name: 'Home', href: '/', current: true },
	{ name: 'My Courses', href: '/courses', current: false },
];

export default {
	inject: ['$auth'],
	components: {
		Disclosure,
		DisclosureButton,
		DisclosurePanel,
		Menu,
		MenuButton,
		MenuItem,
		MenuItems,
		BellIcon,
		MenuIcon,
		SearchIcon,
		XIcon,
	},
	setup() {
		const open = ref(false);

		return {
			user,
			navigation,
			open,
		};
	},
	computed: {
		userNavigation() {
			return [{ name: 'Sign out', action: () => this.$auth.logout() }];
		},
	},
};
</script>
