#!/usr/bin/python3
# -*- coding: utf8 -*-
# Created L/19/10/2020
# Updated S/24/10/2026
#
# Copyright 2020-2027 | Fabrice Creuzot (luigifab) <code~luigifab~fr>
# https://github.com/luigifab/python-radexreader
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

from platform import python_version
import sys
import time
import datetime
import usb
import serial

try:
	datetime.UTC
except AttributeError:
	datetime.UTC = datetime.timezone.utc

# https://stackoverflow.com/a/62804772/2980105
# prevent auto import for "import radexreader" when filename is "radexreader.py"
if "radexreader.py" in sys.argv[0]:
	sys.path = sys.path[1:]
# python3 .../src/radexreader*py use local version when radexreader is not installed from package
elif ".py" in sys.argv[0]:
	import os
	sys.path.insert(0, os.path.dirname(os.path.realpath(sys.argv[0])))

import radexreader

def read_tail(reader):
	reader.print_info()
	prev = None
	while True:
		measures = reader.read(True)
		for timestamp, measure in measures.items():
			if timestamp != prev:
				print('%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)' % (
					str(datetime.datetime.fromtimestamp(timestamp, datetime.UTC)),
					str('{:.2f}'.format(measure['val'])).rjust(6, ' '),
					str(int(measure['pct'])),
					str('{:.2f}'.format(measure['min'])),
					str('{:.2f}'.format(measure['val'])),
					str('{:.2f}'.format(measure['max']))
				), flush=True)
				if reader.com == 'ONEv1':
					print('                     %s µSv accumulated / %s CPM  [±%s%%]' % (
						str('{:.2f}'.format(measure['acc'])).rjust(6, ' '),
						str('{:.0f}'.format(measure['cpm'])).rjust(6, ' '),
						str(int(measure['pct']))
					), flush=True)
			prev = timestamp
		time.sleep(10)

def read_jsontail(reader):
	prev = None
	while True:
		measures = reader.read(True)
		for timestamp, measure in measures.items():
			if timestamp != prev:
				print(json.dumps({timestamp: measure}), flush=True)
			prev = timestamp
		time.sleep(10)

def read_last(reader):
	reader.print_info()
	measures = reader.read(True)
	for timestamp, measure in measures.items():
		print('%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)' % (
			str(datetime.datetime.fromtimestamp(timestamp, datetime.UTC)),
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

def read_jsonlast(reader):
	print(json.dumps(reader.read(True)))

def read_all(reader):
	reader.print_info()
	measures = reader.read(False)
	for timestamp, measure in measures.items():
		print('%s  %s µSv/h  ±%s%% (%s ≤ %s ≤ %s)' % (
			str(datetime.datetime.fromtimestamp(timestamp, datetime.UTC)),
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

def read_jsonall(reader):
	print(json.dumps(reader.read(False)))

def write_erase(reader):
	reader.print_info()
	reader.erase()
	print('done')

if len(sys.argv) > 1:

	msg = '\n radexreader-local ' + radexreader.__version__ + ' − python ' + python_version() + ', pyusb ' + usb.__version__ + ', pyserial ' + serial.__version__

	if sys.argv[1] == 'tail':
		print(msg)
		try:
			reader = radexreader.RadexReader()
			read_tail(reader)
		except KeyboardInterrupt:
			print("")
		sys.exit(0)

	if sys.argv[1] == 'jsontail' or sys.argv[1] == 'tailjson':
		import json
		try:
			reader = radexreader.RadexReader()
			read_jsontail(reader)
		except KeyboardInterrupt:
			print("")
		sys.exit(0)

	if sys.argv[1] == 'last' or sys.argv[1] == 'readlast':
		print(msg)
		reader = radexreader.RadexReader()
		read_last(reader)
		sys.exit(0)

	if sys.argv[1] == 'jsonlast':
		import json
		reader = radexreader.RadexReader()
		read_jsonlast(reader)
		sys.exit(0)

	if sys.argv[1] == 'all' or sys.argv[1] == 'readall':
		print(msg)
		reader = radexreader.RadexReader()
		read_all(reader)
		sys.exit(0)

	if sys.argv[1] == 'jsonall':
		import json
		reader = radexreader.RadexReader()
		read_jsonall(reader)
		sys.exit(0)

	if sys.argv[1] == 'erase':
		print(msg)
		reader = radexreader.RadexReader()
		write_erase(reader)
		sys.exit(0)

	if sys.argv[1] == 'interactive':
		print(msg)
		try:
			reader = radexreader.RadexReader()
			while True:
				try:
					print("\n---------------------------")
					print("1 t ↣ tail (CTRL+C to stop)")
					print("2 l ↣ last")
					print("3 a ↣ all")
					print("4 e ↣ erase")
					print("5 q ↣ quit")
					choix = input("your choice: ").strip().lower()
					if choix == '1' or choix == 't':
						print("---------------------------\n")
						try:
							read_tail(reader)
						except KeyboardInterrupt:
							print("")
					elif choix == '2' or choix == 'l':
						print("---------------------------\n")
						read_last(reader)
					elif choix == '3' or choix == 'a':
						print("---------------------------\n")
						read_all(reader)
					elif choix == '4' or choix == 'e':
						print("---------------------------\n")
						write_erase(reader)
					elif choix == '5' or choix == 'q':
						break
				except (KeyboardInterrupt, EOFError):
					print("")
					break
		except Exception as e:
			print("\n", e)
			try:
				input(" Press enter to quit...")
			except (KeyboardInterrupt, EOFError):
				print("")

		sys.exit(0)

print('Usage: radexreader tail|jsontail|last|jsonlast|all|jsonall|erase|interactive')
sys.exit(1)