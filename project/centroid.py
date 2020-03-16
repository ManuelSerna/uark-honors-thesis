# Classifier: nearest centroid

import file_io as f
import time_series as ts

# TEST: module import
import capture as cp


# Number of samples per class
n = 9

# Nearest Centroid
def avg(t):
    return int(sum(t)/len(t)) # average of array

def nearest_centroid(tx, ty, letters):
    l = len(letters)
    
    # Create dictionary to store centroid/mean location for each letter class
    # Key: letter (class)
    # Value: coordinates for mean/centroid, this is a tuple (x, y) to hold the x and y coordinates
    centroids = {}
    
    # Calculate average of captured data
    captured_x = avg(tx)
    captured_y = avg(ty)
    
    # Calculate mean/centroid for all class labels
    for i in range(l):
        # Arrays to hold average x and y values of all letters of the same class
        ax = []
        ay = []
        
        for j in range(1, n+1):
            # Query current letter data and get the average x and y values to represent the point for the sample
            query = f.get_file(letters[i], j)
            qx = avg(ts.apply_all(query[0]))
            qy = avg(ts.apply_all(query[1]))
            
            # Add average of individual sample for current class
            ax.append(qx)
            ay.append(qy)
            
        # Store centroid (x, y) for current class
        class_x = avg(ax)
        class_y = avg(ay)
        centroids[letters[i]] = (class_x, class_y)
    
    # Get minimum distance from captured point and some class centroid
    print(centroids)
    #centroids = dict(sorted(centroids.items(), key=lambda kv: kv[1]))

# TEST func call
d, x, y = cp.capture()
x = ts.apply_all(x)
y = ts.apply_all(y)

a = ['A', 'AA', 'B', 'C', 'D', 'E', 'EE', 'F', 'G', 'H', 'I', 'II', 'J', 'K', 'L', 'M', 'N', 'NN', 'O', 'OO', 'P', 'Q', 'R', 'S', 'T', 'U', 'UU', 'UUU', 'V', 'W', 'X', 'Y', 'Z']

nearest_centroid(x, y, a)
