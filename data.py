# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:35:07 2017

@author: Jason
"""

import pandas as pd
from pandas_datareader import data as web
from preprocess import add_returns
import datetime
import os
import csv


def update_data(sym,source,path='data'):
    file = os.path.join(path,('%s.csv' % sym.upper()))
    start = datetime.datetime(1900,1,30)
    end = None

    df = web.DataReader(sym,source,start,end)
    df.ix[:,df.columns!='Adj Close'] = df.ix[:,df.columns!='Adj Close'].round(2)
    df['Adj Close'] = df['Adj Close'].round(6)
    if not df.empty:
        df.to_csv(file)
        print('%s updated' % sym)
    else:
        print('Error: no data for %s' % sym)
    return df
    
    
def load_data(sym,path='data'):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),path)
    try:
        df = pd.read_csv(os.path.join(path,'%s.csv' 
                                    % sym.upper())).set_index('Date')  
    except FileNotFoundError: 
        print('Could not locate data for %s. Attempting to download.' %sym)
        src = 'yahoo'
        df = update_data(sym,src,path)
        syms = get_symbol_list()
        syms.append(sym)
        syms = pd.Series(syms)
        syms.to_csv('symbols.csv',index=False,header=None)
        
    df['Volume'] = df['Volume'].astype(float)
    df = add_returns(df)
    return df
    
def get_symbol_list():
    with open('symbols.csv','r') as f:
        reader = csv.reader(f)
        syms = [sym[0] for sym in reader]
    return syms

if __name__=='__main__':
    syms = get_symbol_list()
    src = 'yahoo'
    for sym in syms:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data')
        update_data(sym,src,path)
        
