# Purpose: test the extraction of a subframe within a frame from video

'''
Notes:
    - Video feed: 640 x 480 @ 30 fps
'''

import cv2
import numpy as np


#=================================
# Get roi to get color of user's skin (color we want to track)
# Input: current frame, and width andn height of the frame
# Return: original frame with roi marked; new image for roi
#=================================
def get_roi(frame, w, h):
    # Get center of frame
    cw = w/2
    ch = h/2
    
    # Set offset (will control how big rectangle is)
    s = 50
    
    # Set points for rectangle
    x1 = int(cw - s)
    y1 = int(cw - s)
    x2 = int(cw + s)
    y2 = int(cw + s)
    
    # Draw rectangle onto frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=1)
    
    # TODO: if I can return the roi as some array, this is the place
    return frame



#=================================
# Start
#=================================
# Get video capture object
cap = cv2.VideoCapture(0)

while(True):
    # Get individual frame (an image)
    ret, frame = cap.read()
    
    # Display data
    
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )
    #fps = cap.get(cv2.CAP_PROP_FPS)
    #print('w: {}\nh: {}\nfps: {}'.format(width, height, fps))
    
    # Get roi to extract skin color
    # For simplicity, use the center
    frame = get_roi(frame, w, h)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Keyboard events
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord('i'): # press i
        print('yo') # start some process at this key event
    elif k == 27: # esc key
        break

# Release video capture and close everything
cap.release()
cv2.destroyAllWindows()
