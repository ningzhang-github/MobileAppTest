# -*- coding: utf8 -*-
'''
Created on 2014-10-29

@author: zenist_song
'''

from utils.logger import Logger
from utils.pyTags import singleton
from utils.system_helper import SystemHelper
from utils.androidHelper import AndroidHandler
from setting import devices_info as DEV_INFO
from setting.running_setting import SETTING

@singleton
class MonkeyDevice():

    DEVICES_NAME = u''
    DEVICES_AND_VERSION = u''
    DEVICES_SDK_VERSION = u''
    DEVICES_CPU_TYPE = u''
    DEVICES_DIS_SIZE = u''

    def __init__(self):
        self.__adb = AndroidHandler()

    def getConDev(self):
        '''获取设备连接'''
        # 获取设备列表
        __devList = self.__adb.getConnection()
        #如果获取成功,则获取设备信息
        if len(__devList) != 0:
            return __devList[0]
        #如果获取失败，则返回None
        else:
            return None

    def installTestApk(self, app_path):
        '''安装被测应用程序'''
        __install_cmd = 'adb install -r ' + app_path
        print("Install adt: %s" % __install_cmd)
        __retval, __output = SystemHelper.runCommand(__install_cmd)
        # Logger.d(str(__retval) + ',' + str(__output))

    def getDeviceInfo(self):
        '''获取设备列表,设备属性信息'''
        try:
            __device_info = self.__adb.getDevicesInfo()
            # print __device_info
            self.DEVICES_NAME = __device_info[DEV_INFO.DEVICES_NAME]
            self.DEVICES_AND_VERSION = __device_info[DEV_INFO.DEVICES_AND_VERSION]
            self.DEVICES_CPU_TYPE = __device_info[DEV_INFO.DEVICES_CPU_TYPE]
            self.DEVICES_DIS_SIZE = __device_info[DEV_INFO.DEVICES_DISP_SIZE]
            self.DEVICES_SDK_VERSION = __device_info[DEV_INFO.DEVICES_SDK_VERSION]
        except Exception, e:
            self.DEVICES_NAME = "Unknown"
            self.DEVICES_AND_VERSION = "Unknown"
            self.DEVICES_CPU_TYPE = "Unknown"
            self.DEVICES_DIS_SIZE = "Unknown"
            self.DEVICES_SDK_VERSION = "Unknown"

    def cap_screen(self):
        '''获取设备截屏'''
        __ret_capScreen = self.__adb.cap_screen(self.DEVICES_NAME)
        if __ret_capScreen[0] == 0:
            __dev_screen_file = __ret_capScreen[1]
        else:
            return -1, 'ScpScreen Error'
        __pc_save_path = r'%s\screen\%s' % (SETTING().get_workSpace(), __dev_screen_file.split('/')[-1])
        __ret_pullfile = self.__adb.pull_file(__dev_screen_file, __pc_save_path)
        if __ret_pullfile[0] == 0:
            return 0, __pc_save_path
        else:
            return -1, __ret_pullfile[1]

    def clear_dLog(self):
        '''清除设备端日志缓存'''
        self.__adb.clear_dev_log()

    def get_dLog(self):
        '''获取设备端log'''
        __ret_dump_dlog = self.__adb.dump_dev_log(self.DEVICES_NAME)
        if __ret_dump_dlog[0] == 0:
            __dev_log_file = __ret_dump_dlog[1]
        else:
            return -1, 'Dump log error'
        __pc_save_path = r'%s\log\%s' % (SETTING().get_workSpace(), __dev_log_file.split('/')[-1])
        __ret_pullfile = self.__adb.pull_file(__dev_log_file, __pc_save_path)
        if __ret_pullfile[0] == 0:
            return 0, __pc_save_path
        else:
            return -1, __ret_pullfile[1]
