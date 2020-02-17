#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Program: Track brightly-colored object to draw
# Author: Manuel Serna-Aguilera
# University of Arkansas, Fayetteville
# Spring, 2020
#*********************************

'''
Some notes:

HSV value ranges for opencv:
    - Hue: [0..179]
    - Saturation: [0..255]
    - Value: [0..255]
'''



import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt



#---------------------------------
# Setup
#---------------------------------
win = 'air-writing' # window name
color = 'b' # default color to track is red
draw = False # flag to start/stop drawing letters
blank_drawing = np.zeros((480, 640, 3), np.uint8) # blank image to reset drawing image
drawing = np.zeros((480, 640, 3), np.uint8) # drawing image
drawing_color = (0, 0, 255) # draw characters in this color

# TODO: add counter to enumerate output images (and video?)


#---------------------------------
# Print keyboard instructions
#---------------------------------
print("=============================")
print("Undergraduate Honors Thesis")
print("Hand Tracker and Character Classifier")
print("=============================")
print()
print("    - Press 'esc' to quit the program.")
print("    - To start drawing, press 'd', press 'd' again to stop.")
print("=============================")
print()



#=================================
# Return upper and lower thresholds for hsv color tracking
#=================================
def get_hsv_color(color):
    # Initialize hue
    hsv_color = 0
    
    # Saturation
    lower_sat = 50
    upper_sat = 255
    
    # Value
    lower_val = 50
    upper_val = 255
    
    if color == 'r':
        hsv_color = 0 # red too similar somtimes to skin color
    elif color == 'g':
        hsv_color = 80
    elif color == 'b':
        hsv_color = 120
    elif color == 'p': # pink hsv = 163
        hsv_color = 155
    
    hsv_lower = np.array([hsv_color-10, lower_sat, lower_val])
    hsv_upper = np.array([hsv_color+10, upper_sat, upper_val])
    
    return hsv_lower, hsv_upper
    


#=================================
# Capture video from camera
#=================================
cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID') # video codec
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while(True):
    ret, frame = cap.read() # get frame

    #---------------------------------
    # Track colored object for air-drawing
    # TODO: mark and track object for drawing
    #---------------------------------
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Track specified color (in hsv color space)
    hsv_lower, hsv_upper = get_hsv_color(color)
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame, frame, mask = mask)
    
    #---------------------------------
    # Find contours of brightly-colored drawing object
    #---------------------------------
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours
    if len(contours) > 0:
        cnt = contours[0] # get numpy list of contours
        size = 5 # thickness of contour corners
        
        for i in range(len(cnt)):
            frame = cv2.drawContours(frame, cnt, i, (0,255,0), size)
            #mask = cv2.drawContours(mask, cnt, i, (0,255,0), size)
        
        # Draw minimum enclosing circle
        (x, y), r = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        r = int(r)
        cv2.circle(frame, center, r, (0,255,0), 2)
        size = 4 # keep the size of the drawing circles the same regardless of contours
        
        # If drawing flag is enabled, draw with center of circle
        if draw:
            cv2.circle(drawing, center, size, drawing_color, -1)
            
            # Overlay updated drawing over frame
            roi = frame # copy frame as it is the entire region of interest
            drawing_gray = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
            ret, draw_mask = cv2.threshold(drawing_gray, 10, 255, cv2.THRESH_BINARY)
            draw_mask_inv = cv2.bitwise_not(draw_mask)
            
            frame_bg = cv2.bitwise_and(roi, roi, mask = draw_mask_inv)
            drawing_fg = cv2.bitwise_and(drawing, drawing, mask = draw_mask)
            
            dst = cv2.add(frame_bg, drawing_fg)
            frame = dst
    
    
    #---------------------------------
    # Display images
    #---------------------------------
    # Write out frame to video
    #out.write(frame)
    
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('drawing', drawing)
    
    #-----------------------------
    # Keyboard events
    #-----------------------------
    k = cv2.waitKey(1) & 0xFF
    if k == ord('d'):
        if not draw:
            draw = True
            print("  Drawing START.")
        else:
            draw = False
            cv2.imwrite('drawing.jpg', frame)
            #drawing = blank_drawing # reset drawing image
            drawing = np.zeros((480, 640, 3), np.uint8)
            print("  Drawing STOP.")
    elif k == ord('v'):
        print('Taking video (not actually yet)')
        # TODO: set flag to trigger video capture (?)
    elif k == 27: # esc key
        break

# Release capture when done
#out.release() # when saving video
cap.release()
cv2.destroyAllWindows()

print("Done.")
