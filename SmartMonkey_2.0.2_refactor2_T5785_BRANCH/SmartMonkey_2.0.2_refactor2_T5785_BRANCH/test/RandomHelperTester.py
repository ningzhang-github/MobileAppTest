# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''
import unittest

from setting import key_code
from utils.randomHelper import Random


class randomHelperTester(unittest.TestCase):
    def setUp(self):
        self._random = Random()

    def tearDown(self):
        pass

    def test01_randomSysKey(self):
        _randomKey_1 = self._random.randomSysKeyCode()
        _randomKey_2 = self._random.randomSysKeyCode()
        print _randomKey_1, _randomKey_2
        assert key_code.SYSKEYLIST.count(_randomKey_1) > 0
        assert key_code.SYSKEYLIST.count(_randomKey_2) > 0

    def test02_randomNomKeyCode(self):
        _randomKey_1 = self._random.randomNomKeyCode()
        _randomKey_2 = self._random.randomNomKeyCode()
        print _randomKey_1, _randomKey_2
        assert key_code.NORKEYLIST.count(_randomKey_1) > 0
        assert key_code.NORKEYLIST.count(_randomKey_2) > 0

    def test03_random_display_loc(self):
        _randomLoc_1 = self._random.random_display_loc()
        _randomLoc_2 = self._random.random_display_loc()
        print _randomLoc_1, _randomLoc_2
        assert _randomLoc_1[0] > 0
        assert _randomLoc_1[1] > 0
        assert _randomLoc_2[0] > 0
        assert _randomLoc_2[1] > 0


if __name__ == '__main__':
    unittest.main()