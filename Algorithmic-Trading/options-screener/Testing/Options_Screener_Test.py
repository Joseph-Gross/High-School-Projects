#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 11:40:38 2020

@author: josephgross
"""

import Options_Screener
import datetime as dt


if __name__ == "__main__":
    
    ticker_str = "AMZN"
    
    today = dt.datetime.today() + dt.timedelta(4)
    absolute_timeframe = 30
    
    
    percent_threshold = 15
    atm_percent_threshold = 3
    
    screened_spreads = Options_Screener.get_screened_spreads(ticker_str, today, absolute_timeframe, 
                                                             percent_threshold, atm_percent_threshold=atm_percent_threshold)
    