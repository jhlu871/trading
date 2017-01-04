# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 17:35:54 2017

@author: Jason
"""

import numpy as np
import pandas as pd

def get_returns(df):
    df['ret'] = df['Adj Close'].pct_change()
    return df
    
