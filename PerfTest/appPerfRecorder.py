#!/bin/env python
#encoding: UTF-8
#初版作者：张宁@easou

from time import sleep
from adbpy.adb import Adb
from collections import defaultdict
import threading
import csv
import argparse
import myUtil


ADB_TIMEOUT = 5  #adb通信超时时间
BUSYBOX_PATH = '/data/local/tmp/busybox' #busybox在手机上的路径

class AppUnderTest(object):
    """APP对象，需要传入App的包名作为参数来初始化"""
    def __init__(self,strPackageName):
        self.DEFAULT_ADDRESS = ("localhost",5037)
        self.adb = Adb(self.DEFAULT_ADDRESS)
        self.strPackageName = strPackageName
        self.strUID = self.__get_UID()
        self.listProcessInfo = self.__init_processInfo()
        self.deviceAPILevel = self.__get_androidAPILevel()

    def __sizeof__(self):
        return super(AppUnderTest, self).__sizeof__()

    def __get_androidAPILevel(self):
        """获取手机上androidAPILevel的方法，用于处理dumpsys meminfo的分支判断"""
        APILevel = self.adb.shell('getprop ro.build.version.sdk',timeout=ADB_TIMEOUT)
        return int(APILevel)
    
    def __get_UID(self):
        """#获取App的UID的方法"""
        strTemp = self.adb.shell('dumpsys package "{0}"|{1} grep userId'.format(self.strPackageName,BUSYBOX_PATH),timeout=ADB_TIMEOUT)
        strUID = strTemp[11:16].strip() #切片返回字符串的第11到15个字符，即被测软件包的uid,形如"10086"
        if len(strUID) > 0:
            return strUID
        else:
            raise SystemExit("Cannot get the userID...stopped!!")

    def __init_processInfo(self):
        """#获取app进程及其子进程的processName和PID列表的方法. 返回二维的list，list[n][0]为第n个进程的PID，list[n][1]为其进程名"""
        strTemp = self.adb.shell("{0} top -bn 1|{0} grep '{1}'".format(BUSYBOX_PATH,self.strPackageName),timeout=ADB_TIMEOUT)
        listTemp = [elem.split() for elem in strTemp.splitlines() if elem.find('busybox') == -1] #将得到的返回数据分行并分割成单词list，滤出不包含'busybox'字样的行
        if len(listTemp)!=0:
            listProcessInfo = [[elem[0],elem[-1]] for elem in listTemp] #取listTemp中每个子list的的第一个和最后一个元素组成listProcessInfo,对应PID和processName
            listProcessInfo.sort(key=lambda x:x[1]) #对列表中第二个关键字也就是进程名进行排序，保证主进程所在的子list是listProcessInfo的第0个元素
        else:
            raise SystemExit("App's process is not found!")
        print '[Debug]:ProcessInfo\n', listProcessInfo
        return listProcessInfo

    def __update_processInfo(self,listOutputOfTop):
        if len(listOutputOfTop)!=0:
            listProcessInfo = [[elem[0],elem[-1]] for elem in listOutputOfTop] #取listTemp中每个子list的的第一个和最后一个元素组成listProcessInfo,对应PID和processName
            listProcessInfo.sort(key=lambda x:x[1]) #对列表中第二个关键字也就是进程名进行排序，保证主进程所在的子list是listProcessInfo的第0个元素
        else:
            raise SystemExit("App's process is not found!")
        if cmp(listProcessInfo,self.listProcessInfo) != 0:
            if len(listProcessInfo) > len(self.listProcessInfo):
                tempList = [elem for elem in listProcessInfo if elem not in self.listProcessInfo]
                self.listProcessInfo.extend(tempList)
                # print '[debug]---',tempList
                raise myUtil.FoundNewProcessException
            elif len(listProcessInfo) == len(self.listProcessInfo):
                tempList = [elem for elem in listProcessInfo if elem not in self.listProcessInfo]
                for elem in tempList:
                    flag = 'Not_Found'
                    for i,process in enumerate(self.listProcessInfo):
                        if elem[1] in process:
                            process[0] = elem[0]
                            self.listProcessInfo[i] = process
                            flag = 'Found'
                    if flag == 'Not_Found':
                        self.listProcessInfo.append(elem)
                raise myUtil.ProcessChangedException
            else:
                pass

    def get_networkTraffic(self):
        """#基于UID获取App的网络流量的方法
           modify by oscar@easou,从/proc/net/xt_qtaguid/stats获取网络流量统计，先进行判断存在使用它，不存在使用之前的方法。
        """

        flag_net = self.adb.shell('{0} cat /proc/net/xt_qtaguid/stats'.format(BUSYBOX_PATH),timeout=ADB_TIMEOUT)
        # print flag_net
        if "No such file or directory" not in flag_net:
            list_rx = [] # 接收网络数据流量列表
            list_tx = [] # 发送网络数据流量列表
            str_uid_net_stats = self.adb.shell('{0} cat /proc/net/xt_qtaguid/stats|{0} grep {1}'.format(BUSYBOX_PATH,self.strUID),timeout=ADB_TIMEOUT)
            # print str_uid_net_stats
            try:
                for item in str_uid_net_stats.splitlines():
                    rx_bytes = item.split()[5] # 接收网络数据流量
                    tx_bytes = item.split()[7] # 发送网络数据流量
                    list_rx.append(int(rx_bytes))
                    list_tx.append(int(tx_bytes))
                # print list_rx, sum(list_rx)
                floatTotalNetTraffic = (sum(list_rx) + sum(list_tx))/1024.0/1024.0
                floatTotalNetTraffic = round(floatTotalNetTraffic,4)
                return floatTotalNetTraffic
            except:
                print "[ERROR]: cannot get the /proc/net/xt_qtaguid/stats, return 0.0"
                return 0.0

        else:
            strTotalTxBytes = self.adb.shell('{0} cat /proc/uid_stat/{1}/tcp_snd'.format(BUSYBOX_PATH,self.strUID),timeout=ADB_TIMEOUT)
            strTotalRxBytes = self.adb.shell('{0} cat /proc/uid_stat/{1}/tcp_rcv'.format(BUSYBOX_PATH,self.strUID),timeout=ADB_TIMEOUT)
            try:
                floatTotalTraffic = (int(strTotalTxBytes) + int(strTotalRxBytes))/1024.0/1024.0
                floatTotalTraffic = round(floatTotalTraffic,4)
                return floatTotalTraffic
            except:
                return 0.0  #捕获获取网络流量时的错误并一律视为流量是0（一般是因为被测App无任何网络活动，未在/proc/uid_stat/下生成对应其uid的目录）

    def get_procCPULoad_viaTop(self):
        """#基于listProcessInfo中每个子进程的PID，处理top命令的返回信息来获取所有子进程的CPU占用的方法"""
        listProcCPULoad = []
        strTemp = self.adb.shell("{0} top -bn 1|{0} grep {1}".format(BUSYBOX_PATH,self.strPackageName),timeout=ADB_TIMEOUT) #返回top命令输出中第一个元素为目标进程PID的一行
        #listTemp = [elem.split() for elem in strTemp.split('\r\n')]
        listTemp = [elem.split() for elem in strTemp.splitlines() if elem.find('busybox') == -1]
        self.__update_processInfo(listTemp) #调用此方法检查当前进程信息，如发生变化则抛出异常，由main()里的主循环异常处理函数处理
        for elemOfProcessInfo in self.listProcessInfo:
            flag_Found = False
            for elem in listTemp:
                if (elem != []) and (elem[0] == elemOfProcessInfo[0]):
                    if elem[4] == '<':
                        strSubProcCPULoad = elem[7+1] #有些进程top命令返回信息里stat列是"s <"的形式中间有个空格会被当作分隔符，此时split()后的list里CPULoad对应值的下标得往后一位
                        listProcCPULoad.append(float(strSubProcCPULoad))
                    else:
                        strSubProcCPULoad = elem[7] 
                        listProcCPULoad.append(float(strSubProcCPULoad))
                    flag_Found = True 
                    break
            if flag_Found == False:
                listProcCPULoad.append(0.0) 
        return listProcCPULoad

    def get_procMemUsage(self):
        """#基于listProcessInfo，获取所有子进程内存占用PSS值的方法"""
        listProcMemUsage = []
        if self.deviceAPILevel >= 14:  #安卓4.0及上的，用这种逻辑
            for elem in self.listProcessInfo:
                print '[Debug]:ProcessID---',elem[0]
                strTemp = self.adb.shell("dumpsys meminfo {0}|{1} grep 'TOTAL'".format(elem[0],BUSYBOX_PATH),timeout=ADB_TIMEOUT)
                try:
                    strSubProcMemUsage = strTemp.split()[1].encode('UTF-8')
                except IndexError:
                    currentOutput = self.adb.shell("dumpsys meminfo {0}".format(elem[0]),timeout=ADB_TIMEOUT)
                    if currentOutput.find('No process found')!=-1: #如果不等于-1则表明找到了这段string
                        strSubProcMemUsage = 0.0
                    else:
                        print 'Met an unhandled IndexError. Received this output "{0}" While getting MemUsage of process "{1}"'.format(strTemp,elem[1])
                        print 'Current device output when executing "dumpsys meminfo {} is:'.format(elem[1]), currentOutput
                        raise
                listProcMemUsage.append(round(int(strSubProcMemUsage)/1024.0,4))
            return listProcMemUsage
        else:   #安卓4.0以下的，用这种逻辑
            for elem in self.listProcessInfo:
                strTemp = self.adb.shell("dumpsys meminfo {0}|{1} grep '(Pss)'".format(elem[0],BUSYBOX_PATH),timeout=ADB_TIMEOUT)
                try:
                    strSubProcMemUsage = strTemp.split()[4].encode('UTF-8')
                except IndexError:
                    currentOutput = self.adb.shell("dumpsys meminfo {0}".format(elem[0]),timeout=ADB_TIMEOUT)
                    if currentOutput.find('No process found')!=-1: #如果不等于-1则表明找到了这段string
                        strSubProcMemUsage = 0.0
                    else:
                        print 'Met an unhandled IndexError. Received this output "{0}" While getting MemUsage of process "{1}"'.format(strTemp,elem[1])
                        print 'Current devices output when executing "dumpsys meminfo {} is:'.format(elem[1]), currentOutput
                        raise
                listProcMemUsage.append(round(int(strSubProcMemUsage)/1024.0,4))
            return listProcMemUsage

    def collect_allPerfInfo(self):
        """#将获取的数据汇总处理为中间数据的方法,每运行一次相当于一次采样. 返回一维List：设备时间戳、流量、各子进程的CPUload和MemUsage"""
        strCurrentTime = self.adb.shell(r"date +%s",timeout=ADB_TIMEOUT).replace("\r\n","").encode('UTF-8')
        strCurrentTraffic = self.get_networkTraffic()   
        listEachProcCPULoad = self.get_procCPULoad_viaTop()
        listEachProcMemUsage = self.get_procMemUsage()
        floatTotalCPULoad = round(sum(listEachProcCPULoad),4)
        floatTotalMemUsage = round(sum(listEachProcMemUsage),4)
        listAllPerfInfo = [strCurrentTime,strCurrentTraffic,floatTotalCPULoad,floatTotalMemUsage]
        for x in xrange(len(listEachProcCPULoad)):       #循环遍历listEachProcCPULoad和listEachProcMemUsage,追加到listAllPerfInfo里
            listAllPerfInfo.append(listEachProcCPULoad[x])
            listAllPerfInfo.append(listEachProcMemUsage[x])
        #将执行一次此方法所收集到的性能数据list以更加可读的形式在控制台打印出来
        listForPrinting = [elem for elem in listAllPerfInfo]
        listForPrinting[0] = myUtil.seconds2Str(int(listAllPerfInfo[0]))
        print listForPrinting
        return listAllPerfInfo

