#!/usr/bin/python3
# -*- coding: utf8 -*-
# Created L/19/10/2020
# Updated J/06/05/2021
#
# Copyright 2020-2021 | Fabrice Creuzot (luigifab) <code~luigifab~fr>
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

from datetime import datetime
from platform import python_version
import sys
import time
import usb
import serial

# https://stackoverflow.com/a/62804772/2980105
# prevent auto import for "import radexreader"when filename is "radexreader.py"
sys.path = sys.path[1:]

try:
	import radexreader
	msg = 'Information   python3-radexreader ' + radexreader.__version__
	msg += ' with python ' + python_version() + ' + pyusb ' + usb.__version__ + ' + pyserial ' + serial.__version__
except:
	import os
	sys.path.append(os.path.abspath(__file__).replace('radexreader.py', ''))
	import radexreader
	msg = 'Information   radexreader ' + radexreader.__version__
	msg += ' with python ' + python_version() + ' + pyusb ' + usb.__version__ + ' + pyserial ' + serial.__version__

if len(sys.argv) > 1:

	if sys.argv[1] == 'erase':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		reader.erase()
		print('done')
		exit(0)

	if sys.argv[1] == 'tail':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		prev = None
		while True:
			measures = reader.read(True)
			for timestamp, measure in measures.items():
				if timestamp != prev:
					print('%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)' % (
						str(datetime.utcfromtimestamp(timestamp)),
						str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
						str(int(measure['pct'])),
						str('{:.2f}'.format(measure['min'])),
						str('{:.2f}'.format(measure['val'])),
						str('{:.2f}'.format(measure['max']))
					))
					if reader.com == 'ONEv1':
						print('                     %s µSv accumulated / %s CPM  [±%s%%]' % (
							str('{:.2f}'.format(measure['acc'])).rjust(6, ' '),
							str('{:.0f}'.format(measure['cpm'])).rjust(6, ' '),
							str(int(measure['pct']))
						))
				prev = timestamp
			time.sleep(10)
		exit(0)

	if sys.argv[1] == 'tailjson':
		import json
		reader = radexreader.RadexReader()
		prev   = None
		while True:
			measures = reader.read(True)
			for timestamp, measure in measures.items():
				if timestamp != prev:
					print(json.dumps(measure))
				prev = timestamp
			time.sleep(10)
		exit(0)

	if sys.argv[1] == 'readlast':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		measures = reader.read(True)
		for timestamp, measure in measures.items():
			print('%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)' % (
				str(datetime.utcfromtimestamp(timestamp)),
				str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
				str(int(measure['pct'])),
				str('{:.2f}'.format(measure['min'])),
				str('{:.2f}'.format(measure['val'])),
				str('{:.2f}'.format(measure['max']))
			))
			if reader.com == 'ONEv1':
				print('                     %s µSv accumulated / %s CPM  [±%s%%]' % (
					str('{:.2f}'.format(measure['acc'])).rjust(6, ' '),
					str('{:.0f}'.format(measure['cpm'])).rjust(6, ' '),
					str(int(measure['pct']))
				))
		if not measures:
			print('no data stored')
		exit(0)

	if sys.argv[1] == 'jsonlast':
		import json
		print(json.dumps(radexreader.RadexReader().read(True)))
		exit(0)

	if sys.argv[1] == 'readall':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		measures = reader.read(False)
		for timestamp, measure in measures.items():
			print('%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)' % (
				str(datetime.utcfromtimestamp(timestamp)),
				str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
				str(int(measure['pct'])),
				str('{:.2f}'.format(measure['min'])),
				str('{:.2f}'.format(measure['val'])),
				str('{:.2f}'.format(measure['max']))
			))
			if reader.com == 'ONEv1':
				print('                     %s µSv accumulated / %s CPM  [±%s%%]' % (
					str('{:.2f}'.format(measure['acc'])).rjust(6, ' '),
					str('{:.0f}'.format(measure['cpm'])).rjust(6, ' '),
					str(int(measure['pct']))
				))
		if not measures:
			print('no data stored')
		exit(0)

	if sys.argv[1] == 'jsonall':
		import json
		print(json.dumps(radexreader.RadexReader().read(False)))
		exit(0)

print('Usage: radexreader erase|tail|tailjson|readlast|jsonlast|readall|jsonall')
exit(-1)