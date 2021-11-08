#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:28:05 2020

@author: josephgross
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


class OptionStrategy(object):
    """
    Class for an Option Strategy
    """
    
    
    def __init__(self, strategy_name, direction, underlying_symbol, underlying_price, option_legs):
        """
        The initializer for the Option Strategy Class.

        Parameters
        ----------
        strategy_name : 'str'
            This is the name of the strategy. This can be a preset strategy
            or a custom strategy.
        direction : 'str'
            A description of this strategy. This will encapsulate whether
            this strategy is bullish, bearish, or neutral.
        underlying_symbol : 'str'
            The ticker of the underlying asset.
        underlying_price : 'str'
            The current price of the underlying asset.
        option_legs : 'list'
            A list of option object that are often referred to as legs.

        Returns
        -------
        None.

        """
        
        self.strategy_name = strategy_name
        self.direction = direction
        
        self.underlying_asset_price = underlying_price
        self.underlying_asset_symbol = underlying_symbol
        
        self.legs = option_legs
        self.long_legs = [option for option in self.legs if option.is_long]
        self.short_legs = [option for option in self.legs if not option.is_long]
        self.num_legs = len(self.legs)
        self.strike_prices = sorted([option.strike_price for option in self.legs])
        
        self.current_date = dt.datetime.today()
        self.calculate_values()
        
        
        
    def calculate_values(self):
        """
        A wrapper method for all the different calculate values mehtods.

        Returns
        -------
        None.

        """
        
        self.net_premium = self.calculate_net_premium()
        self.capital_committed = self.calculate_capital_committed()
        
        self.max_profit = self.calculate_max_profit()
        self.max_loss = self.calculate_max_loss()
        
        self.breakeven_prices = self.calculate_breakeven_prices()
        self.max_profit_prices = self.calculate_max_profit_prices()
        self.max_loss_prices = self.calculate_max_loss_prices()
        
        self.timeframe = self.calculate_timeframe()
        
        
        
    def calculate_breakeven_prices(self):
        """
        Calculate all the breakeven prices for this strategy.

        Returns
        -------
        breakeven_prices : 'list'
            A list of breakeven prices.

        """
        
        strikes = self.strike_prices.copy()
        strikes.extend([0, 100000])
    
        strikes = sorted(strikes)
        returns = [self.get_return(strike) for strike in strikes]
        breakeven_prices = []
        
        
        for i in range(len(returns)-1):
            
            if np.sign(returns[i]) != np.sign(returns[i+1]):
                
                m = (returns[i] - returns[i+1]) / (strikes[i] - strikes[i+1])
                b = returns[i] - (m * strikes[i])
                
                breakeven = -b/m
                breakeven_prices.append(breakeven)
                
        return breakeven_prices
    
    
    
    def calculate_max_profit_prices(self):
        """
        Calculates the underlying asset prices that return the greatest profit
        when the underlying asset price moves to these prices.

        Returns
        -------
        max_profit_prices : 'list'
            A list of prices which when reached by the underlying asset,
            will return the greatest profit from this strategy.

        """
        
        max_profit_prices = [strike_price for strike_price in self.strike_prices
                             if self.get_return(strike_price) == self.max_profit]
        
        if len(max_profit_prices) == 0:
            max_profit_prices.append(np.nan)
            
        return max_profit_prices
        
    
        
    def calculate_max_loss_prices(self):
        """
        Calculates the underlying asset prices that return the greatest loss
        when the underlying asset price moves to these prices.

        Returns
        -------
        max_loss_prices : 'list'
            A list of prices which when reached by the underlying asset,
            will return the greatest loss from this strategy.

        """
        
        max_loss_prices = [strike_price for strike_price in self.strike_prices
                             if self.get_return(strike_price) == self.max_loss]
        
        if len(max_loss_prices) == 0:
            max_loss_prices.append(np.nan)
            
        return max_loss_prices
            
        
    
    def calculate_max_profit(self):
        """
        Calculates the maximum possible profit from this strategy.

        Returns
        -------
        max_profit : 'float'
            The maximum profit possible from this strategy.

        """
        
        if self.get_return(self.strike_prices[-1]+1) > self.get_return(self.strike_prices[-1]):
            max_profit = np.inf
        else:
            returns = [self.get_return(strike_price) for strike_price in self.strike_prices]
            returns.append(self.get_return(0))
            
            max_profit = max(returns)
        
        return max_profit
        
    
   
    def calculate_max_loss(self):
        """
        Calculates the maximum possible loss from this strategy.

        Returns
        -------
        max_loss : 'float'
            The maximum loss possible from this strategy.

        """
        
        if self.get_return(self.strike_prices[0]-1) < self.get_return(self.strike_prices[0]):
            max_profit = -np.inf
        else:
            returns = [self.get_return(strike_price) for strike_price in self.strike_prices]
            returns.append(self.get_return(0))
            
            max_profit = min(returns)
        
        return max_profit
        
    
        
    def calculate_net_premium(self):
        """
        Calculates the net premium paid to set up this strategy.

        Returns
        -------
        'float'
            The net premium paid to set up this strategy.

        """
        
        premiums = [option.premium for option in self.legs]
        
        return round(sum(premiums), 2)
        
    
        
    def calculate_capital_committed(self):
        """
        Calculates the capital committed to setting up this strategy.
        
        Returns
        -------
        'float'
            The total capital committed to setting up this strategy.

        """
        
        if self.net_premium < 0:
            return 0
        else:
            return self.net_premium * 100
        
        
    
    def calculate_timeframe(self):
        """
        Calculates the timeframe of this strategy.
        
        Returns
        -------
        'int'
            The number of days until the first option expires.

        """
        
        min_date = self.legs[0].expiration_date
        
        for option in self.legs:
            if option.expiration_date < min_date:
                min_date = option.expiration_date
    
        
        return (min_date-self.current_date).days
        
    
    
    def get_return(self, new_price):
        """
        Returns the return of an option strategy when the underlying
        asset reaches a new price of new_price.
        
        Parameters
        ----------
        new_price : 'float'
            The new price of the underlying asset.
        
        Returns
        -------
        'float'
            The return of this strategy if the underlying asset price moves
            to a new price.
    
        """
        
        returns = [option.get_return(new_price) for option in self.legs]
        
        return round(sum(returns), 2)
        
    
        
    def get_risk_reward_ratio(self, new_price):
        """
        Calculates and returns the risk:reward ratio of this strategy.
        The risk:reward ratio is the ratio that tells you how much you stand
        to gain for each dollar risked.

        Parameters
        ----------
        new_price : 'float'
            The new price of the underlying asset.

        Returns
        -------
        'float'
            The risk:reward ratio of this strategy.

        """
        
        reward = self.get_return(new_price)
        risk = abs(self.max_loss)
        
        if risk == 0:
            risk = 0.01
        
        return round(reward/risk, 2)
        
    
    
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
    
    
    
    def get_profit_loss_table(self, price_range):
        """
        The profit loss table is a table detailing the returns of each leg in
        the strategy as well as the total strategy. Each row is the returns for
        a new underlying asset price and each row increments by one. This table
        also displays the risk:reward ratio.

        Parameters
        ----------
        price_range : 'tuple'
            A tuple with a start and end for a price range.

        Returns
        -------
        'pd.DataFrame'
            A dataframe containing the profit loss information for the overall
            strategy as well as each individual leg.

        """
        
        start = round(price_range[0])
        end = round(price_range[1])
        prices = pd.Series(range(start, end))
       
        series_dict = {}
        series_dict["Prices"] = prices
        
        for i, option in enumerate(self.legs):
            contract_name = option.get_contract_name()
            temp_returns = prices.apply(lambda x: option.get_return(x))
            series_dict["%s Returns" % contract_name] = temp_returns
            
        strategy_returns = prices.apply(lambda x: self.get_return(x))
        series_dict[ "%s Returns" % self.strategy_name] = strategy_returns
        
        strategy_risk_reward_ratios = prices.apply(lambda x: self.get_risk_reward_ratio(x))
        series_dict["%s Risk:Reward" % self.strategy_name] = strategy_risk_reward_ratios
        
        return pd.DataFrame(series_dict)
        
    
    
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
        
        # Creates the price range of 80% to 120%
        start = round(self.underlying_asset_price*0.7, 2)
        end = round(self.underlying_asset_price*1.3, 2)
        price_range = (start,end)
        
        prices, returns = self.get_return_arrays(price_range)
        
        # Creates the titles and axis labels
        title = "{}: {}".format(self.strategy_name, self.underlying_asset_symbol)
        xlabel = "New Price ($)"
        ylabel = "Return ($)"
    
        # Creates the labels for each strike price and each breakeven price
        strike_price_labels = ["Strike Price: {}".format(strike) for strike in self.strike_prices]
        breakeven_price_labels = ["Breakeven Price: {}".format(breakeven) for breakeven in self.breakeven_prices]
        
        max_profit_label = "Max Profit: {}".format(self.max_profit)
        max_loss_label = "Max Loss: {}".format(self.max_loss)
        
        
        plt.figure()
        plt.title(title)
        
        plt.plot(prices, returns)
        
        # Loops through each breakeven price and strike price and plots a vertical line
        for i, strike_label in enumerate(strike_price_labels):
            plt.axvline(x=self.strike_prices[i], color='k', linestyle='-', label=strike_label) 
        for i, breakeven_label in enumerate(breakeven_price_labels):
            plt.axvline(x=self.breakeven_prices[i], color='b', linestyle='--', label=breakeven_label)
        
        # Plots a horizontal line for the max profit, max loss, and 0
        if self.max_profit != np.inf:
            plt.hlines(y=self.max_profit, xmin=start, xmax=end, label=max_profit_label, 
                       color='c', linestyle="-")
        if self.max_loss != -np.inf:
            plt.hlines(y=self.max_loss, xmin=start, xmax=end, label=max_loss_label, 
                       color='c', linestyle="-")
        plt.hlines(y=0, xmin=start, xmax=end)
        
        # Fill the area under the curve with green or red
        plt.fill_between(prices, returns, where=np.array(returns)>0, color='g')
        plt.fill_between(prices, returns, where=np.array(returns)<0, color='r')
        
        # Create a legend outside the box and label the axes.
        plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
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
        
        # Creates the price range of 80% to 120%
        start = round(self.underlying_asset_price*0.7, 2)
        end = round(self.underlying_asset_price*1.3, 2)
        price_range = (start,end)
        
        prices, returns = self.get_return_arrays(price_range)
        

        # Percent Price Change
        
        # Create the 3 prices arrays as a price change in percent
        prices_1 = (prices - self.underlying_asset_price)/self.underlying_asset_price * 100
        strike_price_changes_1 = [round((strike - self.underlying_asset_price)/
                                   self.underlying_asset_price*100, 2) for strike in self.strike_prices]
        breakeven_price_changes_1 = [round((breakeven - self.underlying_asset_price)/
                                   self.underlying_asset_price*100, 2) for breakeven in self.breakeven_prices]
            
        # Create the title and x-axis label with percent signs
        title_1 = "{}: {} {} Change".format(self.strategy_name, self.underlying_asset_symbol, "%")
        xlabel_1 = "Price Change (%)"
        
        # Create all of the strike price and breakeven price labels with percent signs.
        strike_price_labels_1 = ["Strike Price Change: {}{}".format(strike_price_change, "%") for 
                                strike_price_change in strike_price_changes_1]
        breakeven_price_labels_1 = ["Breakeven Price Change: {}{}".format(breakeven_price_change, "%") for 
                                  breakeven_price_change in breakeven_price_changes_1]
          
        
        # Absolute Price Change
        
        # Create the 3 prices arrays as a price change in absolute dollars.
        prices_2 = prices - self.underlying_asset_price
        strike_price_changes_2 = [round(strike - self.underlying_asset_price, 2) for strike in self.strike_prices]
        breakeven_price_changes_2 = [round(breakeven - self.underlying_asset_price, 2) for breakeven in self.breakeven_prices]
            
        # Create the title and x-axis label with dollar signs
        title_2 = "{}: {} {} Change".format(self.strategy_name, self.underlying_asset_symbol, "$")
        xlabel_2 = "Price Change ($)"
            
        # Create all of the strike price and breakeven price labels with dollar signs.
        strike_price_labels_2 = ["Strike Price Change: {}{}".format("$", strike_price_change) for 
                                strike_price_change in strike_price_changes_2]
        breakeven_price_labels_2 = ["Breakeven Price Change: {}{}".format("$", breakeven_price_change) for 
                                  breakeven_price_change in breakeven_price_changes_2]
        
    
        # Plotting
        ylabel = "Return ($)"
        max_profit_label = "Max Profit: {}".format(self.max_profit)
        max_loss_label = "Max Loss: {}".format(self.max_loss)
        
        fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 6))


        # Percent Change Plot
        ax1.plot(prices_1, returns)
        
        # Plotting a vertical line for each of the strike price and breakeven price
        # all with the percent change values.
        for i, strike_label in enumerate(strike_price_labels_1):
            ax1.axvline(x=strike_price_changes_1[i], color='k', linestyle='-', label=strike_label) 
        for i, breakeven_label in enumerate(breakeven_price_labels_1):
            ax1.axvline(x=breakeven_price_changes_1[i], color='b', linestyle='--', label=breakeven_label)
        
        # Plotting a horizontal line for the max profit, max loss, and 0. The line is only
        # plotted if the value is not infinity.
        if self.max_profit != np.inf:
            ax1.hlines(y=self.max_profit, xmin=prices_1[0], xmax=prices_1[len(prices_1)-1], 
                       label=max_profit_label, color='c', linestyle="-")
        if self.max_loss != -np.inf:
            ax1.hlines(y=self.max_loss, xmin=prices_1[0], xmax=prices_1[len(prices_1)-1], 
                       label=max_loss_label, color='c', linestyle="-")
        ax1.hlines(y=0, xmin=prices_1[0], xmax=prices_1[len(prices_1)-1])
        
        # Filling the area under the curve in the percent change plot with green and red.
        ax1.fill_between(prices_1, returns, where=np.array(returns)>0, color='g')
        ax1.fill_between(prices_1, returns, where=np.array(returns)<0, color='r')
        
        # Setting the title and axes and creating a legend outside the box,for the 
        # percent change plot.
        ax1.set_title(title_1)
        ax1.set(xlabel=xlabel_1, ylabel=ylabel)
        ax1.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
        
        
        # Absolute Price Change Plot
        ax2.plot(prices_2, returns)
        
        # Plotting a vertical line for each of the strike price and breakeven price
        # all with the absolute price change information.
        for i, strike_label in enumerate(strike_price_labels_2):
            ax2.axvline(x=strike_price_changes_2[i], color='k', linestyle='-', label=strike_label) 
        for i, breakeven_label in enumerate(breakeven_price_labels_2):
            ax2.axvline(x=breakeven_price_changes_2[i], color='b', linestyle='--', label=breakeven_label)
        
        # Plotting a horizontal line for the max profit, max loss, and 0. The line is only
        # plotted if the value is not infinity.
        if self.max_profit != np.inf:
            ax2.hlines(y=self.max_profit, xmin=prices_2[0], xmax=prices_2[len(prices_2)-1], 
                       label=max_profit_label, color='c', linestyle="-")
        if self.max_loss != -np.inf:
            ax2.hlines(y=self.max_loss, xmin=prices_2[0], xmax=prices_2[len(prices_2)-1], 
                       label=max_loss_label, color='c', linestyle="-")
        ax2.hlines(y=0, xmin=prices_2[0], xmax=prices_2[len(prices_2)-1])
        
        # Filling the area under the curve in the aboslute price change plot with green and red.
        ax2.fill_between(prices_2, returns, where=np.array(returns)>0, color='g')
        ax2.fill_between(prices_2, returns, where=np.array(returns)<0, color='r')
        
        # Setting the title and axes and creating a legend outside the box, for the 
        # absolute price change plot.
        ax2.set_title(title_2)
        ax2.set(xlabel=xlabel_2, ylabel=ylabel)
        ax2.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')


        # Entire figure
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
        
        print("Strategy Name: %s" %str(self.strategy_name))
        print("Direction: %s" % str(self.direction))
        
        print("Underlying Asset Symbol: %s" % str(self.underlying_asset_symbol))
        print("Underlying Asset Current Price: %s" % str(self.underlying_asset_price))
        
        print("Number of legs: %s" % str(len(self.legs)))
        print("Legs: %s" % str(', '.join([option.get_contract_name() for option in self.legs])))
        print("Long Legs: %s" % str(', '.join([option.get_contract_name() for option in self.long_legs])))
        print("Short Legs: %s" % str(', '.join([option.get_contract_name() for option in self.short_legs])))
        
        print("Strike Prices: %s" % str(', '.join([str(strike_price) for strike_price in self.strike_prices])))
        print("Strike Price Returns: %s" % str(', '.join([str(self.get_return(strike_price)) for strike_price in self.strike_prices])))
        
        print("Net Premium: %s" % str(self.net_premium))
        print("Capital Committed: %s" % str(self.capital_committed))
        
        print("Breakeven Prices: %s" % str(','.join([str(price) for price in self.breakeven_prices])))
        print("Max Profit Prices: %s" % str(', '.join([str(price) for price in self.max_profit_prices])))
        print("Max Loss Prices: %s" % str(', '.join([str(price) for price in self.max_loss_prices])))
        
        print("Max Profit: %s" % str(self.max_profit))
        print("Max Loss: %s" % str(self.max_loss))
        
        print("Expiration Dates: %s" % ', '.join(sorted([option.expiration_date.strftime("%Y/%m/%d") for option in self.legs])))
        print("Current Date: %s" % self.current_date.strftime("%Y/%m/%d"))
        print("Timeframe: %s (Days)" % str(self.timeframe))
        