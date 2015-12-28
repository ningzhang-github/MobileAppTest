#!/bin/env python
#coding: utf-8

#初版作者：张宁@easou

from reportlab.platypus import BaseDocTemplate,SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,cm
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing,String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from LogFileReader import LogFileReader
import elemGenerator
import myUtil
import argparse
import os

#pdfmetrics.registerFont(TTFont('chsFont','msyh.TTF'))
#pdfmetrics.registerFont(TTFont('chsFontBold','msyhbd.TTF'))

class mySimpleDocTemplate(SimpleDocTemplate):
    """docstring for mySimpleDocTemplate"""
    def __init__(self, fileName,**kw):
        SimpleDocTemplate.__init__(self,fileName,**kw)
        self.leftMargin, self.rightMargin = 0.5*inch,0.5*inch
        self.topMargin,self.bottomMargin = 0.5*inch,0.5*inch


#设定默认页面尺寸
PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = '宜搜Android应用程序系统资源消耗分析'
pageinfo = 'test result'

#定义myFirstPage函数、myLaterPages函数，以便传给文档对象用来设定首页和内容页的模板
def myFirstPage(canvas,doc):
    thisPage_width = PAGE_WIDTH*1.5
    thisPage_height = PAGE_HEIGHT*1.15
    canvas.saveState()
    canvas.setPageSize((thisPage_width,thisPage_height))
    canvas.setFont('chsFont',24)
    canvas.drawCentredString(thisPage_width/2.0,thisPage_height-80,Title)
    canvas.setFont('Times-Roman',12)
    canvas.drawString(inch,0.75*inch,"First page of {0}".format(pageinfo))
    canvas.restoreState()

def myLaterPages(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',12)
    canvas.drawString(inch,0.75*inch,"Page {0} of {1}".format(doc.page,pageinfo))
    canvas.restoreState()


def main():
    #以下是命令行参数处理代码,接受参数指定待处理Log文件所在文件夹，以及输出文件的文件名
    toolHelpDescription = ("""To generate test report from csv log files in a given folder.
        Example:
        >ReportGenerator.py -folder .\logfiles -pdf reportName.pdf""") 

    parser = argparse.ArgumentParser(description = toolHelpDescription, formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-folder', metavar = 'folderName', required = True, dest = 'logFolder', action = 'store', help = "The floder name which contains log files.")
    parser.add_argument('-pdf', metavar = 'fileName', required = True, dest = 'pdfName', action = 'store', help = "output file name, can be in CHS.")
    
    args = parser.parse_args()


    #以下是防御代码，处理找不到文件或者目录的错误
    if os.path.isdir(args.logFolder):
        logFolder = args.logFolder.decode('gbk')
    else:
        raise SystemExit('"{0}" is not a valid folder, please check.'.format(args.logFolder))
    logFileList = [name for name in os.listdir(logFolder) if name.endswith('.csv')]
    if len(logFileList) == 0:
        raise SystemExit('No .csv file is found in "{0}", please check.'.format(args.logFolder))

    #以下是检测当前系统并使用合适字体的代码
    if myUtil.currentPlatform() != 'Win7orLower':
        if myUtil.currentPlatform() == 'Win8':
            pdfmetrics.registerFont(TTFont('chsFont','msyh.TTC'))
        elif myUtil.currentPlatform() == 'MacOS':
            pdfmetrics.registerFont(TTFont('chsFont','XingKai.ttc'))
        elif myUtil.currentPlatform() == 'Linux': #未确定linux上是否能直接用此字体，待实际使用验证
            pdfmetrics.registerFont(TTFont('chsFont','XingKai.ttc'))
    else:
        pdfmetrics.registerFont(TTFont('chsFont','msyh.TTF'))


    #使用SimpleDocTemplate初始化文档对象
    pdfName = args.pdfName.decode('gbk')
    doc = mySimpleDocTemplate(pdfName)
    #初始化包含所有flowable对象的一个list
    story = []
   # story.append(PageBreak())
    #遍历给定子目录下所有的csv文件并生成对应报告页
    for i,name in enumerate(logFileList):
        indexOfLogFile = i+1
        logFile = LogFileReader(os.path.join(logFolder,name))       
        flowablesOfLogFile = elemGenerator.genFlowablesOfLogFile(logFile,indexOfLogFile)
        for each in flowablesOfLogFile:
            story.append(each)
        print u"{} is done!".format(name)
    t = elemGenerator.SummaryTableBuilder.buildTable()
    t.hAlign = 'LEFT' #因reportLab库的设计限制，为完整显示汇总表格而加宽文档首页后，doc对象的Frame元素属性仍然是A4对应大小，左对齐来绕过此问题
    story.insert(0,t) #在内容story列表的第2个位置插入汇总报告表
    #将包含所有flowable对象的list生成为PDF文档
    print u"Generating test report file {}.....".format(pdfName)
    doc.build(story,onFirstPage=myFirstPage,onLaterPages=myLaterPages)
    print u"All done!"

if __name__ == '__main__':
    main()
