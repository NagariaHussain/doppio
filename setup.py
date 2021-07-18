from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in doppio/__init__.py
from doppio import __version__ as version

setup(
	name='doppio',
	version=version,
	description='A dream.',
	author='Hussain Nagaria',
	author_email='hussainbhaitech@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
