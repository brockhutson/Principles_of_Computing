# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:01:54 2019

@author: Brock
"""
import random
import statistics as stats

def dice_roll():
    x = random.randint(1,6)
    y = random.randint(1,6)
    
    return (x, y)


def hardways(repeated):
    hardway = []
    count = 0
    prev_roll = None
    
    while len(hardway) < repeated:
        roll = dice_roll()
        count += 1
        if len(hardway) == 0 and roll[0] == roll[1]:
            hardway.append(roll)
        else:
            if roll[0] == roll[1]:
                if prev_roll == roll and roll == hardway[0]:
                    hardway.append(roll)
                else:
                    hardway = []
        prev_roll = roll
        
    return count


def hardway_simulator(events, repeats):
    list_of_rolls = [hardways(repeats) for x in range(events)]
        
    answer = ('Average rolls: ' + str(stats.mean(list_of_rolls)) + 
              '\nMedian Rolls: ' + str(stats.median(list_of_rolls)) +
              '\nMin Rolls: ' + str(min(list_of_rolls)) +
              '\nMax Rolls: ' + str(max(list_of_rolls)))
    print (answer)
    return answer

hardway_simulator(1000, 4)