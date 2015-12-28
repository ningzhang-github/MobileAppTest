# -*- coding: utf8 -*-
'''
Created on 2014-11-06

@author: zenist_song
'''

import os

import wx

from monkey.monkey_logic import MonkeyLogic
from monkey.mThreads.monkey_threads import MonkeyThread
from monkey.mThreads.monkey_helper import MonkeyHelper
from monkey.monkey_checker import MonkeyChecker
from monkey.mThreads.monkey_process import MonkeyProcess
from monkey_devices import MonkeyDevice
from setting.running_setting import SETTING
from setting import monkey_event as MEVT
from utils.logger import Logger

# @singleton
class MonkeyListener():

    def __init__(self, window):
        self.__window = window
        self.__monkey_device = MonkeyDevice()

    def get_logfile_path(self):
        return self.__window.logfile_path

    def get_workspace(self):
        return  SETTING().get_workSpace()

    def get_aut_list(self):
        return SETTING().get_aut_list()

    def get_throttle_list(self):
        return SETTING().get_throttle_list()

    def get_pct_list(self):
        return self.__window.pct_list

    def if_usePkgSelect_check(self):
        return self.__window.usePkgSelect.IsChecked()

    def get_run_count(self):
        return self.__window.run_count

    def get_package_value(self):
        return  self.__window.run_pkg.GetValue()
        # return SETTING().get_aut()

    def get_aut_path(self):
        return  self.__window.test_app.GetValue()

    def get_throotle_value(self):
        return SETTING().get_throotle()

    def get_run_count_value(self):
        return self.__window.run_count.GetValue()

    def enable_btRun(self):
        '''启用运行按钮'''
        self.__window.runButton.Enable(True)

    def enable_norFunBt(self):
        '''启用功能区域按钮'''
        self.__window.btScreenCap.Enable(True)
        self.__window.btClearDLog.Enable(True)
        self.__window.btGetDLog.Enable(True)

    def enble_btCheckDevice(self):
        '''启用检测设备按钮'''
        self.__window.btcheckDevice.Enable(True)

    def checkDeviceConn(self, event):
        '''检测按钮事件监听器'''
        try:
            # 开启mk_checkdevices检测线程
            self.__window.btcheckDevice.Enable(False)
            self.thread = MonkeyHelper(self, MEVT.EVT_CHECK_DEVICES)
            self.thread.start()
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def initDevice(self, event):
        '''初始设备环境'''

    def enablePackageSelect(self, event):
        '''启用被测应用选取功能'''
        try:
            self.__window.btScanPkg.Enable(True)
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def selectTestPkg(self, event):
        '''选择被测程序'''
        try:
            __file_wildcard = "App files(*.apk)|*.apk|All files(*.*)|*.*"
            __dlg = wx.FileDialog(self.__window, u"浏览被测应用app文件...",
                                  os.getcwd(),
                                  style=wx.OPEN,
                                  wildcard=__file_wildcard)
            if __dlg.ShowModal() == wx.ID_OK:
                self.__apppath = __dlg.GetPath()
                Logger.d("apppath=" + self.__apppath)
                self.__window.test_app.SetValue(self.__apppath)
            __dlg.Destroy()
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def onThrottleSelect(self, event):
        '''选择操作间隔监听器'''
        __currentIndex = self.__window.throttle_Combox.GetSelection()
        if wx.NOT_FOUND == __currentIndex:
            return
        __throotle = self.__window.throttle_Combox.GetItems()[__currentIndex].encode('utf-8')
        SETTING().set_throotle(__throotle)
        Logger.d("throotle ->" + SETTING().get_throotle())

    def run_monkey(self, event):
        '''运行按钮监听器'''
        try:
            self.__monkey_running_thread = MonkeyThread(self, MEVT.EVT_START_MONKEY)
            self.__monkey_checker_thread = MonkeyChecker()
            self.__monkey_process_thread = MonkeyProcess(self, self.get_run_count().GetValue(), self.get_throotle_value())
            self.__monkey_running_thread.start()
            # self.__monkey_checker_thread.start()
            # self.__monkey_process_thread.start()
            self.__window.stopRunButton.Enable(True)
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def stop_monkey(self, event):
        '''停止运行按钮'''
        try:
            retval, output = MonkeyLogic.stopMonkey()
            if retval == -1:
                self.appendOutputStream(output)
            elif retval == 0:
                self.appendOutputStream(output)
            self.__monkey_process_thread.stop()
            self.__monkey_checker_thread.stop()
            self.__monkey_running_thread.stop()
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def scanLogPath(self, event):
        '''浏览log存储位置'''
        try:
            __dlg = wx.DirDialog(self.__window.panel, u"浏览日志存储位置", os.getcwd(), style=wx.OPEN)
            if __dlg.ShowModal() == wx.ID_OK:
                self.logpath = __dlg.GetPath()
                Logger.d("logpath=" + self.logpath)
                self.__window.log_savnPath.SetValue(self.logpath)
            __dlg.Destroy()
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def openLogPath(self, event):
        '''打开log存储位置'''
        try:
            logfile_path = self.__window.log_savnPath.GetValue().encode('utf-8')
            os.startfile(logfile_path)
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def clearOutput(self, evnet):
        '''清除屏幕log信息'''
        try:
            Logger.d("Clear output log...")
            self.__window.output.Clear()
        except Exception, e:
            self.__genDailog(1, u"%s" % str(e))

    def screenCap(self, event):
        '''截屏'''
        Logger.d("Screen Caper...")
        __start_msg = u'截屏、数据传输中，请稍候...'
        self.appendOutputStream(__start_msg)
        try:
            __rst_capScreen = self.__monkey_device.cap_screen()
            if __rst_capScreen[0] == 0:
                __output_msg = u'Success, 存储路径: %s' % __rst_capScreen[1]
            else:
                __output_msg = u'[ERROR]%s'%__rst_capScreen[1]
            self.appendOutputStream(__output_msg)
        except Exception,e:
            __output_msg = u'[ERROR]Adb连接失败'
            self.appendOutputStream(__output_msg)

    def clearDLog(self, event):
        '''截屏'''
        Logger.d("CLear Device log buffer...")
        try:
            __start_msg = u'设备端缓存log清理中...'
            self.appendOutputStream(__start_msg)
            self.__monkey_device.clear_dLog()
            __output_msg = u'Success, 清理完毕'
            self.appendOutputStream(__output_msg)
        except Exception,e:
            __output_msg = u'[ERROR]Adb连接失败'
            self.appendOutputStream(__output_msg)

    def getDLog(self, event):
        '''截屏'''
        Logger.d("CLear Device log buffer...")
        try:
            __start_msg = u'dump、传输设备log中...'
            self.appendOutputStream(__start_msg)
            __rst_getDLog = self.__monkey_device.get_dLog()
            if __rst_getDLog[0] == 0:
                __output_msg = u'Success, 存储路径: %s' % __rst_getDLog[1]
            else:
                __output_msg = u'[ERROR]%s'%__rst_getDLog[1]
            self.appendOutputStream(__output_msg)
        except Exception,e:
            __output_msg = u'[ERROR]Adb连接失败'
            self.appendOutputStream(__output_msg)

    def __saveOutput(self, event):
        '''保存控制台信息'''

    def updateProcessBarTest(self, event):
        # self.__window.processBar.SetValue(50.5)
        self.__monkey_process_thread = MonkeyProcess(self, self.get_run_count().GetValue(), self.get_throotle_value())
        self.__monkey_process_thread.start()

    def startMonkeyChecker(self):
        '''开启MonkeyChecker进程'''
        self.__monkey_checker_thread.start()

    def stopMonkeyChecker(self):
        '''关闭monkeychecker进程'''
        self.__monkey_checker_thread.stop()

    def startProcessBar(self):
        '''启动进度信息显示'''
        self.__monkey_process_thread.start()

    def updateProcessBar(self, percent):
        '''更新进度信息'''
        self.__window.processBar.SetValue(percent)

    def stopProcessBar(self):
        self.__window.processBar.SetValue(100)
        self.__monkey_process_thread.stop()

    def appendOutputStream(self, msg):
        '''向log输出控制台输出log'''
        try:
            self.__window.output.AppendText(msg + '\r\n')
        except UnicodeDecodeError:
            self.__window.output.AppendText(str(msg).decode('utf-8') + '\r\n')

    def __genDailog(self, type, msg):
        '''
        对话框
        :param type: 0 alert， 1 error
        :param msg: 输出的信息
        :return:
        '''
        if type == 1:
            __title = u"!!! You Find a BUG !!!"
            __icon = wx.ICON_ERROR
        else:
            __title = u'??? No Way ???'
            __icon = wx.ICON_QUESTION

        __msg = u'%s' % str(msg)
        dlg = wx.MessageDialog(None, __msg, __title, __icon)
        dlg.ShowModal()
        dlg.Destroy()

        # def __saveLogFile(self):
        # '''保存log文件'''
        #     try:
        #         self.logfile_path = self.log_savnPath.GetValue().encode('utf-8')
        #         if self.logfile_path == '' or self.output.GetValue() == '':
        #             Logger.d("do nothing...")
        #             return
        #         # 拼接log文件名称
        #         logfile_name = 'monkey_%s.log' % (SystemHelper.getFormatData())
        #
        #         logfile_abs_path = self.logfile_path + '\\' + logfile_name
        #         Logger.d("Save log to: " + logfile_abs_path)
        #         #打开并写入log文件
        #         logfile = open(logfile_abs_path, 'w')
        #         logfile.write(self.output.GetValue())
        #         logfile.close()
        #     except Exception, e:
        #         self.genDailog(u"%s" % str(e))