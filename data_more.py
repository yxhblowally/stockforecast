import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
warnings.filterwarnings('ignore')   #过滤警告

# 获取数据
def getdata():
    data = pd.read_excel('D:/Stock forecasts/stockdata.xls',
                         sheet_name=1)   #读取工作簿的第二个工作表
    data = data.sort_values(by='日期')  # 按日期这一列进行排序
    # data.to_csv('data.csv', encoding='utf-8')
    data = data.set_index('日期')
    data_two = data.drop(['涨跌额','涨跌幅(%)','振幅(%)','换手率(%)'],axis=1)
    data_two = data_two.applymap(lambda x:x.replace(',','')).astype(float)   #去掉数字千分位的逗号,且将字符串转化为浮点型
    data_two.to_csv('data_all.csv')   #将数据存为csv格式
    return data_two
getdata()

# 数据归一化
def normalization():
    data = pd.read_csv('data_all.csv')
    columns = [x for x in data.columns if x not in ['成交金额(万元)','日期']]   #去掉成交金额这一列
    max_min_scaler = lambda x : (x-np.min(x)) / (np.max(x)-np.min(x))
    for title in columns:
        data[title] = data[[title]].apply(max_min_scaler)
    data.to_csv('datanorm.csv',index=None)
normalization()

# 从文件中导入数据
origdf = pd.read_csv('datanorm.csv')
df = origdf[['收盘价', '最高价', '最低价', '开盘价', '成交量(手)']]
featureData = df[['收盘价', '最高价', '最低价', '成交量(手)']]
# 划分特征值和目标值
feature = featureData.values
# print(feature)
target = np.array(df['开盘价'])
# 划分训练集，测试集
feature_train, feature_test, target_train, target_test = train_test_split(feature, target, test_size=0.25,shuffle=False)
x_f = feature_train
m,n = np.shape(x_f)
# print(x_f)
y_f = target_train.reshape(43,1)
# print(y_f)
x_t = feature_test
# print(x_t)
y_t = target_test.reshape(15,1)
# print(y_t)

# 激活函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 激活函数的导数
def dsigmoid(x):
    return np.exp(-x) / (1 + np.exp(-x)) ** 2

epoch = 20000  # 训练次数
HNum = 3  # 隐藏层节点数
HCNum = 1  # 隐藏层层数
# emax = 0.01  # 最大允许的均方差根
alpha = 0.00001  # 学习率
# theta = np.ones((4,27))
SNum = len(x_f)  # 样本数
INum = len(x_f[0])  # 输入层节点数（每组数据的维度）
ONum = len(y_f[0])  # 输出层节点数（结果的维度）
# studytime = 0  # 学习次数
lost = 0.0  # 均方差根
Teacher = np.zeros(ONum)
Ii = np.zeros(INum)  # 样本数(4,)
Hi = np.zeros((HCNum, HNum))  # 隐藏层的输入(1*3)
Ho = np.zeros((HCNum, HNum))  # 隐藏层的输出(1*3)
Oi = np.zeros(ONum)  # 输出层的输入(1,)
Oo = np.zeros(ONum)  # 输出层的输出(1,)
w = 0.2 * np.ones((INum, HNum))  # 初始化第一层权值矩阵(4*3)
v = 0.2 * np.ones((HNum, ONum))  # 初始化第二层权值矩阵(3*1)
Hb = np.zeros((HCNum, HNum))  # 初始化第一层偏执矩阵(1*3)
Ob = np.zeros(ONum)  # 初始化第二层偏置矩阵(1,)

# BP模型
def BP(x,y):
    global Hi, Oi, Oo, Ho, Ii, Teacher, lost, w, v, Hb, Ob, He, Oe,dOb,dHb
    lost = 0.0
    v_gra_increas = np.zeros((3,1))
    Ob_gra_increas = np.zeros((1,1))
    w_gra_increas = np.zeros((4,3))
    Hb_gra_increas = np.zeros((3,3))
    for ismap in range(0, SNum, 1):
        Ii = x_f[ismap]  # 训练集的输入
        Teacher = y_f[ismap]  # 训练集的输出

        ##########     前向传播     ##########

        Hi = Ii.dot(w)  # 1*3
        Ho = sigmoid(Hi + Hb)  # 1*3
        Oi = Ho.dot(v)  # 1*1
        Oo = sigmoid(Oi + Ob)  # 1*1
        # print(Oo)

        ############     反向传播     ##########

        #####   损失函数   #####
        error = np.subtract(Teacher, Oo)  # 每一层期望输出与实际输出的差值
        lost = np.sum(error ** 2) / len(Teacher)  # 均方差损失函数
        # print(lost)

        Oe = error * dsigmoid(Oi + Ob)   #输出层反向输出的值
        dOb = Oe
        # print(dOb)
        # print(Oe)   #1*1

        #####   反向更新v   #####
        dv = Oi.T.dot(Oe)  # 计算隐藏层与输出层神经元的梯度项
        # print(dv)
        v_gra_increas += dv
        # print(v_gra_increas)
        dv = np.average(v_gra_increas)
        # print(dv)
        v = np.subtract(v, dv * alpha)  # 更新 v
        # print(v)   #3*1

        #####   反向更新w   #####
        He = v.dot(Oe)
        He = dsigmoid(Hi + Hb) * He # 隐藏层反向输出的值
        dHb = He
        # print(dHb)
        dw = (Hi.T).dot(He)  # 计算隐藏层神经元的梯度项
        w_gra_increas += dw
        # print(w_gra_increas)
        dw = np.average(w_gra_increas)
        # print(dw)
        w = np.subtract(w, dw * alpha)
        # print(w)

        #####   反向更新b   #####
        Ob_gra_increas += dOb
        # print(Ob_gra_increas)
        dOb = np.average(Ob_gra_increas)
        # print(dOb)
        Ob = np.subtract(Ob, dOb * alpha)
        # print(Ob)

        Hb_gra_increas += dHb
        # print(Hb_gra_increas)
        dHb = np.average(Hb_gra_increas)
        # print(dHb)
        Hb = Hb - dHb * alpha
        # print(Hb)
# BP(x_f,y_f)

def predict(x):
    x_result = np.zeros((x.shape[0], 1))
    for isamp in range(0, x.shape[0], 1):
        Hi = x[isamp].dot(w)
        Ho = sigmoid(np.add(Hi, Hb))

        ########   计算输出层输入输出 Oi Oo    ########
        Oi = np.dot(Ho, v)
        Oo = sigmoid(np.add(Oi, Ob))
        x_result[isamp] = Oo
    return x_result

# for i in range(1, epoch, 1):
#     if i % 1000 == 0:
#         # print(lost)
#         print('已训练 %d 千次 ,误差均方差 %f' % ((i / 1000), lost))
#     BP(x_f,y_f)
# print('训练完成，共训练 %d 次，误差均方差 %f' % (i, lost))

result = predict(x_t)

# print('模型预测结果 : ')
# for i in result:
#     print('%f' % i)
#
# print('\n实际结果 : ')
# for i in y_t:
#     print(i)
















