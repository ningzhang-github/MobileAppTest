#coding: utf-8
#初版作者：张宁@easou

import csv
import os
import myUtil

class LogFileReader(object):
    """读取csv格式的log文件，解析返回报告生成工具需要的数据结构"""
    def __init__(self, csvFilePath):
        self.csvFilePath = csvFilePath
        self.csvFileName = os.path.basename(self.csvFilePath).rpartition('.')[0] #在csv目录变量中获取CSV文件名，并用字符串对象内置函数rpartition去掉扩展名
        self.csvDataSet = self.__getCSVDataSet(self.csvFilePath)
        self.timeSeries = self.__getTimeSeries()
        self.headerLine = self.__getHeaderLine()

    def __getCSVDataSet(self,csvFilePath):
        """私有方法，给__init__()方法调用，在实例化时一次性将所有CSV数据读入为内存的字典对象，减少频繁的磁盘I/O"""
        with open(self.csvFilePath,'rb') as f:
            f_csv = csv.DictReader(f)
            csvDataSet = [dictRow for dictRow in f_csv]
        return csvDataSet

    def __getColumnData(self,columnName):
        """得到指定列数据"""
        listTemp = []
        for row in self.csvDataSet:
            listTemp.append(row[columnName])
        return listTemp

    def __getHeaderLine(self):
        """得到csv文件的列头一行的list对象"""
        with open(self.csvFilePath,'rb') as f:
            f_csv = csv.reader(f)
            headerLine = next(f_csv)
            headerLine[0] = headerLine[0].replace('\xef\xbb\xbf','')
            return headerLine

    def __getTimeSeries(self):
        """调用__getColumData方法得到log中的时间序列,并转化为hhmmss的浮点数格式方便比较大小"""
        listTemp = self.__getColumnData('\xef\xbb\xbf'+'Time') #\xef\xbb\xbf为文件头,性能测试工具生成的csv文件为兼容windows文件编码防止乱码而写入的
        timeSeries = [int(elem) for elem in listTemp]
        return timeSeries

    def getValueSeries(self,columnName):
        """调用__getColumData方法得到log中指定列名的值序列,并全部转化为浮点值"""
        valueSeries = self.__getColumnData(columnName)
        valueSeries = [float(eachValue) for eachValue in valueSeries]
        return valueSeries

    def getLinePlotData(self,columnName):
        """使用python内置的zip方法得到reportlab折线图所需的数据形式：list of list of tuple of 2 values[[(time,value),(time,value)]]"""
        valueSeries = self.getValueSeries(columnName)
        linePlotData = [zip(self.timeSeries,valueSeries),]
        return linePlotData

    def getValueMax(self,columnName):
        """得到指定列的最大值"""
        valueMax = max(self.getValueSeries(columnName))
        return round(valueMax,3)
    
    def getValueMin(self,columnName):
        """得到指定列的最小值"""
        valueMin = min(self.getValueSeries(columnName))
        return round(valueMin,3)

    def getValueAvg(self,columnName):
        """得到指定列的平均值"""
        sumOfValueSeries = sum(self.getValueSeries(columnName))
        valueAvg = float(sumOfValueSeries)/len(self.getValueSeries(columnName))
        return round(valueAvg,3)

    def getValueDelta(self,columnName):
        """得到指定列的首尾数值变化值，就算算总网络流量专用"""
        valueSeries = self.getValueSeries(columnName)
        return round((valueSeries[-1] - valueSeries[0]),3)


def testRun():
    logFile = LogFileReader("test.csv")
    # print logFile.headerLine
    # print logFile.timeSeries,"\nlen of this list: ",len(logFile.timeSeries)
    # print logFile.getValueSeries("TotalNetworkTraffic(KB)"), "\nlen of this list: ",len(logFile.getValueSeries("TotalNetworkTraffic(KB)"))
    print logFile.getLinePlotData("TotalNetworkTraffic(KB)"),"\nlen of this list: ",len(logFile.getLinePlotData("TotalNetworkTraffic(KB)")[0])
    print myUtil.str2Seconds('10:09:59')

if __name__ == "__main__":
    testRun()
