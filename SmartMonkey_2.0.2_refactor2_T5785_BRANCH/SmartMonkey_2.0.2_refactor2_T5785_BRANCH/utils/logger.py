# -*- coding: utf8 -*-
'''
Created on 2014-10-29
@author: zen
'''

import codecs

from utils.timeHelper import Timer


class Logger():
    def __init__(self, device, path):
        __date_time = Timer().getCurTime()
        self.logFileName = "%s_monkey_%s.log" % (device, __date_time)
        self.file = codecs.open(path + '//' + self.logFileName, 'wb', 'utf-8')

    def writeLog(self, log):
        self.file.write(log)
        self.file.write('\r\n')

    def closeLog(self):
        self.file.close()

    @classmethod
    def i(cls, msg):
        print("[INFO] %s" % msg)

    @classmethod
    def d(cls, msg):
        print("[DEBUG] %s" % msg)

    @classmethod
    def e(cls, msg):
        print("[ERROR] %s" % msg)