#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Program: Track brightly-colored object to draw characters, the drawing and the time series for the x and y coordinates will be saved in a sub-directory.
# Author: Manuel Serna-Aguilera
# University of Arkansas, Fayetteville
# Spring 2020
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
import json
import matplotlib
import numpy as np
import os
import sys

from matplotlib import pyplot as plt



#---------------------------------
# Setup ("global" variables)
#---------------------------------
counter = 0 #TODO: automate assignment of this var
letter = (sys.argv[1]).upper() # letter to be drawn (taken in from cmd line)

# Drawing-related
draw = False # flag to start/stop drawing letters
drawing = np.zeros((480, 640, 3), np.uint8) # drawing image
drawing_color = (0, 0, 255) # draw characters in this color

# Time series recorded here for x and y coords
x = []
y = []

# Other variables
video = False # flag to enable video capture
win = 'air-writing' # window name

# TODO?: add counter to enumerate output images (and video?)


#---------------------------------
# Print user prompt
#---------------------------------
print("=============================")
print("Undergraduate Honors Thesis")
print("Color Tracker and Character Classifier")
print("-----------------------------")
print("    - Press 'esc' to quit the program.")
print("    - To start drawing, press 'd', press 'd' again to stop.")
print("=============================")



#=================================
# Set thresholds to filter an hsv image on
# Return: lower and upper thresholds
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
def overlay(img):
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
# Input: raw video frame, center of drawing circle, and its radius/size
# Return: unedited frame if user is not drawing; if the drawing flag is True, then return frame with drawing overlayed (look at function "overlay")
#=================================
def update_drawing(frame, center, r):
    if draw:
        r = 5 # radius/size of circle drawn
        
        # Draw circle and add center=(x,y) to corresponding time series
        if r > 0:
            cv2.circle(drawing, center, r, drawing_color, -1)            
            x.append(center[0])
            y.append(center[1])
        
        # Overlay updated drawing over frame
        frame = overlay(frame)
    
    return frame



#=================================
# Based on hsv image contours, draw circles on frame (if the user is drawing)
# Input: raw video frame, contours based on the threshold mask (calculated prior to this function call)
# Return: frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
#=================================
def draw_contours(frame, contours):
    if len(contours) > 0:
        cnt = contours[0] # get numpy list of contours
        contour_size = 5 # thickness of contour corners
        
        for i in range(len(cnt)):
            frame = cv2.drawContours(frame, cnt, i, (255,255,0), contour_size)
            #mask = cv2.drawContours(mask, cnt, i, (255,255,0), contour_size)
        
        # Get params for min. enclosing circle, and draw
        (x, y), r = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y)) # center for enclosing circle
        r = int(r) # radius of drawing circle 
        cv2.circle(frame, center, r, (0,255,0), 2)
        
        # If drawing flag is enabled, draw with respect to center of circle and overlay it on top of the current frame
        frame = update_drawing(frame, center, r)
    return frame



#=================================
# Save drawing and time series to appropriate sub-directories
# Input: video frame with drawing, x and y time series lists
# Return: emptied times series lists (to record new drawing)
#=================================
# TODO: import os and write time series and PNGs to sub-directories
def write_data(img, x, y):
    global counter
    counter += 1
    
    data = {}
    data['x'] = x
    data['y'] = y
    
    # Get sub-directory
    here = os.path.dirname(os.path.realpath(__file__))
    sub_dir = 'letters/' + letter
    
    # If sub-directory does not exist, make directory
    if not os.path.isdir(os.path.join(here, sub_dir)):
        os.mkdir(os.path.join(here, sub_dir))
    
    # Time series file path
    out_data = "{}{}.json".format(letter, counter)
    data_path = os.path.join(here, sub_dir, out_data)
    
    # Image path
    out_img = "{}{}.png".format(letter, counter)
    img_path = os.path.join(here, sub_dir, out_img)    
    
    # Write files to sub-directory
    try:
        with open(data_path, 'w') as file:
            file.write(json.dumps(data, indent=4)) # write data
        cv2.imwrite(img_path, img) # write image
    except IOError:
        print("Wrong path provided, could not write files!")
    
    # Reset and return x and y time series lists
    x = []
    y = []
    return x, y



#=================================
# Start capturing video and track object to draw
#=================================
cap = cv2.VideoCapture(0)

if video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # video codec
    out = cv2.VideoWriter('output3.avi', fourcc, 20.0, (640,480))

while(True):
    ret, frame = cap.read() # get frame
    frame = cv2.flip(frame, 1) # flip an image

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
    frame = draw_contours(frame, contours)
    
    #---------------------------------
    # Display images
    #---------------------------------
    if video:
        out.write(frame) # write frame out to video
    cv2.imshow('frame', frame)
    cv2.imshow('drawing only', drawing)
    #cv2.imshow('mask', mask) # see what the color thresholding is keeping
    
    #-----------------------------
    # Keyboard events
    #-----------------------------
    k = cv2.waitKey(1) & 0xFF
    if k == ord('d'):
        if not draw:
            draw = True
            print(" Start drawing.")
        else:
            draw = False
            print(" End drawing. Saving data.")
            x, y = write_data(drawing, x, y) # save drawing and coords to files
            drawing = np.zeros((480, 640, 3), np.uint8) # reset drawing image
    elif k == ord('v'):
        print(' Taking video.')
        # TODO: set flag to trigger video capture (?), update toggle flag
        #video = True
    elif k == 27: # esc key
        break

# Release capture when done
if video:
    out.release()

cap.release()
cv2.destroyAllWindows()
