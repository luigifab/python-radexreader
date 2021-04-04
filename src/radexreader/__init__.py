#!/usr/bin/python3
# -*- coding: utf8 -*-
# Created L/19/10/2020
# Updated V/26/03/2021
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

import sys
import usb.core
import usb.util
import usb.backend.libusb1
import serial
import serial.tools.list_ports
import operator

__version__ = '1.1.0'

class RadexReader():

	dev = None
	com = 'usb'

	def __init__(self):
		# search usb device (backend only? for alpine with docker)
		backend  = usb.backend.libusb1.get_backend(find_library=lambda x: '/usr/lib/libusb-1.0.so.0')
		self.dev = usb.core.find(idVendor=0x03eb, idProduct=0x5603, backend=backend)
		# check
		if self.dev is None:
			# search usb serial device (https://stackoverflow.com/a/25112066/2980105)
			self.com = 'serial'
			devices  = serial.tools.list_ports.grep('Radex')
			for device in devices:
				self.dev = serial.Serial(port = device.port, baudrate = 115200, timeout = 0.5)
				break
			# check
			if self.dev is None:
				# debug
				#ports = list(serial.tools.list_ports.comports())
				#for p in ports:
				#	print(p)
				# debug
				raise ValueError('Error: RADEX RD1212 not plugged? (usb or serial)')
		# reset
		else:
			self.dev.reset()
			if sys.platform != 'win32' and sys.platform != 'cygwin' and self.dev.is_kernel_driver_active(0):
				self.dev.detach_kernel_driver(0)
			self.dev.set_configuration()

	def get_device(self):
		return self.dev

	def print_info(self):
		if self.com == 'usb':
			print('Manufacturer  ' + hex(self.dev.idVendor).ljust(7, ' ')  + ' ' + usb.util.get_string(self.dev, self.dev.iManufacturer))
			print('Product       ' + hex(self.dev.idProduct).ljust(7, ' ') + ' ' + usb.util.get_string(self.dev, self.dev.iProduct))
		else:
			print('ComPort       ' + self.dev.port)
		print()
		print('[info] Sensor: Geiger-Müller tube SBM 20-1')
		print('[info] Measuring range: 0.05 - 999 µSv/h')
		print('[info] Uncertainty of the result: ±(15+6/D)%')
		print('[info]   D is the value after a complete cycle of 100 seconds')
		print()
		print('[warn] The values displayed are only an approximation.')
		print('[warn] The actual value can only be measured with suitable professional device.')
		print('[warn] For now, not tested with measured values greater than 0.25 µSv/h.')
		print()

	def hid_set_report(self, report):
		# https://stackoverflow.com/a/52368526/2980105
		if self.com == 'usb':
			self.dev.ctrl_transfer(
				0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
				9,     # SET_REPORT
				0x300, # Vendor Descriptor Type + 0 Descriptor Index
				0,     # USB interface #0
				report # the HID payload as a byte array
			)
		else:
			self.dev.write(report)

	def hid_get_report(self):
		# https://stackoverflow.com/a/52368526/2980105
		if self.com == 'usb':
			return self.dev.ctrl_transfer(
				0xa1,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
				1,     # GET_REPORT
				0x300, # Vendor Descriptor Type + 0 Descriptor Index
				0,     # USB interface #0
				64     # max reply size
			)
		else:
			return self.dev.read(14)

	def print_serial_number(self):
		# https://github.com/luigifab/python-radexreader/issues/6
		print('EXPERIMENTAL')
		self.hid_set_report((0x12, 0x12, 0x01, 0, 0, 0, 0, 0x3c, 0x84, 0x6b, 0xa8, 0xeb, 0x4f))
		print(self.hid_get_report())
		self.hid_set_report((0x12, 0x12, 0x01, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
		print(self.hid_get_report())
		self.hid_set_report((0x12, 0x12, 0x01, 0x01, 0, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
		hexa = self.hid_get_report()
		print(hexa)
		serial = ''
		for i in range(7):
			if i == 1 and (hexa[i] - 6) < 10:
				serial += ' 0' + str(hexa[i] - 6)
			elif i == 1:
				serial += ' ' + str(hexa[i] - 6)
			elif i == 5 and (hexa[i] - 42) < 10:
				serial += ' 0' + str(hexa[i] - 42)
			elif i == 5:
				serial += ' ' + str(hexa[i] - 42)
			elif i == 6 and (hexa[i] - 12) < 10:
				serial += ' 0' + str(hexa[i] - 12)
			elif i == 6:
				serial += ' ' + str(hexa[i] - 12)
			elif hexa[i] < 10:
				serial += ' 0' + str(hexa[i])
			else:
				serial += ' ' + str(hexa[i])
		print()
		print(serial + ' (it is YOUR serial number?)')
		print()
		print(' 0' + str(hexa[0]) + ' xx' + ' 0' + str(hexa[2]) + ' 0' + str(hexa[3]) + ' 0' + str(hexa[4]) + ' xx' + ' xx (debug)')
		print(' 04 19 01 01 00 72 22 (7x2)')
		print(' 0419010 1007222      (2x7)')
		print(' 04190101007222       (1x14)')

	def read(self, last=False):

		values = {}
		if last:
			keys = [0x0]
		else:
			keys = list(range(0x0, 0xb4)) # from 0x0 to 0xb3

		for key in keys:
			self.hid_set_report((0x12, 0x12, 0x01, 0x02, key, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
			hexa = self.hid_get_report()
			if hexa[0] != 0:
				# timestamp - 01/01/2016 00:00:44 = 1451606444
				# timestamp - 01/01/2016 00:00:44 = 172 + 193 (×256) + 133 (×256×256) + 86 (×256×256×256)
				timestamp   = (hexa[2] + hexa[3] * 256 + hexa[4] * 256 * 256 + hexa[5] * 256 * 256 * 256)
				# measure   - 0.15 µSv/h = 15
				measure     = (hexa[6] + hexa[7] * 256 + hexa[8] * 256 * 256) / 100
				# uncertainty of the result
				percent     = 15 + 6 / measure
				measure_min = measure * (1 - percent / 100)
				measure_max = measure * (1 + percent / 100)
				if measure_min < 0:
					measure_min = 0
				if percent > 99.9:
					percent = 99.9
				# memorize
				values[timestamp] = { 'pct': percent, 'min': measure_min, 'val': measure, 'max': measure_max }

		# sort by date
		return dict(sorted(values.items(), key=operator.itemgetter(0)))

	def erase(self):
		self.hid_set_report((0x12, 0x12, 0x01, 0x03, 0, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
