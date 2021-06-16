import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import pandas as pd
import mplfinance as mpf
import data_more
warnings.filterwarnings('ignore')   #过滤警告

# 获取数据
data_first = pd.read_csv('data.csv')
data_second = data_first.drop(['涨跌幅(%)','涨跌额','成交金额(万元)','振幅(%)','换手率(%)'],axis=1)
data_second = data_second.rename(columns={'日期':'Date','开盘价':'Open','最高价':'High','最低价':'Low','收盘价':'Close','成交量(手)':'Volume'})
data_second = data_second.set_index('Date')   #将日期这一列转化为索引
data_second = data_second.loc[:,('Open','High','Low','Close','Volume')].applymap(lambda x:x.replace(',','')).astype(float)
data_second = data_second.reset_index('Date')   #将索引列转化为列
data_second['Date'] = pd.to_datetime(data_second['Date'],infer_datetime_format=True)   #将日期这列的数据类型转化为datatime类型
data_second = data_second.set_index('Date')
data_second.sort_index(inplace=True)  #把数据按照日期排序
data_second.to_csv('data_draw.csv')
# print(data_second.info())
ts_code = '600519' #股票代码

# 绘制股票成交量折线图
def volume():
    plt.figure(figsize=(10,8),dpi=80,num=4)   #设置画布大小（8*6），分辨率为80，
    myfont=mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')   #设置中文字体
    x= data_second['Date']   #设置x轴数据
    y1 = data_second['Volume']   #设置y轴数据
    plt.plot(x, y1, color='r',label='股票成交量',  linewidth=2)   #设置线的颜色、粗细以及坐标轴的抬头
    plt.xlabel('日期',FontProperties=myfont,fontsize=15)  #设置x轴标签
    plt.xticks(rotation=60)   #旋转x轴的标签
    plt.ylabel('成交量',FontProperties=myfont,fontsize=15)   #设置y轴标签
    plt.title('贵州茅台成交量折线图',FontProperties=myfont,fontsize=15)   #设置坐标系的题目
    plt.legend(prop=myfont)
    plt.show()   #展示图形
# volume()

#绘制股票OHLC线图
def OHLC():
    plt.figure(figsize=(12,8),dpi=80,num=4)
    myfont=mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
    x= data_second['Date']
    plt.plot(x, data_second.loc[:,'Open'], label='开盘价',  linewidth=2)
    plt.plot(x, data_second.loc[:,'High'], label='最高价',  linewidth=2)
    plt.plot(x, data_second.loc[:,'Low'], label='最低价',  linewidth=2)
    plt.plot(x, data_second.loc[:,'Close'], label='收盘价',  linewidth=2)
    plt.xticks(rotation=60)
    plt.xlabel('日期',FontProperties=myfont,fontsize=15)
    plt.ylabel('价格/汇率',FontProperties=myfont,fontsize=15)
    plt.title('贵州茅台股票OHLC线图',FontProperties=myfont,fontsize=15)
    plt.legend(prop=myfont)
    plt.show()
# OHLC()

#绘制k线整合均线图
def K_Line():
    mc = mpf.make_marketcolors(up='red',   #价格上涨为红色
                               down='green',   #价格下降为绿色
                               wick='black'   #影线为黑色
                             )
    style = mpf.make_mpf_style(base_mpl_style='ggplot',marketcolors=mc)
    mpf.plot(data_second,type='candle',title=ts_code,style=style,volume=True,mav=(5,10,20,30))
# K_Line()

# 归一化数据可视化
def RealStock():
    datanorm = pd.read_csv('datanorm.csv')
    plt.figure(figsize=(10, 8), dpi=80, num=4)  # 设置画布大小（8*6），分辨率为80，
    myfont = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')  # 设置中文字体
    x = datanorm['日期']  # 设置x轴数据
    y1 = datanorm['开盘价']  # 设置y轴数据
    plt.plot(x, y1, label='实际开盘价', color='r', linewidth=2)  # 设置线的颜色、粗细以及坐标轴的抬头
    plt.xlabel('日期', FontProperties=myfont, fontsize=15)  # 设置x轴标签
    plt.xticks(rotation=60)  # 旋转x轴的标签
    plt.ylabel('开盘价', FontProperties=myfont, fontsize=15)  # 设置y轴标签
    plt.title('贵州茅台历史开盘价', FontProperties=myfont, fontsize=15)  # 设置坐标系的题目
    plt.legend(prop=myfont)
    plt.show()  # 展示图形
# RealStock()

def Predict():
    datanorm = pd.read_csv('datanorm.csv')
    y0 = pd.read_csv('datanorm.csv',usecols=['开盘价'],nrows=43)
    # print(type(y0))
    y0 = y0['开盘价'].tolist()
    # print(y0)
    y2 = data_more.result   #多维数组
    # print(type(y2))
    y2 = y2.flatten()   #降为1维数组
    y2 = y2.tolist()   #转化为列表
    y2 = y0 + y2
    # print(y2)
    plt.figure(figsize=(10, 8), dpi=80, num=4)  # 设置画布大小（8*6），分辨率为80，
    myfont = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')  # 设置中文字体
    x = datanorm['日期']  # 设置x轴数据
    y1 = datanorm['开盘价']  # 设置y轴数据
    plt.plot(x, y1, label='实际开盘价', color='r', lw=2)  # 设置线的颜色、粗细以及坐标轴的抬头
    plt.plot(x, y2, label='预测开盘价', color='b',lw=2,ls='--')
    plt.xlabel('日期', FontProperties=myfont, fontsize=15)  # 设置x轴标签
    plt.xticks(rotation=60)  # 旋转x轴的标签
    plt.ylabel('开盘价', FontProperties=myfont, fontsize=15)  # 设置y轴标签
    plt.title('贵州茅台历史预测开盘与实际开盘的差异', FontProperties=myfont, fontsize=15)  # 设置坐标系的题目
    plt.legend(prop=myfont)
    plt.show()  # 展示图形
Predict()