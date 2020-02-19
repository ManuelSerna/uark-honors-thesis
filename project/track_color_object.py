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
    - Hue: [0..179] <-these are the color wheel values
    - Saturation: [0..255]
    - Value: [0..255]
'''



import cv2
import json
import matplotlib
import numpy as np

from matplotlib import pyplot as plt



#---------------------------------
# For generating labeled data
#---------------------------------
counter = 0
letter = 'B' # character being drawn (add 'a' to end to denote accent)



#---------------------------------
# Setup ("global" variables)
#---------------------------------
color = 'g' # default color to track is red

draw = False # flag to start/stop drawing letters
drawing = np.zeros((480, 640, 3), np.uint8) # drawing image
drawing_color = (0, 0, 255) # draw characters in this color

video = False # flag to enable video capture

win = 'air-writing' # window name

# Time series recorded here for x and y coords
x = []
y = []

# TODO: add counter to enumerate output images (and video?)


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
print()



#=================================
# Return upper and lower thresholds for hsv color tracking
#=================================
def get_hsv_color(color):
    # Initialize hue
    hsv_color = 0
    
    # Saturation
    lower_sat = 100
    upper_sat = 255
    
    # Value
    lower_val = 110
    upper_val = 255
    
    # Choose h value based on arg given
    if color == 'r':
        hsv_color = 0 # red sometimes too similar to skin color and my CS jacket :-(
    elif color == 'g':
        hsv_color = 60 # this value works better against other potential common greens in the background
        #hsv_color = 45
        #hsv_color = 80 # works good if I have a neon-like green marker with me
    elif color == 'b':
        hsv_color = 120
    
    hsv_lower = np.array([hsv_color-10, lower_sat, lower_val])
    hsv_upper = np.array([hsv_color+10, upper_sat, upper_val])
    
    return hsv_lower, hsv_upper



#=================================
# Overlay drawing on given image
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
# Draw on video frame and picture with only the drawing
#=================================
def draw_char(frame, center, r):
    if draw:
        r = 5 # radius/size of circle drawn
        
        # Draw circles for character with constant size
        if r > 0:
            cv2.circle(drawing, center, r, drawing_color, -1)
            
            # Update time series lists
            x.append(center[0])
            y.append(center[1])
        
        # Overlay updated drawing over frame
        frame = overlay(frame)
    
    return frame



#=================================
# Get contours, draw them, and use them to draw the characters
#=================================
def draw_contours(frame):
    if len(contours) > 0:
        cnt = contours[0] # get numpy list of contours
        contour_size = 5 # thickness of contour corners
        
        for i in range(len(cnt)):
            frame = cv2.drawContours(frame, cnt, i, (0,255,0), contour_size)
            #mask = cv2.drawContours(mask, cnt, i, (0,255,0), contour_size)
        
        # Get params for min. enclosing circle, and draw
        (x, y), r = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y)) # center for enclosing circle
        r = int(r) # radius of drawing circle 
        cv2.circle(frame, center, r, (0,255,0), 2)
        
        # If drawing flag is enabled, draw with respect to center of circle and overlay it on top of the current frame
        frame = draw_char(frame, center, r)
    return frame



#=================================
# Save drawing as an image and write time series to file
#=================================
def write(img, x, y):
    global counter
    counter += 1
    
    out_img = "{}{}.png".format(letter, counter)
    cv2.imwrite(out_img, img) # save drawing as png
    
    # Write time series for x and y coords to JSON    
    data = {}
    data['x'] = x
    data['y'] = y
    
    out_data = "{}{}.json".format(letter, counter)
    with open(out_data, 'w') as file:
        file.write(json.dumps(data, indent=4))
    
    # Reset and return x and y time series lists
    x = []
    y = []
    return x, y



#=================================
# Capture video from camera
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
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # bgr -> hsv
    hsv_lower, hsv_upper = get_hsv_color(color) # set color to threshold on
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper) # treshold hsv image based on color
    
    #---------------------------------
    # Find contours of brightly-colored drawing object
    #---------------------------------
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    frame = draw_contours(frame)
    
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
            print(" started drawing")
        else:
            draw = False
            print(" end drawing")
            x, y = write(drawing, x, y) # save drawing and coords to files
            drawing = np.zeros((480, 640, 3), np.uint8) # reset drawing image
    elif k == ord('v'):
        print('Taking video.')
        # TODO: set flag to trigger video capture (?), update toggle flag
        #video = True
    elif k == 27: # esc key
        break

# Release capture when done
if video:
    out.release()
cap.release()
cv2.destroyAllWindows()

print("Done.")
