#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="pirgblight",
	version="0.5.0",
	author="Toni Kangas",
	description="Server and Home Assistant integration for controlling RGB light via remote Raspberry Pi.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kangasta/pirgblight",
	packages=setuptools.find_packages(),
	scripts=["bin/pirgblight-server"],
	install_requires=[
		'flask>=1.1.1',
		'gunicorn>=19.9.0',
		'pigpio>=1.44',
		'requests>=2.22.0'
	],
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	)
)
