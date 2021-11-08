#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:32:29 2020

@author: josephgross
"""


import pandas as pd

from OptionStrategyObject import OptionStrategy
import time



class OpportunityScreener(object):
    """
    
    
    """
    
    
    def __init__(self, options_chain, target_price, timeframe):
        
        self.options_chain = options_chain
        
        self.underlying_price = options_chain.underlying_asset_price
        self.underlying_symbol = options_chain.underlying_asset_symbol
        
        self.target_price = target_price
        self.timeframe = self.get_closest_timeframe(timeframe)
        self.closest_strike_price = self.get_closest_strike_price(target_price)
        
        
    def get_closest_timeframe(self, timeframe):
        
        return self.options_chain.get_closest_time_to_expiration(timeframe)
    
    
    def get_closest_strike_price(self, target_price):
        
        return self.options_chain.get_closest_strike_price(target_price)
    
    
    def get_spread_info(self, row):
    
        row["Strategy Name"] = row["Spread"].strategy_name
            
        row["Premium"] = [leg.premium for leg in row["Spread"].legs]
        row["Risk:Reward"] = row["Spread"].get_risk_reward_ratio(self.target_price)
        return row
    
    
    def get_top_spreads_df(self):
        spreads_list = self.get_all_spreads_list()
        
        flattened_list = [item for spread in spreads_list for item in spread]
        df = pd.DataFrame(flattened_list)
        df.columns = ["Spread"]
        
        df = (df.apply(self.get_spread_info, axis=1)
              .sort_values(["Strategy Name", "Risk:Reward"], ascending=False)
              .drop_duplicates("Strategy Name")
              .set_index("Strategy Name")
              .sort_values("Risk:Reward", ascending=False))
        
        self.top_spreads_df = df
                
        
        return df
    
    
    def get_all_spreads_list(self):
        
        spreads_list = []
        for i in range(8):
            print(i, "-------------")
            start = time.time()
            spreads_list.append(self.calculate_all_spreads(i))
            end = time.time()
            print("Runtime: %s" % str(end-start))
            
        return spreads_list
            
    
    def calculate_all_spreads(self, i):
        
        if i%8 == 0:
            return self.bear_put_spread()
        elif i%8 == 1:
            return self.bear_call_spread() 
        elif i%8 == 2:
            return self.bull_put_spread() 
        elif i%8 == 3:
            return self.bull_call_spread()
        elif i%8 == 4:
            return self.long_straddle()
        elif i%8 == 5:
            return self.long_strangle()
        elif i%8 == 6:
            return self.iron_condor()
        elif i%8 == 7:
            return self.iron_butterly()
        
    
    def bear_put_spread(self):
        """
        Construction:
        - Long Put
        - Short Put with a lower strike price
        - Same expiration date
        
        """
        strategy_name = "Bear Put Spread"
        
        params_dict = {'Time Interval (days)':('==', self.timeframe)}
        long_put_list = self.options_chain.get_filtered_options_list(params_dict, 'Put', True)
        short_put_list = self.options_chain.get_filtered_options_list(params_dict, 'Put', False)
        
        bear_put_spreads = []
        
        for long_put in long_put_list:
            for short_put in short_put_list:
                
                if short_put.strike_price < long_put.strike_price:
                    option_legs = [short_put, long_put]
                    bear_put_spread = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                     self.underlying_price, option_legs)
                    bear_put_spreads.append(bear_put_spread)
                
        print("%s: %s" % (strategy_name, str(len(bear_put_spreads))))
        
        return bear_put_spreads
        
    
    def bear_call_spread(self):
        """
        Construction:
        - Short Call
        - Long Call with a higher strike price
        - Same expiration date
        
        """
        strategy_name = "Bear Call Spread"
        
        params_dict = {'Time Interval (days)':('==', self.timeframe)}
        long_call_list = self.options_chain.get_filtered_options_list(params_dict, 'Call', True)
        short_call_list = self.options_chain.get_filtered_options_list(params_dict, 'Call', False)
        
        bear_call_spreads = []
        
        for long_call in long_call_list:
            for short_call in short_call_list:
                
                if long_call.strike_price > short_call.strike_price:
                    option_legs = [long_call, short_call]
                    bear_call_spread = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                     self.underlying_price, option_legs)
                    bear_call_spreads.append(bear_call_spread)
                
        print("%s: %s" % (strategy_name, str(len(bear_call_spreads))))
        
        return bear_call_spreads
        
        
    def bull_put_spread(self):
        """
        Construction:
        - Long Put
        - Short Put at a higher strike price
        - Same expiration date
        
        """
        
        strategy_name = "Bull Put Spread"
        
        params_dict = {'Time Interval (days)':('==', self.timeframe)}
        long_put_list = self.options_chain.get_filtered_options_list(params_dict, 'Put', True)
        short_put_list = self.options_chain.get_filtered_options_list(params_dict, 'Put', False)
        
        bull_put_spreads = []
        
        for long_put in long_put_list:
            for short_put in short_put_list:
                
                if short_put.strike_price > long_put.strike_price:
                    option_legs = [short_put, long_put]
                    bull_put_spread = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                     self.underlying_price, option_legs)
                    bull_put_spreads.append(bull_put_spread)
                
        print("%s: %s" % (strategy_name, str(len(bull_put_spreads))))
        
        return bull_put_spreads
        
    
    def bull_call_spread(self):
        """
        Construction:
        - Long Call OTM
        - Short Call with a higher strike price
        - Same expiration date
        
        """
        
        strategy_name = "Bull Call Spread"
        
        params_dict = {'Time Interval (days)':('==', self.timeframe), "Description": ('c', 'OTM')}
        long_call_list = self.options_chain.get_filtered_options_list(params_dict, 'Call', True)
        short_call_list = self.options_chain.get_filtered_options_list(params_dict, 'Call', False)
        
        bull_call_spreads = []
        
        for long_call in long_call_list:
            for short_call in short_call_list:
                
                if short_call.strike_price > long_call.strike_price:
                    option_legs = [long_call, short_call]
                    bull_call_spread = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                     self.underlying_price, option_legs)
                    bull_call_spreads.append(bull_call_spread)
                
        print("%s: %s" % (strategy_name, str(len(bull_call_spreads))))
        
        return bull_call_spreads
        
        
    def long_straddle(self):
        """
        Construction:
        - Long Call
        - Long Put
        - Same underlying asset, same expiration date, same strike price
        - Both ATM or as close to it as possible
        
        """
        
        strategy_name = "Long Straddle"
        
        params_dict = {'Time Interval (days)':('==', self.timeframe), "Description": ('c', 'ATM')}
        long_call_list = self.options_chain.get_filtered_options_list(params_dict, 'Call', True)
        long_put_list = self.options_chain.get_filtered_options_list(params_dict, 'Put', True)
        
        long_straddle_spreads = []
        
        for long_call in long_call_list:
            for long_put in long_put_list:
                
                if long_call.strike_price == long_put.strike_price:
                    option_legs = [long_call, long_put]
                    long_straddle = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                          self.underlying_price, option_legs)
                    long_straddle_spreads.append(long_straddle)
                    
        print("%s: %s" % (strategy_name, str(len(long_straddle_spreads))))
        
        return long_straddle_spreads
        
        
    def long_strangle(self):
        """
        Construction:
        - Long Call
        - Long Put (different strike price)
        - Same underlying asset, same expiration date
        - Both ATM or as close to it as possible
        
        """
        
        strategy_name = "Long Strangle"
        
        params_dict = {'Time Interval (days)':('==', self.timeframe), "Description": ('c', 'ATM')}
        long_call_list = self.options_chain.get_filtered_options_list(params_dict, 'Call', True)
        long_put_list = self.options_chain.get_filtered_options_list(params_dict, 'Put', True)
        
        long_strangle_spreads = []
        
        for long_call in long_call_list:
            for long_put in long_put_list:
                
                if long_call.strike_price != long_put.strike_price:
                    option_legs = [long_call, long_put]
                    long_strangle = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                          self.underlying_price, option_legs)
                    long_strangle_spreads.append(long_strangle)
                    
        print("%s: %s" % (strategy_name, str(len(long_strangle_spreads))))
        
        return long_strangle_spreads
        
        
    def iron_condor(self):
        """
        Construction:
        - Long Put (further OTM than short put)
        - Short Put (ATM)
        - Short Call (ATM)
        - Long Call (futher OTM than short call)
        - Same expiration date
        
        """
        
        strategy_name = "Iron Condor"
        
        closest_strike = self.options_chain.get_closest_strike_price(self.underlying_price)
        
        short_legs_params_dict = {'Time Interval (days)':('==', self.timeframe), "strike": ('==', closest_strike)}
        short_call_list = self.options_chain.get_filtered_options_list(short_legs_params_dict, 'Call', False)
        short_put_list = self.options_chain.get_filtered_options_list(short_legs_params_dict, 'Put', False)
        
        long_legs_params_dict = {'Time Interval (days)':('==', self.timeframe), "Description": ('c', 'OTM')}
        long_call_list = self.options_chain.get_filtered_options_list(long_legs_params_dict, 'Call', True)
        long_put_list = self.options_chain.get_filtered_options_list(long_legs_params_dict, 'Put', True)
        
        iron_condor_spreads = []
        
        for long_call in long_call_list:
            for long_put in long_put_list:
                for short_call in short_call_list:
                    for short_put in short_put_list:
                        if long_call.strike_price != long_put.strike_price:
                            option_legs = [long_call, long_put, short_call, short_put]
                            iron_condor = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                           self.underlying_price, option_legs)
                            iron_condor_spreads.append(iron_condor)
                            
        print("%s: %s" % (strategy_name, str(len(iron_condor_spreads))))
        
        return iron_condor_spreads
        
        
    def iron_butterly(self):
        """
        Construction:
        - Long Call (far OTM, expected to expire OTM)
        - Short Call (nearest strike price to the target/expected new price)
        - Short Put (nearest strike price to the target/expected new price)
        - Long Put (far OTM, expected to expire OTM)
        - Both short strikes are equal and lower than the long call strike
        
        """
        
        strategy_name = "Iron Butterfly"
        
        short_legs_params_dict = {'Time Interval (days)':('==', self.timeframe), "strike": ('==', self.closest_strike_price)}
        short_call_list = self.options_chain.get_filtered_options_list(short_legs_params_dict, 'Call', False)
        short_put_list = self.options_chain.get_filtered_options_list(short_legs_params_dict, 'Put', False)
        
        long_legs_params_dict = {'Time Interval (days)':('==', self.timeframe), "Description": ('c', 'OTM')}
        long_call_list = self.options_chain.get_filtered_options_list(long_legs_params_dict, 'Call', True)
        long_put_list = self.options_chain.get_filtered_options_list(long_legs_params_dict, 'Put', True)
        
        iron_butterfly_spreads = []
        
        for long_call in long_call_list:
            for long_put in long_put_list:
                for short_call in short_call_list:
                    for short_put in short_put_list:
                        if long_call.strike_price != long_put.strike_price:
                            option_legs = [long_call, long_put, short_call, short_put]
                            iron_butterfly = OptionStrategy(strategy_name, "N/A", self.underlying_symbol, 
                                                           self.underlying_price, option_legs)
                            iron_butterfly_spreads.append(iron_butterfly)
                            
        print("%s: %s" % (strategy_name, str(len(iron_butterfly_spreads))))
        
        return iron_butterfly_spreads
        
    
    def create_summary_stats(self, row):
        
        row["Net Premium"] = row["Spread"].net_premium
        row["Capital Committed"] = row["Spread"].capital_committed
        row["Max Profit"] = row["Spread"].max_profit
        row["Max Loss"] = row["Spread"].max_loss
        
        row["Legs"] = [leg.get_contract_name() for leg in row["Spread"].legs]
            
        return row
        
        
    def output_summary_stats(self):
        
        top_spreads_df = self.get_top_spreads_df()
        top_spreads_df = top_spreads_df.apply(self.create_summary_stats, axis=1)
        
        
        return top_spreads_df
        