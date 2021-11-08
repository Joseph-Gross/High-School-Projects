#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:53:57 2020

@author: elliotgross
"""


# ===========================================================
# Imports
# ===========================================================

#TODO: Dont use pandas datareader. Find another way to import data
# Maybe try alphavantage or another yahoo finance library

import pandas as pd

import datetime as dt

import numpy as np

import calendar

import yfinance as yf

# ===========================================================
# Getting Data
# ===========================================================



def get_stock_data(ticker, years=1):
    '''
    This method returns the historical data of the given ticker, given the desired 
    historical timeframe.
    
    This method takes the amount of years given, and multiplies it by 365 days 
    to get the desired timeframe. It then inputs the ticker and timeframe to the yahoofin 
    function 'download' and retireves the historical data. After, it creates 'Day of Week',
    'Day of Month', and 'Month' columns and returns the final dataframe.

    Parameters
    ----------
    ticker : 'String'
        The string used to retrive the appropiate data.
    years : 'float', optional
        The number used to determine the timeframe of the data. The default is 1.

    Returns
    -------
    stock_df : 'pd.Dataframe'
        A pandas dataframe of the desired stock's data.

    '''
    
    num_days = round(years*365)
    year_ago = dt.datetime.today() - dt.timedelta(num_days)
    
    print("-------------------------------")
    print("Years: %s" % years)
    print("Number of Days: %s" % num_days)
    print("-------------------------------")
    
    
    stock_df = pd.DataFrame()
    
    stock_df = yf.download(ticker, year_ago).reset_index()
    
    stock_df['Day of Week'] = stock_df["Date"].dt.dayofweek
    stock_df['Day of Month'] = stock_df["Date"].dt.day
    stock_df['Month'] = stock_df["Date"].dt.month
    
    return stock_df

# ===========================================================
# Weekly
# ===========================================================


def get_weekly_options_chain_time_delta(today):
    '''
    This method takes in the day's date and returns the amount of time till the 
    next weekly options chain's expiration date.
    
    This method first converts the day inputed to the day of the week and subtracts 5 
    to get the difference between that day and friday (The day of weekly expiration date).
    If the diffrence is less than three, that means the day is a thursday-sunday, so the 
    next expiration date is that of the next week's friday, so 7 is added to the 
    difference (Variable: timedelta). Then it returns the the final diffrence, the time_delta.
    
    *Note: The minimum valid absolute timeframe is three*
    

    Parameters
    ----------
    today : 'datetime object'
        The desired day for obtaining the time delta.

    Returns
    -------
    time_delta : 'int'
        The amount of days between the inputed day and the next weekly expiration date.

    '''
    
    # Accounts for just market dayas
    
    day_of_week = today.weekday()
    # 5 = frday day of week + 1
    time_delta = 5 - day_of_week
    
    
    if time_delta < 3: # If today is Thursday through Sunday, trade for next week
        time_delta += 7
        
    return time_delta


def get_weekly_analysis(ticker, today, years=1):
    '''
    This method takes in a ticker, a day, and an amount of years, and returns an 
    analized dataframe of the stock's historical data going back the amount of years desired.
    
    This method first converts the given day to the day of the week value. If it is greater
    than 4, then that day is a weekend and is converted to monday value (which is 0). Then
    the absolute timeframe is calculated using the get_weekly_options_chain_time_delta(today)
    method and the trading timeframe is calculated using the get_trading_timeframe(today,
    absolute_timeframe) method. Then the method displays the progress so far and retrives
    the historical price data using the get_historical_price_data(ticker, trading_timeframe,
    years=years) method. Using that dataframe, the mean and standadard deviation is 
    calculated. The method then returns a filtered out dataframe, the mean, and the standard
    deviation.
    
    Parameters
    ----------
    ticker : 'String'
        The variable used to create the yf object.
    today : 'Datetime object'
        The day used to calcualte the timeframes and timedelta.
    years : 'float', optional
        The number used to determine the timeframe of the data. The default is 1.

    Returns
    -------
    'pd.Dataframe'
        The analized data of the desired ticker.
    mean : 'float'
        The average of the maximum percent change of the stock at the each timeframe.
    standard_deviation : 'float'
        the standard deviation of the maximum percent change of the stock at each timeframe.

    '''
    
    day_of_week = today.weekday()
    if day_of_week > 4:
        day_of_week = 0
    absolute_timeframe = get_weekly_options_chain_time_delta(today)
    trading_timeframe = get_trading_timeframe(today, absolute_timeframe)
    
    print("Today Date: %s, Day of Week: %s, Absolute Timeframe: %s, Trading Timeframe: %s" % (today.date(), day_of_week, absolute_timeframe, trading_timeframe))
    
    historical_price_data = get_adjusted_historical_price_data(ticker, trading_timeframe, years=years)
    mean, standard_deviation = get_mean_and_standard_deviation(historical_price_data['Max % Change'])
    
    return historical_price_data[historical_price_data["Day of Week"] == day_of_week], mean, standard_deviation


# ===========================================================
# Monthly
# ===========================================================

    
def calculate_third_friday_day_of_month(month, year):
    '''
    This method, given a month and year, calculates the date of the third friday of
    that month.
    
    This method first finds the day of the week of the first friday of the inputed month.
    It then uses that day_of_week value to find the first Friday of that month. If that
    value is less than one, than the month starts on a saturday/sunday so 7 is added. 
    After finding out the first friday of the month, 14 days (two week) is added to the 
    aformention valuein order to find the third friday of that month.
    
    Parameters
    ----------
    month : 'int'
        int from 1-12 used for determining the month.
    year : 'int'
        The year used to get the exact month.

    Returns
    -------
    third_friday_day_of_month : 'int'
        The day of the month that the third friday lands on.

    '''
    
    
    # Calculate the date of the third friday of that month
    
    first_day_of_month_day_of_week = calendar.monthrange(year, month)[0]
    
    first_friday_day_of_month = 5 - first_day_of_month_day_of_week
    
    # Handles the scenarios when the month starts on a Saturday or Sunday
    if first_friday_day_of_month < 1:
        first_friday_day_of_month += 7
        
    
    #print("Current Month: %s" % month)
    #print("First Friday Day of Month: %s" % first_friday_day_of_month)
    
    
    third_friday_day_of_month = first_friday_day_of_month + 14
    
    return third_friday_day_of_month 


def calculate_days_left_in_month(day, month, year):
    '''
    This method, given the day, month, and year, calucaltes the remaning days in the given
    month, starting form the given day, not including the given day.
    
    This method calcualtes the amount of days in the month. It then substract the day
    given from the number days in the month and add one. That aformentioned value is then
    returned.

    Parameters
    ----------
    day : 'int'
        The day of month.
    month : 'int'
        int 1-12 determining the specific month.
    year : 'int'
        Variable used to determine the specific year.

    Returns
    -------
    'int'
        The amount of days left in the month given, starting from the given day + 1.

    '''
    
    days_in_month = calendar.monthrange(year, month)[1]
    
    return days_in_month - day + 1


def get_monthly_options_chain_time_delta(today):
    '''
    This method gets the amount of days until the next monthly options chain's expiration
    date, starting from the given date, 'today'.

    This method first gets the current month and year form the given date. It then
    calculates the current day of the month. Using the current month and current year, 
    the method calculates the thrid firday of that month using the 
    calculate_third_friday_day_of_month(current_month, current_year) method. Using that value
    and the current day of the month+1, the time delta (days until the third firday of 
    the month) is calculated. If the time delta is less than three, then it is two days 
    before the expiration days and if it is less than 0, then it is after the expiration date. 
    In both cases, the days left in the month is calculated as well as the amount of 
    days untill the third friday in the next month. Those two values are added to get the 
    new timedelta. Then, for all cases, the timedelta is returned.
    
    Parameters
    ----------
    today : 'datetime object'
        The current day.

    Returns
    -------
    time_delta : 'int'
        Days until the next monthly options chain's expiration date.

    '''
    
    current_month = today.month
    current_year = today.year
    
    current_day_of_month = today.day
    third_friday_day_of_current_month = calculate_third_friday_day_of_month(current_month, current_year)
    
    #print("Third Friday of Current Month Day: %s" % third_friday_day_of_current_month)
    
    time_delta = third_friday_day_of_current_month - current_day_of_month + 1
    
    if time_delta < 3:
        days_left_in_current_month = calculate_days_left_in_month(current_day_of_month, current_month, current_year)
        next_month = (current_month+1) % 12 if (current_month+1) % 12 != 0 else 1
        third_friday_day_of_next_month = calculate_third_friday_day_of_month(next_month, current_year)
        
        time_delta = days_left_in_current_month + third_friday_day_of_next_month
        
        
        #print("Third Friday of Next Month Day: %s" % third_friday_day_of_next_month)
        #print("Days left in Current Month: %s" % days_left_in_current_month)
        #print("Timeframe: %s" % time_delta)
    
    return time_delta


def get_monthly_analysis(ticker, today, years=1):
    '''
    This method, given the ticker, date, and years, calculates the analized stock's 
    historical data, going back the amount of years desired.
    
        
    This method first converts the given day to the day of the month.  Then
    the absolute timeframe is calculated using the get_monthly_options_chain_time_delta(today)
    method and the trading timeframe is calculated using the get_trading_timeframe(today,
    absolute_timeframe) method. Then the method displays the progress so far. If the 
    trading time is less than 8, then the method reverts to the weekly analysis and 
    returns that. If it is greater than or equal to 8, the method retrives the historical 
    price data using the get_historical_price_data(ticker, trading_timeframe,years=years) 
    method. Using that dataframe, the mean and standadard deviation is 
    calculated. The method then returns a filtered out dataframe, the mean, and the standard
    deviation.
    

    Parameters
    ----------
    ticker : 'String'
        Variable used to get the desired stock data.
    today : 'datetime object'
        The day used to calcualte the timeframes and timedelta.
    years : 'float', optional
        The number used to determine the timeframe of the data. The default is 1.

    Returns
    -------
    'pd.Dataframe'
        The analized data of the desired ticker.
    mean : 'float'
        The average of the maximum percent change of the stock at the each timeframe.
    standard_deviation : 'float'
        The standard deviation of the maximum percent change of the stock at each timeframe.

    '''
    
    day_of_month = today.day
    absolute_timeframe = get_monthly_options_chain_time_delta(today)
    trading_timeframe = get_trading_timeframe(today, absolute_timeframe)
    
    print("Today Date: %s, Day of Month: %s, Absolute Timeframe: %s, Trading Timeframe: %s" % (today.date(), day_of_month, absolute_timeframe, trading_timeframe))
    
    if trading_timeframe < 8: # if the monthly falls within 7 trading days of today (i.e. thursday week before)
        print("Reverting to Weekly")
        return get_weekly_analysis(ticker, today, years=years)
    else:
        historical_price_data = get_adjusted_historical_price_data(ticker, trading_timeframe, years=years)
        mean, standard_deviation = get_mean_and_standard_deviation(historical_price_data['Max % Change'])
        
        historical_price_data["Absolute Timeframe"] = historical_price_data.apply(lambda row: get_monthly_options_chain_time_delta(row["Date"]), axis=1)
        historical_price_data["Trading Timeframe"] = historical_price_data.apply(lambda row: get_trading_timeframe(today, row["Absolute Timeframe"]), axis=1)
        
        # Monthly duplicates are dropped to prevent weekends from influencing the data (will have the same trading days but different absolute)
        return historical_price_data[historical_price_data["Trading Timeframe"] == trading_timeframe].drop_duplicates('Month'), mean, standard_deviation


# ===========================================================
# General
# ===========================================================
        
def get_trading_timeframe(today, time_delta):
    '''
    This method, given the date and the timedelta, calculates the amount of trading days
    (No weekends; Holidays are ingonred) withing the given date and the time_delta + 
    the given date.
    
    This method first calculates the end date by adding the time delta to the given date.
    It then returns the value of the numpy function, np.busday_count(start_date, end_date),
    substituting start_date with the date given and end_date with the end date calculated.

    Parameters
    ----------
    today : 'datetime object'
        The start of the timeframe.
    time_delta : 'int'
        The span of the timeframe.

    Returns
    -------
    'int'
        The amount of trading days withing the date given and the date give + the time delta.
        *Note: This method removes weekends, but does not account for holidays*

    '''
    
    # Given a start day and the number of days, get the number of
    # trading days
    
    end_date = today + dt.timedelta(time_delta)
    
    return np.busday_count(today.date(), end_date.date())


def calculate_percent_change(open_series, future_price_series):
    '''
    This method, given an open_series and a future_price series, returns the (positive) 
    percent of change from the values in the open series to the values in the future price
    series.
    
    This method calcualtes the positive difference of the open_series and the 
    future_price_series and divides it over the open_series. It then returns this value
    *100 and rounded to the hundreth decimal place. 

    Parameters
    ----------
    open_series : 'pd.Series'
        A series of all the open prices of a stock.
    future_price_series : 'pd.Series'
        A series of all the future prices of a stock.
        *Note: This is generally the max or min price of the stock within a certain timeframe*

    Returns
    -------
    'pd.Series'
        A series of the percent changes from the open_series values to the 
        future_price_series values.

    '''
    percent_change = abs(open_series - future_price_series) / open_series
    
    return round(percent_change * 100, 2)


def calculate_max_percent_change(open_series, timeframe_max_series, timeframe_min_series):
    '''
    This method, given the open_series, the timeframe_max_series, and the 
    timeframe_min_series, returns the series where each row is the maximum of the 
    two % changes that would result in profitability.
    
    This method first calculates the timeframe of the max and min percent changes using
    the calculate_percent_change(open_series, future_price_series) methods accordingly. It then assigns each new variable 
    accordingly to a new emtpy dataframe. This method then returns that new dataframe.
    

    Parameters
    ----------
    open_series : 'pd.Series'
        A series of a stock's open prices.
    timeframe_max_series : 'pd.Series'
        A series of a stock's maximum prices withing a ceratin timeframe.
    timeframe_min_series : 'pd.Series'
        A series of a stock's minimum prices within a certain timeframe.

    Returns
    -------
    'pd.Series'
        A series where each row is the maximum of the two % changes that would
        result in profitability.

    '''
    timeframe_max_percent_change = calculate_percent_change(open_series, timeframe_max_series)
    timeframe_min_percent_change = calculate_percent_change(open_series, timeframe_min_series)
    
    df = pd.DataFrame()
    
    df["Timeframe Max % Change"] = timeframe_max_percent_change
    df["Timeframe Min % Change"] = timeframe_min_percent_change 

    return df.max(axis=1)


def get_adjusted_historical_price_data(ticker, timeframe, years=1):
    '''
    This method, given a ticker, timeframe, and amount of years, returns that ticker's
    historical data, going back the amount of years desired, with additional columns
    'Timeframe Max', 'Timeframe Min', and 'Max % Change'.
    
    This method first gets the ticker's data using the get_stock_data(ticker, years=years)
    method. Using that dataframe, it adds a column 'Timeframe Max' which is the max price
    of each rolling window of the column 'High', with window sizes of timeframe. It then adds 
    the column 'Timeframe Min' which is the min price of each rolling window of the column
    'Low', with widow sizes of timeframe. It then adds the column 'Max % Change' by 
    using the calculate_max_percent_change(df["Open"], df["Timeframe Max"], 
    df["Timeframe Min"]) method. It then returns the df with all NaN values droped.

    Parameters
    ----------
    ticker : 'String'
        The desired stock's ticker.
    timeframe : 'int'
        The size of each rolling window.
    years : 'float', optional
        The number used to determine the historical timeframe of the data. The default is 1.

    Returns
    -------
    'pd.Dataframe'
        The desired stock's data with extra columns 'Timeframe Max', 'Timeframe Min', and
        'Max % Change'.

    '''
    df = get_stock_data(ticker, years=years)
    
    # The maximum stock with the timeframe (i.e. the open of the date you buy to
    # the close of the day of expiry which is the end of timeframe)
    df["Timeframe Max"] = (df['High'].rolling(timeframe, min_periods=timeframe).max()
                           .shift((timeframe-1)*-1))
    df["Timeframe Min"] = (df['Low'].rolling(timeframe, min_periods=timeframe).min()
                           .shift((timeframe-1)*-1))
    df["Max % Change"] = calculate_max_percent_change(df["Open"], df["Timeframe Max"],
                                                      df["Timeframe Min"])
    
    return df.dropna()


def get_mean_and_standard_deviation(percent_change_series):
    '''
    This method, given the percent_change_series, returns both the mean of the series
    rounded to 2 decimal places and the standard deviation of the series rounded to 2 
    decimal places.

    Parameters
    ----------
    percent_change_series : 'pd.Series'
        The series for which the developer wants the mean and standard deviation
        to be calculated for.

    Returns
    -------
    'float'
        The mean of the inputed series.
    'float'
        The standard deviation of the inputed series.

    '''
    return round(percent_change_series.mean(), 2), round(percent_change_series.std(), 2)


# ===========================================================
# Wrapper
# ===========================================================



def get_analysis(ticker, today, weekly=True):
    '''
    This method, given the ticker, the date, and the type of analysis, returns the 
    desired analized dataframe for the inputed ticker.

    Parameters
    ----------
    ticker : 'String'
        The variable representing the stock.
    today : 'datetime object'
        The current date.
    weekly : 'boolean', optional
        The type of analisys . The default is True.

    Returns
    -------
    'pd.Dataframe'
        Complete Analzized Pandas Dataframe of the inputed ticker's historical data.

    '''
    
    if weekly:
        return get_weekly_analysis(ticker, today, years=1)
    else:
        return get_monthly_analysis(ticker, today, years=1)
    




#columns_to_keep = ["Date", "Open", "Timeframe Max", "Timeframe Min", "Max % Change"]
#today = dt.datetime.today() - dt.timedelta(7)
#df, mean, standard_deviation = get_analysis('AAPL', today, weekly=False)