class CSVRecorder(object):
    """CSV格式Log保存器，初始化时需要2个参数：以APP对象的get_processInfo()方法返回的list来初始化csv文件的列名，以LogFileName来创建Log文件；
    运行时，接受App对象collect_allPerfInfo方法返回的List作为一行新数据追加到csv中"""
    def __init__(self,listProcessInfo,logFileName):
        """#创建并初始化CSV Log文件的数据列名"""
        listProcName = self.__getProcessName(listProcessInfo)
        print listProcName
        self.logFileName = logFileName
        listColumnHeader = ['Time','TotalNetworkTraffic(MB)','CPULoad(%)_Total','MemUsage(MB)_Total']
        for elem in listProcName:  #遍历进程信息list,添加所有进程名对应的CPUload列和MemUsage列到表头行
            listColumnHeader.append('CPULoad(%)_' + elem)
            listColumnHeader.append('MemUsage(MB)_' + elem)
        # print '----dabao--test----\n',listColumnHeader
        with open(logFileName,'wb') as csvFile:
            csvFile.write('\xEF\xBB\xBF') #为兼容windows文件编码写入的文件头，防止乱码
            writer = csv.writer(csvFile)
            writer.writerow(listColumnHeader)


    def __getProcessName(self,listProcessInfo):
        """获取运行app程序的进程名字列表，如果有重名则后缀加_1进行区分，返回进程名字列表"""
        listProcName = []
        for elem in listProcessInfo:
            listProcName.append(elem[1])

        #如果有重名则后缀加_1进行区分
        lastList=listProcName[-1]
        for i in range(len(listProcName)-2,-1,-1):
            if listProcName[i]==lastList:
                listProcName[i]=str(listProcName[i]) + "_1"
                # list0.remove(list0[i])
            else:
                lastList=listProcName[i]
        return listProcName

    def saveCurrentData(self,listAllPerfInfo,testStep = None):
        """#将汇总的数据结构存储追加到CSV Log文件的方法"""
        with open(self.logFileName,'ab') as csvFile:
            writer = csv.writer(csvFile)
            if testStep == None:
                writer.writerow(listAllPerfInfo)
            else:
                listAllPerfInfo[0] = ''.join([listAllPerfInfo[0],testStep])
                writer.writerow(listAllPerfInfo)            


