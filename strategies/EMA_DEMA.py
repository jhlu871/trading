# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:51:02 2017

@author: Jason
"""

import numpy as np
import pandas as pd
from backtest import Strategy
from indicators import add_indicators, column_name
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
    
    def __init__(self,symbol,EMA_period=20,DEMA_period=20,trade_time='Close'):
        """ Initialize the ticker and get pandas DataFrame of data """
        self.symbol = symbol
        self.data = add_indicators(load_data(symbol),
                                   EMA={'period':EMA_period},
                                   DEMA={'period':DEMA_period})
        self.EMA_period = EMA_period
        self.DEMA_period = DEMA_period
        self.trade_time = trade_time

        
    def generate_signals(self):
        """ Create a pandas DataFrame of trading signals."""
        EMA_name = column_name('EMA',self.EMA_period)
        DEMA_name = column_name('DEMA',self.DEMA_period)
        self.data['pos'] = ((self.data['Adj Close'] < self.data[EMA_name]) & 
                    (self.data['Adj Close'] < self.data[DEMA_name])).astype(int).shift()
        if self.trade_time == 'Close':
            self.data['trades'] = self.data.pos.diff().shift(-1)
        elif self.trade_time == 'Open':
            self.data['trades'] = self.data.pos.diff()   
        self.signals = self.data[['pos','trades']].dropna()
        self.signals['price'] = self.data[self.trade_time]
        return self.signals