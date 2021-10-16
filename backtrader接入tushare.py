import backtrader as bt
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
from datetime import datetime, date

class my_strategy1(bt.Strategy):
    def log(self, txt, dt=None, doprint=False):
        ''' 日志函数，用于统一输出日志格式 '''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        # 初始化相关数据
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 五日移动平均线
        self.sma5 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=5)
        # 十日移动平均线
        self.sma10 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=10)

    def notify_order(self, order):
        """
        订单状态处理

        Arguments:
            order {object} -- 订单状态
        """
        if order.status in [order.Submitted, order.Accepted]:
            # 如订单已被处理，则不用做任何事情
            return

        # 检查订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        # 订单因为缺少资金之类的原因被拒绝执行
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # 订单状态处理完成，设为空
        self.order = None

    def notify_trade(self, trade):
        """
        交易成果

        Arguments:
            trade {object} -- 交易状态
        """
        if not trade.isclosed:
            return

        # 显示交易的毛利率和净利润
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), doprint=True)

    def next(self):
        ''' 下一次执行 '''

        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])

        # 是否正在下单，如果是的话不能提交第二次订单
        if self.order:
            return

        # 是否已经买入
        if not self.position:
            # 还没买，如果 MA5 > MA10 说明涨势，买入
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy()
        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()

    def stop(self):
        self.log(u'(金叉死叉有用吗) Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=True)



import tushare as ts
def get_data(code,start='2010-01-01',end='2020-03-31'):
    df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    df.index=pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    return df
# 加载数据
dataframe=get_data('600000')
start=datetime(2010, 1, 1)
end=datetime(2020, 3, 31)
data = bt.feeds.PandasData(dataname=dataframe,fromdate=start,todate=end)
# 初始化cerebro回测系统设置
cerebro = bt.Cerebro()
#将数据传入回测系统
cerebro.adddata(data)
# 将交易策略加载到回测系统中
cerebro.addstrategy(my_strategy1)
cerebro.addsizer(bt.sizers.FixedSize, stake=100)
# 设置初始资本为10,000
startcash = 10000
cerebro.broker.setcash(startcash)
# 设置交易手续费为 0.2%
cerebro.broker.setcommission(commission=0.002)
d1=start.strftime('%Y%m%d')
d2=end.strftime('%Y%m%d')
print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')
#运行回测系统
cerebro.run()
#获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
#打印结果
print(f'总资金: {round(portvalue,2)}')
cerebro.plot(style='candlestick')
print(f'净收益: {round(pnl,2)}')