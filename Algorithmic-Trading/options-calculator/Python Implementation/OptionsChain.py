#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:52:19 2020

@author: josephgross
"""


import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
    
from CallObject import Call
from PutObject import Put

class OptionsChain():
    """
    This class contains the options chain info for a specific
    underlying asset (only 1) and a specific date.
    
    The main properties are the two dataframes: call_chain and 
    put_chain. This method will also calculate a bunch of values.
    The rows of these dataframes can be used to instantiate call
    and put objects.
    
    This class will also allow you to filter through the chain and 
    obtain call or put objects without actually altering any of this
    class's properties.
    """
    
    def __init__(self, underlying_symbol, underlying_price):
        """
        
        Initializes thes OptionsChain Instance

        Parameters
        ----------
        underlying_symbol : 'str'
            The underlying asset symbol (i.e. AAPL, AMZN, etc.).
        underlying_price : 'float'
            The underlying asset price.

        Returns
        -------
        None.

        """
        
        self.underlying_asset_symbol = underlying_symbol
        self.underlying_asset_price = underlying_price
        
        
        # self.options_chain_dict = s elf._get_options_chain_csv(dt.date.today())
        self.options_chain_dict = self._get_options_chain_yahoo()
        
        self.call_chain = self.options_chain_dict["Calls"]
        self.put_chain = self.options_chain_dict["Puts"]
        
        self.date_created = dt.datetime.today()
        
      
        self.calculate_all_values()
        print(self.put_chain.dtypes)
        
        
        
    def _get_options_chain_csv(self, date):
        """
        Reads a csv from the csv directory csv_dir and pulls
        the options data from that specific date.
        
        IMPROVEMENTS: Add an extra parameters to be a list of
        stock symbols to pull data from.

        Parameters
        ----------
        date : 'str'
            The date to pull data from 'YYYY-MM-DD'.

        Returns
        -------
        options_data : 'dictionary'
            Dictionary of dataframes containing the call and put data.

        """
        
        csv_dir = "csv_dir/"
    
        file_path_calls = csv_dir + "calls/%s.csv" % str(date) 
        file_path_puts = csv_dir + "puts/%s.csv" % str(date) 
    
        options_data = {}
        options_data["Calls"] = pd.read_csv(file_path_calls)
        options_data["Puts"] = pd.read_csv(file_path_puts)
        
        return options_data
    
    
    
    def _get_options_chain_yahoo(self):
        """
        Obtains the live options data from yahoo finance. This
        method takes around 8 seconds to complete (4 for calls
        and 4 for puts). 
        
        IMPROVEMENTS: Add an extra parameters to be a list of
        stock symbols to pull data from. Must find a way to improve
        speed if this is implemented.

        Returns
        -------
        options_chain_dict : 'dict'
            Dictionary of dataframes containing the call and put data.

        """
        
        ticker = yf.Ticker(self.underlying_asset_symbol)
        expDates = ticker.options
        calls_list = []
        puts_list = []

        columns_to_keep = ['strike','bid','ask','volume', 'impliedVolatility'] # contractSize removed
    
        for i,date in enumerate(expDates):
            try:
                opts = ticker.option_chain(date)
                
                calls_df = opts.calls[columns_to_keep]
                puts_df = opts.puts[columns_to_keep]
    
                #calls_df = calls
                calls_list.append(calls_df)
                puts_list.append(puts_df)
            
            except:
                continue
    
        all_calls_df= (pd.concat(calls_list, keys=expDates, names=['expirationDate'])
                  .fillna(0).reset_index().drop("level_1", axis=1))
        all_puts_df = (pd.concat(puts_list, keys=expDates, names=['expirationDate'])
                  .fillna(0).reset_index().drop("level_1", axis=1))
        
        
        options_chain_dict = {}
        options_chain_dict["Calls"] = all_calls_df
        options_chain_dict["Puts"] = all_puts_df
        
        for key in options_chain_dict.keys():
        
            condition_1 = (options_chain_dict[key]["volume"] > 10)
            condition_2 = (options_chain_dict[key]["ask"] > 1)
            condition_3 = (options_chain_dict[key]["bid"] > 1)
            
            options_chain_dict[key] = options_chain_dict[key][condition_1 & condition_2 & condition_3]
            
        return options_chain_dict
    
    
    
    
    
    def calculate_bid_ask_spreads(self):
        """
        Calculates the bid/ask spread for each option.

        Returns
        -------
        None.

        """
        
        self.call_chain["Bid Ask Spread"] =  self.call_chain["ask"] - self.call_chain["bid"]
        self.put_chain["Bid Ask Spread"] = self.put_chain["ask"] - self.put_chain["bid"]
        
        
        
    def calculate_descriptions(self):
        """
        Calculates the descriptions of each option (OTM, ITM, ATM).
        Currently, the threshold for ATM is a strike price within one
        percent of the current price.

        Returns
        -------
        None.

        """
        
        self.call_chain["Underlying Price"] = self.underlying_asset_price
        self.put_chain["Underlying Price"] = self.underlying_asset_price
        
        # Call Chain
        
        delta_price = self.call_chain["Underlying Price"] - self.call_chain["strike"]
        delta_price_percentage = abs(delta_price) / self.call_chain["Underlying Price"] *100 
        self.call_chain["Description"] = np.where(delta_price_percentage < 3,
                                                  "ATM",
                                                  np.where(delta_price<0 , #if strike > underlying, OTM
                                                           "OTM", "ITM")
                                                  )
        
        # Put Chain
        
        delta_price = self.put_chain["Underlying Price"] - self.put_chain["strike"]
        delta_price_percentage = abs(delta_price) / self.put_chain["Underlying Price"] * 100 
        self.put_chain["Description"] = np.where(delta_price_percentage < 3,
                                                  "ATM",
                                                  np.where(delta_price>0, #if strike < underlying, OTM
                                                           "OTM", "ITM")
                                                  )
        
        
        
    def calculate_premiums(self):
        """
        Calculates the premiums of each option. Currently this
        sets the premium equal to the ask price but can be modified
        to split the difference between ask and bid.

        Returns
        -------
        None.

        """
        
        # Call Chain
        self.call_chain["Premium"] = self.call_chain["ask"]
        
        # Put Chain
        self.put_chain["Premium"] = self.put_chain["ask"]
        
        
        
    def calculate_intrinstic_values(self):
        """
        Calculates the intrinsic value of each option.

        Returns
        -------
        None.

        """
        
        # Call Chain
        delta_price = self.call_chain["Underlying Price"] - self.call_chain["strike"]
        self.call_chain["Intrinsic Value"] = np.where(delta_price>0, # Underlying > Strike
                                                      delta_price,
                                                      0)
        
        # Put Chain
        delta_price = self.put_chain["strike"] - self.put_chain["Underlying Price"]
        self.put_chain["Intrinsic Value"] = np.where(delta_price>0, # Strike > Underlying
                                                      delta_price,
                                                      0)
        
        

    def calculate_time_values(self):
        """
        Calculates the time value of each option.

        Returns
        -------
        None.

        """
        
        # Call Chain
        self.call_chain["Time Value"] = self.call_chain["Premium"] - self.call_chain["Intrinsic Value"]
        
        # Put Chain
        self.put_chain["Time Value"] = self.put_chain["Premium"] - self.put_chain["Intrinsic Value"]
        
        
        
    def calculate_time_to_expiry(self):
        """
        Calculates the time in days until the option contract expires.

        Returns
        -------
        None.

        """
        
        # Call Chain
        
        self.call_chain["Expiration Date"] = pd.to_datetime(self.call_chain["expirationDate"])
        self.call_chain["Time Interval (days)"] = self.call_chain.apply(lambda row: 
                                                                            (row["Expiration Date"] - 
                                                                             self.date_created).days, 
                                                                            axis=1)
            
        # Put Chain
            
        self.put_chain["Expiration Date"] = pd.to_datetime(self.put_chain["expirationDate"])
        self.put_chain["Time Interval (days)"] = self.put_chain.apply(lambda row: 
                                                                        (row["Expiration Date"] - 
                                                                         self.date_created).days, 
                                                                        axis=1)
    

        
    def save_to_csv(self):
        """
        Saves the entire options chain (both call and put) to CSVs.
        This method creates two CSVs which are mostly used for testing
        and quicker loading times.

        Returns
        -------
        None.

        """
        
        self.call_chain.to_csv("Test CSVs/Call Test.csv")
        self.put_chain.to_csv("Test CSVs/Put Test.csv")
        
            
        
        
    def calculate_all_values(self):
        """
        Calculates all the the above "calculate..." values. This is
        a helper method that encapsulates those method calls so that
        the overall code is easier to read and cleaner.

        Returns
        -------
        None.

        """
        
        #self.calculate_bid_ask_spreads()
        self.calculate_descriptions()
        self.calculate_premiums()
        self.calculate_intrinstic_values()
        self.calculate_time_values()
        self.calculate_time_to_expiry()
        
        
    def get_closest_time_to_expiration(self, time_to_expiration):
        unique_timeframes_list = list(set(self.call_chain["Time Interval (days)"].tolist()))
        
        absolute_difference_function = lambda list_value : abs(list_value - time_to_expiration)

        return min(unique_timeframes_list, key=absolute_difference_function)
    
    def get_closest_strike_price(self, target_price):
        unique_strikes_list = list(set(self.call_chain["strike"].tolist()))
        
        absolute_difference_function = lambda list_value : abs(list_value - target_price)

        return min(unique_strikes_list, key=absolute_difference_function)
        
        
    def get_filtered_df(self, df, key, value):
        
        if type(value) == bool:
            df = df[df[key] == value]
        
        if type(value) == tuple:
                
            if value[0] == "==":
                df = df[df[key] == value[1]]
                            
            elif value[0] == ">=":
                df = df[df[key] >= value[1]]
                            
            elif value[0] == ">":
                df = df[df[key] > value[1]]
                            
            elif value[0] == "<=":
                df = df[df[key] <= value[1]]
                            
            elif value[0] == "<":
                df = df[df[key] < value[1]]
                            
            elif value[0] == "!=":
                df = df[df[key] != value[1]]
                            
            elif value[0] == 'c':
                df = df[df[key].str.lower().str.contains(value[1].lower())]
                            
            elif value[0] == '!c':
                df = df[~df[key].str.lower().str.contains(value[1].lower())]
                
            elif value[0] == 'in':
                df = df[df[key].str.lower().isin(value[1].replace(" ", "").lower().split(','))]
                            
        return df
    
        
    def get_filtered_options_df(self, params_dict, option_type):
        """
        This method takes in a bunch of parameters and returns
        a dictionary of dataframes: one for puts and one for calls. Each 
        dataframe will be filtered based on the input parameters.
        requirements.

        Parameters
        ----------
        parameters_dict : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        df = pd.concat(self.options_chain_dict.copy()).droplevel(-1)
        df.index.name = "type"
        df.reset_index(inplace=True)
        
        
        for key in params_dict.keys():
            value = params_dict[key]
            
            #print(key, value)
            
            if key not in df.columns:
                continue
            
            if type(value) != list:
                df = self.get_filtered_df(df, key, value)
                        
            else:
                for value in params_dict[key]:
                    df = self.get_filtered_df(df, key, value)
        
        
        df = df[df["type"].str.lower().str.contains(option_type.lower())]
        
        return df
   
    
    def get_filtered_options_list(self, params_dict, option_type, is_long):
        """
        This method takes in a bunch of parameters and returns
        two lists: one for puts and one for calls. Each list will
        be a list of Option Object instances that meet the filter
        requirements.
        
        AVAILABLE PARAMETERS:
            Keys: Any column Name
            Values: 'tuple', '==', '!=', 'c', '!c', 'boolean'
                Tuple: (constraint, value)
                    constraints: '==', '!=', '>=', '>', '<=', '<', 'c', '!c', 'in'
                    values: 'int', 'float', 'str', 'datetime'

        Parameters
        ----------
        parameters_dict : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        filtered_options_df = self.get_filtered_options_df(params_dict, option_type)
        
        # Create an empty list 
        options_list =[] 
          
        # Iterate over each row 
        for index, row in filtered_options_df.iterrows(): 
            
            # Create list for the current row 
            info_series = row[['strike', 'bid', 'ask', 'impliedVolatility', 'volume', 'expirationDate']]
              
            if 'call' in option_type.lower():
                option = Call(self.underlying_asset_symbol, self.underlying_asset_price, info_series, is_long)
            else:
                option = Put(self.underlying_asset_symbol, self.underlying_asset_price, info_series, is_long)
            
            # append the list to the final list 
            options_list.append(option) 
        
        
        return options_list
