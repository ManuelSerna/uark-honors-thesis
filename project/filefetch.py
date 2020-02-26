#*********************************
# Module: Separate getter files for time series (in JSON) and PNG images
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import json
import numpy as np
import os

#=================================
# Get directory info
'''
Input:
    - subpath: optional string for sub-directory, otherwise empty
Return:
    - current path (same as file) as a string
    - sub-directory if there is one
'''
#=================================
def get_dir(subpath=''):
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = 'letters/' + subpath
    
    return here, subdir



#=================================
# Get image
'''
Inputs:
    - name: name of letter to fetch info of
    - num: "id" for specific letter
    - color: set image to a certain color (white is default)
Return: image (3D cv2 array)

NOTE: Assume letters are drawn in BGR where red = 255, blue and green are 0
'''
#=================================
def get_img(name, num, color='w'):
    # Get current dir
    here, subdir = get_dir(name)
    
    # Fetch image
    in_img = "{}{}.png".format(name, num)
    img_path = os.path.join(here, subdir, in_img)
    img = cv2.imread(img_path)
    
    # Correct BGR->RGB due to OpenCV, switch R and B
    if color == 'w':
        img = img[:, :, 2] # populate all color channels
    elif color == 'r':
        full = img[:, :, 2] # get only populated channel (blue)
        img[:, :, 0] = full # fill red channel
        img[:, :, 2] = np.zeros((480, 640), np.uint8) # zero blue chanel
    elif color == 'c':
        full = img[:, :, 2] # get only populated channel (blue)
        img[:, :, 1] = full # populate green to get cyan
    else: # error check: color white
        img = img[:, :, 2]
    
    return img



#=================================
# Fetch time series
'''
Inputs:
    - name: name of letter to fetch info of
    - num: "id" for specific letter
Return: array that holds the x and y time series
'''
#=================================
def get_file(name, num):
    # Get current dir
    here, subdir = get_dir(name)
    
    # Fetch file
    in_data = "{}{}.json".format(name, num)
    data_path = os.path.join(here, subdir, in_data)
    text = open(data_path, 'r') # read file from sub-directory
    text_str = text.read()
    time_series = json.loads(text_str)
    text.close()
    
    # Extract data from time series
    x = time_series['x']
    y = time_series['y']
    
    return [x, y]

