#coding: UTF-8
#初版作者：张宁@easou

from reportlab.platypus import Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing,String
from reportlab.graphics.charts.lineplots import LinePlot
import myUtil

styleSheet = getSampleStyleSheet()

def chs(string,fontSize=10,style='Normal'):
    """工具函数，将中文字符串转化为带字体tag的paragraph对象"""
    para = Paragraph('<font name="chsFont" size={0}>{1}</font>'.format(fontSize,string), styleSheet[style])
    return para

class SummaryTableBuilder(object):
    """此类不需实例化，它作为生成首页汇总表格的类,以下类方法直接调用：
           - cls.addOneRow(data):在为单个Log文件生成报告的功能代码里，构造好该Log文件在汇总
                表格里对应的行数据list后，直接调本方法来追加
           - cls.buildTable(): 待本工具的主函数中已经完成了整个PDF内容story的构造后，使用
                list.insert()方法将本类的buildTable方法返回值加入到story中文档首页标题后位置即可"""

    dataOfSummaryTable = [['测试场景','网络流量\n(MB)','最小CPU\n占用(%)','最大CPU\n占用(%)','平均CPU\n占用(%)',
                            '最小内存\n消耗(MB)','最大内存\n消耗(MB)','平均内存\n消耗(MB)']]
    @classmethod
    def addOneRow(cls,data,index):
        """传入的行内容的首元素是CSV文件名，将其添加Link tag后再变为Paragraph对象，则可以跳转
        到href值对应的anchor标签处（在genFlowablesOfLogFile()函数中已为每个Log文件的首行增加
        了ancher tag '<a name=#index/>'）"""
        nameWithLinkTag = u'<link href="#{0}" color="blue" fontName="chsFont">{0}. <u>{1}</u></link>'.format(index,data[0])
        data[0] = Paragraph(nameWithLinkTag,styleSheet["Normal"])
        SummaryTableBuilder.dataOfSummaryTable.append(data)

    @classmethod
    def buildTable(cls):
        sty = [
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,0),colors.lightblue),
            ('FONT',(0,0),(-1,0),'chsFont'),
            ('SIZE',(0,0),(-1,0),10),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('RIGHTPADDING',(0,0),(-1,-1),0),
           ]
        t=Table(SummaryTableBuilder.dataOfSummaryTable,style=sty,
               rowHeights=[30,].extend([14]*len(SummaryTableBuilder.dataOfSummaryTable)),
               colWidths=[380,60,60,60,60,60,60,60])  #列宽如果使用'x%'的形式来设定，首列的Log文件名不会自动换行，所以此处用hardcoded的数字
        return t

def genTableOfSingleTest(objLogFileReader,index):
    """生成单个测试场景Log数据的简报表格,同时把该测试场景的简报加入到汇总报告表格的数据集中"""
    colKPI = [x for x in objLogFileReader.headerLine if x != 'Time'] #从CSV格式log文件首行获取除"Time"外的列名，作为测试场景简报首列内容
    networkTraffic = objLogFileReader.getValueDelta(colKPI[0])
    rowInSummaryTable = [objLogFileReader.csvFileName,networkTraffic,] #用来追加到汇总表中本文件对应行的数据

    data =  [[chs('性能指标项'),chs('关键值'), chs('数值')],
             [colKPI[0], chs('总流量'), networkTraffic],
            ]
    for x in xrange(1,len(colKPI)):
        valueMin = objLogFileReader.getValueMin(colKPI[x])
        valueMax = objLogFileReader.getValueMax(colKPI[x])
        valueAvg = objLogFileReader.getValueAvg(colKPI[x])
        data.append([colKPI[x],chs('最小值'),valueMin])
        data.append([colKPI[x],chs('最大值'),valueMax])
        data.append([colKPI[x],chs('平均值'),valueAvg])
        if x == 1: 
        # 当下标等于1，则表示当前在处理csvlog文件中主进程CPUload那一列数据，就将该列的最大、最小、平均值加入到
        #本文件在汇总表格中的对应行数据中
            rowInSummaryTable.append(valueMin)
            rowInSummaryTable.append(valueMax)
            rowInSummaryTable.append(valueAvg)
        elif x == 2:
        # 当下标等于2，则表示当前在处理csvlog文件中主进程内存占用那一列数据，就将该列的最大、最小、平均值加入到
        #本文件在汇总表格中的对应行数据中
            rowInSummaryTable.append(valueMin)
            rowInSummaryTable.append(valueMax)
            rowInSummaryTable.append(valueAvg)
    SummaryTableBuilder.addOneRow(rowInSummaryTable,index) #往汇总报表里添加一行数据
    sty = [
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,0),colors.lightblue),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
           ]
    for x in xrange(len(colKPI)-1):
        offset = 2+x*3
        sty.append(('SPAN',(0,offset),(0,offset+2)))
    lst = []
    lst.append(chs('测试场景结果简报:'))
    lst.append(Spacer(0,3))
    #t=Table(data,style=sty,rowHeights = [15]*len(data))
    t=Table(data,style=sty,rowHeights = [15]*len(data),colWidths=['*','15%','15%'])
    lst.append(t)
    return lst

