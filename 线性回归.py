import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 计算均方误差函数
def get_mse(records_real, records_predict):
    if len(records_real) == len(records_predict):
        return sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real)
    else:
        return None

# poly是多元回归分析器
def POLY(a,b,c,d):
    x_train=a
    x_test=c
    y_train=b
    y_test=d
    degree = 1
    poly = PolynomialFeatures(degree)
    x_train_poly = poly.fit_transform(x_train)
    x_test_poly = poly.fit_transform(x_test)
    lg = LinearRegression()
    lg.fit(x_train_poly, y_train)
    poly.predicted = lg.predict(x_test_poly)
    p_pre = poly.predicted
    mse = get_mse(p_pre, y_test)
    return (mse, p_pre)

def main():
    plt.figure(figsize=(15,9))
    path = 'C:\\Users\\GaoShiyan\\Desktop\\shuju\\'
    B = pd.read_csv(path + 'all.csv', header=0)

    now_data = B.iloc[:, [0]]  # 选属性（time open high low）
    tag=B.iloc[:, 4]
    # 取前n行数据进行训练
    train=now_data[0:200000]
    test=tag[0:200000]

    # 取n-∞的数据进行预测
    needpredict=now_data[200000:]
    realvalue=tag[200000:]

    X=needpredict['time']
    X=X.tolist()
    (mse, pre)=POLY(train,test,needpredict,realvalue)
    realvalue=realvalue.tolist()
    plt.plot(X, realvalue, label='真实价格', color='red', linewidth=0.7)
    plt.plot(X, pre, label='预测价格', color='blue', linewidth=0.7)
    plt.legend()
    plt.show()

main()



