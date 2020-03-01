#*********************************
# Classifier: Time series of letters
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import numpy as np
import math
import sys

import file_io as f
import plot

infty = 999999

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
# Insert estimated elements in between consecutive elements in a given list
'''
Input:
    - og_list: original list
    - step: jump by this many elements in og_list to spread insertions evenly
    - insertions: number of times left to insert
Return:
    - list with new length
NOTE: function may be called recursively in order to account for large difference in drawing velocities between the two letters
'''
#=================================
def insert_between(og_list, step, insertions):
    new_list = og_list[:1]
    prev = new_list[0]
    
    # Construct new list with added elements
    for i in og_list[1:]:
        # Add new element according to step size
        if len(new_list) % step == 0 and insertions > 0:
            new = int((i+prev)/2) # estimate intermediate element
            new_list.append(new)
            insertions -= 1 # one less insertion to make
        
        new_list.append(i)
        prev = i
    
    # If there are still insertions to make, make a recursive call to keep inserting
    if insertions > 0:
        new_list = insert_between(new_list, step, insertions)
    
    return new_list



#=================================
# Equalize the length between two time series t1 and t2 based on the larger one
'''
Input: two time series
Return: 
    - if, somehow, t1 and t2 are the same length, return the input time series
    - two time series, now equal in length
        NOTE: function insert_between may be called recursively to keep filling in elements if the difference between the lengths is greater than the length of the smaller list
'''
#=================================
def eq_len(t1, t2):
    # Get lengths of each time series
    l1 = len(t1)
    l2 = len(t2)
    
    # Calculate how often to insert new elements into shorter list
    min_len = min(l1, l2)
    max_len = max(l1, l2)
    
    # Avoid division by zero error
    diff = max_len - min_len
    if diff == 0:
        return t1, t2
    else:
        step = int(math.ceil(min_len/diff))
    
    # Lengthen the shorter list to be as long as the longer list
    if l1 == max_len:
        t2 = insert_between(t2, step, diff)
    else:
        t1 = insert_between(t1, step, diff)
    
    return t1, t2



#=================================
# Scale time series t to be in the some range
# Input: time series t
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
# Dynamic Time Warping: find minimum edit distance
# Input: two time series t1 and t2
# Return: minimum edit distance--a measure of similarity (the lower=the more similar the two time series)
#=================================
def dtw(t1, t2):
    # Get lengths n and m
    n = len(t1)+1
    m = len(t2)+1
    
    # Create (n+1 x m+1) list and zero-initialize
    result = [[0 for i in range(n)] for j in range(m)]
    
    # Fill in 0th row and 0th column to have t2's and t1's elements respective as initial values for the algorithm to work
    for i in range(0, n-1):
        result[i+1][0] = t1[i]
    for j in range(0, m-1):
        result[0][j+1] = t2[j]
    
    # Initialize all other elements to "infinity"
    for i in range(1, n):
        for j in range(1, m):
            result[i][j] = infty
    result[0][0] = 0
    result[1][1] = 0
    
    # Calculate minimum edit distance
    for i in range(1, n):
        for j in range(1, m):
            dist = abs(result[i][0]-result[0][j])
            result[i][j] = dist + min(
                result[i-1][j],# insertion
                result[i][j-1],# deletion
                result[i-1][j-1] # match
                )
    
    #for row in result:
    #    print(row)
    
    return result[n-1][m-1]


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

# Get time series
x1 = p.data1[0]
y1 = p.data1[1]
x2 = p.data2[0]
y2 = p.data2[1]


#---------------------------------
# Operations on time series
#---------------------------------
# 1) 
# Translate time series to start at zero
x1 = start_zero(x1)
y1 = start_zero(y1)
x2 = start_zero(x2)
y2 = start_zero(y2)

# 2)
# Force x and y time series to be the same length
x1, x2 = eq_len(x1, x2)
y1, y2 = eq_len(y1, y2)

# 3)
# Scale time series to some common out range
x1 = scale(x1)
y1 = scale(y1)
x2 = scale(x2)
y2 = scale(y2)

# 4)
# Calculate minimum edit distance
distancex = dtw(x1, x2)
distancey = dtw(y1, y2)
print("X min edit distance: ", distancex)
print("Y min edit distance: ", distancey)



# Set modified time series in plot object
p.data1[0] = x1
p.data1[1] = y1
p.data2[0] = x2
p.data2[1] = y2

# Display plot
p.overlay_plots()
p.show()
