# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 16:20:28 2017

@author: Jason
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:51:02 2017

@author: Jason
"""

import numpy as np
import pandas as pd
from backtest import Strategy, Portfolio
from preprocess import add_returns
from indicators import add_all_technicals
from data import load_data

class EMA_DEMA(Strategy):
    """ Derives from Strategy to produce a set of signals that 
    are randomly generated long/shorts. Toy example.
    
    Parameters:
    -----------
    ticker: string
        Ticker of the instrument
        
    data: pandas DataFrame
        Data pertaining to the instrument. Should include at least
        timestamp and price. Can also include open, high, low, volume
        
    Attributes
    -----------
    signals: pandas dataframe
        trading signals with timestamps
    """
    
    def __init__(self,symbol):
        """ Initialize the ticker and get pandas DataFrame of data """
        self.symbol = symbol
        self.data = load_data(symbol)
        
    def generate_signals(self):
        """ Creates a pandas DataFrame of trading signals."""
        df = add_returns(self.data)
        df = add_all_technicals(df)
        df['pos'] = ((df['Adj Close'] < df['EMA30']) & 
                    (df['Adj Close'] < df['DEMA30'])).astype(int).shift()
        self.signals = df.pos.dropna().diff()
        self.signals[0] = 0
        return self.signals