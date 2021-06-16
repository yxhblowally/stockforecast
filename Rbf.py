import numpy as np
import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf
import warnings
warnings.filterwarnings('ignore')
tf.disable_v2_behavior()

date_axis = np.linspace(0, 30, 31)   #在0-30范围内返回均匀的间隔
close_price = np.array(
    [1997.0, 2059.45, 2100, 2140, 2090, 2099.73, 2160.9, 2164, 2134, 2082, 2063, 2009.41, 2040.63, 2070,2079.95, 2175,
     2141.89, 2089, 2088, 2116.18, 2109.32, 2145, 2189.91, 2320.85, 2313, 2368.8, 2456.43, 2601, 2471, 2460])
open_price = np.array(
    [1999.98, 1990, 2064.8, 2097, 2142, 2090, 2088, 2164, 2115, 2061.06, 2073.11, 2008, 2048, 2069, 2083, 2185, 2141.89, 2080,
     2101.19, 2130, 2112.22, 2150, 2191, 2325, 2337, 2368.8, 2485, 2587.98, 2451.16, 2455])


# def draw_figure():
#     plt.figure()
#     for i in range(30):
#         date = np.zeros([2])
#         date[0] = i + 1
#         date[1] = i + 1
#         gain = np.zeros([2])
#         gain[0] = open_price[i]
#         gain[1] = close_price[i]
#         plt.plot(date,gain,'g',linewidth = 2)
#         if open_price[i] < close_price[i]:
#             plt.plot(date, gain, 'r', lw=8)
#         else:
#             plt.plot(date, gain, 'g', lw=8)

datenormal = np.zeros([30, 1])
pricenormal = np.zeros([30, 1])
max_price = max(close_price)
min_price = min(close_price)

for i in range(30):  # 归一化处理
    datenormal[i] = (i + 1 - 1) / (30 - 1)
    pricenormal[i] = (close_price[i] - min_price) / (max_price - min_price)

x = tf.placeholder(tf.float32, shape=[None, 1])   #形式参数，用于定义过程，在执行时再赋具体的值
y = tf.placeholder(tf.float32, shape=[None, 1])

w = tf.Variable(tf.random_uniform([20, 1], seed=1))  # 隐层至输出层权重，隐含层的节点为20
b = tf.Variable(tf.constant(0.1))  # 输出层偏置

c = tf.Variable(tf.random_normal([20, 1], seed=1))  # 中心点
delta = tf.Variable(tf.random_normal([1, 20], seed=1))
dist = tf.reduce_sum(tf.square(tf.subtract(tf.tile(x, [20, 1]), c)), 1)  # 欧氏距离（维度：1*20）
delta_2 = tf.square(delta)

rbf_out = tf.exp(tf.multiply(-1.0, tf.divide(dist, tf.multiply(2.0, delta_2))))  # 通过径向基函数（高斯）算得隐层输出

y_pred = tf.nn.relu(tf.matmul(rbf_out, w) + b)  # 预测输出

mse = tf.reduce_mean(tf.square(y - y_pred))  # 损失函数为均方误差

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(mse)   #设置学习率为0.01，且处理了梯度计算和参数更新两个操作

#使用Session来激活整个流程
with tf.Session() as sess:
    tf.global_variables_initializer().run()   #初始化
    pred = np.zeros([30, 1])
    for step in range(1000):
        for i in range(len(datenormal)):
            sess.run(train_step, feed_dict={x: np.mat(datenormal)[i], y: np.mat(pricenormal)[i]})
        if step % 100 == 0:
            for j in range(len(datenormal)):
                loss = sess.run(mse, feed_dict={x: np.mat(datenormal)[j], y: np.mat(pricenormal)[j]})
                y_ = sess.run(y_pred, feed_dict={x: np.mat(datenormal)[j]})
                pred[j, 0] = (y_ * (max_price - min_price) + min_price)[0]
            # draw_figure()
            plt.plot(date_axis[1:], open_price, 'r', linewidth=2)
            plt.plot(date_axis[1:], pred.tolist(), 'b', linewidth=2,ls='--')
            plt.grid()
            plt.show()
            print("After %d training steps,mse on all data is %g" % (step, loss))
