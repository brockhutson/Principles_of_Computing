# -*- coding: utf-8 -*-
"""

@author: Brock

http://www.codeskulptor.org/#user46_DD9q9r7tcBK7wOk.py

Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.total_cookies_produced = 0.0
        self.current_time = float(0.0)
        self.current_CPS = float(1.0)
        self.cookies_stored = float(0.0)
        self.item_name = None
        self.item_cost = float(0.0)
        self.history = [(0.0, None, 0.0, 0.0)] #(time, item, cost of item, total cookies)
       
    def __str__(self):
        """
        Return human readable state
        """   
        return ("\nCurrent time: " + str(self.current_time) + 
                "\nCurrent CPS: " + str(self.current_CPS) + 
                "\nCurrent Cookies: " + str(self.cookies_stored) +
                "\nTotal Cookies Produced: " + str(self.total_cookies_produced) + "\n")
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.cookies_stored
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.current_CPS
   
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > 0 and cookies >= self.cookies_stored:	
            return math.ceil((cookies - self.cookies_stored) / self.current_CPS)
        else:
            return 0.0
        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self.current_time += time
            self.cookies_stored += self.current_CPS * time
            self.total_cookies_produced += self.current_CPS * time
        else:
            pass
                
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.cookies_stored < cost:
            pass
        elif self.cookies_stored >= cost:
            self.item_name = item_name
            self.item_cost = cost
            self.cookies_stored -= cost
            self.current_CPS += additional_cps
            
            event = (self.current_time, self.item_name, self.item_cost, self.total_cookies_produced)
            self.history.append(event)

   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_clone = build_info.clone()
    simulation = ClickerState() 
    
    while simulation.get_time() < duration:
        t_minus = duration - simulation.get_time()
        
        item_name = strategy(simulation.get_cookies(), simulation.get_cps(), simulation.get_history(), t_minus, build_clone)
        
        if item_name == None:
            break
            
        if simulation.time_until(build_clone.get_cost(item_name)) > t_minus:
            break
            
        else:
            item_name = strategy(simulation.get_cookies(), simulation.get_cps(), simulation.get_history(), t_minus, build_clone)
            simulation.wait(simulation.time_until(build_clone.get_cost(item_name)))
            simulation.buy_item(item_name, build_clone.get_cost(item_name), build_clone.get_cps(item_name))
            build_clone.update_item(item_name)
    
    simulation.wait(t_minus)
    
    return simulation


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """

    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_list = build_info.build_items()
    price_list = map(build_info.get_cost, item_list)
    cheapest_item_index = price_list.index(min(price_list))
    cheapest_item = item_list[cheapest_item_index]
    
    if (cookies + cps * time_left) < price_list[cheapest_item_index]:
        return None
    else:
        return cheapest_item
        
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    if time_left <= 0:
        return None
    else:
        item_list = build_info.build_items()
        most_expensive = None
        highest_price = 0
        for item in item_list:
            item_price = build_info.get_cost(item)
            if  item_price <= (cookies + cps * time_left) and item_price > highest_price:
                highest_price = item_price
                most_expensive = str(item)
        return most_expensive

    

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    if time_left <= 0:
        return None
    else:
        item_list = build_info.build_items()
        best_item = None
        efficiency = float('-inf')
        for item in item_list:
            price = build_info.get_cost(item)
            item_cps = build_info.get_cps(item)
            if item_cps / price > efficiency:
                best_item = item
                efficiency = item_cps / price
        return best_item
    
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

     #history = state.get_history()
     #history = [(item[0], item[3]) for item in history]
     #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

