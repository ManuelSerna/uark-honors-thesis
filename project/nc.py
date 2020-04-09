#*********************************
# Classifier: Nearest Centroid
# Author: Manuel Serna-Aguilera
#*********************************

import math

import file_io as f
#import time_series as ts



def avg(a):
    return int(sum(a)/len(a)) # average of elements in an array a

#=================================
# Nearest Centroid: find the centroid/mean that most closely matches the captured data's centroid/mean
'''
Input:
    - tx, ty: captured letter time series
    - letters: list of letters to iterate over
    - n: number of samples for each class
Return:
    - best_match: the closest centroid to captured centroid
'''
#=================================
def nearest_centroid(tx, ty, letters, n):
    l = len(letters)
    infty = 999999
    
    # Create dictionary to store centroid/mean location for each letter class
    # Key: letter (class)
    # Value: coordinates for mean/centroid, this is a tuple (x, y) to hold the x and y coordinates
    centroids = {}
    
    # Calculate mean/centroid for all class labels
    for i in range(l):
        # Arrays to hold average x and y values of all letters of the same class
        ax = []
        ay = []
        
        for j in range(1, n+1):
            # Query current letter data and get the average x and y values to represent the point for the sample
            query = f.get_file(letters[i], j)
            qx = avg(query[0])
            qy = avg(query[1])
            
            # Add average of individual sample for current class
            ax.append(qx)
            ay.append(qy)
            
        # Store centroid (x, y) for current class
        class_x = avg(ax)
        class_y = avg(ay)
        centroids[letters[i]] = (class_x, class_y)
    
    # Calculate centroid/mean of captured data
    captured_x = avg(tx)
    captured_y = avg(ty)
    
    # Compute minimum distance between captured data and all centroids
    min_distance = infty
    best_match = 'na'
    
    for key, value in centroids.items():
        distance = math.sqrt((captured_x-value[0])**2+(captured_y-value[1])**2)
        
        if distance < min_distance:
            min_distance = distance
            best_match = key
    
    return best_match
