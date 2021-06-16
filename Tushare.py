import tushare as ts
import numpy as np
import pandas as pd
import warnings
import matplotlib
import mplfinance as mpf
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# token = '89b177c56ac9d11aa22c9807de0a54d8e36af4c19bc48571aafe7556'
# pro = ts.pro_api(token)

data = ts.get_hist_data('600519',start='2020-04-28',end='2021-04-28')   #读取股票代码为600519的股票，且起始时间为2020-04-28，终止时间为2021-04-28
data = data.iloc[::-1]   #按时间顺序排列
data['日期'] = data.index   #将索引列转化为一列新特征，以‘日期’命名
data['日期'] = pd.to_datetime(data['日期'],infer_datetime_format=True)   #将日期列类型转化为日期类型
# print(data)
data.to_csv('data_almost.csv')

# 数据归一化
def normalization():
    data = pd.read_csv('data_almost.csv')
    columns = [x for x in data.columns if x not in ['date','volume','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20','turnover','日期']]   #去掉成交金额这一列
    max_min_scaler = lambda x : (x-np.min(x)) / (np.max(x)-np.min(x))
    for title in columns:
        data[title] = data[[title]].apply(max_min_scaler)
    data.to_csv('dataalmostnorm.csv',index=None)
normalization()

#贵州茅台历史成交量
def volume():
    plt.figure(figsize=(8,6),dpi=80,num=4)
    myfont=matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
    x= data['日期']
    y1 = data['volume']
    plt.plot(x, y1, color='r',label='股票成交量',  linewidth=2)
    plt.xlabel('日期',FontProperties=myfont,fontsize=15)
    plt.ylabel('成交量',FontProperties=myfont,fontsize=15)
    plt.title('股票成交量折线图',FontProperties=myfont,fontsize=15)
    plt.legend(prop=myfont)
    plt.show()
# volume()

#贵州茅台开盘价、最高价、最低价、收盘价
def ohlc():
    plt.figure(figsize=(12, 8), dpi=80, num=4)
    myfont = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
    x = data['日期']
    plt.plot(x, data.loc[:, 'open'], label='开盘价', linewidth=2)
    plt.plot(x, data.loc[:, 'high'], label='最高价', linewidth=2)
    plt.plot(x, data.loc[:, 'low'], label='最低价', linewidth=2)
    plt.plot(x, data.loc[:, 'close'], label='收盘价', linewidth=2)
    plt.xlabel('日期', FontProperties=myfont, fontsize=15)
    plt.ylabel('价格/汇率', FontProperties=myfont, fontsize=15)
    plt.title('贵州茅台股票OHLC线图', FontProperties=myfont, fontsize=15)
    plt.legend(prop=myfont)
    plt.show()
# ohlc()

#绘制K线图
def k_line():
    df = ts.get_hist_data('600519',start='2020-10-28',end='2021-04-28')
    # data = data.drop('日期',axis=1)
    data = df.reset_index('date')  # 将索引列转化为列
    data['date'] = pd.to_datetime(data['date'], infer_datetime_format=True)  # 将日期这列的数据类型转化为datatime类型
    data = data.set_index('date')
    mc = mpf.make_marketcolors(up='red',  # 价格上涨为红色
                               down='green',  # 价格下降为绿色
                               wick='black'  # 影线为黑色
                               )
    style = mpf.make_mpf_style(base_mpl_style='ggplot', marketcolors=mc)
    mpf.plot(data, type='candle', title='600519', style=style, volume=True, mav=(5, 10, 20, 30))
k_line()