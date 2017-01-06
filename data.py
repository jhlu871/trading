# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:35:07 2017

@author: Jason
"""

import pandas as pd
from pandas_datareader import data as web
import datetime
import os

def update_data(sym,source,path='data'):
    file = os.path.join(path,('%s.csv' % sym))
    try:
        df1 = pd.read_csv(file)
        start = datetime.datetime.strptime(df1.iloc[-1].Date,'%Y-%m-%d') + \
                datetime.timedelta(days=1)
        print('Previous data found. Appending all new data')
    except FileNotFoundError:
        print('File does not exist, gathering all data and creating new file')  
        df1 = pd.DataFrame()
        start = datetime.datetime(1900,1,30)
    end = None
    
    if start.date() != datetime.datetime.now().date():
        df = web.DataReader(sym,source,start,end).round(2)
        if not df.empty:
            if df1.empty:
                df.to_csv(file)
            else:
                df.to_csv(file,mode='a',header=None)
        print('%s updated' % sym)
    else:
        print('%s already up to date. Skipping' % sym)
    
def load_data(sym,path='data'):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),path)
    df = pd.read_csv(os.path.join(path,'%s.csv' 
                                    % sym.upper())).set_index('Date')  
    df['Volume'] = df['Volume'].astype(float)
    return df

if __name__=='__main__':
    syms = ['VXX','SPY','USO','IEF']
    src = 'yahoo'
    for sym in syms:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data')
        update_data(sym,src,path)
        
