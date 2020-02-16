# Track hand using histogram backprojection

'''
Notes:
    - Video feed: 640 x 480 @ 30 fps
    - For good drawing space, have hand about 18 cm from camera lens

Tracking assumptions (for histogram approach to work):
    - Lighting does not change
    - Environment does not change significantly
'''

import cv2
import numpy as np


#=================================
# Get roi to get color of user's skin (color we want to track)
# Input: current frame, and width andn height of the frame
# Return: original frame with roi marked; new image for roi
#=================================
def get_roi(frame):
    # Set offset (will control how big rectangle is)
    size = 90
    
    # Set points for rectangle roi (upper-left corner)
    x1 = 50
    y1 = 50
    x2 = x1 + size
    y2 = y1 + size
    
    # Draw rectangle onto frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), thickness=1)
    
    roi = frame[x1+1:x2, y1+1:y2]
    return frame, roi



#=================================
# Get histogram for region of interest
# Input: region of interest from captured from a frame and the current frame
# Return: TODO
#=================================
def get_roi_hist(frame, roi):
    # Get hsv color space images for frame and roi
    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    hsvf = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    # Calculating object histogram
    roihist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    
    # Normalize histogram and apply backprojection
    cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)
    dst = cv2.calcBackProject([hsvf], [0,1], roihist, [0,180,0,256], 1)
    
    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    cv2.filter2D(dst, -1, disc, dst)
    
    # Threshold and binary AND
    ret, thresh = cv2.threshold(dst, 50, 255, 0)
    thresh = cv2.merge((thresh, thresh, thresh))
    res = cv2.bitwise_and(frame, thresh)
    
    return thresh, res



#=================================
# Start
#=================================
# Setup
roi_captured = False

# Get video capture object
cap = cv2.VideoCapture(0)

while(True):
    # Get individual frame (an image)
    ret, frame = cap.read()
    
    # Display data
    #w = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
    #h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #fps = cap.get(cv2.CAP_PROP_FPS)
    #print('w: {}\nh: {}\nfps: {}'.format(width, height, fps))
    
    # Get roi to extract skin color
    if not roi_captured:
        frame, roi = get_roi(frame)
        # TODO: continue to get histogram until user presses 's'
        thresh, res = get_roi_hist(frame, roi)
    #else:
    #    print('now we dont include roi capture')
    #    print(roi)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('roi', roi)
    #cv2.imshow('thresh', thresh)
    cv2.imshow('res', res)

    # Keyboard events
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord('s'):
        roi_captured = True
    elif k == 27: # esc key
        break

# Release video capture and close everything
cap.release()
cv2.destroyAllWindows()
