# -*- coding: utf8 -*-
'''
Created on 2014-10-17
@author: zen
'''
import unittest

from utils.androidHelper import AndroidHandler


class AndroidHanlderTester(unittest.TestCase):
    def setUp(self):
        self._adb = AndroidHandler()

    def tearDown(self):
        pass

    def test01_deviceConn(self):
        print("Test: testDeviceConn=" + str(self._adb))
        assert self._adb != None

    def test02_getDisSize(self):
        _dis_size = self._adb.getDisSize()
        print("dis_size=" + str(_dis_size))
        # assert _dis_size == (480, 600)

    def test03_getDevices(self):
        __devices = self._adb.getConnection()
        print __devices

    def test04_getDeviceInfo(self):
        __devices_info = self._adb.getDevicesInfo()
        print __devices_info

    def test05_runShell(self):
        print self._adb.shell('ls', '4d0088254b015125')
        # print self._adb.shell('ls', '022ATK7N36070339')

    def test06_createDir(self):
        __dir_name = 'smonky1'
        print self._adb.create_dir(__dir_name)

    def test07_initSmonkeyDir(self):
        print self._adb.init_smonkey_dir()

    def test08_capScreen(self):
        print self._adb.cap_screen()

    def test09_pullFile(self):
        __dev_path = self._adb.cap_screen()[1]
        __pc_path = 'D:/smonkey/'+__dev_path.split('/')[-1]
        print self._adb.pull_file(__dev_path, __pc_path)

    def test10_clearDevlog(self):
        self._adb.clear_dev_log()

    def test11_dumpDevLog(self):
        print self._adb.dump_dev_log()

    def test12_getTimeLog(self):
        __dev_path = self._adb.dump_dev_log()
        __pc_path = 'D:/smonkey/'+__dev_path.split('/')[-1]
        print self._adb.pull_file(__dev_path, __pc_path)

    def test13_getRawLog(self):
        __dev_path = self._adb.dump_dev_log(1)
        __pc_path = 'D:/smonkey/'+__dev_path.split('/')[-1]
        print self._adb.pull_file(__dev_path, __pc_path)

    def test14_find_process_id(self):
        print self._adb.find_process_id('esbook')

    def test15_find_and_kill_process(self):
        print self._adb.find_and_kill_process('dsf54')

# def testStartActivity():
# adb = AndroidHandler()
#     print("Test: testStartActivity")
#     print adb.startAct("com.esbook.reader/com.esbook.reader.activity.ActLoading")
#
# def testSendSwipe():
#     adb = AndroidHandler()
#     from_xy = (800, 400)
#     to_xy = (200,400)
#     print("Test: testSendSwipe")
#     print adb.sendSwip(from_xy,to_xy)
#
# def testSendTap():
#     adb = AndroidHandler()
#     xy = (400, 400)
#     print("Test: testSendTap")
#     print adb.sendTap(xy)
#
# def testGetCurrentComp():
#     adb = AndroidHandler()
#     print("Test: testGetCurrentComp")
#     print adb.getCurComp()
#
# def testGetCurrentApp():
#     adb = AndroidHandler()
#     print("Test: testGetCurrentApp")
#     print adb.getCurApp()
#
# def testGetCurrentAct():
#     adb = AndroidHandler()
#     print("Test: testGetCurrentAct")
#     print adb.getCurAct()
#
# def testSendKey():
#     adb = AndroidHandler()
#     print("Test: testSendKey")
#     print adb.senKey(KEY_CODE.KEYCODE_BACK)
#     print adb.senKey(KEY_CODE.KEYCODE_BACK)
#
# def testSingleton():
#     adb1 = AndroidHandler()
#     adb2 = AndroidHandler()
#     print adb1
#     print adb2
#     adb1.DISPLAY_SIZE = (100,200)
#     print adb1.DISPLAY_SIZE
#     print adb2.DISPLAY_SIZE
# testSingleton()
# testDeviceConn()
# testGetDisSize()
# testStartActivity()
# time.sleep(5)
# testSendSwipe()
# testSendTap()
# time.sleep(0.5)
# testGetCurrentComp()
# testGetCurrentApp()
# testGetCurrentAct()
# testSendKey()