def genLinePlot(objLogFileReader,columnName):
    """生成单个测试场景Log数据的指定数值列的折线图"""
    plotWidth,plotHeight = 500,180
    d = Drawing(plotWidth,plotHeight)
    title = columnName
    d.add(String(0,plotHeight-10,title,fontSize=12,fillColor=colors.black))
    data = objLogFileReader.getLinePlotData(columnName)
    lp = LinePlot()
    lp.x,lp.y = 50,25
    lp.width,lp.height = plotWidth-50,plotHeight-50
    lp.data = data
    lp.joinedLines = 1
    lp.lines[0].strokeColor = colors.blue
    lp.lines[0].strokeWidth = 1
    #设置图表x轴的标尺步长、数据标签文本格式等属性
    lp.xValueAxis.valueMin = min([x[0] for x in data[0]])
    lp.xValueAxis.valueMax = max([x[0] for x in data[0]])
    xValueRange = lp.xValueAxis.valueMax - lp.xValueAxis.valueMin
    lp.xValueAxis.valueStep = xValueRange/10.0
    lp.xValueAxis.labelTextFormat = myUtil.seconds2Str
    #设置图表y轴的标尺步长、数据标签文本格式等属性
    yValueMin = min([x[1] for x in data[0]])
    yValueMax = max([x[1] for x in data[0]])   
    yValueRange = yValueMax - yValueMin
    if (yValueMin-yValueRange/2) > 0:
        lp.yValueAxis.valueMin = yValueMin - yValueRange/2
    else:
        lp.yValueAxis.valueMin = yValueMin
    lp.yValueAxis.valueMax = yValueMax+ 0.01 + yValueRange/3 #+1避免当y轴最大值和最小值相等时valuseStep为0,导致绘图库计算y轴格数时出现除零错误
    lp.yValueAxis.valueStep = (lp.yValueAxis.valueMax - lp.yValueAxis.valueMin)/10
    lp.yValueAxis.labelTextFormat = '%.2f'
    lp.yValueAxis.visibleGrid = 1
    lp.yValueAxis.gridStrokeWidth = 0.5
    lp.yValueAxis.gridStrokeColor = colors.gray
    d.add(lp)
    return d

def genFlowablesOfLogFile(objLogFileReader,index):
    """负责为单个csv文件生成报告内容，接受参数：logFile对象，索引号；返回值：flowable对象列表"""
    story = [PageBreak()]
    #Reportlab库有设计缺陷，如果anchor tag的name属性直接用文件名，太长时则会在paragraph模块中被自动换行时报错，因此用index来作为anchor名称
    firstLine = u'<a name="{0}"/><font name="chsFont">{0}. {1}</font>'.format(index,objLogFileReader.csvFileName)
    story.append(Paragraph(firstLine,styleSheet["Heading1"]))
    #将单个测试场景的数值报告表追加到story里
    for each in genTableOfSingleTest(objLogFileReader,index):
        story.append(each)
    story.append(Spacer(0,2))
    #将单个测试场景的所有数值列生成折线图后追加到story里
    for columnName in objLogFileReader.headerLine:
        if columnName == 'Time':
            continue    #跳过时间序列那一列
        story.append(Spacer(0,2))
        story.append(genLinePlot(objLogFileReader,columnName))
    return story
