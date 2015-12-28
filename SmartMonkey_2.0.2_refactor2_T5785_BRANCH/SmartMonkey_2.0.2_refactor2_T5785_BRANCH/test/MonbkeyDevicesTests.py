# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''
import unittest

from monkey.monkey_devices import MonkeyDevice

class MonkeyDevicesTests(unittest.TestCase):

    def setUp(self):
        self.__monkey_device = MonkeyDevice()

    def test01_capScreen(self):
        print self.__monkey_device.cap_screen()

    def test02_clearDLog(self):
        print self.__monkey_device.clear_dLog()

    def test03_getDLog(self):
        print self.__monkey_device.get_dLog()
