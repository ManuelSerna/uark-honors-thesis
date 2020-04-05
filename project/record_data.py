#*********************************
# Program: Record training or testing data or record a drawing session
#   - Use the capture module to specifically record data
# Author: Manuel Serna-Aguilera
#*********************************

import sys

import capture as cp



'''
Program cmd inputs:
- argv[1]: this will dictate whether we want to record
    '1' training data, or
    '2' testing data

- argv[2]: true label for data
'''
task = sys.argv[1]
letter = (sys.argv[2]).upper()


if task == '1':
    cp.capture(letter=letter, training=True)
elif task == '2':
    cp.capture(letter=letter, testing=True)
elif task == '3':
    print('TODO: take video')
