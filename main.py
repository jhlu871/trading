# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 17:42:32 2017

@author: Jason
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import load_data
from preprocess import add_returns
from indicators import add_all_technicals

syms = ['SPY']
for s in syms:
    df = load_data(s)
    df = add_returns(df)
    df = add_all_technicals(df).dropna()
df['pos'] = ((df['Adj Close'] < df['EMA30']) & (df['Adj Close'] < df['DEMA30'])).astype(int).shift()
df = df.dropna()
    
pnl = df.ret*df.pos
nav = np.cumprod(pnl+1)
nav.plot(rot=50)
df[['Adj Close','DEMA30','EMA30']].iloc[-200:].plot()
plt.show()

wrong_pred = ((np.sign(df.ret)==-1) & (df.pos==1)).astype(int)
print('Correct Direction %: ',1-wrong_pred.sum()/len(wrong_pred))
print('Sharpe: ', np.mean(pnl)*np.sqrt(252)/np.std(pnl)) 

plt.plot(nav.values)
plt.plot(np.cumprod(df.ret+1).values)
plt.show()