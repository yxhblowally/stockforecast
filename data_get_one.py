import requests
from bs4 import BeautifulSoup
import xlwt
import xlrd
from xlutils.copy import copy
import random
import bs4

user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

# 获取个股网页数据
def getHTMLText(url):
    try:
        r = requests.get(url,headers = {'User-Agent':random.choice(user_agent)},timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 解析个股网页数据
def parserHTML(html,stocklist):
    soup = BeautifulSoup(html,'lxml')
    for tr in soup.find_all('table',class_='table_bg001 border_box limit_sale'):
        if isinstance(tr,bs4.element.Tag):
            tds = tr('td')
            # print(tds)
            for i in range(0,len(tds),11):
                td = tds[i:i+11]
                # print(td)
                stocklist.append([td[0].string,td[1].string,td[2].string,td[3].string,td[4].string,td[5].string,
                                  td[6].string,td[7].string,td[8].string,td[9].string,td[10].string])
            # print(stocklist)
            return stocklist

# 打印网页列表
def printstocklist(stocklist,num):
    tplt = "{0:^3}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\t{5:^10}\t{6:^10}\t{7:^10}\t{8:^10}\t{9:^10}\t{10:^10}"
    for i in range(num):
        s = stocklist[i]
        stocklists = tplt.format(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10])
        return stocklists
        # print(stocklists)

# 存储数据
def loaddatas(stocklists):
    rb = xlrd.open_workbook('stockdata.xls',formatting_info=True)   #打开已有的工作簿
    wb = copy(rb)    #对已有的工作簿进行复制
    sheet2 = wb.add_sheet('贵州茅台历史数据一览',cell_overwrite_ok=True)
    style = xlwt.XFStyle()   #创建一个样式对象，初始化样式
    a = xlwt.Alignment()   #设置单元格的对齐方式
    a.horz = 0x02   #水平方向上居中对齐
    a.vert = 0x01   #垂直方向上居中对齐
    style.alignment = a
    row0 = ['日期','开盘价','最高价','最低价','收盘价','涨跌额','涨跌幅(%)','成交量(手)','成交金额(万元)','振幅(%)','换手率(%)']
    for x in range(0,len(row0)):
        sheet2.write(0,x,row0[x],style)
        for i in range(0,len(stocklists)):
            for j in range(0,len(stocklists[i])):
                sheet2.col(j).width = 3333   #设置单元格宽度为3333
                sheet2.write(i+1,j,stocklists[i][j],style)
    wb.save('stockdata.xls')

# 主函数
def main():
    stocklist = []
    url = "http://quotes.money.163.com/trade/lsjysj_600519.html?year=2021&season=1"
    html = getHTMLText(url)
    stocklists = parserHTML(html,stocklist)
    printstocklist(stocklist,58)
    loaddatas(stocklists)

main()