#*********************************
# Classify: Time series of letters
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import numpy as np
import sys

import filefetch as f
import plot

#=================================
# Adjust starting point to (0,0), apply change to all points in time series
# Move start point to (0,0)
# Input: time series t
# Return: modified time series
#=================================
def start_zero(t):
    offset = t[0]
    
    for i in range(len(t)):
        t[i] = t[i] - offset
    
    return t



# TODO: make the lists the same length, only then can I do a proper scaling
# Equalize the length between two time series t1 and t2
def eq_len(t1, t2):
    l1 = len(t1)
    l2 = len(t2)
    
    # Get max length
    max_len = max(l1, l2)
    
    # TODO: find which time series is smaller, and populate with points in between until l1==l2
    
    return a, b



#=================================
# Scale time series t to be in the some range
# Return: scaled time series t now in range [outmin...outmax]
#=================================
def scale(t):
    # input range
    inmin = np.amin(t)
    inmax = np.amax(t)
    
    print(len(t))
    
    # Output range
    outmin = 0
    outmax = 99
    
    for i in range(len(t)):
        t[i] = outmax * (t[i] - inmin) / (inmax - inmin) 
    
    return t



#=================================
# Start
#=================================
# Specify which letter to plot from cmd line
letter1 = (sys.argv[1]).upper()
num1 = sys.argv[2]
letter2 = (sys.argv[3]).upper()
num2 = sys.argv[4]

# Create plot object
p = plot.plot(letter1, num1, letter2, num2)

# Get and modify time series
x1 = start_zero(p.data1[0])
y1 = start_zero(p.data1[1])
x2 = start_zero(p.data2[0])
y2 = start_zero(p.data2[1])

# Force x and y time series to be the same length


#p.data1[0] = start_zero(p.data1[0])
#p.data1[1] = start_zero(p.data1[1])
#p.data2[0] = start_zero(p.data2[0])
#p.data2[1] = start_zero(p.data2[1])


# Display plot
p.overlay_plots()
p.show()
