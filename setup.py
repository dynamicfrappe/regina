from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in regina/__init__.py
from regina import __version__ as version

setup(
	name="regina",
	version=version,
	description="Regina Resort",
	author="Dynamic Business Solutions",
	author_email="beshoy.atef@dynamiceg.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
