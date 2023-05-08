from pathlib import Path
from unittest import TestCase
from doppio.commands.spa_generator import SPAGenerator
from doppio.commands import add_frappe_ui_starter


class TestSPAGeneration(TestCase):
	def setUp(self):
		# create ../apps/fake_app directory
		self.app_path = Path("../apps/fake_app")
		self.app_path.mkdir(parents=True, mode=0o755, exist_ok=True)
		
		self.app_path.joinpath("fake_app/www").mkdir(parents=True, mode=0o755, exist_ok=True)
		self.app_path.joinpath("fake_app/public").mkdir(parents=True, mode=0o755, exist_ok=True)
		# create a file hooks.py inside ../apps/fake_app
		self.app_path.joinpath("fake_app/hooks.py").touch(exist_ok=True)

	def test_generate_spa_core(self):
		spa_generator = SPAGenerator("vue", "dashboard", "fake_app", False, False)
		spa_generator.generate_spa()

		# check if the dashboard directory was created
		self.assertTrue(self.app_path.joinpath("dashboard").exists())

		# check if the dashboard directory contains the correct files
		self.assertTrue(self.app_path.joinpath("dashboard").joinpath("src").exists())
		self.assertTrue(self.app_path.joinpath("dashboard").joinpath("src").joinpath("main.js").exists())
		self.assertTrue(self.app_path.joinpath("dashboard").joinpath("src").joinpath("App.vue").exists())

		# check if package.json has correct build command
		package_json = self.app_path.joinpath("dashboard").joinpath("package.json")
		self.assertTrue(package_json.exists())
		self.assertTrue('"build": "vite build --base=/assets/fake_app/dashboard/ && yarn copy-html-entry"' in package_json.read_text())

		# check if hooks.py has correct list website_route_rules
		hooks_py = self.app_path.joinpath("fake_app").joinpath("hooks.py")
		self.assertTrue(hooks_py.exists())
		self.assertTrue("{'from_route': '/dashboard/<path:app_path>', 'to_route': 'dashboard'}" in hooks_py.read_text())
		
	def test_add_frappe_ui(self):
		"""Tests if add_frappe_ui_starter function works as expected"""
		# run the command
		add_frappe_ui_starter("frontend", "fake_app")

		# check if the frontend directory was created
		self.assertTrue(self.app_path.joinpath("frontend").exists())

		# check if the frontend directory contains the correct files
		self.assertTrue(self.app_path.joinpath("frontend").joinpath("src").exists())
		self.assertTrue(self.app_path.joinpath("frontend").joinpath("src").joinpath("main.js").exists())
		self.assertTrue(self.app_path.joinpath("frontend").joinpath("src").joinpath("App.vue").exists())

		# check if package.json has correct build command
		package_json = self.app_path.joinpath("frontend").joinpath("package.json")
		self.assertTrue(package_json.exists())
		self.assertTrue('"build": "vite build --base=/assets/fake_app/frontend/ && yarn copy-html-entry"' in package_json.read_text())




