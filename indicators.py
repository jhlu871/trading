# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:06:42 2017

@author: Jason
"""

import numpy as np
import pandas as pd
import talib as ta

def column_name(name,*args):
    """ Helper to print out correct column names. Attaches each param
    to the end of the name with a preceding underscore"""
    for arg in args:
        name += '_' + str(arg)
    return name
    
def add_overlap_indicator(df,name,period=20,nbdev=2,matype=0,vfactor=0.7,
                acc=.02,sar_max=.2):
    """ Adds output of selected overlap indicator from talib as a
        column to the input pandas DataFrame 
        
    Parameters
    ----------
    df: pandas DataFrame 
        Data that includes at least a timestamp, Adj Close, High, and Low
        
    name: string
        Name of the talib indicator (Ex. DEMA)
        
    period: int (Optional)
        Number of periods for overlap window (Default: 20)
        
    nbdev: int (Optional)
        Number of standard deviations away for upper and lower Bollinger
        Bands (Default: 2).
        
    matype: int or talib.MA_TYPE (Optional)
        Moving average type to use (Default: 0).
        
    vfactor: float (Optional)
        Weighting ratio for T3. T3 = GD 3 times. A GD with vfactor of 1
        is the same as the DEMA. A GD with a vfactor of zero is the same 
        as an Exponential Moving Average (Default: .7).
        
    acc: float (Optional)
        acceleration factor (AF) for SAR (Default: .02).
        
    sar_max: float (Optional)
        max value for accuulated AF for SAR (Default: .2).
        
    Returns
    -------
    df: pandas DataFrame with indicator results added as columns.
    
    """     
    # indicators that only require price and period
    period_only = ['DEMA','EMA','KAMA','MIDPOINT','SMA','T3','TEMA',
                   'TRIMA','WMA']
    # indicators that use high and low instead of adj close
    high_lo = ['MIDPRICE','SAR','SAREXT']
    
    if name in high_lo:
        high = df['High'].values
        low =  df['Low'].values
    else:
        close = df['Adj Close'].values
    f = getattr(ta,name)
    if name in period_only:
        df[column_name(name,period)] = f(close,period)
    elif name == 'HT_TRENDLINE':
        df[name] = f(close)
    elif name == 'BBANDS':
        up,mid,low = f(close,period,nbdev,nbdev,matype)
        df[column_name(name,period,nbdev,matype,'up')] = up
        df[column_name(name,period,nbdev,matype,'mid')] = mid
        df[column_name(name,period,nbdev,matype,'low')] = low
    elif name == 'T3':
        df[column_name(name,period,vfactor)] = f(close,period,vfactor)
    elif name == 'MIDPRICE':
        df[column_name(name,period)] = f(high,low,period)
    elif name == 'SAR': # stop loss and reversal point calculation
        df[column_name(name,acc,sar_max)] = f(high,low,acc,sar_max)
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df
    
def add_momentum_indicator(df,name,period=20,fastperiod=12,slowperiod=26,
                 signalperiod=9,matype=0,fastk_period=5,slowk_period=3,
                 slowk_matype=0,fastd_period=3,slowd_period=3,
                 slowd_matype=0,fastd_matype=0,period2=14,period3=28):
    high = df['High'].values
    low = df['Low'].values
    close = df['Adj Close'].values
    
    # indicators that use high, low, close, and period
    hlcp = ['ADX','ADXR','CCI','DX','MINUS_DI','PLUS_DI','WILLR']
    # indicators that use high, low, and period
    hlp = ['AROONOSC','MINUS_DM','PLUS_DM']
    # indicators that use close and period
    cp = ['CMO','MACDFIX','MOM','ROC','ROCP','ROCR100','RSI','TRIX']
    
    f = getattr(ta,name)
    if name in hlcp:
        df[column_name(name,period)] =f(high,low,close,period)
    elif name in hlp:
        df[column_name(name,period)] = f(high,low,period)
    elif name in cp:
        df[column_name(name,period)] = f(close,period)
    elif name in ['APO','PPO']:
        df[column_name(name,fastperiod,slowperiod,matype)] = \
           f(close,fastperiod,slowperiod,matype)
    elif name == 'AROON':
        down, up = f(high,low,period)
        df[column_name(name,period,'down')] = down
        df[column_name(name,period,'up')] = up
    elif name == 'BOP':
        op = df['Open'].values
        df[name] = f(op,high,low,close)
    elif name == 'MACD':
        df[column_name(name,fastperiod,slowperiod,signalperiod)] = \
           f(close,fastperiod,slowperiod,signalperiod)
    elif name == 'MFI':
        volume = df['Volume'].values
        df[column_name(name,period)] = f(high, low, close, volume,period)
    elif name == 'STOCH':
        k,d = f(high,low,close,fastk_period,slowk_period,slowk_matype,
                slowd_period,slowd_matype)
        df[column_name(name,fastk_period,slowk_period,slowk_matype,
                slowd_period,slowd_matype,'k')] = k
        df[column_name(name,fastk_period,slowk_period,slowk_matype,
                slowd_period,slowd_matype,'d')] = d
    elif name == 'STOCHF':
        k,d = f(high,low,close,fastk_period,fastd_period,fastd_matype)
        df[column_name(name,fastk_period,
                       fastd_period,fastd_matype,'k')] = k
        df[column_name(name,fastk_period,
                       fastd_period,fastd_matype,'d')] = d
    elif name =='STOCHRSI':
        k,d = f(close,period,fastk_period,fastd_period,fastd_matype)
        df[column_name(name,period,
                       fastk_period,fastd_period,fastd_matype,'k')] = k
        df[column_name(name,period,
                       fastk_period,fastd_period,fastd_matype,'d')] = d
    elif name == 'ULTOSC':
        df[column_name(period,period2,period3)] = \
           f(high,low,close,period,period2,period3)
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df
    
def add_volume_indicator(df,name,fastperiod=3,slowperiod=10):
    high = df['High'].values
    low = df['Low'].values
    close = df['Adj Close'].values
    volume = df['Volume'].values
    
    f = getattr(ta,name)
    if name == 'AD':
        df[name] = f(high,low,close,volume)
    elif name == 'ADOSC':
        df[column_name(name,fastperiod,slowperiod)] = \
           f(high,low,close,volume,fastperiod,slowperiod)
    elif name == 'OBV':
        df[name] = f(close,volume) 
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df
    
def add_cycle_indicator(df,name):
    close = df['Adj Close'].values
    f = getattr(ta,name)
    if name == 'HF_PHASOR':
        inphase,quadrature = f(close)
        df[column_name(name,'inphase')] = inphase
        df[column_name(name,'quadrature')] = quadrature
    elif name == 'HF_SINE':
        sine,leadsine = f(close)
        df[column_name(name,'sine')] = sine
        df[column_name(name,'leadsine')] = leadsine
    elif name in ['HT_DCEPERIOD','HT_DCPHASE','HT_TRENDMODE']:
        df[name] = f(close)
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df
        
def add_price_transform(df,name):
    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values
    
    f = getattr(ta,name)
    if name =='AVGPRICE': # (open+high+low+close)/4
        op = df['Open'].values
        df[name] = f(op,high,low,close)
    elif name == 'MEDPRICE': # (high + low)/2
        df[name] = f(high,low)
    elif name in ['TYPPRICE','WCLPRICE']:
        # Typical Price (high + low + close)/3
        # Weighted close price (high+low+2*close)/4
        df[name] = f(high, low, close)
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df
    
def add_volatility_indicator(df,name,period=20):
    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values
    
    f = getattr(ta,name)
    if name == 'TRANGE':
        df[name] = f(high,low,close)
    elif name in ['ATR','NATR']:
        df[column_name(name,period)] = f(high,low,close,period)
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df
    
def add_pattern_indicator(df,name,penetration=0):
    op = df['Open'].values
    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values
    
    ohlc = ['2CROWS','3BLACKCROWS','3INSIDE','3LINESTRIKE','3OUTSIDE',
            '3STARSINSOUTH','3WHITESOLDIERS','ADVANCEBLOCK','BELTHOLD',
            'CLOSINGMARUBOZU','CONCEALBABYSWALL','COUNTERATTACK','DOJI',
            'DOJISTAR','DRAGONFLYDOJI','ENGULFING','GAPSIDESIDEWHITE',
            'GRAVESTONEDOJI','HAMMER','HANGINGMAN','HARAMI','HARAMICROSS',
            'HIGHWAVE','HIKKAKE','HIKKAKEMOD','HOMINGPIGEON',
            'IDENTICAL3CROWS','INNECK','INVERTEDHAMMER','KICKING',
            'KICKINGBYLENGTH','LADDERBOTTOM','LONGLEGGEDDOJI','LONGLINE',
            'MARUBOZU','MATCHINGLOW','ONNECK','PIERCING','RICKSHAWMAN',
            'RISEFALL3METHODS','SEPARATINGLINES','SHOOTINGSTAR','SHORTLINE',
            'SPINNINGTOP','STALLEDPATTERN','STICKSANDWICH','TAKURI',
            'TASUKIGAP','THRUSTING','TRISTAR','UNIQUE3RIVER',
            'UPSIDEGAP2CROWS','XSIDEGAP3METHODS']
    
    # requires penetration paramater
    penetration = ['ABANDONEDBABY','DARKCLOUDCOVER','EVENINGDOJISTAR',
                   'EVENINGSTAR','MATHOLD','MORNINGDOJISTAR','MORNINGSTAR']
    
    f = getattr(ta,name)
    if name in ohlc:
        df[name] = f(op,high,low,close)
    elif name in penetration:
        df[column_name(name,penetration)] = f(op,high,low,close,penetration)
    else:
        raise AttributeError('Indicator not found: %s' % name)
    return df

def add_indicators(df,**kwargs):
    """ Adds all the specified indicators to the input DataFrame.
    
    Parameters
    ----------
    df: pandas DataFrame
        Input DataFrame of basica data
        
    **kwargs: Variable numbe keyword={params} pairs
        Each keyword is the name of an indicator, and the dict params is a 
        named keyword value dictionary of the parameters used for the 
        indicator
    
    Returns
    -------
    df: pandas DataFrame
        Returns the input dataframe with the indicator results attached
        as columns
    
    Example usage: add_indicators(df,EMA={'period':30},DEMA={'period':20})
    
    """
    function_groups = ta.get_function_groups()
    for k,arg in kwargs.items():
        group = None
        for g,funcs in function_groups.items():
            if k in funcs:
                group = g.split()[0]
                break
        if group:
            if group == 'Price':
                f_name = 'add_price_transform'
            else:
                f_name = 'add_' + group.lower() + '_indicator'
            f = globals()[f_name]
            df = f(df,k,**arg)
        else:
            raise AttributeError('Indicator not found: %s' % k)
    return df
        
        
#def add_all_technicals(df):
#    prices = df['Adj Close'].values
#    
#    # EMA 50, 100, 200  period
#    df['EMA30'] = ta.EMA(prices,20)
#    
#    # DEMA double exponential moving average
#    # more responsive to shorter flucutations
#    # (2*EMA) - EMA(EMA)
#    df['DEMA30'] = ta.DEMA(prices,20)
#    
#    
#    
#    return df