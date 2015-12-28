# -*- coding: utf8 -*-
'''
Created on 2014-10-29
@author: zen
'''

from utils.system_helper import SystemHelper
from utils.logger import Logger
from utils.androidHelper import AndroidHandler

class MonkeyLogic():
    @classmethod
    def runMonkey(cls, package, pct_touch, pct_motion, pct_nav, throttle, count):
        '''
        根据传入的参数运行monkey命令
        :param package: 被测包名称
        :param pct_touch 点击百分比
        :param pct_motion 移动百分比
        :param pct_nav 按键百分比
        :param throttle 操作间隔
        :param count 操作数量
        :return: retval 运行结果,output结果输出
        '''
        __com_head = 'adb shell monkey'
        # 指定运行包
        __com_package = ' -p ' + package
        # 制定事件百分比
        __com_pct = ' --pct-touch %s --pct-motion %s --pct-nav %s' % (pct_touch, pct_motion, pct_nav)
        #指定运行间隔
        __com_throttle = ' --throttle ' + throttle
        #设置log等级
        # __com_log = ' -v'
        __com_log = ''
        #制定运行次数
        __com_count = ' ' + count
        #拼接命令
        com_all = __com_head + __com_package + __com_pct + __com_throttle + __com_log + __com_count
        #运行命令
        retval, output = SystemHelper.runCommand(com_all)

        return retval, output

    @classmethod
    def stopMonkey(cls):

        '''关闭monkey'''
        # 获取monkey程序PID
        monkeyProcess = None

        __retVal = AndroidHandler().find_and_kill_process('com.android.commands.monkey')
        if __retVal[0] == -1:
            Logger.e("未发现monkey进程")
            return -1, "未发现monkey进程"
        elif __retVal[0] == 0:
            return 0, "monkey已停止"
        else:
            return __retVal[0],__retVal[1]


