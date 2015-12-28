# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''

import time

from utils.pyTags import singleton


@singleton
class Timer():
    '''提供时间相关方法'''

    def getCurTime(self, type=2):
        '''
        获取当前时间
        :type 返回类型，
            =0 1414396760.707
            =1 20141027
            =2 20141027-1539
            =3 20141027-153902
        :return:
        '''
        if type == 0:
            _curtime = time.time()
        elif type == 1:
            _curtime = time.strftime("%Y%m%d")
        elif type == 2:
            _curtime = time.strftime("%Y%m%d-%H%M")
        elif type == 3:
            _curtime = time.strftime("%Y%m%d-%H%M%S")
        else:
            _curtime = time.strftime("%Y%m%d-%H%M")

        return _curtime