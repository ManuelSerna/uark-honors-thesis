#*********************************
# Module: Capture functions
'''
    - The user calls "process_frame" to update the letter drawing and frame.
    - This module is meant to be used in several places where capturing is required.
    Like for data recording, drawing practice, and classification scenarios.
'''
# Author: Manuel Serna-Aguilera
#*********************************

'''
Some notes:

HSV value ranges for opencv:
    - Hue: [0..179] <-these are the color wheel values
    - Saturation: [0..255]
    - Value: [0..255]
    
    Besides tracking the default hue val of 60, other values that can work are: 45, 80 (variations of green); 120 (blue)
'''

import cv2
import numpy as np



#=================================
# Print prompt
# Called by: Outside of module before capturing.
#=================================
def prompt():
    print("=============================")
    print("  Color Tracker and Character Classifier")
    print("-----------------------------")
    print("    - Press 'esc' to quit the program.")
    print("    - To start drawing, press 'd', press 'd' again to stop.")
    print("=============================")



#=================================
# Set thresholds to filter an hsv image on
# Return: lower and upper thresholds
# Called by: process_frame
#=================================
def get_hsv_color():
    # Initialize hue
    hsv_color = 60 # default color-to-track is GREEN
    
    # Saturation ranges
    lower_sat = 100
    upper_sat = 255
    
    # Value ranges
    lower_val = 110
    upper_val = 255
    
    hsv_lower = np.array([hsv_color-10, lower_sat, lower_val])
    hsv_upper = np.array([hsv_color+10, upper_sat, upper_val])
    
    return hsv_lower, hsv_upper



#=================================
# Overlay drawing on given image
# Input: raw video frame
# Return: camera frame with updated drawing added
#=================================
def overlay(img, drawing):
    roi = img # region of interest = entire given image
    gray_img = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
    ret, draw_mask = cv2.threshold(gray_img, 10, 255, cv2.THRESH_BINARY)
    draw_mask_inv = cv2.bitwise_not(draw_mask)
    
    img_bg = cv2.bitwise_and(roi, roi, mask = draw_mask_inv) # 0-value every pixel except for pixels overlapping with mask
    img_fg = cv2.bitwise_and(drawing, drawing, mask = draw_mask) # apply drawing to image
    
    # Add drawing to given image
    img = cv2.add(img_bg, img_fg)
    return img



#=================================
# Draw on video frame
'''
Inputs:
    - center:  center coordinates (u, v) of drawing circle (from contours)
    - draw:    flag for drawing
    - drawing: image to hold air-written character
    - frame:   raw video frame
    - x:       x time series
    - y:       y time series

Outputs:
    - drawing: image to hold air-written character
    - frame:   frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
    - x:       updated x time series for drawn letter
    - y:       updated y time series for drawn letter
'''
# Called by: draw_contours.
#=================================
def update_drawing(center, draw, drawing, frame, r, x, y):
    drawing_color = (0, 0, 255)
    if draw:
        r = 5 # radius/size of circle drawn
        
        # Draw circle and add center=(x,y) to corresponding time series
        if r > 0:
            cv2.circle(drawing, center, r, drawing_color, -1)            
            x.append(center[0])
            y.append(center[1])
        
        # Overlay updated drawing over frame for user
        frame = overlay(frame, drawing)
    
    return drawing, frame, x, y



#=================================
# Based on hsv image contours, draw circles on frame (if the user is drawing)
'''
Inputs:
    - contours: contours/edges extraced from color threshold mask
    - draw:     flag for drawing
    - drawing:  image to hold air-written character
    - frame:    raw video frame
    - x:        x time series
    - y:        y time series

Outputs:
    - drawing: modified image to hold air-written character
    - frame: frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
    - x:       updated x time series for drawn letter
    - y:       updated y time series for drawn letter
'''
# Called by: process_frame.
#=================================
def draw_contours(contours, draw, drawing, frame, x, y):
    if len(contours) > 0:
        cnt = contours[0] # get numpy list of contours
        contour_size = 5 # thickness of contour corners
        
        for i in range(len(cnt)):
            frame = cv2.drawContours(frame, cnt, i, (255,255,0), contour_size)
            #mask = cv2.drawContours(mask, cnt, i, (255,255,0), contour_size)
        
        # Get params for min. enclosing circle with center (u, v), and draw
        (u, v), r = cv2.minEnclosingCircle(cnt)
        center = (int(u), int(v)) # center for enclosing circle
        r = int(r) # radius of drawing circle 
        cv2.circle(frame, center, r, (0,255,0), 2)
        
        # If drawing flag is enabled, draw with respect to center of circle and overlay it on top of the current frame
        drawing, frame, x, y = update_drawing(center, draw, drawing, frame, r, x, y)
    return drawing, frame, x, y



#=================================
'''
Identify marker in given frame and allow user to draw.
    - First, identify a color in a specified range (idealy this should be a circular object). Second, threshold the image in hsv given hsv ranges to get the mask. Third, with the binary mask, find the edges (recall it should be a circle that we extract the contours from). Fourth and finally, draw circles given the information based on the contours.

Inputs:
    - draw:     flag for drawing
    - drawing:  image to hold air-written character
    - frame:    raw video frame
    - x:        x time series
    - y:        y time series
Outputs:
    - drawing: modified image to hold air-written character
    - frame: frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
    - x:       updated x time series for drawn letter
    - y:       updated y time series for drawn letter
'''
# Called by: outside of module by other programs.
#=================================
def process_frame(draw, drawing, frame, x, y):
    frame = cv2.flip(frame, 1) # flip image horizontally for easier drawing
    
    #---------------------------------
    # Track colored object for air-drawing
    #---------------------------------
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert bgr -> hsv
    hsv_lower, hsv_upper = get_hsv_color() # set color to threshold on
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper) # treshold hsv image based on hsv ranges
    
    #---------------------------------
    # Find contours of brightly-colored drawing object
    #---------------------------------
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing, frame, x, y = draw_contours(contours, draw, drawing, frame, x, y)
    
    #---------------------------------
    # Display images for user
    #---------------------------------
    cv2.imshow('Frame', frame)
    cv2.imshow('Air-written Letter', drawing)
    #cv2.imshow('mask', mask) # see what the color thresholding is keeping
    
    return drawing, frame, x, y



#=================================
# Reset image and time series
'''
Inputs:
    - drawing:  image that holds drawing that is no longer needed
    - x:        x time series
    - y:        y time series
Outputs:
    - drawing: blacked-out drawing
    - x:       empty list
    - y:       empty list
'''
# Called by: Outside of module by other programs.
#=================================
def reset(drawing, x, y):
    drawing = np.zeros((480, 640, 3), np.uint8)
    x = []
    y = []
    return drawing, x, y
