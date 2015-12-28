# -*- coding: utf8 -*-
'''
Created on 2014-10-29

@author: zenist_song
'''
import threading
import time
import random

from utils.logger import Logger
from utils.pyTags import singleton
from utils.androidHelper import AndroidHandler
from setting.running_setting import SETTING

class MonkeyChecker(threading.Thread):

    __current_act = ''
    __current_app = ''
    __target_package = ''
    __think_count = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.__android_helper = AndroidHandler()
        self.__threap_stop = True

        self.__timeToQuit = threading.Event()
        self.__timeToQuit.clear()

    def stop(self):
        self.__threap_stop = False
        self.__timeToQuit.set()

    def __monkey_checker(self):

        __act = self.__android_helper.getCurAct()
        __app = self.__android_helper.getCurApp()
        Logger.d("App: %s, Act: %s " % (__act, __app))

        # 第一次进入，设置Act为当前Act
        if self.__current_act == '':
            self.__current_act = __act
            self.__max_thinking_time = SETTING().get_max_thinging_time()
            self.__think_max_count = random.randint(1, self.__max_thinking_time)
            Logger.d("New Acticity, Max thing time = %s s" % self.__think_max_count)
        #如果两次相同，发送2次Back按键，并设置Act为空
        elif self.__current_act == __act:
            if self.__think_count == self.__think_max_count:
                self.__android_helper.senKey(4)
                self.__android_helper.senKey(4)
                self.__current_act = ''
                self.__think_count = 0
                Logger.d("Seam Acticity Max count: Back.")
            else:
                self.__think_count += 1
                Logger.d("Seam Activity think count " + str(self.__think_count))
        #如果两次不相同，则设置Act为当前act
        else:
            self.__current_act = __act
            self.__max_thinking_time = SETTING().get_max_thinging_time()
            self.__think_max_count = random.randint(1, self.__max_thinking_time)
            self.__think_count = 0
            Logger.d("Diff Activity think count empty, Reset Max thing time = %s s" % self.__think_max_count)

            # if not self.__current_app == 'com.esbook.reader':
            #     self.__android_helper.startAct('com.esbook.reader/com.esbook.reader.activity.ActLoading')

    def run(self):
        while self.__threap_stop:
            self.__monkey_checker()
            time.sleep(1)