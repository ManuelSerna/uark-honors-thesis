#*********************************
# Module: Capture functions
#   - This module contains all the code needed to track the marker, draw, and save/return the data. The user simply calls the function capture.
# Author: Manuel Serna-Aguilera
#*********************************

'''
Some notes:

HSV value ranges for Opencv:
    - Hue: [0..179] <-these are the color wheel values
    - Saturation: [0..255]
    - Value: [0..255]
    
    Besides tracking the default hue val of 60, other values that can work are: 45, 80 (variations of green); 120 (blue)
'''

import cv2
import numpy as np

# Import custom modules
import file_io as f
import time_series as ts



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
# Overlay drawing on given frame
'''
Input:
    - frame: frame from video stream
    - drawing: recently updated letter drawing to be added to frame image
Return:
    - frame: updated picture with drawing added to it
'''
# Called by: update_drawing
#=================================
def overlay(frame, drawing):
    roi = frame # region of interest = entire frame
    gray_img = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
    ret, draw_mask = cv2.threshold(gray_img, 10, 255, cv2.THRESH_BINARY)
    draw_mask_inv = cv2.bitwise_not(draw_mask)
    
    img_bg = cv2.bitwise_and(roi, roi, mask = draw_mask_inv) # 0-value every pixel except for pixels overlapping with mask
    img_fg = cv2.bitwise_and(drawing, drawing, mask = draw_mask) # apply drawing to image
    
    # Add drawing to given frame
    frame = cv2.add(img_bg, img_fg)
    return frame



#=================================
# Draw on video frame
'''
Input:
    - center:  center coordinates (u, v) of drawing circle (from contours)
    - draw:    flag for drawing
    - drawing: image to hold air-written character
    - frame:   frame from video stream
    - r:       radius of circle to be put onto drawing
    - x:       x time series
    - y:       y time series

Output:
    - drawing: image to hold air-written character
    - frame:   frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
    - x:       updated x time series for drawn letter
    - y:       updated y time series for drawn letter
'''
# Called by: draw_contours
#=================================
def update_drawing(center, draw, drawing, frame, r, x, y):
    drawing_color = (255,255,255) # white
    if draw:
        r = 7 # radius/size of circle drawn
        
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
    - contours: contours/edges extracted from color threshold mask
    - draw:     flag for drawing
    - drawing:  image to hold air-written character
    - frame:    frame from video stream
    - x:        x time series
    - y:        y time series

Outputs:
    - drawing: modified image to hold air-written character
    - frame: frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
    - x:       updated x time series for drawn letter
    - y:       updated y time series for drawn letter
'''
# Called by: process_frame
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
    - frame:    frame from video stream
    - x:        x time series
    - y:        y time series
Outputs:
    - drawing: modified image to hold air-written character
    - frame: frame with updated drawing (other functions specifically deal with this, look at function "update_drawing")
    - x:       updated x time series for drawn letter
    - y:       updated y time series for drawn letter
'''
# Called by: capture function
#=================================
def process_frame(draw, drawing, frame, x, y):
    frame = cv2.flip(frame, 1) # flip image horizontally for easier drawing
    
    #---------------------------------
    # Track colored object for air-drawing
    #---------------------------------
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert bgr -> hsv
    hsv_lower, hsv_upper = get_hsv_color() # set color to threshold on
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper) # threshold hsv image based on hsv ranges
    
    #---------------------------------
    # Find contours of brightly-colored drawing object
    #---------------------------------
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing, frame, x, y = draw_contours(contours, draw, drawing, frame, x, y)
    
    #---------------------------------
    # Display images for user
    #---------------------------------
    cv2.imshow('Frame', frame)
    #cv2.imshow('Air-written Letter', drawing) # displays only the drawing itself
    #cv2.imshow('Mask', mask) # see what the color thresholding is keeping
    
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
#=================================
def reset(drawing, x, y):
    drawing = np.zeros((480, 640, 3), np.uint8)
    x = []
    y = []
    return drawing, x, y



#=================================
# Function for data capture, this is the only function any outside program has to call in order to capture data.
'''
Input:
    - letter: letter to be recorded (specified by user)
    - video: set true to save capture session
    - training: set true to record training data
    - testing: set true to record testing data
Return:
    - drawing: image that now holds air-drawn letter
    - x: populated time series for x coordinates
    - y: populated time series for y coordinates
'''
#=================================
def capture(letter = "", training = False, testing = False, video=False):
    # Drawing variables
    counter = 0 # keeps track of letter identifier
    draw = False
    drawing = np.zeros((480, 640, 3), np.uint8)
    
    # ROI variables
    center_x = 320
    center_y = 240
    offset = 150
    pt1 = (center_x-offset, center_y-offset)
    pt2 = (center_x+offset, center_y+offset)
    
    # Create empty time series
    x = []
    y = []
    
    # Begin video capture
    cap = cv2.VideoCapture(0)
    
    if video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # video codec
        video_file = 'recording-{}.avi'.format(letter)
        out = cv2.VideoWriter(video_file, fourcc, 20.0, (640,480))
    
    print("  Marker Tracker. Press: 'esc' to quit; 'd' to start/stop drawing.")
    
    while(True):
        # Get current frame to extract info and modify it
        ret, frame = cap.read()
        
        # Draw roi where we would ideally want to draw the letter
        cv2.rectangle(frame, pt1, pt2, (0,0,255), thickness=1)
        
        # Process frame
        drawing, frame, x, y = process_frame(draw, drawing, frame, x, y)
        
        # Save frame in video
        if video:
            out.write(frame)
        
        # Keyboard events
        k = cv2.waitKey(1) & 0xFF
        
        if k == ord('d'):
            if not draw:
                draw = True
                print(" Start drawing.")
            else:
                draw = False
                print(" Capture complete.")
                
                # Consider only the region of interest
                roi = drawing[
                    center_y-offset+1:center_y+offset,
                    center_x-offset:center_x+offset-1
                ]
                
                if training:
                    counter += 1
                    f.write_img(roi, letter, counter) # save only region-of-interest
                    f.write_json(name=letter, num=counter, x=x, y=y, og=True) # unmodified time series
                    f.write_json(letter, counter, ts.apply_all(x), ts.apply_all(y)) # modified time series
                    
                    drawing, x, y = reset(drawing, x, y)
                elif testing:
                    counter += 1
                    
                    # NOTE: writing to 'testing' directory
                    f.write_img(img=roi, name=letter, num=counter, training=False) # save only region-of-interest
                    f.write_json(name=letter, num=counter, x=x, y=y, og=True, training=False) # unmodified time series
                    f.write_json(name=letter, num=counter, x=ts.apply_all(x), y=ts.apply_all(y), training=False) # modified time series
                    
                    drawing, x, y = reset(drawing, x, y)
                else:
                    break
        elif k == 27:
            print(" Exiting capture procedure.")
            break # esc key
    
    # Release capture when done
    if video:
        out.release()
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Return drawing data if not recording or not collecting data
    if training or testing or video:
        return
    else:
        return roi, x, y
