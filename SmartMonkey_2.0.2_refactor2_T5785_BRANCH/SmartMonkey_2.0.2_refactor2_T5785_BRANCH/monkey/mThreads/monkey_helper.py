# -*- coding: utf8 -*-
'''
Created on 2014-10-29

@author: zenist_song
'''
import threading

import wx

from monkey.monkey_devices import MonkeyDevice
from monkey.monkey_logic import MonkeyLogic
from utils.logger import Logger

class MonkeyHelper(threading.Thread):

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

    def __checkDevice(self):
        msg = u"检测设备连接..."
        wx.CallAfter(self.__listener.appendOutputStream, msg)
        device_list = self.__monkey_device.getConDev()

        if device_list == None:
            msg = u"未找到连接设备，请查看连接是否正确!!!"
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            self.__listener.enble_btCheckDevice()
        else:
            msg = u"发现设备：" + str(device_list)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            # 获取设备信息
            msg = u'===================================='
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'1. 运行设备信息如下'
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'===================================='
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            self.__monkey_device.getDeviceInfo()

            msg = u"设备名称：" + self.__monkey_device.DEVICES_NAME
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'设备型号：' + self.__monkey_device.DEVICES_NAME
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'安卓版本：' + self.__monkey_device.DEVICES_AND_VERSION
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'SDK版本：' + self.__monkey_device.DEVICES_SDK_VERSION
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'CPU类型：' + self.__monkey_device.DEVICES_CPU_TYPE
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            msg = u'分辨率：%s x %s ' % (self.__monkey_device.DEVICES_DIS_SIZE[0], self.__monkey_device.DEVICES_DIS_SIZE[1])
            # logger.writeLog(msg)
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            if self.__monkey_device.DEVICES_CPU_TYPE == "Unknown":
                msg = u'\r\n注：设备信息获取结果异常不影响monkey运行！！！'
                # logger.writeLog(msg)
                wx.CallAfter(self.__listener.appendOutputStream, msg)

            msg = u"请设置运行参数,并开始运行测试..."
            wx.CallAfter(self.__listener.appendOutputStream, msg)
            # 启用相关按钮
            self.__listener.enable_btRun()
            self.__listener.enable_norFunBt()
            self.stop()

    def run(self):
        # mk_checkdevices线程事件
        self.__checkDevice()
