#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:15:13 2020

@author: josephgross
"""

from OptionObject import Option



class Call(Option):
    """
    A Call object which implements the Option class as a parent class.
    """
    
    
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
        
        self.type = "CALL"
        super().__init__(underlying_symbol, underlying_price, info_series, is_long)
        
    
    def calculate_description(self):
        """
        Calculates the description of this call: (ITM, ATM, OTM).

        Returns
        -------
        'str'
            ITM, ATM, or OTM.

        """
        
        delta_price = self.underlying_asset_price - self.strike_price
        delta_price_percentage = abs(delta_price) / self.underlying_asset_price * 100 
        
        if delta_price_percentage < 3:
            return "ATM"
        elif delta_price > 0: # if strike < underlying, ITM
            return "ITM"
        elif delta_price < 0:
            return "OTM"
        
        
    def calculate_intrinsic_value(self):
        """
        Calculates the intrinsic value of this contract.

        Returns
        -------
        'float'
            Intrinsic value of this call.

        """
        
        delta_price = self.underlying_asset_price - self.strike_price
        
        if delta_price > 0:
            return 0
        else:
            return -1*delta_price
    
    
    def calculate_breakeven_price(self):
        """
        Calculates the breakeven price point of this contract.

        Returns
        -------
        'float'
            The breakeven price point for this call.

        """
        
        return self.strike_price + self.premium
        
    
    def get_return(self, new_price):
        """
        Calculates and return the return of this contract if the 
        underlying asset price moves to the new price "new_price".

        Parameters
        ----------
        new_price : 'float'
            The new price of the underlying asset.

        Returns
        -------
        'float'
            The return of this contract if the underlying asset 
            price moves to the new price "new_price".

        """
        
        delta_price = new_price - self.strike_price
        
        if delta_price > 0:
            return round(self.direction * (abs(delta_price)-abs(self.premium)), 2)
        else:
            return round(self.direction * -1 * abs(self.premium), 2)
        