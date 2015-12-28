# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''
import random

from setting import key_code
from utils.pyTags import singleton
from utils.androidHelper import AndroidHandler


@singleton
class Random():
    '''运行工作随机数值成成工具实现'''

    def randomSysKeyCode(self):
        '''
        随机生成系统按键键值
        :return:
        '''
        _system_key_range = len(key_code.SYSKEYLIST)
        _random_index = random.randint(0, _system_key_range - 1)
        _random_keycode = key_code.SYSKEYLIST[_random_index]
        return _random_keycode

    def randomNomKeyCode(self):
        '''
        随机生成普通按键键值
        :return:
        '''
        _system_key_range = len(key_code.NORKEYLIST)
        _random_index = random.randint(0, _system_key_range - 1)
        _random_keycode = key_code.NORKEYLIST[_random_index]
        return _random_keycode

    def random_display_loc(self):
        '''生成设备随机地址'''
        _display_scope = AndroidHandler().DISPLAY_SIZE
        _rand_x = random.randint(1, _display_scope[0])
        _rand_y = random.randint(1, _display_scope[1])
        return (_rand_x, _rand_y)