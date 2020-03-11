#*********************************
# Program: Record data
#   - Use the capture module to specifically record data
# Author: Manuel Serna-Aguilera
#*********************************

import sys

import capture as cp

# Get char from command line
letter = (sys.argv[1]).upper()

# Capture data, turn recording flag on
cp.capture(letter=letter, recording=True, video=False)
