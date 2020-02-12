# -*- coding: utf-8 -*-
"""

@author: Brock
"""
import matplotlib
import math

#def area(func, low, high, stepsize):
#    total = 0.0
#    loc = low
#    while loc < high:
#        total += func(loc) * stepsize
#        loc += stepsize
#    return total
#
#def f(x):
#    return x
#
#def g(x):
#    return x ** 2
#
#print (area(f, 0, 10, .01))
#print (area(g, 0, 10, .0001))
#
#def h(x):
#    if x < 3:
#        return x
#    elif x < 7 :
#        return x ** 2
#    else:
#        return 7 * x - 4
#
#print (area(h, 0, 10, 0.001))

def build_plot(plot_size, plot_function, plot_type = STANDARD):
    """
    Build plot of the number of increments in mystery funciton
    -Uses code sculptor plotting library 
    """
    global counter
    plot = []
    for input_val in range(2, plot_size):
        counter = 0
        plot_function(input_val)
        if plot_type == STANDARD:
            plot.append([input_val, counter])
        else:
            plot.append([math.log(input_val), math.log(counter)])
    return plot