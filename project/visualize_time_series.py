# Plot two letters side-by-side

import sys
import plot

# Specify which letter to plot from cmd line
letter1 = (sys.argv[1]).upper()
num1 = sys.argv[2]

# Check if 3rd and 4th args are empty
letter2 = ""
num2 = ""
try:
    letter2 = (sys.argv[3]).upper()
    num2 = sys.argv[4]
except IndexError:
    print("  No second letter provided.")

# Create plot object
p = plot.plot(letter1, num1, letter2, num2)
p.overlay_plots()
p.show()
