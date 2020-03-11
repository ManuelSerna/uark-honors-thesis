# Test making clusters for k-nearest neighbors
# TODO: Rename file to set up for k-nearest neighbors. I want to run this program and will save the clusters out of the already recorded letter time series.

# PLAN TODO: average all x and y time series together and plot single dots. Then I want to save all these labeled data points in a JSON file in another directory.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import file_io as f
import plot as p
import time_series as ts



# List of letters
letters = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']

# List of unique markers to correspond to letters
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

# Create plot
#_, ax = plt.subplots(figsize=(4,4))
#plt.title('Letters')
#plt.ylim(0, 550)
#plt.xlim(0, 550)

l = len(letters)
print(l)

for i in range(l):
    #print(letters[i], markers[i])
    #print(i)
    for j in range(1, 10):
        # Query current letter data
        query = f.get_file(letters[i], j)
        query_x = ts.apply_all(query[0])
        query_y = ts.apply_all(query[1])

        # Get integer means of x and y time series
        avg_x = int(sum(query_x)/len(query_x))
        avg_y = int(sum(query_y)/len(query_y))
        
        # Plot point
        #plt.plot(avg_x, avg_y, markers[letters[i]])

#plt.show()

print('\nDone.')
