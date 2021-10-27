import time
import tushare as ts
import datetime
import matplotlib.pyplot as plt
import os
import datacompy, pandas as pd, sys
from pandas import Series, DataFrame
token='d5771776cad2569e0b087f46614868b53072dad53b7f2faa981cc4a4'
ts.set_token(token)
pro=ts.pro_api(token)
df1=pd.DataFrame(pd.read_csv('C:\\Users\\GaoShiyan\\Desktop\\重要资料\\study\\000002.XSHE_1d_.csv'))
t_list=[]
for i in df1['time']:
	i=str(i)
	t1=time.strptime(i,"%Y/%m/%d")
	t2=time.strftime("%Y-%m-%d",t1)
	t_list.append(t2)
df1['time']=t_list
df1 = df1[['time', 'open', 'high', 'low', 'close']]
#将csv时间的格式改为了Y-m-d
df2 = ts.get_k_data('000002', autype='qfq', start='2005-01-04', end='2021-09-30')
df2 = df2[['date', 'open', 'high', 'low', 'close']]
df2.columns = Series(['time', 'open', 'high', 'low', 'close'])
df1.index = pd.to_datetime(df1.time)
df2.index = pd.to_datetime(df2.time)
df1[['time']].apply(tuple, axis=1)
df2[['time']].apply(tuple, axis=1).to_list()
slice_lable = (
    df1[['time']].apply(tuple, axis=1)
    .isin(df2[['time']].apply(tuple, axis=1)
          .to_list()
         )
)

slice_lable
df2 = df2.round({'open': 2, 'high': 2, 'low': 2, 'close': 2})
df3 = df1.drop(labels=df2.axes[0])
df4 = df1.drop(labels=df3.axes[0])
df2.index=[i for i in range(df4.shape[0])]
df4.index=[i for i in range(df4.shape[0])]
compare = datacompy.Compare(df2, df4, join_columns='time')
print(compare.matches()) # 最后判断是否相等，返回 bool
print(compare.report()) # 打印报告详情，返回 string



