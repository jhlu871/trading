# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 21:01:53 2017

@author: Jason
"""

import numpy as np
import pandas as pd


def calc_pnl(df,bidask):
    pnl = df.ret*df.pos
    nav = np.cumprod(pnl+1)