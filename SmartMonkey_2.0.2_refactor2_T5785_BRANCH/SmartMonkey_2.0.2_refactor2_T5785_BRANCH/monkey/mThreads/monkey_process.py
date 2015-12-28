# -*- coding: utf8 -*-
'''
Created on 2014-10-29

@author: zenist_song
'''
import threading
import time

class MonkeyProcess(threading.Thread):

    def __init__(self, listener, total, interval):
        threading.Thread.__init__(self)

        self.__listener = listener
        self.__total = total
        self.__interval = interval

        self.__timeToQuit = threading.Event()
        self.__timeToQuit.clear()

    def stop(self):
        self._per = 100
        self.__timeToQuit.set()

    def run(self):
        try:
            __count = 0
            __interval = float(self.__interval)/1000
            print "Total count %f " % float(self.__total)
            print "Update process interval %f" % (__interval)
            while True:
                self._per = __count / float(self.__total) * 100 * 2.5
                # print "Update process bars to %f" % _per
                self.__listener.updateProcessBar(self._per)
                __count += 1
                time.sleep(__interval)
                if self._per >= 100:
                    break
        finally:
            self.stop()