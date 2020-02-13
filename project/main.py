#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Main Program
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
# Capture video from camera
#=================================
cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID') # video codec
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #---------------------------------
    # Track colored object for air-drawing
    # NOTE: detect green-colored object for now
    # TODO: mark and track object for drawing
    #---------------------------------
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lower = np.array([70, 50, 50])
    hsv_upper = np.array([90, 255, 250])
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask = mask)
    
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    
    # Write out frame to video
    #out.write(frame)

    # Display the resulting frame
    cv2.imshow(win, res)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture when done
#out.release() # when saving video
cap.release()
cv2.destroyAllWindows()

print("Done.")
