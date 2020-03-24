#*********************************
# Module: time series operations
#   - Store time series operations to be reused with programs that deal with time series. The user only has to call the function apply_all to apply all these transformations.
# Author: Manuel Serna-Aguilera
#*********************************

import numpy as np
import math



#=================================
# Sub-Procedure: Increase length of time series by estimating distance between two consecutive points
'''
Input:
    - t: some time series
    - new_length: desired length for new time series
Return:
    - s: newly-sized time series
'''
# Called by: set_length
#=================================
def increase_len(t, new_length):
    s = [t[0]]
    l = len(t)
    diff = new_length - l
    step = int(math.floor(new_length/diff)-1)
    
    if step <= 1:
        step = 2
    
    while diff > 0:
        for i in range(1, l):
            current_val = t[i]
            if i % step == 0 and diff > 0:
                prev_val = t[i-1]
                est_val = int((current_val + prev_val)/2)
                
                s.append(est_val)
                s.append(current_val)
                
                diff -= 1
            else:
                s.append(current_val)
        
        if diff == 1:
            # Interpolate between first and second elements
            est_val = int((s[0]+s[1])/2)
            s.insert(1, est_val)
            diff -= 1
        
        # Recalcuate step size according to new output time series size
        if diff > 0:
            t = s # reference s as t now
            s = [t[0]] # reset s
            l = len(t)
            diff = new_length - l
            step = int(math.floor(new_length/diff)-1)
            
            if step <= 1:
                step = 2
    return s



#=================================
# Sub-Procedure: Reduce length of time series by estimating distance between two consecutive points
'''
Input:
    - t: some time series
    - new_length: desired length for new time series
Return:
    - s: newly-sized time series
'''
# Called by: set_length
#=================================
def decrease_len(t, new_length):
    s = [t[0]] # reduced time series s
    l = len(t)
    diff = l - new_length
    step = int(math.floor(l/diff)-1)
    
    if step <= 1:
        step = 2
    
    while diff > 0:
        for i in range(1, l):
            current_val = t[i]
            if i % step == 0 and diff > 0:
                prev_val = t[i-1]
                est_val = int((current_val + prev_val)/2)
                
                x = s.pop(-1)
                s.append(est_val)
                
                diff -= 1
            else:
                s.append(current_val)
                
        if diff == 1:
            # Interpolate between first and second elements
            est_val = int((s[0]+s[1])/2)
            s.insert(1, est_val)
            diff -= 1
        
        # Recalcuate step size according to new output time series size
        if diff > 0:
            t = s # reference s as t now
            s = [t[0]] # reset s
            l = len(t)
            diff = l - new_length
            step = int(math.floor(l/diff)-1)
            
            if step <= 1:
                step = 2
    return s



#=================================
# Set length of time series t to some set number
'''
Input:
    - t: some time series
    - new_length: shrink or grow list to be this new length (default=175)
Return:
    - t: modified time series of length 'new_length'
'''
#=================================
def set_length(t, new_length=175):
    l = len(t)
    
    if l < new_length:
        t = increase_len(t, new_length)
    elif l > new_length:
        t = decrease_len(t, new_length)
    
    return t



#=================================
# Scale time series t to be in the some range
# Input: some time series t
# Return: scaled time series t now in range [outmin...outmax]
#=================================
def scale(t):
    # input range
    inmin = np.amin(t)
    inmax = np.amax(t)
    
    # Output range
    outmin = 0
    outmax = 99
    
    for i in range(len(t)):
        t[i] = outmax * (t[i] - inmin) / (inmax - inmin) 
    
    return t



#=================================
# Move start point to (0,0) and translate entire time series
# Input: time series t
# Return: modified time series
#=================================
def start_zero(t):
    offset = t[0]
    for i in range(len(t)):
        t[i] = t[i] - offset
    return t



#=================================
# Apply all modifications
# Input: raw time series t
# Return: modified time series with modifications above applied
#=================================
def apply_all(t):
    t = start_zero(t)
    t = scale(t)
    t = set_length(t)
    return t
