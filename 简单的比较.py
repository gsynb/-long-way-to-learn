import pandas as pd
import tushare as ts
import datetime
import matplotlib.pyplot as plt
import os
fig =plt.figure(figsize=(15,9))
A=pd.read_csv(r'C:\\Users\\GaoShiyan\\Desktop\\allstock\\300002.SZ.csv')

token='d5771776cad2569e0b087f46614868b53072dad53b7f2faa981cc4a4'
ts.set_token(token)
pro=ts.pro_api(token)
B = pro.daily(ts_code='300002.SZ', start_date='20091030', end_date='20200810')
A=A.values
B=B.values
for x in range(0,2500):
    a=A[x,5]
    b=B[x,5]
    if a!=b:
        print(x)
