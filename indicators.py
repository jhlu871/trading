# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:06:42 2017

@author: Jason
"""

import numpy as np
import pandas as pd
import talib as ta

def add_all_technicals(df):
    prices = df['Adj Close'].values
    
    # EMA 50, 100, 200  period
    df['EMA30'] = ta.EMA(prices,20)
    
    # DEMA double exponential moving average
    # more responsive to shorter flucutations
    # (2*EMA) - EMA(EMA)
    df['DEMA30'] = ta.DEMA(prices,20)
    
    
    
    return df