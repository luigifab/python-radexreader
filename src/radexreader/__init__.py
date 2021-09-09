#!/usr/bin/python3
# -*- coding: utf8 -*-
# Created L/19/10/2020
# Updated M/10/08/2021
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
import operator
import time
# pyusb
import usb.core
import usb.util
import usb.backend.libusb1
# pyserial
import serial
import serial.tools.list_ports

__version__ = '1.2.1'

class RadexReader():

	com = None
	usb = None
	serial = None
	keyA = None
	keyB = None
	keyC = None
	keyD = None

	def __init__(self):

		# backend only for alpine with docker?
		backend = usb.backend.libusb1.get_backend(find_library=lambda x: '/usr/lib/libusb-1.0.so.0')

		# RADEX RD1212 v2
		# search usb device (03EB/5603)
		self.usb = usb.core.find(idVendor=0x03eb, idProduct=0x5603, backend=backend)
		if self.usb is not None:
			self.com = 'RD1212v2'
			# usb reset
			self.usb.reset()
			if sys.platform != 'win32' and sys.platform != 'cygwin' and self.usb.is_kernel_driver_active(0):
				self.usb.detach_kernel_driver(0)
			self.usb.set_configuration()
			return # device found

		# RADEX RD1212 v1
		# search usb device (10C4/EA60 = Silicon labs USB to UART bridge)
		self.usb = usb.core.find(idVendor=0x10c4, idProduct=0xea60, backend=backend)
		if self.usb is not None:
			self.com = 'RD1212v1'
			# search usb serial device (https://stackoverflow.com/a/25112066/2980105)
			devices  = serial.tools.list_ports.grep('RADEX')
			for device in devices:
				self.serial = serial.Serial(port = device.device, baudrate = 115200, timeout = 0.5)
				return # device found
			if self.serial is None:
				raise ValueError('Error: RADEX RD1212 (serial) not found')

		# RADEX ONE v1
		# search usb device (ABBA/A011)
		self.usb = usb.core.find(idVendor=0xabba, idProduct=0xa011, backend=backend)
		if self.usb is not None:
			self.com = 'ONEv1'
			# search usb serial device (https://stackoverflow.com/a/25112066/2980105)
			devices  = serial.tools.list_ports.grep('RADEX')
			for device in devices:
				self.serial = serial.Serial(port = device.device, baudrate = 9600, timeout = 0.5)
				return # device found
			if self.serial is None:
				raise ValueError('Error: RADEX ONE (serial) not found')

		# no devices found
		if self.usb is None:
			raise ValueError('Error: RADEX RD1212 (usb) and RADEX ONE (usb) not plugged?')

	def get_device(self, getusb=False):
		if not getusb and self.serial is not None:
			return self.serial
		return self.usb

	def print_info(self):
		if self.com == 'RD1212v2':
			print('Manufacturer  ' + hex(self.usb.idVendor).ljust(7, ' ')  + ' ' + usb.util.get_string(self.usb, self.usb.iManufacturer))
			print('Product       ' + hex(self.usb.idProduct).ljust(7, ' ') + ' ' + usb.util.get_string(self.usb, self.usb.iProduct))
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
		elif self.com == 'RD1212v1':
			print('Manufacturer  ' + hex(self.usb.idVendor).ljust(7, ' ')  + ' ' + usb.util.get_string(self.usb, self.usb.iManufacturer))
			print('Product       ' + hex(self.usb.idProduct).ljust(7, ' ') + ' ' + usb.util.get_string(self.usb, self.usb.iProduct))
			print('ComPort       ' + self.serial.port)
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
		elif self.com == 'ONEv1':
			if sys.platform != 'win32' and sys.platform != 'cygwin':
				print('Manufacturer  ' + hex(self.usb.idVendor).ljust(7, ' ')  + ' ' + usb.util.get_string(self.usb, self.usb.iManufacturer))
				print('Product       ' + hex(self.usb.idProduct).ljust(7, ' ') + ' ' + usb.util.get_string(self.usb, self.usb.iProduct))
			else:
				print('Manufacturer  -x----  QUARTA-RAD')
				print('Product       -x----  RADEX ONE')
			print('ComPort       ' + self.serial.port)
			print()
			print('[info] Sensor: Geiger-Müller tube SBM 20-1')
			print('[info] Measuring range: 0.05 - 999 µSv/h')
			print('[info] Uncertainty of the result: ±(15+6/D)%')
			print('[info]   D is the value after a complete cycle of 100? seconds')
			print()
			print('[warn] The values displayed are only an approximation.')
			print('[warn] The actual value can only be measured with suitable professional device.')
			print('[warn] For now, not tested with measured values greater than 0.25 µSv/h.')
			print()

	def hid_set_report(self, report):
		if self.com == 'RD1212v2':
			# https://stackoverflow.com/a/52368526/2980105
			self.usb.ctrl_transfer(
				0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
				9,     # SET_REPORT
				0x300, # Vendor Descriptor Type + 0 Descriptor Index
				0,     # USB interface #0
				report # the HID payload as a byte array
			)
		elif self.com == 'RD1212v1':
			self.serial.write(report)
		elif self.com == 'ONEv1':
			self.serial.write(report)

	def hid_get_report(self):
		if self.com == 'RD1212v2':
			# https://stackoverflow.com/a/52368526/2980105
			return self.usb.ctrl_transfer(
				0xa1,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
				1,     # GET_REPORT
				0x300, # Vendor Descriptor Type + 0 Descriptor Index
				0,     # USB interface #0
				64     # max reply size
			)
		elif self.com == 'RD1212v1':
			return self.serial.read(14)
		elif self.com == 'ONEv1':
			return self.serial.read(12 + 21 + 2 + 2 + 2 + 2 + 1)

	def read(self, last=False):

		if self.com == 'ONEv1':
			return self.readOne()

		values = {}
		if last:
			keys = [0x0]
		else:
			keys = list(range(0x0, 0xb4)) # from 0x0 to 0xb3

		for key in keys:
			self.hid_set_report((0x12, 0x12, 0x01, 0x02, key, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
			hexa = self.hid_get_report()
			if hexa[0] != 0:
				# timestamp = 01/01/2016 00:00:44 = 1451606444
				# timestamp = 01/01/2016 00:00:44 = 172 + 193 (×256) + 133 (×256×256) + 86 (×256×256×256)
				timestamp   = (hexa[2] + hexa[3] * 256 + hexa[4] * 256 * 256 + hexa[5] * 256 * 256 * 256)
				# measure   = 0.15 µSv/h = 15
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

		return dict(sorted(values.items(), key=operator.itemgetter(0))) # sort by date

	def readOne(self):

		if self.keyA is None:
			self.keyA = 0x04 - 0x04
			self.keyB = 0x00
			self.keyC = 0x5a + 0x04
			self.keyD = 0x00

		self.keyA += 0x04
		self.keyC -= 0x04
		if self.keyA > 0xff:
			self.keyA -= 0xfe
			self.keyB += 0x01
			if self.keyB > 0xff:
				self.keyB = 0x00
			self.keyC -= 0x01
		elif self.keyC < 0x00:
			self.keyC += 0xff
			self.keyD -= 0x01
			if self.keyD < 0x00:
				self.keyD = 0xff

		self.hid_set_report((0x7b, 0xff, 0x20, 0, 0x06, 0, self.keyA, self.keyB, 0, 0, self.keyC, self.keyD, 0, 0x08, 0x0c, 0, 0xf3, 0xf7))
		hexa = self.hid_get_report()

		# measure   = 0.15 µSv/h = 15 / 0.15 µSv accumulated = 15 / 15 CPM = 15
		measure     = (hexa[20] + hexa[21] * 256 + hexa[22] * 256 * 256) / 100
		measure_acc = (hexa[24] + hexa[25] * 256 + hexa[26] * 256 * 256) / 100
		measure_cpm =  hexa[28] + hexa[29] * 256 + hexa[30] * 256 * 256
		# uncertainty of the result
		percent     = 15 + 6 / measure
		measure_min = measure * (1 - percent / 100)
		measure_max = measure * (1 + percent / 100)
		if measure_min < 0:
			measure_min = 0
		if percent > 99.9:
			percent = 99.9

		timestamp = int(time.time())
		return { timestamp: { 'pct': percent, 'min': measure_min, 'val': measure, 'max': measure_max, 'acc': measure_acc, 'cpm': measure_cpm } }

	def erase(self):
		if self.com == 'RD1212v2':
			self.hid_set_report((0x12, 0x12, 0x01, 0x03, 0, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
		elif self.com == 'RD1212v1':
			self.hid_set_report((0x12, 0x12, 0x01, 0x03, 0, 0, 0, 0, 0, 0, 0, 0, 0x3c, 0x84))
