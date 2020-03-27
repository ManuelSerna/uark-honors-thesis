#*********************************
# Classifier: Support Vector Machine (SVM)
# Author: Manuel Serna-Aguilera
#*********************************

import cv2
import numpy as np
import random
import sklearn
from sklearn import svm

import file_io as f



#=================================
# Initialize SVM classifier
'''
Input:
    - n: number of training samples for each class
    - letters: array that contains letters whose data we want the SVM to train on
Return:
    - SVM classifier that has been trained on some data set
'''
#=================================
def initialize(n, letters):
    classifier = svm.SVC()
    
    # Initialize test data and class label arrays
    num_samples = n * len(letters)
    train_data = np.zeros(shape=(num_samples, 784))
    labels = []
    
    # Transform training data (images)
    counter = 0
    for letter in letters:
        for num in range(1, n+1):
            train_data[counter] = transform_img(letter, num)
            labels.append(letters.index(letter))
            counter += 1
    
    # Fit to data
    classifier.fit(train_data, labels)
    
    return classifier



#=================================
# Transform image to make it easier and faster to process
'''
Input:
    - letter: letter we want to query
    - num: number identifier
    - img: optional numpy image array
Return:
    - ndarray of size (m*m,) to serve as a sample in the test data array
'''
#=================================
def transform_img(letter='', num=0, img=np.array([])):
    # Query image if IDing info was given
    if img.size == 0:
        img = f.get_img(letter, num)
    
    # Grayscale image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Downscale image to be m*m, m defined below
    '''
    Note: image sizes
        if m = 20, then 400 pixels to process
        if m = 28, then 784 pixels to process
    '''
    m = 28
    img = cv2.resize(img , (m, m), interpolation = cv2.INTER_CUBIC)
    
    # Get normalized list
    img = img/255.0 # normalize every element
    
    # Flatten array into (m*m,) ndarray
    img = img.flatten()
    
    return img



#=================================
# SVM classifier
'''
Input:
    - classifier: specific instance of SVM
    - drawing: air-written letter we want to classify
    - letters: list of letters to iterate over (class labels)
Return: best match found with this classifier
'''
#=================================
def classify(classifier, drawing, letters):
    test_sample = np.array([transform_img(img=drawing)])
    prediction = classifier.predict(test_sample)
    
    return letters[prediction[0]]
