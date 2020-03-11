#*********************************
# Program: Classify letter
#   - Use the functions of my custom capture module to get the air-written letter from the user and use several classifiers to identify what was written.
# Author: Manuel Serna-Aguilera
#*********************************

import capture as cp
import dtw
import file_io as f
import time_series as ts



#=================================
# Start
#=================================
infty = 999999
letters = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']

# DTW variables
minx = infty # min edit dist for x
miny = infty # min edit dist for y
dtw_match = ''
threshold = 450

# TODO: knn variables

# Capture air-drawn letter and apply time series modifications
drawing, captured_x, captured_y = cp.capture()
captured_x = ts.apply_all(captured_x)
captured_y = ts.apply_all(captured_y)

# Loop through only one sample per category
for letter in letters:
    # Query data for current labeled letter
    query = f.get_file(letter, 1)
    query_x = ts.apply_all(query[0])
    query_y = ts.apply_all(query[1])
    
    #dx, dy = compare_letter(letter, 1)
    # Calculate minimum edit distances for x and y time series
    dx = dtw.dtw(captured_x, query_x)
    dy = dtw.dtw(captured_y, query_y)
    
    if minx > dx and miny > dy:
        minx = dx
        miny = dy
        dtw_match = letter

# Print matches for classifiers
print("  Best Matches.")
print("  DTW: {}".format(dtw_match))
# TODO: print best matches from the other classifiers here
