# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''

from utils.pyTags import singleton


@singleton
class SETTING():
    def __init__(self):
        self.initDefaultValues()

    def initDefaultValues(self):

        # 默认工作空间
        self.__DEF_WROKSPACE = r'D:\Smonkey'
        # 可选AUT列表
        self.__AUT_LIST = ['esBook', 'esVideo', 'lockScreen', 'veryNews', 'easouSearch']
        # 可选操作间隔列表
        self.__THROTTLE_LIST = ['0', '100', '300', '500']
        # AUT被测应用程序
        self.__AUT = 'com.esbook.reader'
        self.__THROOTLE = '100'
        # 操作时间百分比配置
        self.__PER_TAP = 70  # 点击事件
        self.__PER_SWIP = 20  # 翻页事件
        self.__PER_KEY = 10  # 按键事件
        # 按键
        self.__PER_SYSKEY = 20  # 系统按键占按键总数的百分比
        # 页面思考时间变量
        self.__MAX_THINKING_TIME = 60  # 页面检测间隔

    def get_workSpace(self):
        return self.__DEF_WROKSPACE

    def set_workSpace(self, workspace):
        self.__DEF_WROKSPACE = workspace

    def get_aut_list(self):
        '''返回可选被测应用程序列表'''
        return self.__AUT_LIST

    def get_throttle_list(self):
        '''返回操作间隔列表'''
        return self.__THROTTLE_LIST

    def set_aut(self, aut):
        '''设置被测应用程序'''
        self.__AUT = aut

    def get_aut(self):
        '''获取被测应用程序'''
        return self.__AUT

    def set_throotle(self, throotle):
        '''设置操作间隔'''
        self.__THROOTLE = throotle

    def get_throotle(self):
        '''获取操作间隔'''
        return self.__THROOTLE

    # 设置点击事件百分比
    def set_per_tap(self, percent):
        if percent > 100 or percent < 0:
            percent = 10
        self.__PER_TAP = percent

    # 获取点击事件百分比
    def get_per_tap(self):
        return self.__PER_TAP

    #设置滑动事件百分比
    def set_per_swip(self, percent):
        if percent > 100 or percent < 0:
            percent = 10
        self.__PER_SWIP = percent

    #获取滑动事件百分比
    def get_per_swip(self):
        return self.__PER_SWIP

    #设置按键事件百分比
    def set_per_key(self, percent):
        if percent > 100 or percent < 0:
            percent = 10
        self.__PER_KEY = percent

    #获取按键事件百分比
    def get_per_key(self):
        return self.__PER_KEY

    #设置系统按键所占总按键事件百分比
    def set_per_syskey(self, percent):
        if percent > 100 or percent < 0:
            percent = 10
        self.__PER_TAP = percent

    #获取系统按键所占总按键事件百分比
    def get_per_syskey(self):
        return self.__PER_SYSKEY

    #获取普通按键所占总按键事件百分比
    def get_per_norkey(self):
        return (100 - self.__PER_SYSKEY)

    #设置页面最长停留时间
    def set_max_thinging_time(self, second):
        self.__MAX_THINKING_TIME = second

    #获取页面最长停留时间
    def get_max_thinging_time(self):
        return self.__MAX_THINKING_TIME