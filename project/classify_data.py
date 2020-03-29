#*********************************
# Program: Classify letter
#   - Use the functions of my custom capture module to get the air-written letter from the user and use several classifiers to identify what was written.
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import sys
import time

# Import classifier modules
import dtw
import knn
import nc
import svm

# Import custom modules
import capture as cp
import file_io as f
import time_series as ts



#---------------------------------
# Setup
#---------------------------------
print("  Setting up...")
true_label = (sys.argv[1]).upper()
results = [] # store all results for all tests in the session
trials = 50 # number of times user will input test data

all_letters = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']
no_accents = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
accents = ['A', 'AA', 'E', 'EE', 'I', 'II', 'N', 'NN', 'O', 'OO', 'U', 'UU', 'UUU']
selected_list = all_letters

infty = 999999
n = 40 # number of samples currently recorded for each letter class
test_iteration = 1 # ith test in the session

# SVM setup
svm_classifier = svm.initialize(n, selected_list)



#---------------------------------
# Continuously test input from capture
#---------------------------------
while test_iteration <= trials:
    print("  ******** Trial: {} ********".format(test_iteration))
    current = []
    
    # Capture air-drawn letter and apply time series modifications
    drawing, captured_x, captured_y = cp.capture()
    captured_x = ts.apply_all(captured_x)
    captured_y = ts.apply_all(captured_y)
    
    #.............................
    # 1. Perform DTW minimum edit distance calculation
    #.............................
    # NOTE: Iterating through all samples for dtw takes a long time, even going through several samples takes several seconds. Which is why I decided to only consider the first indexed letter.
    
    minx = infty # min edit dist for x
    miny = infty # min edit dist for y
    
    max_sample_size = 1 # consider this many samples
    #start = time.time()
    
    for letter in selected_list:
        for i in range(1, max_sample_size+1):
            # Query data for current labeled letter
            query = f.get_file(letter, i)
            query_x = query[0]
            query_y = query[1]
            
            # Calculate minimum edit distances for x and y time series
            dx = dtw.dtw(captured_x, query_x)
            dy = dtw.dtw(captured_y, query_y)
            
            if minx > dx and miny > dy:
                minx = dx
                miny = dy
                dtw_match = letter
    
    #finish = round(time.time() - start, 3)
    #print("\tDTW: {} (time: {} s)".format(dtw_match, finish))
    current.append(dtw_match)
    
    #.............................
    # 2. Perform k-nearest neighbors classification
    #.............................
    #start = time.time()
    knn_match = knn.knn(captured_x, captured_y, selected_list, n)
    #finish = round(time.time() - start, 3)
    #print("\tKNN: {} (time: {} s)".format(knn_match, finish))
    current.append(knn_match)
    
    #.............................
    # 3. Perform nearest centroid classification
    #.............................
    #start = time.time()
    nc_match = nc.nearest_centroid(captured_x, captured_y, selected_list, n)
    #finish = round(time.time() - start, 3)
    #print("\tNC: {} (time: {} s)".format(nc_match, finish))
    current.append(nc_match)
    
    #.............................
    # 4. Support vector machine
    #.............................
    #start = time.time()
    svm_match = svm.classify(svm_classifier, drawing, selected_list)
    #finish = round(time.time() - start, 3)
    #print("\tSVM: {} (time: {} s)".format(svm_match, finish))
    current.append(svm_match)
    
    results.append(current)
    test_iteration += 1



#---------------------------------
# After the session, calculate each method's accuracy
#---------------------------------
num_tests = len(results)

dtw_accuracy = 0
knn_accuracy = 0
nc_accuracy = 0
svm_accuracy = 0

for test in results:
    dtw = test[0]
    if dtw == true_label:
        dtw_accuracy += 1
    
    knn = test[1]
    if knn == true_label:
        knn_accuracy += 1
    
    nc = test[2]
    if nc == true_label:
        nc_accuracy += 1
    
    svm = test[3]
    if svm == true_label:
        svm_accuracy += 1

print('Results:')
print('dtw: {}\nknn: {}\nnc: {}\nsvm: {}'.format(dtw_accuracy/num_tests, knn_accuracy/num_tests, nc_accuracy/num_tests, svm_accuracy/num_tests))

print()
print("  End testing session.")
