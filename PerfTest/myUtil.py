#coding: UTF-8
#初版作者: 张宁@easou
import platform
import time
import subprocess

def timeIsUp(timeoutEvent):
    """工具函数，给appPerfRecorder.py的定时器线程回调"""
    print "Time is up!"
    timeoutEvent.set()
    

def seconds2Str(seconds):
    """工具函数，将Unix时间戳转为DD:HH:MM:SS格式string"""
    structedTimeList = time.localtime(seconds)
    timeString = time.strftime("%H:%M:%S",structedTimeList)
    return timeString


def currentPlatform():
    """工具函数，获取测试工具所在PC机的操作系统平台以决定生成报告时使用什么字体"""
    if platform.system() == 'Windows':
        if platform.win32_ver()[0] == '8':
            return 'Win8'
        else:
            return 'Win7orLower'
    elif platform.system() == 'Linux':
        return 'Linux'
    else:
        return 'MacOS'

def checkDevice():
    """工具函数，检查adb.exe是否可用，手机上的busybox是否可用，以及自动安装busybox"""
    listOfErrorString = ('not found','denied','Unable to','Read-only','not permitted')
    try:
        Output = subprocess.check_output('adb.exe shell /data/local/tmp/busybox')
    except subprocess.CalledProcessError:
        raise RuntimeError("Got an error when using adb.exe, please check:\n"
                            "    1. The android dev environment on your PC is installed properly.\n"
                            "    2. Device serial number is listed in the output of 'adb devices' command.")
    if Output.find('BusyBox v1.') == -1:
        print 'Busybox is not found, installing!'
        cmdReturnCode = subprocess.call('adb.exe push busybox /data/local/tmp/')
        if cmdReturnCode != 0:
            raise RuntimeError("""Got an error when pushing busybox to device's '/data/local/tmp/' folder, please confirm that:
            1. 'busybox' is in this script's folder.
            2. Adb connection is OK.""")
        else:
            Output = subprocess.check_output('adb.exe shell chmod 755 /data/local/tmp/busybox')
            for errorString in listOfErrorString:
                if Output.find(errorString) != -1:
                    raise RuntimeError('Unable to install busybox, found "{0}" from device output below:\n'.format(errorString),Output)
            print 'Busybox has been installed successfully!'
    return

def dumpDeviceLog(logFileName):
    try:
        subprocess.call("adb logcat -v threadtime -d > {0}_LogCat.log".format(logFileName),shell=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Got an error when using adb.exe, please check:\n"
                            "    1. The android dev environment on your PC is installed properly.\n"
                            "    2. Device serial number is listed in the output of 'adb devices' command.")
    except Exception:
        raise
    else:
        subprocess.call("adb logcat -c")


class ProcessNotFoundException(Exception):
    pass

class FoundNewProcessException(Exception):
    pass

class ProcessChangedException(Exception):
    pass