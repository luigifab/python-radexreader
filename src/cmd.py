#!/usr/bin/python3
# -*- coding: utf8 -*-
# Created L/19/10/2020
# Updated D/08/11/2020
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

from datetime import datetime
from platform import python_version
import time
import sys
import usb

try:
	import radexreader
	msg = 'Information   python3-radexreader ' + radexreader.__version__ + ' with python ' + python_version() + ' and pyusb ' + usb.__version__
except:
	import os
	sys.path.append(os.path.abspath(__file__).replace('cmd.py', ''))
	import radexreader
	msg = 'Information   radexreader ' + radexreader.__version__ + ' with python ' + python_version() + ' and pyusb ' + usb.__version__

if len(sys.argv) > 1:

	if sys.argv[1] == 'erase':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		reader.erase()
		print('done!')
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
					print("%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)" % (
						str(datetime.utcfromtimestamp(timestamp)),
						str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
						str(int(measure['pct'])),
						str('{:.2f}'.format(measure['min'])),
						str('{:.2f}'.format(measure['val'])),
						str('{:.2f}'.format(measure['max']))
					))
				prev = timestamp
			time.sleep(10)
		exit(0)

	if sys.argv[1] == 'readlast':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		measures = reader.read(True)
		for timestamp, measure in measures.items():
			print("%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)" % (
				str(datetime.utcfromtimestamp(timestamp)),
				str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
				str(int(measure['pct'])),
				str('{:.2f}'.format(measure['min'])),
				str('{:.2f}'.format(measure['val'])),
				str('{:.2f}'.format(measure['max']))
			))
		if not measures:
			print("no data stored")
		exit(0)

	if sys.argv[1] == 'readall':
		print(msg)
		reader = radexreader.RadexReader()
		reader.print_info()
		measures = reader.read(False)
		for timestamp, measure in measures.items():
			print("%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)" % (
				str(datetime.utcfromtimestamp(timestamp)),
				str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
				str(int(measure['pct'])),
				str('{:.2f}'.format(measure['min'])),
				str('{:.2f}'.format(measure['val'])),
				str('{:.2f}'.format(measure['max']))
			))
		if not measures:
			print("no data stored")
		exit(0)

	if sys.argv[1] == 'jsonlast':
		import json
		print(json.dumps(radexreader.RadexReader().read(True)))
		exit(0)

	if sys.argv[1] == 'jsonall':
		import json
		print(json.dumps(radexreader.RadexReader().read(False)))
		exit(0)

print('Usage: radexreader erase|tail|readlast|readall|jsonlast|jsonall')
exit(-1)