def main():
    #以下是命令行参数处理代码
    toolHelpDescription = ("This tool can record 3 key runtime performance indicators of android app into a csv file:\n"
        "\tTotalNetworkTraffic: Tx+Rx traffic of app.(KB)\n"
        "\tCPULoad: Each subprocess's CPULoad(%).\n"
        "\tMemUsage: Each subprocess's memory usage(KB).") 
    parser = argparse.ArgumentParser(description = toolHelpDescription, formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-p', metavar = 'appPackageName', required = True, dest = 'strPackageName', action = 'store', help = 'The package name of your app under testing, such as com.esbook.reader/com.esvideo. You can find it from the AndroidManifest.xml file of your app')
    parser.add_argument('-f', metavar = 'LogCSVFileName', required = True, dest = 'strLogFileName', action = 'store', help = 'It should be end with .csv, and will be saved at the same folder. Existing file with the same name will be overwrited!')
    parser.add_argument('-t', metavar = 'Execution time', required = False, dest = 'intTime', action = 'store', default= 'NULL' ,help = 'Specific a total execution time(in seconds). ')
    args = parser.parse_args()


    #以下是主函数执行代码
    try:
        myUtil.checkDevice()
    except Exception as e:
        print e
        return
    app = AppUnderTest(args.strPackageName)
    dataRecorder = CSVRecorder(app.listProcessInfo,args.strLogFileName)
    errorCounts = 0
    SamplingInterval = 0.5
    timeoutEvent = threading.Event()
    if args.intTime != 'NULL':  #如果执行时间这个参数不是默认的NULL值，则启动定时线程
        t = threading.Timer(int(args.intTime),myUtil.timeIsUp,args=(timeoutEvent,))
        t.start()

    while True:
        if timeoutEvent.isSet() != True:
            try:
                currentPerfInfo = app.collect_allPerfInfo()
                print '[Debug]:---before save csv test---'
                dataRecorder.saveCurrentData(currentPerfInfo)
                #print '---after save csv dabao test---'
                sleep(SamplingInterval)    
            except KeyboardInterrupt:
                if args.intTime != 'NULL' and timeoutEvent.isSet() != True:
                    t.cancel()
                myUtil.dumpDeviceLog(args.strLogFileName.rpartition('.')[0])
                raise SystemExit('Stopped by user! Performance log has been saved to .\\{0}'.format(args.strLogFileName))
            except myUtil.FoundNewProcessException:
                print "Found new subprocess!"
            except Exception as e:
                errorCounts+=1
                if errorCounts <= 3:
                    print "An error is occurred! wait for 1 sec and retry."
                    sleep(1)            
                else:
                    if args.intTime != 'NULL' and timeoutEvent.isSet() != True:
                        t.cancel()
                    myUtil.dumpDeviceLog(args.strLogFileName.rpartition('.')[0])
                    raise SystemExit("\nCatched runtime error for 3 times, program is terminated by below reason:\n{0}".format(e))
            else:
                errorCounts = 0
        else:
            myUtil.dumpDeviceLog(args.strLogFileName.rpartition('.')[0])
            return

if __name__ == '__main__':
    main()
