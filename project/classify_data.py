#*********************************
# Program: Calculate accuracies of all classifiers on all test samples for all letter labels
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import json
import math
import time

# Import classifier modules
import dtw
import knn
import nc
import svm

# Import custom module(s)
import file_io as f



print("  Setting up.")
start = time.time()

letters = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']

n_train = 80
n_test = 30

'''
Results dictionary
    - Key: letter label
    - Value: dictionary to store classifier accuracies
        - key: element from classifiers list
        - value: accuracy (in range [0.0...1.0])
'''
results={}

# Setup
infty = 999999
svm_classifier = svm.initialize(n_train, letters)
print("  Setup done.")



'''
For each letter in the set of letters (Spanish alphabet), calculate the overall accuracy of each classifier.
'''
for letter in letters:
    '''
    i. For all n_test samples of a certain letter, get the best match from each classifier
    '''
    current_letter_results = [] # store match results for each sample here
    
    for letter_id in range(1, n_test+1):
        '''
        Values at each index:
            0: dtw_match
            1. knn_match
            2. nc_match
            3. svm_match
        '''
        matches = []
        
        # Query test data for each letter label (use l as true label)
        test_sample = f.get_file(name=letter, num=letter_id, training=False)
        test_sample_x = test_sample[0]
        test_sample_y = test_sample[1]
        test_drawing = f.get_img(name=letter, num=letter_id, training=False)
        
        #.........................
        # DTW
        #.........................
        minx = infty
        miny = infty
        
        max_sample_size = 1 # consider this many samples
        
        for i in letters:
            for j in range(1, max_sample_size+1):
                # Query time series data from training set for current letter
                query = f.get_file(name=i, num=j) # get "ideal" letter from training data set
                query_x = query[0]
                query_y = query[1]
                
                # Calculate minimum edit distances for x and y time series
                dx = dtw.dtw(test_sample_x, query_x)
                dy = dtw.dtw(test_sample_y, query_y)
                
                # Get best match
                if minx > dx and miny > dy:
                    minx = dx
                    miny = dy
                    dtw_match = i
        matches.append(dtw_match)
        
        #.........................
        # KNN
        #.........................
        knn_match = knn.knn(test_sample_x, test_sample_y, letters, n_train)
        matches.append(knn_match)
        
        #.........................
        # NC
        #.........................
        nc_match = nc.nearest_centroid(test_sample_x, test_sample_y, letters, n_train)
        matches.append(nc_match)
        
        #.........................
        # SVM
        #.........................
        svm_match = svm.classify(svm_classifier, test_drawing, letters)
        matches.append(svm_match)
        
        # Add match results for current letter sample
        current_letter_results.append(matches)
        
        
    '''
    ii. With the individual matches, now we calculate the overall accuracy of the classifiers for the current letter.
    '''
    dtw_accuracy = 0
    knn_accuracy = 0
    nc_accuracy = 0
    svm_accuracy = 0
    
    for sample_matches in current_letter_results:
        dtw_match = sample_matches[0]
        if dtw_match == letter:
            dtw_accuracy += 1
        
        knn_match = sample_matches[1]
        if knn_match == letter:
            knn_accuracy += 1
        
        nc_match = sample_matches[2]
        if nc_match == letter:
            nc_accuracy += 1
        
        svm_match = sample_matches[3]
        if svm_match == letter:
            svm_accuracy += 1
    
    # Add classifier accuracies for current letter to final dictionary
    accuracies = {}
    
    accuracies['DTW'] = dtw_accuracy/n_test
    accuracies['KNN'] = knn_accuracy/n_test
    accuracies['NC'] = nc_accuracy/n_test
    accuracies['SVM'] = svm_accuracy/n_test
    
    print('{}: {}'.format(letter, accuracies))
    
    results[letter] = accuracies

# Write dictionary to JSON file
with open("results.json", 'w') as file:
    file.write(json.dumps(results, indent=4))

finish = round(time.time() - start, 3)
print("Total time: {}".format(finish))
