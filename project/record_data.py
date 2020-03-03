#*********************************
# Program: Record data
#   - Use the functions of my custom capture module to get the air-written letter from the user and store the data (images and time series) in sub-directories.
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import numpy as np
import sys

import capture as cp
import file_io as f

#---------------------------------
# Setup
#---------------------------------
counter = 0 # keeps track of number identifiers for letters drawn
draw = False # flag to start/stop drawing letters
drawing = np.zeros((480, 640, 3), np.uint8) # drawing image
letter = (sys.argv[1]).upper() # letter to be drawn (from cmd line)
video = False # flag to enable video capture
x = [] # x time series
y = [] # t time series



#=================================
# Start capture process
#=================================
cp.prompt() # display instructions

cap = cv2.VideoCapture(0)

if video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # video codec
    out = cv2.VideoWriter('output3.avi', fourcc, 20.0, (640,480))

while(True):
    # Get current frame to extract info and modify it
    ret, frame = cap.read()
    drawing, frame, x, y = cp.process_frame(draw, drawing, frame, x, y)
    
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
            counter += 1
            f.write_img(drawing, letter, counter)
            f.write_json(letter, counter, x, y)
            drawing, x, y = cp.reset(drawing, x, y)
            print(" End drawing for {}{}. Saved data.".format(letter, counter))
    elif k == 27: # esc key
        break

# Release capture when done
if video:
    out.release()

cap.release()
cv2.destroyAllWindows()
