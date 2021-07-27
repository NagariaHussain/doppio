import { ref, onMounted, watch, reactive, computed } from 'vue';

class User {
	constructor() {
		this.name = 'Halwa';
	}

	setName(name) {
		this.name = name;
	}
}

export default function useComposeTest(userName) {
	const numbers = ref([]);
	const user = reactive(new User());
	const secretMessage = ref('');

	const insertNewNumber = () => {
		console.log('inserting new number');
		numbers.value.push(Math.ceil(Math.random() * 100));
	};

	onMounted(() => console.log('onMounted of setup() on Test.vue'));
	watch(() => user.name, (n, o) => console.log('user changed.', n, o), {deep: true});

	const encryptedMessage = computed(() => {
		if (!secretMessage.value) {
			return '';
		}
		return Array(secretMessage.value.length).fill('*').join('');
	});

	return {
		user,
		numbers,
		secretMessage,
		insertNewNumber,
		encryptedMessage,
	};
}
