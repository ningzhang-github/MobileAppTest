# -*- coding: utf8 -*-
'''
Created on 2014-10-29

@author: zenist_song
'''
import threading

import wx

from monkey.monkey_devices import MonkeyDevice
from monkey.monkey_logic import MonkeyLogic
from monkey.monkey_checker import MonkeyChecker
from setting import monkey_event as MEVT
from utils.logger import Logger

class MonkeyThread(threading.Thread):

    def __init__(self, listener, event):
        threading.Thread.__init__(self)
        self.__monkey_logic = MonkeyLogic()
        self.__monkey_device = MonkeyDevice()

        self.__listener = listener
        self.__event = event
        self.__timeToQuit = threading.Event()
        self.__timeToQuit.clear()

    def stop(self):
        self.__timeToQuit.set()

    def __runMonkey(self):
        # 初始化日志文件
        logger = Logger(self.__monkey_device.DEVICES_NAME, self.__listener.get_logfile_path())

        __pct_list = self.__listener.get_pct_list().GetValue().encode('utf-8').split(',')
        __pct_touch = __pct_list[0]
        __pct_motion = __pct_list[1]
        __pct_sysnav = __pct_list[2]
        __run_count = self.__listener.get_run_count().GetValue()

        msg = '===================================='
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        msg = u'2. 运行设置信息如下'
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        msg = u'===================================='
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        __package = self.__listener.get_package_value()
        msg = u'被测程序: ' + __package
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        __throotle = self.__listener.get_throotle_value()
        msg = u'操作间隔: ' + __throotle + ' ms'
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        msg = u'事件数量: ' + self.__listener.get_run_count_value()
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        msg = u'事件百分比设置: 点击 %s、拖动 %s、系统按键 %s' % (__pct_touch, __pct_motion, __pct_sysnav)
        logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)

        msg = '===================================='
        # logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        msg = u'3. 安装被测应用程序'
        # logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        msg = u'===================================='
        # logger.writeLog(msg)
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        test_app = self.__listener.get_aut_path()

        if self.__listener.if_usePkgSelect_check() == False or test_app == '':
            msg = u'不需要安装被测程序, skip...'
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'===================================='
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
        else:
            msg = u'安装被测应用: ' + test_app + ' ...'
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            self.__monkey_device.installTestApk(test_app)
            msg = u'安装被测应用完成'
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'===================================='
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)

        self.__listener.startProcessBar()
        self.__listener.startMonkeyChecker()

        logger.writeLog(u'====================================' + '\r\n')
        logger.writeLog(u'4. 运行过程log信息如下' + '\r\n')
        logger.writeLog(u'====================================' + '\r\n')
        retval, output = MonkeyLogic.runMonkey(__package, __pct_touch, __pct_motion, __pct_sysnav,
                                               __throotle, __run_count)
        print output
        for line in output.split('\n'):
            line = u"" + line.replace('\r', '').replace('\n', '')
            wx.CallAfter(self.__listener.appendOutputStream, line)
            logger.writeLog(line + '\r\n')
        logger.closeLog()

        self.__listener.stopMonkeyChecker()
        self.__listener.stopProcessBar()


    def __monkey_checker(self):
        pass

    def run(self):
        # mk_checkdevices线程事件
        try:
            self.__runMonkey()
        except Exception, e:
            raise e