#!/usr/bin/python3
# -*- coding: utf8 -*-
# Created L/19/10/2020
# Updated M/10/11/2020
#
# Copyright 2020 | Fabrice Creuzot (luigifab) <code~luigifab~fr>
# https://github.com/luigifab/python-radexreader
# https://www.luigifab.fr/python/radexreader
#
# This program is free software, you can redistribute it or modify
# it under the terms of the GNU General Public License (GPL) as published
# by the free software foundation, either version 2 of the license, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but without any warranty, without even the implied warranty of
# merchantability or fitness for a particular purpose. See the
# GNU General Public License (GPL) for more details.

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

try:
	with open("README.md", "r") as fh:
		long_description = fh.read().replace('(images/', '(https://raw.githubusercontent.com/luigifab/python-radexreader/master/images/').replace('[PYPI package](https://pypi.org/project/radexreader/)', '[GitHub](https://github.com/luigifab/python-radexreader)')
	setup(
		name='radexreader',
		version='1.0.0',
		description='Python library for the RADEX RD1212 Geiger counter.',
		long_description=long_description,
		long_description_content_type="text/markdown",
		license='GPL 2',
		author='Fabrice Creuzot',
		author_email='code@luigifab.fr',
		url='https://github.com/luigifab/python-radexreader',
		packages=['radexreader'],
		install_requires=['pyusb']
	)
except:
	setup(
		name='radexreader',
		version='1.0.0',
		description='Python library for the RADEX RD1212 Geiger counter.',
		license='GPL 2',
		author='Fabrice Creuzot',
		author_email='code@luigifab.fr',
		url='https://github.com/luigifab/python-radexreader',
		packages=['radexreader'],
		install_requires=['pyusb']
	)