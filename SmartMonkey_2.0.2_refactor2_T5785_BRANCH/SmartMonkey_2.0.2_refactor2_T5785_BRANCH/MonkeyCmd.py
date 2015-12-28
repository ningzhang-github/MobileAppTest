# -*- coding: utf8 -*-
'''
Created on 2014-10-29

@author: zenist_song
'''
import sys

from monkey.monkey_logic import MonkeyLogic


class MonkeyCmd():
    def __usage(self):
        print '''
        Usage:
            monkeyCommand.py package ptc ptc ptc throttle count
        '''
        sys.exit()

    def __checkArg(self):
        ARGVS = sys.argv
        print len(ARGVS)
        if len(ARGVS) != 7:
            self.__usage()

        self.PACKAGE = str(ARGVS[1])
        self.pct_touch = str(ARGVS[2])
        self.pct_motion = str(ARGVS[3])
        self.pct_nav = str(ARGVS[4])
        self.throttle = str(ARGVS[5])
        self.count = str(ARGVS[6])

    def __runMonkey(self):
        MonkeyLogic.runMonkey(self.PACKAGE, self.pct_touch, self.pct_motion, self.pct_nav, self.throttle, self.count)

    @classmethod
    def run(self):
        self.__checkArg()
        self.__runMonkey()


def main():
    MonkeyCmd.run()


if __name__ == '__main__':
    main()
        