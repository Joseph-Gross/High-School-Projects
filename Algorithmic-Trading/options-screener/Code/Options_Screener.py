#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:32:04 2020

@author: elliotgross
"""

# ===========================================================
# Imports
# ===========================================================


import pandas as pd
import numpy as np

import datetime as dt
from yahoo_fin import stock_info as si

import yfinance as yf

# ===========================================================
# Getting nearest expiration date to datetime (after datetime)
# ===========================================================


def get_nearest_expiration_date(ticker_str, today, absolute_timeframe):
    
    
    
    ticker = yf.Ticker(ticker_str)
    
    expiration_dates = [dt.datetime.strptime(date, '%Y-%m-%d') for date in ticker.options]
    timeframe_end_date = today + dt.timedelta(absolute_timeframe)
    print('\n', "-----------------------------------", '\n')
    print("Timeframe End Date: %s" % timeframe_end_date.date())
    print('\n', "-----------------------------------", '\n')
    
    expiration_dates_timedeltas = [abs((timeframe_end_date - expiration_date).days) for expiration_date in expiration_dates]
    min_timedelta_index = expiration_dates_timedeltas.index(min(expiration_dates_timedeltas))
   
    print("Expiration Dates: ", '\n')     
    for expiration_date in expiration_dates:
        print(str(expiration_date.date()), "Timedelta: %s" % abs((timeframe_end_date - expiration_date).days))
        
        
    return expiration_dates[min_timedelta_index].strftime("%Y-%m-%d")


# ===========================================================
# Getting options chain from Yahoo Finance and cleaning them
# ===========================================================


def get_options_chain_dfs_yahoo(ticker_str, expiration_date, stock_price, atm_percent_threshold=10):
    '''
    Uses the expiration date to get all the calls and puts that expire that day

    Parameters
    ----------
    ticker : 'String'
        Used to get the dfs.
    expiration_date : 'String'
        Used to find which calls/puts to get.

    Returns
    -------
    calls_df : 'pd.Dataframe'
    puts_df : 'pd.Dataframe'

    '''
    
    ticker = yf.Ticker(ticker_str)
    options_chain = ticker.option_chain(expiration_date)
    
    
    
    calls_df = options_chain.calls
    calls_atm_multiplier = 1 + atm_percent_threshold/100 # Number to multiply stock price by to get ATM
    calls_df["Type"] = np.where(calls_df["inTheMoney"], "ITM", np.where(calls_df['strike']<stock_price*calls_atm_multiplier, 
                                'ATM', 'OTM'))
    calls_df["Call Exp. Date"] = expiration_date
    
    puts_df = options_chain.puts
    puts_atm_multiplier = 1 - atm_percent_threshold/100 # Number to multiply stock price by to get ATM
    puts_df["Type"] = np.where(puts_df["inTheMoney"], "ITM", np.where(puts_df['strike']>stock_price*puts_atm_multiplier, 
                                'ATM', 'OTM'))
    puts_df["Put Exp. Date"] = expiration_date
    
    return calls_df, puts_df


def get_clean_call_df(calls_df, percent_threshold, stock_price):
    '''
    Filters, Cleans, and adds a breakeven column to the df

    Parameters
    ----------
    calls_df : 'pd.Dataframe'
        Is being cleand.
    percent_threshold : 'float'
        Used to filter df.
    stock_price : 'float'
        Used to filter df.

    Returns
    -------
    filtered_df : 'pd.Dataframe'

    '''
    
    
    cols_to_keep = ['contractSymbol', 'strike', 'ask', 'bid', 'Call Exp. Date', 'Type']
    calls_df = calls_df[cols_to_keep]
    
    new_col_names_base = ['Contract Name','Strike','Ask','Bid', 'Exp. Date', 'Type']
    new_col_names = ['Call %s'%col for col in new_col_names_base]
    calls_df.columns = new_col_names
    
    
    
    max_premium = percent_threshold * stock_price / 100
    filtered_df = calls_df[(calls_df['Call Ask'] < max_premium) &
                         (calls_df['Call Type']=='ATM')]

    print("# Calls: %s" % (filtered_df.shape[0]))
    
    return filtered_df.reset_index(drop=True)


def get_clean_put_df(puts_df, percent_threshold, stock_price):
    '''
    Filters, Cleans, and adds a breakeven column to the df

    Parameters
    ----------
    puts_df : 'pd.Dataframe'
        Is being cleand.
    percent_threshold : 'float'
        Used to filter df.
    stock_price : 'float'
        Used to filter df.

    Returns
    -------
    filtered_df : 'pd.Dataframe'

    '''
    
    cols_to_keep = ['contractSymbol', 'strike', 'ask', 'bid', 'Put Exp. Date', 'Type']
    puts_df = puts_df[cols_to_keep]
    
    new_col_names_base = ['Contract Name','Strike','Ask','Bid', 'Exp. Date', 'Type']
    new_col_names = ['Put %s'%col for col in new_col_names_base]
    puts_df.columns = new_col_names
    
    
    max_premium = percent_threshold * stock_price / 100
    filtered_df = puts_df[(puts_df['Put Ask'] < max_premium) &
                         (puts_df['Put Type']=='ATM')]

    print("# Puts: %s" % (filtered_df.shape[0]))
    
    return filtered_df.reset_index(drop=True)


def get_cleaned_options_chain_dfs(ticker_str, expiration_date, percent_threshold, stock_price, 
                                  atm_percent_threshold=10):
    '''
    
    Ties in the previous methods to return two cleaned-up dataframes, puts_df and calls_df.

    Parameters
    ----------
    ticker : 'String'
        Used to find the Data from Yahoo.
    expiration_date : 'String'
        USed to find the Data from Yahoo.
    percent_threshold : 'float'
        Used to clean dfs.
    stock_price : 'float'
        Used to clean dfs.

    Returns
    -------
    calls_df : 'pd.Dataframe'
    puts_df : 'pd.Dataframe'

    '''
    
    print('\n', "------------OBTAINING OPTIONS CHAIN------------", '\n')
    calls_df, puts_df = get_options_chain_dfs_yahoo(ticker_str, expiration_date, stock_price, 
                                                    atm_percent_threshold=atm_percent_threshold)
    calls_df = get_clean_call_df(calls_df, percent_threshold, stock_price)
    puts_df = get_clean_put_df(puts_df, percent_threshold, stock_price)

    return calls_df, puts_df

# ===========================================================
# Creating all possible spreads and filtering them 
# ===========================================================
    

def create_spreads_series(call_series, put_series, percent_threshold, stock_price):
    '''
    Takes in two series (call and put) and creates a new series to be
    used as a row in the spreads df.
    
    The output will contain the following fields: call/put contract name, 
    call/put bid, call/put ask, call/put strike, call/put breakeven price, 
    net premium, max %, min %, bid_ask_range.
    
    If the net-premium is greater than the percent*stock_price, then return 
    NaN. If not, then return the full spread series.

    Parameters
    ----------
    call_series : 'pd.Series'
        Used for data.
    put_series : 'pd.Series'
        Used for Data
    stock_price : 'float'
        Used for new features
    percent_threshold : 'float'
        Used for filtering

    Returns
    -------
    row : 'pd.Series'
        Series object that contains the spreads info.

    '''
    
    if call_series['Call Ask'] + put_series['Put Ask'] < stock_price*percent_threshold:
        
        row = pd.concat([call_series, put_series])
        row['Bid-Ask Range'] = '%s - %s' % (round(call_series['Call Bid']+put_series['Put Bid'], 2),
                                            round(call_series['Call Ask']+put_series['Put Ask'], 2))
        row['Net Premium'] = call_series['Call Ask'] + put_series['Put Ask']
        row["Breakeven Max"] = call_series['Call Strike'] + row['Net Premium']
        row["Breakeven Min"] = put_series['Put Strike'] - row['Net Premium']
        
        breakeven_percents_list = [round(abs(stock_price - row["Breakeven Max"]) / stock_price * 100, 2),
                                   round(abs(stock_price - row["Breakeven Min"]) / stock_price * 100, 2)]
        
        row["Breakeven Max %"] = max(breakeven_percents_list)
        row["Breakeven Min %"] = min(breakeven_percents_list)
        
        return row
    
    else:
        return np.nan


def create_spreads_df(calls_df, puts_df, percent_threshold, stock_price):
    '''
    This creates a spread of all possible combinations of put and call and then filters it.
    It itterates through all combinations and checks for the conditionals

    Parameters
    ----------
    call_df : 'pd.Dataframe'
        Information Used
    put_df : 'pd.Dataframe'
        Information Used.
    stock_price : 'float'
        Used for filtering
    percent_threshold : 'float'
        Used for Filtering

    Returns
    -------
    spread_df : 'pd.Dataframe'

    '''
    all_spreads_list = []
    
    for i, calls_row in calls_df.iterrows():
        for j, puts_row in puts_df.iterrows():
            spread = create_spreads_series(calls_row, puts_row, 
                                           percent_threshold, stock_price)
    
            if spread["Breakeven Max %"] < percent_threshold:
                all_spreads_list.append(spread)
            
            
    all_spreads_df = pd.DataFrame(all_spreads_list).reset_index(drop=True)
            
    return all_spreads_df.sort_values("Breakeven Max %").reset_index(drop=True)
    
    
# ===========================================================
# Main Method
# ===========================================================
        

def get_screened_spreads(ticker_str, today, absolute_timeframe, percent_threshold, atm_percent_threshold=10):
    
    timeframe_description = "Weekly" if absolute_timeframe < 10 else "Monthly"
    stock_price = round(si.get_live_price(ticker_str), 2)


    expiration_date = get_nearest_expiration_date(ticker_str, today, absolute_timeframe)
    print('\n', "-----------------------------------", '\n')
    print("Today: %s, Timeframe: %s, Nearest Expiration Date: %s" % (today.date(), absolute_timeframe, expiration_date))
    print('\n', "-----------------------------------", '\n')
    
    calls_df, puts_df = get_cleaned_options_chain_dfs(ticker_str, expiration_date, percent_threshold, 
                                                      stock_price, atm_percent_threshold=atm_percent_threshold)


    print("%s Price: %s" % (ticker_str, stock_price))
    print("Expiration Date: %s" % expiration_date)
    
    
    print('\n', "------------SCREENING FOR SPREADS------------", '\n')
    print("Criteria to Meet:")
    print("Description: %s" % timeframe_description)
    print("Absolute Timeframe: %s" % absolute_timeframe)
    print("Percent Threshold: %s" % percent_threshold)
    print('\n', "-----------------------------------", '\n')
    
    
    try:
        final_spread = create_spreads_df(calls_df, puts_df, percent_threshold, stock_price)
        print('\n', '********** SPREADS FOUND **********', '\n')
        return final_spread
    except:
        print('\n', '********** NO VALUES MATCHED CRITERIA **********', '\n')
        return None
    