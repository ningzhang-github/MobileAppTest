# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''

import unittest

from utils.timeHelper import Timer


class TimeHelperTester(unittest.TestCase):
    def setUp(self):
        self.my_timer = Timer()

    def tearDown(self):
        pass

    def test01_getTime1(self):
        print self.my_timer.getCurTime(0)

    def test02_getTime2(self):
        print self.my_timer.getCurTime(1)

    def test03_getTime3(self):
        print self.my_timer.getCurTime(2)

    def test04_getTime4(self):
        print self.my_timer.getCurTime(3)


if __name__ == '__main__':
    unittest.main()