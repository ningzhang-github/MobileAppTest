# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''

import time

from adbpy.adb import Adb
from adbpy.host_command import host_command

from setting import key_code as KEY_CODE
from setting import devices_info as DEV_INFO
from utils.pyTags import singleton
from utils.logger import Logger
from utils.system_helper import SystemHelper


@singleton
class AndroidHandler():
    '''android系统及设备相关功能实现'''

    DISPLAY_SIZE = (480, 600)
    _adb = None

    def __init__(self):
        '''
        AndroidHandler构造函数
        '''
        if self._adb == None:
            self._adb = Adb()

    def getConnection(self):
        '''
        获取设备连接状态
        :return: 连接的设备列表
        '''
        __ret_device_list = []
        __devices_list = self._adb.devices()
        if len(__devices_list) == 0:
            pass
        else:
            for _dev in __devices_list:
                __ret_device_list.append(_dev[0])

        return __ret_device_list

    def shell(self, cmd, serial=None, timeout=None):
        '''
        运行设备端命令
        :param shell_cmd: 命令
        :param timeout: 超时时间，默认无
        :return: 命令运行返回值
        '''
        if serial == None:
            _cmd = str(cmd)
            _retVal = self._adb.shell(cmd, timeout=timeout)
        else:
            _retVal = self._adb.shell(cmd, serial, timeout=timeout)
            # with self._adb.socket.Connect():
            #     print self._adb.socket.address
            #     # _cmd = host_command(serial, cmd)
            #     # _cmd = 'host:get-serialno'
            #     # _cmd = 'host:devices'
            #     # _cmd = 'host: -s 4d0088254b015125 shell ls'
            #     _cmd = 'host-serial:4d0088254b015125: uninstall com.gfth.coouj'
            #     print _cmd
            #     _retVal = self._adb._command(_cmd)
        return _retVal

    def getDevicesInfo(self):
        '''
        获取设备信息
        :return: 设备信息字典
        '''
        __device_info_dic = {}
        __device_info = self.shell('getprop').replace('\n','').split('\r')
        # __device_info = self.shell('getprop')
        print __device_info
        for __prop in __device_info:
            if __prop.count(':') > 0:
                try:
                    # print("split prop: %s" % __prop)
                    __prop_key = str(__prop).split(u'[')[1].split(u']')[0]
                    __prop_value = str(__prop).split(u'[')[2][0:-1]
                    # __prop_value = str(__prop).split(u':')[1]
                except:
                    print "split prop %s exception" % str(__prop)
            else:
                continue

            if __prop_key == 'dalvik.vm.heapsize':
                print __prop
                __device_info_dic[DEV_INFO.DEVICES_HEAPSIZE] = __prop_value
                Logger.d("Get DEVICES_HEAPSIZE = " + __device_info_dic[DEV_INFO.DEVICES_HEAPSIZE])

            if __prop_key == 'ro.build.version.release':
                __device_info_dic[DEV_INFO.DEVICES_AND_VERSION] = __prop_value
                Logger.d("Get DEVICES_AND _VERSION = " + __device_info_dic[DEV_INFO.DEVICES_AND_VERSION])

            if __prop_key == 'ro.build.version.sdk':
                __device_info_dic[DEV_INFO.DEVICES_SDK_VERSION] = __prop_value
                Logger.d("Get DEVICES_SDK_VERSION = " + __device_info_dic[DEV_INFO.DEVICES_SDK_VERSION])

            if __prop_key == 'ro.product.cpu.abi':
                __device_info_dic[DEV_INFO.DEVICES_CPU_TYPE] = __prop_value
                Logger.d("Get DEVICES_CPU_TYPE = " + __device_info_dic[DEV_INFO.DEVICES_CPU_TYPE])

            if __prop_key == 'ro.product.manufacturer':
                devices_n1 = __prop_value
            if __prop_key == 'ro.product.model':
                devices_n2 = __prop_value

        try:
            __dev_name = str(devices_n1 + '-' + devices_n2).replace(' ','-')
            __device_info_dic[DEV_INFO.DEVICES_NAME] = __dev_name
            Logger.d("Get DEVICES_NAME = " + __device_info_dic[DEV_INFO.DEVICES_NAME])
        except Exception, e:
            print "Get device name error"

        #获取显示信息
        try:
            __device_info_dic[DEV_INFO.DEVICES_DISP_SIZE] = self.getDisSize()
        except Exception, e:
            print  "Get device display  error"

        return __device_info_dic

    def senKey(self, key_code):
        '''
        发送按键
        :KEY_CODE: 系统按键编码
        :return: null
        '''
        if KEY_CODE.SYSKEYLIST.count(key_code) == 0 and KEY_CODE.NORKEYLIST.count(key_code) == 0:
            return -1
        else:
            self.shell('input keyevent %s' % key_code)
            return 0


    def sendTap(self, xy):
        '''
        发送点击事件
        :xy: 屏幕坐标（x,y）
        :return:'''
        if len(xy) > 2 or xy[0] < 0 or xy[1] < 0:
            return -1
        else:
            self.shell('input tap  %s %s' % (xy[0], xy[1]))

    def sendSwip(self, from_xy, to_xy):
        '''
        发送滑动事件
        :from_xy: 起始屏幕坐标（x,y）
        :to_xy: 终点屏幕坐标（x,y）
        :return:
        '''
        if len(from_xy) > 2 or from_xy[0] < 0 or from_xy[1] < 0:
            return -1
        if len(to_xy) > 2 or to_xy[0] < 0 or to_xy[1] < 0:
            return -1

        self.shell('input swipe %s %s %s %s' % (from_xy[0], from_xy[1], to_xy[0], to_xy[1]))

    def startAct(self, comppent):
        '''
        启动App
        :return:
        '''
        retval = self.shell('am start -n ' + comppent)
        if retval.count("ERROR") > 0:
            return False
        else:
            return True

    def getCurComp(self):
        '''
        获取当前Activity
        :return: 当前activity名称
        '''
        _retVal = self.shell('dumpsys window| grep "mCurrentFocus"')
        _comp = _retVal.split(" ")[-1].split("}")[0]
        return _comp

    def getCurAct(self):
        '''
        获取当前Activity
        :return: 当前activity名称
        '''
        return self.getCurComp().split('.')[-1]

    def getCurApp(self):
        '''
        获取当前Activity
        :return: 当前app名称
        '''
        return self.getCurComp().split('/')[0]

    def getDisSize(self):
        '''
        获取屏幕区域范围
        :return: （x,y）
        '''
        _retVal = self.shell('dumpsys window windows | grep mFrame')
        _display_x = _retVal.split('[')[2].split(']')[0].split(',')[0]
        _display_y = _retVal.split('[')[2].split(']')[0].split(',')[1]
        self.DISPLAY_SIZE = (_display_x, _display_y)
        return (_display_x, _display_y)

    def create_dir(self, dir_name):
        '''建立设备端文件夹'''
        _retVal = self.shell('mkdir -p %s'%(dir_name))
        if _retVal.count('exists') == 0:
            return 0
        else:
            return -1

    def init_smonkey_dir(self):
        '''初始化Smonkey工作目录'''
        __date = time.strftime("%Y%m%d")
        __work_dir = '/sdcard/smonkey/' + __date
        __retval = self.create_dir(__work_dir)
        if __retval == 0:
            return 0,__work_dir
        else:
            return -1, __work_dir

    def clear_dev_log(self):
        '''清楚设备端内容log'''
        # adb shell logcat -c 清楚内存log
        __clear_log = 'logcat -c'
        self._adb.shell(__clear_log)

    def dump_dev_log(self, flag='', type=0):
        '''dump设备端log'''
        # adb shell logcat -v raw -d > d:/xx.log    log 简要
        # adb shell logcat -v time -d > d:/xx.log   log 含时间戳
        #log文件存储地址
        __save_path = self.init_smonkey_dir()[1]
        __log_file_name = flag+'_'+time.strftime("%Y%m%d-%H%M%S")+'.log'
        __log_save_path = __save_path+'/'+__log_file_name
        if type == 0:
            __log_cmd = 'logcat -v time -d > '+ __log_save_path
        else:
            __log_cmd = 'logcat -v raw -d > '+ __log_save_path
        self._adb.shell(__log_cmd)
        return 0, __log_save_path

    def pull_file(self, dev_path, pc_path):
        '''拷贝设备端文件至PC'''
        __pull_cmd = 'adb.exe pull %s %s'%(str(dev_path),str(pc_path))
        __retval, __output = SystemHelper.runCommand(__pull_cmd)
        return __retval, __output

    def cap_screen(self, file_flage='', save_path=None):
        '''截屏'''
        #判断截屏文件名
        __file_name = file_flage + '_' +time.strftime("%Y%m%d-%H%M%S")+'.png'
        #初始化存储地址
        __save_path = self.init_smonkey_dir()[1]
        __save_file = __save_path + '/' +__file_name
        #执行截屏命令
        __cmd_capScreen = '/system/bin/screencap -p %s'%(__save_file)
        __retVal = self.shell(__cmd_capScreen)
        if __retVal.count('Error'):
            return -1,__retVal
        else:
            return 0,__save_file

    def find_process_id(self, proc_name):
        '''查询进程名称'''
        __retVal = self._adb.shell('ps')
        __proc_list = __retVal.split('\n')
        for __proc in __proc_list:
            if __proc.count(proc_name):
                while __proc.count('  ') > 0:
                    __proc = __proc.replace('  ',' ')
                __proc_info = __proc.split(' ')
                return __proc_info[0], __proc_info[1],__proc_info[-1]
        return None,None,None

    def find_and_kill_process(self, proc_name):
        '''发现并结束制定进程'''
        _puser, _pid, _pname = self.find_process_id(proc_name)
        if _pid == None:
            return (-1, "None such process %s" % proc_name)
        if _puser == 'shell':
            __kill_cmd = 'kill -9 %s' % _pid
        else:
             __kill_cmd = 'am force-stop %s' % _pname
        print 'kill %s use cmd: %s' % (proc_name, __kill_cmd)
        return SystemHelper.runCommand('adb shell %s' % __kill_cmd)


