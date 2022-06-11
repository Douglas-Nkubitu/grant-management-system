from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in grant_management_system/__init__.py
from grant_management_system import __version__ as version

setup(
	name="grant_management_system",
	version=version,
	description="A Non profit app for Grant Management",
	author="Navari Limited",
	author_email="info@navari.co.ke",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
