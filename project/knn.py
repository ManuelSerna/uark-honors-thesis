#*********************************
# Classifier: K-Nearest Neighbors
# Author: Manuel Serna-Aguilera
#*********************************

import math
from statistics import mode
from string import digits

import file_io as f
import time_series as ts



def avg(a):
    return int(sum(a)/len(a)) # average of elements in an array a

#=================================
# K-Nearest Neighbors: find the most closest neighbors of the same class
'''
Input:
    - tx, ty: captured letter time series
    - letters: list of letters to iterate over
    - n: number of samples for each class
Return:
    - best_match: mode of k closest neighbors
'''
#=================================
def knn(tx, ty, letters, n):
    k = 2*n-1 # k neighbors to consider
    l = len(letters)
    
    # Create dictionary to store the distances
    # Key: letter with identifying number
    # Value: distance between this sample point and the captured data point
    distances = {}
    
    # Use time series x and y component averages to get sample point
    cx = avg(tx)
    cy = avg(ty)
    
    for i in range(l):
        for j in range(1, 10):
            # Query current letter data and get the average x and y values to represent the point for the sample
            query = f.get_file(letters[i], j) 
            qx = avg(ts.apply_all(query[0]))
            qy = avg(ts.apply_all(query[1]))
            
            # Calculate Euclidean distance between captured point and query point
            distance = math.sqrt((cx-qx)**2+(cy-qy)**2)
            distances['{}{}'.format(letters[i], j)] = distance
    
    # Sort lists (sorted() function in Python uses TimSort, which is a hybrid sorting algorithm with insertion and merge sort)
    distances = dict(sorted(distances.items(), key=lambda kv: kv[1]))
    
    # Pick the first k letter labels, filter out number identifiers
    k_closest = list(distances.keys())[0: k]
    #print('k-closest list with nums: ',k_closest)
    
    remove_digits = str.maketrans('', '', digits)
    for i in range(len(k_closest)):
        k_closest[i] = k_closest[i].translate(remove_digits)
    
    # Of the k terms, pick the mode
    #print('final list ', k_closest)
    best_match = mode(k_closest)
    
    return best_match
