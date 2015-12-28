# -*- coding: utf8 -*-
'''
Created on 2014-10-28
@author: zen
'''

import unittest

from setting.running_setting import SETTING


class RunningSettingTester(unittest.TestCase):
    def setUp(self):
        self.__obj_setting = SETTING()

    def tearDown(self):
        pass

    def test01_defaultValue(self):
        assert self.__obj_setting.get_per_tap() == 70
        assert self.__obj_setting.get_per_swip() == 20
        assert self.__obj_setting.get_per_key() == 10

    def test02_setPerValue(self):
        self.__obj_setting.set_per_tap(50)
        self.__obj_setting.set_per_swip(30)
        self.__obj_setting.set_per_key(20)

        assert self.__obj_setting.get_per_tap() == 50
        assert self.__obj_setting.get_per_swip() == 30
        assert self.__obj_setting.get_per_key() == 20

    def test03_mObjGetAndSetValue(self):
        __obj_setting_2 = SETTING()
        self.__obj_setting.set_per_tap(50)

        assert __obj_setting_2.get_per_tap() == 50