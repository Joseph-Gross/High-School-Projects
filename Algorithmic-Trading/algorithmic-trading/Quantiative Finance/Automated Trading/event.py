#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:15:49 2020

@author: josephgross
"""


class Event(object):
    """
    Event is base class providing an interface for all subsequent
    (inherited) events, that will trigger events in the trading 
    infrastructure
    
    """
    
    pass




class MarketEvent(Event):
    """
    Handles the event of recieving a new market update with 
    corresponding bars
    
    """
    
    def __init__(self):
        """
        Initializes the MarketEvent

        Returns
        -------
        None.

        """
        self.type = 'MARKET'




class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy
    object. This is recieved by a Portoflio object and acted upon
    
    """
    
    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        """
        Initializes the SignalEvent.

        Parameters
        ----------
        strategy_id : 'int'
            The unique identifier for the strategy that generated the 
            signal.
        symbol : 'str'
            The ticker symbol, e.g. 'GOOG'.
        datetime : 'datetime'
            The timestamp at which the signal was generated.
        signal_type : 'str'
            'LONG' or 'SHORT'.
        strength : 'float'
            An adjustment factor "suggestion" used to scale quantity
            at the portfolio level. Useful for pairs strategies.

        Returns
        -------
        None.

        """
        
        self.type = 'SIGNAL'
        self.stategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength
        
        
        
    
class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system. The
    order contains a symbol (e.g. GOOG), a type (market or limit), 
    quantitiy, and a direction.
    
    """
    
    def __init__(self, symbol, order_type, quantity, direction):
        """
        Inititalizes the order type, setting whether it is a Market
        order ('MKT') or Limit order ('LMT'), has a quantity (integral)
        and its direction ('BUY' or 'SELL')

        Parameters
        ----------
        symbol : 'str'
            The instrument to trade.
        order_type : 'str'
            'MKT' or 'LMT' for Market or Limit.
        quantity : 'int'
            Non-negative integer for quantity.
        direction : 'str'
            'BUY' or 'SELL' for long or short.

        Returns
        -------
        None.

        """
        
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = self._check_set_quantity_positive(quantity)
        self.direction = direction
    
    def _check_set_quantity_positive(self, quantity):
        """
        Checks that quantity is a positive integer.

        """
        
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Order event quantity is not a positive integer")
        
        return quantity
    
    def print_order(self):
        """
        Outputs the values within the Order.

        Returns
        -------
        None.

        """
        
        print(
            "Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" %
            (self.symbol, self.order_type, self.quantity, self.direction)
        )
        
        
        
class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned from a brokerage. 
    Stores the quantity of an instrument actually filles and at what price. 
    In additon, stores the commission of the trade brokerage.
    """
    
    def __init__(self, timeindex, symbol, exchange, quantity, direction, 
                 fill_cost, commission=None):
        """
        Inititalizes the FillEvent object. Sets the symbol, exchange, quantity, 
        direction, cost of fill, and an optional comission.
        
        If commission if not provided, the Fill object will calculate it based
        on the trade size and Interactive Brokers fees.

        Parameters
        ----------
        timeindex : TYPE
            The bar-resolution when the order was filled.
        symbol : 'str'
            The instrument which was filled.
        exchange : 'str'
            The exchange where the order was filled.
        quantity : 'float'
            The filled quantity.
        direction : 'str'
            The direciton of the fill ('BUY' or 'SELL).
        fill_cose : 'float'
            The holdings value in dollars.
        commission : 'float', optional
            An optional commission sent from IB. The default is None.

        Returns
        -------
        None.

        """
        
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        
        # Calculate commission
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission
            
        
    def calculate_ib_commission(self):
        """
        Calculates the fees of trading based on an Interactive Brokers
        fee structure for API, in USD.
        
        This does not include exchange or ECN fees.
        
        Based on "US API Directed Orders"
        https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2

        Returns
        -------
        'float'
            The commission cost.

        """
        
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013 * self.quantity)
        else: # Greater than 500
            full_cost = max(1.3, 0.008 * self.quantity)
        return full_cost
    
    