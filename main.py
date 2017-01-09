# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 17:42:32 2017

@author: Jason
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategies.EMA_DEMA import EMA_DEMA
from portfolios.market_portfolio import MarketPortfolio

syms = ['SPY','AAPL']
signals = []
initial_capital = 100000
for sym in syms:
    ed = EMA_DEMA(sym,20,20)
    signals.append(ed.generate_signals())
port = MarketPortfolio(syms,signals,initial_capital)

#pnl = df.ret*df.pos
#nav = np.cumprod(pnl+1)
#nav.plot(rot=50)
#df[['Adj Close','DEMA30','EMA30']].iloc[-200:].plot()
#plt.show()
#
#wrong_pred = ((np.sign(df.ret)==-1) & (df.pos==1)).astype(int)
#print('Correct Direction %: ',1-wrong_pred.sum()/len(wrong_pred))
#print('Sharpe: ', np.mean(pnl)*np.sqrt(252)/np.std(pnl)) 
#
#plt.plot(nav.values)
#plt.plot(np.cumprod(df.ret+1).values)
#plt.show()