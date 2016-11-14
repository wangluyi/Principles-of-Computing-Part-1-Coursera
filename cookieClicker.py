"""
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
        self._total_num_of_cookies = 0.0
        self._current_num_of_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        
        self._history = [(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        return 'total number: ' + str('{0:.1f}'.format(self._total_num_of_cookies)) + '\n' \
                'current number: ' + str('{0:.1f}'.format(self._current_num_of_cookies)) + '\n' \
                'current time: ' + str(self._current_time) + '\n' \
                'current CPS: ' + str(self._current_cps)

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_num_of_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_num_of_cookies >= cookies:
            return 0.0
        elif self._current_cps!=0:
            return math.ceil( (cookies-self._current_num_of_cookies)/self._current_cps  )
        else:
            return float('inf')
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time<=0.0:
            pass
        else:
            self._total_num_of_cookies += self._current_cps * time
            self._current_num_of_cookies += self._current_cps * time
            self._current_time += time


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_num_of_cookies < cost:
            pass
        else:
            self._current_num_of_cookies -= cost
            self._current_cps += additional_cps
            self._history.append( (self._current_time, item_name, cost, self._total_num_of_cookies) )
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    my_build_info = build_info.clone()
    my_clickerState = ClickerState()
    
    while duration >= 0:
        item = strategy(my_clickerState.get_cookies(), my_clickerState.get_cps(), my_clickerState.get_history(), duration - my_clickerState.get_time(), my_build_info)
        if item == None:
            break
        item_cost = my_build_info.get_cost(item)
        wait_time = my_clickerState.time_until(item_cost)
        
        if duration < wait_time:
            break
        else:
            duration -= wait_time
            my_clickerState.wait(wait_time)
            my_clickerState.buy_item(item, item_cost, my_build_info.get_cps(item))
            my_build_info.update_item(item)
        
    my_clickerState.wait(duration)
    
    return my_clickerState

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
    cost_of_item = {}
    for item in build_info.build_items():
        cost_of_item[item] = build_info.get_cost(item)
    cheapest_cost = min(cost_of_item.values())
    if cheapest_cost <= (cookies + cps * time_left):
        for name, cost in cost_of_item.items():
            if cost == cheapest_cost:
                return name
                

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cost_of_item = {}
    name = None
    
    for item in build_info.build_items():
        cost_of_item[item] = build_info.get_cost(item)
    most_expensive_cost = max(cost_of_item.values())
    if most_expensive_cost <= (cookies + cps * time_left):
        for name, cost in cost_of_item.items():
            if cost == most_expensive_cost:
                return name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_lst = build_info.build_items()
  
    max_efficiency = 0
    most_efficient_item = None
    
    for item in item_lst:
        index_efficiency = float(build_info.get_cps(item)) / float(build_info.get_cost(item))
        if index_efficiency > max_efficiency:
            max_efficiency = index_efficiency
            most_efficient_item = item
            
    return most_efficient_item
    
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time
    history = state.get_history()
    history_item0_item3 = [(item[0],item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history_item0_item3], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
    

