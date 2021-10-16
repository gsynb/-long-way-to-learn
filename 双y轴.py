import pandas as pd
import matplotlib.pyplot as plt
import os
fig =plt.figure(figsize=(15,9))
path ='D:\\shujug\\'
A = pd.read_csv(path + 'allg.csv',header=0)
path1 = 'C:\\Users\\GaoShiyan\\Desktop\\shuju\\'
B = pd.read_csv(path1 + 'all.csv',header=0)
ax1 = fig.add_subplot(111)
ax1.plot(A['time'], A['Close'], '-', color='b', label='A close')
ax1.set_ylabel('Close')
ax1.legend(loc=2)
ax2 = ax1.twinx()
ax2.plot(B['time'], B['Close'], '-', color='orange',label='B close')
ax2.set_ylabel('Close')
ax2.set_xlabel('Same')
ax2.legend(loc=1)
plt.show()
