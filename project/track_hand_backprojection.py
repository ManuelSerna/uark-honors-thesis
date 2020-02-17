# Track hand using histogram backprojection

'''
Notes:
    - Video feed: 640 x 480 @ 30 fps
    - For good drawing space, have hand about 18 cm from camera lens

Tracking assumptions (for histogram approach to work):
    - Environment does not change significantly
'''



import cv2
import numpy as np



#=================================
# Setup
#=================================
roi_captured = False # mark as true if user is ready to acquire skin-color histogram
drawing = False # marked as true when user is ready to immediately begin drawing with their palm centroid

# Haar cascades can be found on my Mnajaro sys here: 
# /usr/lib/python3.8/site-packages/cv2/data/
face_cascade = cv2.CascadeClassifier('/usr/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/lib/python3.8/site-packages/cv2/data/haarcascade_eye.xml')



#=================================
# Display video capture info
# Input: video capture object
# Return: NA
#=================================
def get_cap_info(cap):
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('width: {}\nheight: {}\nfps: {}'.format(width, height, fps))



#=================================
# Exclude face by drawing a filled rectangle over it
# Input: frame with face visible
# Return: edited frame with face blacked out
#=================================
def exclude_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Draw rectangle over detected face
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), -1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
    
    return frame



#=================================
# Get roi to get color of user's skin (color we want to track)
# Input: current frame, and width andn height of the frame
# Return: original frame with roi marked; new image for roi
#=================================
def get_roi(frame):
    # Set offset (will control how big rectangle is)
    size = 60
    
    # Set points for rectangle roi (upper-left corner)
    # NOTE: flipping x and y corrects drawing
    x1 = 300
    y1 = 90
    x2 = x1 + size
    y2 = y1 + size
    
    # Draw rectangle onto frame
    cv2.rectangle(frame, (y1, x1), (y2, x2), (0, 0, 255), thickness=1)
    
    # Get region of interest to calc color histogram on
    roi = frame[x1+1:x2, y1+1:y2]
    return frame, roi



#=================================
# Get histogram for region of interest using backprojection
# Input: region of interest from captured from a frame and the current frame
# Return: threshold image; binary AND resulting image
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
# Program Start
#=================================
cap = cv2.VideoCapture(0) # get video capture object

while(True):
    ret, frame = cap.read() # get individual frame (an image)
    frame = exclude_face(frame) # detect and exclude face
    
    #-----------------------------
    # Get roi to extract skin color
    #-----------------------------
    if not roi_captured:
        frame, roi = get_roi(frame)
    
    #-----------------------------
    # Get threshold image from user's skin color
    #-----------------------------
    thresh, res = get_roi_hist(frame, roi)
    
    # Binarize image using skin color
    #ret, thresh = cv2.threshold(thresh, 200, 255, cv2.THRESH_BINARY)
    #ret, thresh = cv2.threshold(thresh, 127, 255, cv2.THRESH_TRUNC)
    
    '''
    TODO: before finding contours, do the following
    - remove noise
    - smooth threshold image
    - find canny edge detection
    '''
    # Remove noise
    #thresh = cv2.blur(thresh,(5,5)) # blurs image significantly
    #thresh = cv2.GaussianBlur(thresh,(5,5),0)
    #thresh = cv2.medianBlur(thresh, 5) # gives good output
    #thresh = cv2.bilateralFilter(thresh,9,75,75)
    
    '''
    low = 150
    high = 250
    thresh = cv2.Canny(thresh, low, high)
    '''
    
    # TODO: after performing the previous TODO ops, find contours from edge image
    '''
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]
    M = cv2.moments(cnt) # get image moments
    # Get centroid x and y
    #cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])
    hull = cv2.convexHull(cnt) # get convex hull
    size = 10
    for i in range(len(hull)):
        thresh = cv2.drawContours(thresh, hull, i, (255,255,0), size)
        frame = cv2.drawContours(frame, hull, i, (255,255,0), size)
    #'''
    
    #-----------------------------
    # Display
    #-----------------------------
    cv2.imshow('frame', frame)
    #cv2.imshow('roi', roi)
    cv2.imshow('thresh', thresh)
    #cv2.imshow('res', res)
    
    #-----------------------------
    # Keyboard events
    #-----------------------------
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        roi_captured = True
    elif k == 27: # esc key
        break

# Release video capture and close everything
cap.release()
cv2.destroyAllWindows()
