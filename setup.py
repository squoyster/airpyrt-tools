from setuptools import setup

setup(
	name="acp",
	version="2.0",
	description="AirPyrt Tools",
	author="Vince Cali",
	author_email="0x56.0x69.0x6e.0x63.0x65@gmail.com",
	packages=["acp", "acp.clibs"],
	entry_points = {
		"console_scripts": ["acp=acp.cli:main"],
		},
	install_requires=[
		"pycryptodome",
		],
	python_requires=">=3.8",
	)
