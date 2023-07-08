from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mssql_integration/__init__.py
from mssql_integration import __version__ as version

setup(
	name="mssql_integration",
	version=version,
	description="mssql integration",
	author="ahmed",
	author_email="ahmed751995@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
