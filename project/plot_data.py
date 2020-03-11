#*********************************
# Program: Display time series
#   - Use the plot module to plot two time series
# Author: Manuel Serna-Aguilera
#*********************************

import sys
import plot

# Get char data from command line
letter1 = (sys.argv[1]).upper()
num1 = sys.argv[2]
letter2 = (sys.argv[3]).upper()
num2 = sys.argv[4]

plot.overlay_plots(letter1, num1, letter2, num2)
