#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Program: Track brightly-colored object to draw
# Author: Manuel Serna-Aguilera
# University of Arkansas, Fayetteville
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



#---------------------------------
# Print keyboard instructions
#---------------------------------
print("=============================")
print("Undergraduate Honors Thesis")
print("Hand Tracker and Character Classifier")
print("=============================\n")
# print("Instructions: ")
# TODO: include manual segmentation instructions here (toggle on and off)
print("    - Press 'q' to quit the program.")



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
        hsv_color = 0
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
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(True):
    ret, frame = cap.read() # get frame

    #---------------------------------
    # Track colored object for air-drawing
    # TODO: mark and track object for drawing
    #---------------------------------
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Track specified color (in hsv color space)
    hsv_lower, hsv_upper = get_hsv_color('p')
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask = mask)
    
    #---------------------------------
    # Find contours of brightly-colored drawing object
    #---------------------------------
    #edges = cv2.Canny(mask, 100, 200)
    #ret, thresh = cv2.threshold(edges, 127, 255, 0)
    
    #ret, thresh = cv2.threshold(mask, 127, 255, 0)
    #contours,hierarchy = cv2.findContours(thresh, 1, 2)
    #cnt = contours[0]
    
    #x,y,w,h = cv2.boundingRect(cnt)
    #frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
    
    
    
    #marker = mask # copy mask image to identify drawing "marker"
    
    #edges = cv2.Canny(mask, 100, 200)
    #cv2.imshow('proposed new image for contours', edges)
    #ret, thresh = cv2.threshold(edges, 127, 255, 0) # TODO: redo comment -> find contours in mask copy (since it's already a binary image)
    #cv2.imshow('thresh', thresh)
    
    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # get contours
    
    # Draw contours on original frame
    '''
    if len(contours) > 0:
        cnt = contours[0] # get numpy list of contours
        size = 10 # thickness of contour corners
        for i in range(len(cnt)):
            frame = cv2.drawContours(frame, cnt, i, (255,0,0), size)
    '''
    
    #---------------------------------
    # Display images
    #---------------------------------
    # Write out frame to video
    #out.write(frame)

    # Display frames, mask, and\or result
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    #cv2.imshow(win, res)
    
    #---------------------------------
    # Handle key events
    #---------------------------------
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture when done
#out.release() # when saving video
cap.release()
cv2.destroyAllWindows()

print("Done.")
