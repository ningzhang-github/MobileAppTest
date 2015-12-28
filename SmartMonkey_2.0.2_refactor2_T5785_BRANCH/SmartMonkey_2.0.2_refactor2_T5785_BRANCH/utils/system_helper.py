# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''
import subprocess

from utils.logger import Logger as zLog

class SystemHelper():

    @classmethod
    def runCommand(cls, cmd):
        '''运行命令行'''
        __output = ''
        try:
            __output = subprocess.check_output(cmd, shell=True)
            __retval = 0
        except Exception,e:
            __retval = -1
            __output = '%s : \r\n %s' %(str(e), __output)
        return __retval, __output
