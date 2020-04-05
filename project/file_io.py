#*********************************
# Module: Write and read files
#   - This module takes care of writing the time series data into JSON files, as well as the drawings to PNG files, onto the appropriate directories. This module also allows the user to get recorded data and images.
#   - NOTE: I will return the modified time series. I also store the original time series just in case.
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
    - img: go to image directory (flag defaulted to true)
    - og: go to unmodified time series directory (flag defaulted to false)
    - letter_dir: letter directory
    - training: flag that decides whether we interact with training or testing data
Return:
    - here:   current path (same as file) as a string
    - subdir: sub-directory if there is one
'''
# Called by: all the get and write file functions in this module
#=================================
def get_dir(img=True, og=False, letter_dir='', training=True):
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = 'letters/'
    
    if training:
        subdir += 'training/'
    else:
        subdir += 'testing/'
    
    if img:
        subdir += 'images/'
    else:
        if og:
            subdir += 'original_ts/'
        else:
            subdir += 'modified_ts/'
    
    subdir += letter_dir
    
    return here, subdir



#=================================
# Get image
'''
Input:
    - name: name of letter to fetch info of
    - num: "id" for specific letter
    - color: set image to a certain color (defaulted to empty string to represent white)
    - training: set to true to get data from training data directory
Return: image (3D cv2 array)

NOTE: Assume letters are drawn in BGR where red = 255, blue and green are 0
'''
#=================================
def get_img(name='', num=0, color='', training=True):
    # Get current dir
    here, subdir = get_dir(letter_dir=name, training=training)
    
    # Fetch image
    in_img = "{}{}.png".format(name, num)
    img_path = os.path.join(here, subdir, in_img)
    img = cv2.imread(img_path)
    
    zero = np.zeros((299, 299), np.uint8)
    
    # Set color of letter, account for BGR color space in OpenCV
    if color == 'r': 
        img[:, :, 1] = zero
        img[:, :, 2] = zero
    elif color == 'g':
        img[:, :, 0] = zero
        img[:, :, 2] = zero
    elif color == 'b':
        img[:, :, 0] = zero
        img[:, :, 1] = zero
    elif color == 'c':
        img[:, :, 0] = zero
    elif color == 'y':
        img[:, :, 2] = zero
    
    return img



#=================================
# Get time series
'''
Input:
    - name: name of letter to fetch info of
    - num: "id" for specific letter
    - og: flag to dictate if we want to query the original time series (defaulted to false)
    - training: set to true to get data from training data directory
Return: array that holds the x and y time series
'''
#=================================
def get_file(name='', num='', og=False, training=True):
    # Get current dir
    here, subdir = get_dir(img=False, og=og, letter_dir=name, training=training)
    
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



#=================================
# Write image
'''
Input:
    - img:  image to be saved to a PNG file
    - name: name of letter
    - num: "id" for specific letter
    - training: set to true to write data to training data directory
'''
#=================================
def write_img(img, name, num, training=True):
    # Get current dir
    here, subdir = get_dir(letter_dir=name, training=training)
    
    # If sub-directory does not exist, make directory
    if not os.path.isdir(os.path.join(here, subdir)):
        os.mkdir(os.path.join(here, subdir))
    
    # Image path
    out_img = "{}{}.png".format(name, num)
    img_path = os.path.join(here, subdir, out_img)
    print('Wrote img to: ', img_path)
    
    # Write to sub-directory
    try:
        cv2.imwrite(img_path, img)
    except:
        print("ERROR: could not write image.")



#=================================
# Write time series to JSON
'''
Input:
    - name: name of letter
    - num:  "id" for specific letter
    - x:    x time series
    - y:    y time series
    - og: flag to dictate if we want to query the original time series (defaulted to false)
    - training: set to true to write data to training data directory
'''
#=================================
def write_json(name='', num='', x=[], y=[], og=False, training=True):
    data = {}
    data['x'] = x
    data['y'] = y
    
    # Get current dir
    here, subdir = get_dir(img=False, og=og, letter_dir=name, training=training)
    
    # If sub-directory does not exist, make directory
    if not os.path.isdir(os.path.join(here, subdir)):
        os.mkdir(os.path.join(here, subdir))
    
    # Time series file path
    out_data = "{}{}.json".format(name, num)
    data_path = os.path.join(here, subdir, out_data)
    print('Wrote data to: ', data_path)
    
    # Write time series to sub-directory
    try:
        with open(data_path, 'w') as file:
            file.write(json.dumps(data, indent=4)) # write data
    except IOError:
        print("ERROR: could not write image.")
