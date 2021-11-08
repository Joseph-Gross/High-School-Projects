#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:40:02 2020

@author: josephgross
"""


from abc import ABCMeta, abstractmethod

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


class Option(object):
    """
    Abstract Class for an Option Object
    """
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self, underlying_symbol, underlying_price, info_series, is_long):
        """
        Initializes the Call instance.

        Parameters
        ----------
        underlying_symbol : 'str'
            The ticker for the underlying asset.
        underlying_price : 'float'
            The price of the underlying asset.
        info_series : 'pd.Series'
            A pandas Series containing information about the Call (strike,
            bid, ask, impliedVolatility, volume, expirationDate, contractSize)
        is_long : 'Boolean'
            A boolean whether the Call is long or short.

        Returns
        -------
        None.

        """
        
        self.underlying_asset_price = underlying_price
        self.underlying_asset_symbol = underlying_symbol
        
        self.strike_price = info_series["strike"]
        self.bid = info_series["bid"]
        self.ask = info_series["ask"]
        self.implied_volatility = info_series["impliedVolatility"]
        self.volume = info_series["volume"]
        self.expiration_date = pd.to_datetime(info_series["expirationDate"])
        
        self.is_long = is_long
        self.direction = 1 if self.is_long else -1
        
        self.premium = self.ask * self.direction
        self.description = self.calculate_description()
        self.intrinsic_value = self.calculate_intrinsic_value()
        self.time_value = self.calculate_time_value()
        self.capital_committed = self.calculate_capital_committed()
        
        self.current_date = dt.datetime.today()
        self.time_to_expiry = (self.expiration_date - self.current_date).days
        self.breakeven_price = self.calculate_breakeven_price()
        
        
    
    @abstractmethod
    def calculate_description(self):
        """
        Calculates the description of an ooption bject (ITM, ATM, OTM)

        """
        
        raise NotImplementedError("Should implement calculate_description()")
        
        
    @abstractmethod
    def calculate_intrinsic_value(self):
        """
        Calculates the intrinsic value of an Option Object.

        """
        
        raise NotImplementedError("Should implement calculate_intrinsic_value()")
        
    
    @abstractmethod 
    def calculate_breakeven_price(self):
        """
        Calculates the breakeven price point of an option object.

        """
        
        raise NotImplementedError("Should implement calculate_breakeven_point()")
        
        
    @abstractmethod
    def get_return(self, new_price):
        """
        Returns the return of an option object when the underlying
        asset reaches a new price of new_price.
    
        """
        
        raise NotImplementedError("Should implement get_return()")
        
        
    def get_contract_name(self):
        """
        Generates and returns the call contract name
         
        Returns
        -------
        'str'
            The official call contract name.

        """
        
        symbol = self.underlying_asset_symbol 
        expiration_date = self.expiration_date.strftime("%y%m%d")
        call_or_put = self.type[0]
        strike_price = "{:.2f}".format(round(self.strike_price, 2)).replace(".", "").zfill(7)
        
        return symbol + expiration_date + call_or_put + strike_price
        
        
    
    def calculate_capital_committed(self):
        """
        Calculates the capital committed to this scenario. If
        the call is long then the capital committed is the premium
        times 100. If its short, then no capital is committed.

        Returns
        -------
        'float'
            The capital committed for this scenario.

        """
        
        
        return self.premium * 100
        
        
    def calculate_time_value(self):
        """
        Calculates the time value of this contract.

        Returns
        -------
        'float'
            Time value of this call.

        """
        
        return abs(self.premium) - self.intrinsic_value
        
    
    def get_return_arrays(self, price_range):
        """
        Calculates and returns two arrays: the returns array and 
        the prices array. The prices array is an array of prices 
        from the lower end of the price range to the upper end, 
        incrementing by 0.01. The returns array is an array of the 
        return of this call for each price in the prices array.

        Parameters
        ----------
        price_range : 'tuple'
            A tuple with a start and end for a price range.

        Returns
        -------
        prices : 'np.array'
            An array of prices from the lower end of the price 
            range to the upper end, incrementing by 0.01.
        returns : 'np.array'
            An array of the return of this call for each price in 
            the prices array.

        """
        
        start = price_range[0]
        end = price_range[1]
        sampling_rate = int((end - start)/0.01)
        
        prices = pd.Series(np.linspace(start, end, num=sampling_rate))
        returns = prices.apply(lambda x: self.get_return(x))
        
        #print("Start Price: %s" % str(start))
        #print("End Price: %s" % str(end))
        
        return prices, returns
        
    
    def visualize_profit_graph_new_price(self):
        """
        
        Visualizes the return of this call contract on a graph.
        The y axis is the return and the x axis is the new price 
        of the underlying asset. The prices range from a 20% change
        in the underlying asset price in either direction.

        Returns
        -------
        None.

        """
        
        start = round(self.underlying_asset_price*0.8, 2)
        end = round(self.underlying_asset_price*1.2, 2)
        price_range = (start,end)
        
        prices, returns = self.get_return_arrays(price_range)
        
        title = "{}: {}".format(self.get_contract_name(), self.underlying_asset_symbol)
        xlabel = "New Price ($)"
        ylabel = "Return ($)"
        label1 = "Strike Price: {}".format(self.strike_price)
        label2 = "Breakeven Price: {}".format(self.breakeven_price)
        label3 = "Current Price: {}".format(self.underlying_asset_price)
        
        plt.figure()
        plt.title(title)
        
        
        plt.plot(prices, returns)
        plt.axvline(x=self.strike_price, color='k', linestyle='-', label=label1)
        plt.axvline(x=self.breakeven_price, color='b', linestyle='--', label=label2)
        plt.axvline(x=self.underlying_asset_price, color='r', linestyle='-', label=label3)
        plt.hlines(y=0, xmin=start, xmax=end)
        
        
        plt.fill_between(prices, returns, where=np.array(returns)>0, color='g')
        plt.fill_between(prices, returns, where=np.array(returns)<0, color='r')
        
        plt.legend()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation='45') # rotating tick marks
        plt.show()
        
        
    def visualize_profit_graph_price_change(self):
        """
        Visualizes the return of this call contract. There are two
        plots, one for percent change, and one for absolute change.
        The y-axis for both is the returns and the x-axis is the 
        either the percent change in price or the absolute change.
        The price changes range from a 20% change in either direction.

        Returns
        -------
        None.

        """
     
     
        start = round(self.underlying_asset_price*0.8, 2)
        end = round(self.underlying_asset_price*1.2, 2)
        price_range = (start,end)
        
        prices, returns = self.get_return_arrays(price_range)
        
        
        # Percent Price Change
        prices_1 = (prices - self.underlying_asset_price)/self.underlying_asset_price * 100
        strike_price_change_1 = round((self.strike_price - self.underlying_asset_price)/
                                   self.underlying_asset_price*100, 2)
        breakeven_price_change_1 = round((self.breakeven_price - self.underlying_asset_price)/
                                   self.underlying_asset_price*100, 2)
            
        title_1 = "{}: {} {} Change".format(self.get_contract_name(), self.underlying_asset_symbol, "$")
        xlabel_1 = "Price Change (%)"
            
        strike_label_1 = "Strike Price Change: {}{}".format(strike_price_change_1, "%")
        breakeven_label_1 = "Breakeven Price Change: {}{}".format(breakeven_price_change_1, "%")
          
        
        # Absolute Price Change
        prices_2 = prices - self.underlying_asset_price
            
        strike_price_change_2 = round(self.strike_price - self.underlying_asset_price, 2)
        breakeven_price_change_2 = round(self.breakeven_price - self.underlying_asset_price, 2)
            
        title_2 = "{}: {} {} Change".format(self.get_contract_name(), self.underlying_asset_symbol, "$")
        xlabel_2 = "Price Change ($)"
            
        strike_label_2 = "Strike Price Change: {}{}".format("$", strike_price_change_2)
        breakeven_label_2 = "Breakeven Price Change: {}{}".format("$", breakeven_price_change_2)
        
    
    
        # Plotting
        ylabel = "Return ($)"
        
        fig, (ax1, ax2) = plt.subplots(2, figsize=(6,6))

        
        ax1.plot(prices_1, returns)
        ax1.axvline(x=strike_price_change_1, color='k', linestyle='-', label=strike_label_1)
        ax1.axvline(x=breakeven_price_change_1, color='b', linestyle='--', label=breakeven_label_1)
        ax1.hlines(y=0, xmin=prices_1[0], xmax=prices_1[len(prices_1)-1])
        
        ax1.fill_between(prices_1, returns, where=np.array(returns)>0, color='g')
        ax1.fill_between(prices_1, returns, where=np.array(returns)<0, color='r')
        
        ax1.set_title(title_1)
        ax1.set(xlabel=xlabel_1, ylabel=ylabel)
        ax1.legend()
        
        
        ax2.plot(prices_2, returns)
        ax2.axvline(x=strike_price_change_2, color='k', linestyle='-', label=strike_label_2)
        ax2.axvline(x=breakeven_price_change_2, color='b', linestyle='--', label=breakeven_label_2)
        ax2.hlines(y=0, xmin=prices_2[0], xmax=prices_2[len(prices_2)-1])
        
        ax2.fill_between(prices_2, returns, where=np.array(returns)>0, color='g')
        ax2.fill_between(prices_2, returns, where=np.array(returns)<0, color='r')
        
        ax2.set_title(title_2)
        ax2.set(xlabel=xlabel_2, ylabel=ylabel)
        ax2.legend()

        fig.tight_layout(pad=2)
        plt.show()
        

    def output_summary_stats(self):
        """
        This method outputs the stats of this call contract. This is mainly
        used for debugging and making sure every method is working the way
        it should be.

        Returns
        -------
        None.

        """
        
        print("Contract Name: %s" %str(self.get_contract_name()))
        print("Type: %s" % str(self.type))
        print("Underlying Asset Symbol: %s" % str(self.underlying_asset_symbol))
        print("Underlying Asset Current Price: %s" % str(self.underlying_asset_price))
        print("Strike Price: %s" % str(self.strike_price))
        print("Direction: %s" % str(self.direction))
        
        print("Bid: %s" % str(self.bid))
        print("Ask: %s" % str(self.ask))
        print("Premium: %s" % str(self.premium))
        
        print("Description: %s" % str(self.description))
        print("Implied Volatility: %s" % str(self.implied_volatility))
        print("Volume: %s" % str(self.volume))
        
        print("Intrinsic Value: %s" % str(self.intrinsic_value))
        print("Time Value: %s" % str(self.time_value))
        print("Capital Committed: %s" % str(self.capital_committed))
        print("Breakeven Price: %s" % str(self.breakeven_price))
        
        #print("Contract Size: %s" % self.contract_size)
        print("Expiration Date: %s" % self.expiration_date.strftime("%Y/%m/%d"))
        print("Current Date: %s" % self.current_date.strftime("%Y/%m/%d"))
        print("Time to Expiration: %s" % str(self.time_to_expiry))
        
        
        