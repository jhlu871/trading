# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:26:05 2017

@author: Jason
"""

from abc import ABCMeta, abstractmethod

class Strategy():
    """ Strategy is an abstract base class providing an interface
    for all subsequent (inherited) trading strategies.
    
    The goal of a (derived) Strategy object is to output a list of 
    signals, which has the ofrm of a time series index pandas DataFrame
    
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generate_signals(self):
        """ An implementation is required to return the Dataframe of symbols
        to go long, short or hold (1,-1, or 0)."""
        raise NotImplementedError("Should implement generate_signals()!")
    

        
class Portfolio():
    """ An abstract base class representing a portfolio of positions
    (including both instruments and cash), determined on the basis of
    a set of signals provided by a Strategy. """

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_positions(self):
        """Provides the logic to determine how the portfolio positions 
        are allocated ont he basis of forecasting signals and available
        cash"""
        raise NotImplementedError("Should implement generate_positions()!")
        
    @abstractmethod
    def backtest_portfolio(self):
        """Provides the logic to generate the trading orders and 
        subsequent equity curve (i.e. growth of total equity),
        as a sum of holdings and cash, and the returns associated with 
        this curve based on teh 'positiions' DataFrame.
        
        Produces a portfolio object that can be examined by other
        classes/functions."""
        raise NotImplementedError('Should implement backtest_portfolio()!')
        
        
                