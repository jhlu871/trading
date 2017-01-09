# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 13:20:55 2017

@author: Jason
"""
import numpy as np
import pandas as pd
from backtest import Portfolio
from data import load_data
from functools import reduce

class MarketPortfolio(Portfolio):
    
    def __init__(self,symbols,signals,initial_capital=100000):
        if not type(symbols) is list:
            symbols = [symbols]
            signals = [signals]
        self.symbols = symbols
        self.data = {}
        self.signals = {}
        for i,sym in enumerate(self.symbols):
            self.data[sym] = load_data(sym)
            self.signals[sym] = signals[i]
        self.initial_capital = initial_capital
        self.positions,self.trades = self.generate_positions_and_trades()
        
    def generate_positions_and_trades(self):  
        positions = pd.concat([x.pos for x in self.signals.values()],
                                    axis=1)
        positions.columns = self.symbols
        positions = positions.fillna(method='ffill').fillna(0)
        trades = pd.concat([x[['trades','price']] for x in self.signals.values()],
                            axis=1,keys=self.symbols)
        return positions,trades
        
    def backtest_portfolio(self):
        portfolio = self.data.pos*self.data.price
        trades = self.trades.swaplevel(axis=1)
        cash = (trades.trades*trades.price).cumsum()
        close = pd.concat([x['])
        holdings = self.positions * 
        
        