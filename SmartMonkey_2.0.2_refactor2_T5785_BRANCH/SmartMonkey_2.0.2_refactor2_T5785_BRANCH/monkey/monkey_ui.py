# -*- coding: utf8 -*-
'''
Created on 2014-2-10
@author: zenist_song
'''

import os

import wx

from monkey.monkey_listener import MonkeyListener

monkey_inter = None

class MonkeyUI(wx.Frame):
    def __init__(self, parent):
        #初始化窗体
        title = "Monkey Test V2.0.1 - By Easou QA"
        wx.Frame.__init__(self, parent, title=title)
        #初始化监听器
        self.initListener()
        #初始化工作空间
        self.initWorkSpace()
        #初始化UI
        self.initUI()
        #加载监听器
        self.addListener()

    def initListener(self):
        '''初始化监听器'''
        self.__listener = MonkeyListener(self)

    def initWorkSpace(self):
        '''初始化工作空间'''
        __workspace = self.__listener.get_workspace()
        __monkeyRst_path = r'%s\monkey'%__workspace
        __screenCap_path = r'%s\screen'%__workspace
        __logdump_path = r'%s\log'%__workspace
        #1. 初始化主工作空间
        if not os.path.exists(__workspace):
            os.mkdir(__workspace)
        #2. 初始化monkey结果目录
        if not os.path.exists(__monkeyRst_path):
            os.mkdir(__monkeyRst_path)
        #3. 初始化截屏目录
        if not os.path.exists(__screenCap_path):
            os.mkdir(__screenCap_path)
        #4. 初始化log目录
        if not os.path.exists(__logdump_path):
            os.mkdir(__logdump_path)

    def initUI(self):
        '''初始化UI布局'''
        self.panel = wx.Panel(self)
        ##############################################################################
        # Area 1:
        # 1. 设备检测
        # 2. monkey运行设置
        ###############################################################################
        '''检查设备连接'''
        # 设备连接判断
        wx.StaticText(self.panel, -1, u"1. 检测设备连接:", pos=(10, 10))
        self.btcheckDevice = wx.Button(self.panel, label=u"连接检测", pos=(10, 40))
        # 初始化手机环境
        self.btInitDevice = wx.Button(self.panel, label=u"设备初始化", pos=(110, 40))
        self.btInitDevice.Enable(False)

        '''选择被测应用'''
        # 被测应用标签及浏览框
        wx.StaticText(self.panel, -1, u"2.选择被测程序:", pos=(10, 80))
        #应用选择被测程序复选框
        self.usePkgSelect = wx.CheckBox(self.panel, -1, pos=(110, 76), size=(25, 25))
        #备选应用程序选择显示框
        self.test_app = wx.TextCtrl(self.panel, pos=(10, 106), size=(190, 25), style=wx.TE_READONLY)
        #浏览被测应用程序按钮
        self.btScanPkg = wx.Button(self.panel, label=u"浏览", pos=(210, 106), size=(50, 25))
        self.btScanPkg.Enable(False)

        '''运行设置'''
        wx.StaticText(self.panel, - 1, u"3. 设置运行参数:", pos=(10, 140))
        #应用程序选择
        wx.StaticText(self.panel, -1, u"    选择应用程序:", (10, 170))
        # __packageList = self.__listener.get_aut_list()
        # self.package_Combox = wx.ComboBox(self.panel, -1, value="select", pos=(130, 166), choices=__packageList,
        #                                   style=wx.CB_READONLY)
        self.run_pkg = wx.TextCtrl(self.panel, pos=(130, 166))

        #操作间隔
        wx.StaticText(self.panel, -1, u"    操作半分比设置: 点击%,滑动%,系统按键%", (10, 230))
        self.pct_list = wx.TextCtrl(self.panel, -1, "70,20,10", pos=(50, 256), size=(70, 25))

        #操作间隔选择
        wx.StaticText(self.panel, -1, u"    选择操作间隔:", (10, 200))
        __throttleList = self.__listener.get_throttle_list()
        self.throttle_Combox = wx.ComboBox(self.panel, -1, value="select", pos=(130, 196), choices=__throttleList,
                                           style=wx.CB_READONLY)
        wx.StaticText(self.panel, -1, "ms", pos=(190, 200))

        #运行次数
        wx.StaticText(self.panel, -1, u"    随机事件数量:", (10, 290))
        self.run_count = wx.TextCtrl(self.panel, pos=(120, 286))

        #运行按钮
        self.runButton = wx.Button(self.panel, label=u'开始运行', pos=(30, 320), size=(80, 25))
        self.runButton.Enable(False)

        #停止运行按钮
        self.stopRunButton = wx.Button(self.panel, label=u'停止运行', pos=(120, 320), size=(80, 25))
        self.stopRunButton.Enable(False)

        # 运行进度显示
        wx.StaticText(self.panel, - 1, u"4. 设置进度:", pos=(10, 360))
        self.processBar = wx.Gauge(self.panel, -1, 100, pos=(10, 386), size=(200, 25), style = wx.GA_PROGRESSBAR)

        # btProcessTest =  wx.Button(self.panel, label=u'进度测试', pos=(100, 420), size=(80, 25))
        # btProcessTest.Bind(wx.EVT_BUTTON, self.__listener.updateProcessBarTest)

        ##############################################################################
        # Area 2:
        # 1. 输出控制台
        # 2. 日志文件存储位置
        ###############################################################################
        #控制台输出
        self.output = wx.TextCtrl(self.panel, pos=(270, 10), size=(600, 500),
                                  style=wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        #日志存储位置
        wx.StaticText(self.panel, - 1, u"存储位置:", pos=(270, 520))
        self.log_savnPath = wx.TextCtrl(self.panel, pos=(360, 516), size=(330, 25), style=wx.TE_READONLY)
        self.log_savnPath.SetValue(self.__listener.get_workspace())
        self.logfile_path = self.log_savnPath.GetValue().encode('utf-8')

        #浏览日志存放文件夹
        self.btScaneFloder = wx.Button(self.panel, label=u"浏览", pos=(700, 516), size=(80, 25))

        #打开日志存放文件夹
        self.btOpenFloder = wx.Button(self.panel, label=u"打开", pos=(790, 516), size=(80, 25))

        #清除控制台输出
        self.clearOutput = wx.Button(self.panel, label=u"清除屏幕", pos=(270, 550), size=(80, 25))

        #保存控制台输出
        self.saveOutput = wx.Button(self.panel, label=u"保存日志", pos=(370, 550), size=(80, 25))
        self.saveOutput.Enable(False)

        ##############################################################################
        # Area 3:
        # 1. 截屏
        # 2. 获取日志
        ###############################################################################
        '''截屏'''
        # 截屏功能描述
        wx.StaticText(self.panel, -1, u"1. 截取当前屏幕:", pos=(880, 10))
        # 截屏按钮
        self.btScreenCap = wx.Button(self.panel, label=u"截屏", pos=(880, 40), size=(80, 25))
        self.btScreenCap.Enable(False)
        '''设备端日志操作'''
        # 日志功能描述
        wx.StaticText(self.panel, -1, u"2. 设备端log:", pos=(880, 80))
        # 日志功能按钮
        self.btClearDLog = wx.Button(self.panel, label=u"清空缓存", pos=(880, 100), size=(80, 25))
        self.btClearDLog.Enable(False)
        self.btGetDLog = wx.Button(self.panel, label=u"获取日志", pos=(880, 130), size=(80, 25))
        self.btGetDLog.Enable(False)
        self.SetSize((1000, 630))
        self.SetMinSize((1000, 630))
        self.SetMaxSize((1000, 630))
        self.Show()

    def addListener(self):
        '''
        启用按钮监听器
        :return:
        '''
        # 1. 设备连接按钮监听器
        self.btcheckDevice.Bind(wx.EVT_BUTTON, self.__listener.checkDeviceConn)
        # 2. 启动安装被测程序选项
        self.usePkgSelect.Bind(wx.EVT_CHECKBOX, self.__listener.enablePackageSelect)
        # 3. 被测程序流浪按钮监听器
        self.btScanPkg.Bind(wx.EVT_BUTTON, self.__listener.selectTestPkg)
        # 4. 被测程序选择浏览空间监听器
        # self.package_Combox.Bind(wx.EVT_COMBOBOX, self.__listener.onPackageSelect)
        # 4. 选择时间间隔空间监听器
        self.throttle_Combox.Bind(wx.EVT_COMBOBOX, self.__listener.onThrottleSelect)
        # 5. 开始运行按钮监听器
        self.runButton.Bind(wx.EVT_BUTTON, self.__listener.run_monkey)
        # 6. 停止运行按钮监听器
        self.stopRunButton.Bind(wx.EVT_BUTTON, self.__listener.stop_monkey)
        # 7. 浏览日志存储文件夹按钮监听器
        self.btScaneFloder.Bind(wx.EVT_BUTTON, self.__listener.scanLogPath)
        # 8. 打开日志存储位置按钮监听器
        self.btOpenFloder.Bind(wx.EVT_BUTTON, self.__listener.openLogPath)
        # 9. 清除输出区域内容按钮监听器
        self.clearOutput.Bind(wx.EVT_BUTTON, self.__listener.clearOutput)
        # 10.保存输出区域内容按钮监听器
        # self.saveOutput.Bind(wx.EVT_BUTTON, MonkeyListener().bind(self, MEVT))#self.__saveLogFile)
        # 11.截屏按钮监听器
        self.btScreenCap.Bind(wx.EVT_BUTTON, self.__listener.screenCap)
        # 12.清除设备日志缓存监听器
        self.btClearDLog.Bind(wx.EVT_BUTTON, self.__listener.clearDLog)
        # 13.获取设备日志监听器
        self.btGetDLog.Bind(wx.EVT_BUTTON, self.__listener.getDLog)
        # 14.初始化手机环境
        self.btInitDevice.Bind(wx.EVT_BUTTON, self.__listener.initDevice)

def main():
    global monkey_inter
    #初始化UI
    app = wx.App(False)
    MonkeyUI(None)
    app.MainLoop()


if __name__ == '__main__':
    main()
        
        
        