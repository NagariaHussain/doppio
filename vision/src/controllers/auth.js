import call from './call';

export default class Auth {
	constructor() {
		this.isLoggedIn = false;
		this.user = null;
		this.user_image = null;
		this.cookie = null;

		this.cookie = Object.fromEntries(
			document.cookie
				.split('; ')
				.map((part) => part.split('='))
				.map((d) => [d[0], decodeURIComponent(d[1])])
		);

		this.isLoggedIn = this.cookie.user_id && this.cookie.user_id !== 'Guest';
	}

	async login(email, password) {
		let res = await call('login', {
			usr: email,
			pwd: password,
		});
		if (res) {
			this.isLoggedIn = true;
			return res;
		}
		return false;
	}

	async logout() {
		await call('logout');
		this.isLoggedIn = false;
		window.location.reload();
	}

	async resetPassword(email) {
		console.log('resetting password');
		// Implement if you want
	}
}
