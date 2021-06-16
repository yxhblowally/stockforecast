import requests
import bs4
from bs4 import BeautifulSoup
import xlwt
import random
import re

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

# 获取网页数据
def getHTMLText(url):
    try:
        r = requests.get(url,headers={'User-Agent':random.choice(user_agent)},timeout =30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 解析网页数据
def parHTMLText(stocklist,demo):
    soup = BeautifulSoup(demo,"lxml")
    for tr in soup.find_all('table',class_="m-table1"):
        if isinstance(tr,bs4.element.Tag):
            tds = tr('td')
            # print(tds)   #生成一个列表
            for i in range(0,len(tds),10):
                td = tds[i:i+10]  #将以上生成的列表分割成多个列表
                # print(td)
                stocklist.append([td[0].string, td[1].string, td[2].string, td[3].string, td[4].string,
                                  td[5].string, td[6].string, td[7].string, td[8].string, td[9].string])
            return stocklist
            # print(stocklist)

# 打印十股网页列表
def printstocklist(stocklist,num):
    tplt = "{0:^3}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\t{5:^10}\t{6:^10}\t{7:^10}\t{8:^10}\t{9:^10}"
    for i in range(num):
        s = stocklist[i]
        stocklists = tplt.format(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9])
        return stocklists
        # print(stocklists)

# 存储网页数据
def loadstockdata(stocklists,html):
    time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", html)   #利用正则表达式获取时间参数
    index = len(stocklists)
    wb = xlwt.Workbook()   #创建工作簿
    sheet = wb.add_sheet('沪深十大成交股',cell_overwrite_ok=True)   #创建表单
    style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    a = xlwt.Alignment()  # 设置单元格的对齐方式
    a.horz = 0x02  # 水平方向向上居中对齐
    style.alignment = a
    row0 = ['排名','股票代码','股票简称','收盘价','涨跌幅',
           '涨跌额','买入金额','卖出金额','净买额','成交金额']
    for i in range(0,len(row0)):
        sheet.write(0,i,row0[i],style)
        for row in range(0,index):
            for column in range(0,len(stocklists[row])):
                sheet.col(column).width = 3333
                sheet.write(row+1,column,stocklists[row][column],style)
    sheet.write(0,11,time.group(),style)   #写入时间参数
    f_path = 'D:/Stock forecasts/stockdata.xls'
    wb.save(f_path)

# 主函数
def main():
    stockinfo = []
    url = "http://data.10jqka.com.cn/hgt/hgtb/"
    html = getHTMLText(url)
    stockdatas = parHTMLText(stockinfo,html)
    printstocklist(stockdatas,10)
    loadstockdata(stockdatas,html)

main()









