#*********************************
# Program: Visualize all data samples or the centroids for each letter class.
# Author: Manuel Serna-Aguilera
#*********************************

import matplotlib.pyplot as plt
import sys

import file_io as f



choice = sys.argv[1]

def avg(t):
    return sum(t)/len(t)

markers = {
'A': 'b.',
'AA': 'g.',
'B': 'r.',
'C': 'c.',
'D': 'm.',
'E': 'y.',
'EE': 'k.',
'F': 'bs',
'G': 'gs',
'H': 'rs',
'I': 'cs',
'II': 'ms',
'J': 'ys',
'K': 'ks',
'L': 'b+',
'M': 'g+',
'N': 'r+',
'NN': 'c+',
'O': 'm+',
'OO': 'y+',
'P': 'k+',
'Q': 'bx',
'R': 'gx',
'S': 'rx',
'T': 'cx',
'U': 'mx',
'UU': 'yx',
'UUU': 'kx',
'V': 'bD',
'W': 'gD',
'X': 'rD',
'Y': 'cD',
'Z': 'mD'
}

# Different possible lists of letters
all_letters = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']

no_accents = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

accents = ['A', 'AA', 'E', 'EE', 'I', 'II', 'N', 'NN', 'O', 'OO', 'U', 'UU', 'UUU']

'''
# Letters and their accented counterparts
['A', 'AA']
['E', 'EE']
['I', 'II']
['O', 'OO']
['U', 'UU', 'UUU']
['N', 'NN']

# Sets of samples that overlap
['AA', 'II', 'OO']

['B', 'D', 'E', 'R']

['C', 'N', 'M', 'V']

['G', 'II', 'UU']

['H', 'I', 'NN', 'S']

['M', 'NN', 'H']

- KNN misclassifications for N were very random, too many letters
['N', 'A', 'C', 'O', 'V']

['OO', 'EE', 'II', 'Q']

['R', 'D', 'K']

- KNN misclassifications for S were very random

['U', 'X']

- KNN misclassifications for V were very random

['W', 'EE', 'O']

- Z is a letter of interest since KNN failed 30 times to correctly id it
['Z', 'S', 'I', 'H', 'M']
'''
selected_list=all_letters

# Number of samples to plot
n = 80

# Of the possible lists to plot, choose one
#selected_list = all_letters
#selected_list = no_accents
#selected_list = accents

# Plot data according to choice:
# Centroids
if choice == 'c':
    for l in selected_list:
        samples_x = []
        samples_y = []
        
        for i in range(1, n+1):
            #sample = f.get_file(l, i, og=True)
            sample = f.get_file(l, i)
            
            x = avg(sample[0])
            y = avg(sample[1])
            
            samples_x.append(x)
            samples_y.append(y)
        
        cx = avg(samples_x)
        cy = avg(samples_y)
        
        plt.plot(cx, cy, markers[l], label='{}'.format(l))
# All individual data samples
else:
    for l in selected_list:
        for i in range(1, n+1):
            data = f.get_file(l, i)
            x = avg(data[0])
            y = avg(data[1])
            if i == 1:
                plt.plot(x, y, markers[l], label='{}'.format(l)) # include label in key only once
            else:
                plt.plot(x, y, markers[l])

'''
# Code to visulize the letters based on the time series instead

data = f.get_file('U', 1)
x = data[0]
y = data[1]

l = len(x)
y_max = 99.0

for i in range(l):
    plt.plot(x[i], (-1*y[i])+y_max, 'b.')

plt.xlim(0, 100)
plt.ylim(0, 100)
'''


plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.title('Letter Data')
plt.xlabel('x coordinate')
plt.xlim(0, 99)
plt.ylabel('y coordinate')
plt.ylim(0, 99)

print("  Press 'q' to quit.")
plt.show()
