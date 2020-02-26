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



#=================================
#=================================




#=================================
# Start
#=================================
# Specify which letter to plot from cmd line
letter1 = (sys.argv[1]).upper()
num1 = sys.argv[2]
letter2 = (sys.argv[3]).upper()
num2 = sys.argv[4]

# Get images
img1 = f.get_img(letter1, num1, 'c')
data1 = f.get_file(letter1, num1)
img2 = f.get_img(letter2, num2, 'r') # color cyan
data2 = f.get_file(letter2, num2)

# Create plot object
p = plot.plot(letter1, num1, letter2, num2)

# Get and modify time series
p.data1[0] = start_zero(data1[0])
p.data1[1] = start_zero(data1[1])
p.data2[0] = start_zero(data2[0])
p.data2[1] = start_zero(data2[1])



# Display plot
p.overlay_plots()
p.show()
