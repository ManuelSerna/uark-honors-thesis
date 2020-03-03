#*********************************
# Classifier: Time series of letters
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import numpy as np
import math
import sys

import capture as cp
import file_io as f
import plot

infty = 999999
letters = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']

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
# Increase length of time series by estimating distance between two consecutive points
'''
Input:
    - t: some time series
    - new_length: desired length for new time series
Return:
    - s: newly-sized time series
'''
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
# Reduce length of time series by estimating distance between two consecutive points
'''
Input:
    - t: some time series
    - new_length: desired length for new time series
Return:
    - s: newly-sized time series
'''
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
    - new_length: shrink or grow list to be this new length
Output:
    - t: modified time series of length 'new_length'
'''
#=================================
def set_length(t, new_length):
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
# Dynamic Time Warping: find minimum edit distance
'''
Input:
    - t1 and t2: two time series to compare
Return:
    - result[n-1][m-1]: minimum edit distance--a measure of similarity (the lower=the more similar the two time series)
'''
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
# Function for data capture
'''
Return:
    - drawing: image that now holds air-drawn letter
    - x: populated time series for x coordinates
    - y: populated time series for y coordinates
'''
#=================================
def capture():
    drawing = np.zeros((480, 640, 3), np.uint8)
    x = []
    y = []
    
    cp.prompt()
    draw = False
    cap = cv2.VideoCapture(0)
    
    while(True):
        # Get current frame to extract info and modify it
        ret, frame = cap.read()
        drawing, frame, x, y = cp.process_frame(draw, drawing, frame, x, y)
        
        # Keyboard events
        k = cv2.waitKey(1) & 0xFF
        
        if k == ord('d'):
            if not draw:
                draw = True
                print(" Start drawing.")
            else:
                draw = False
                cap.release()
                cv2.destroyAllWindows()
                print(" Capture complete.")
                break
    return drawing, x, y



#================================
# Function to contain time series analysis
'''
Input:
    - letter: letter to query
    - num: number identifier for query
Return:
    - calculated minimum edit distance for x time series
    - calculated minimum edit distance for y time series
'''
#================================
def compare_letter(letter, num):
    global captured_x, captured_y
    
    query = f.get_file(letter, num)
    query_x = query[0]
    query_y = query[1]

    #---------------------------------
    # Operations on time series
    #---------------------------------
    # 1) 
    # Translate time series to start at zero
    captured_x = start_zero(captured_x)
    captured_y = start_zero(captured_y)
    query_x = start_zero(query_x)
    query_y = start_zero(query_y)

    # 2)
    # Scale time series to some common output range
    captured_x = scale(captured_x)
    captured_y = scale(captured_y)
    query_x = scale(query_x)
    query_y = scale(query_y)

    # 3)
    # Force x and y time series to be the same length
    new_length = 175
    captured_x = set_length(captured_x, new_length)
    captured_y = set_length(captured_y, new_length)
    query_x = set_length(query_x, new_length)
    query_y = set_length(query_y, new_length)
    
    #plot.overlay_plots(x1=captured_x, y1=captured_y, x2=query_x, y2=query_y)
    
    #---------------------------------
    # Calculate minimum edit distance for x and y time series
    #---------------------------------
    distancex = dtw(captured_x, query_x)
    distancey = dtw(captured_y, query_y)
    threshold = 450 # set threshold for maximum similarity
    
    return distancex, distancey



#=================================
# Start
#=================================
# Capture air-drawn letter
drawing, captured_x, captured_y = capture()

# Store minimum distances for x and y
minx = infty
miny = infty
match = '' # closest match

for letter in letters:
    for num in range(1, 10):
        #print('EVALUATING {}{}'.format(letter, num))
        dx, dy = compare_letter(letter, num)
        if minx > dx and miny > dy:
            minx = dx
            miny = dy
            match = letter
            #print('\tbest match: {}{}'.format(letter, num))

print('  DTW best match: {}'.format(match))
