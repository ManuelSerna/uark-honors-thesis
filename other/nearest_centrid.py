#************************************************
# Nearest centroid demo
# Purpose: Given several (x, y) points, classify as either red (R) or blue (B).
# TODO: can generalize to account for any number of classes
#************************************************

#================================================
# Calculate nearest centroid for each class in Y
# Input: Coordinates x and their corresponding labels y
# Return: The centroids for each class as tuples in the form (x, y)
#================================================
def nearest_centroid(x, y, Y):
    l = len(x[0])
    
    # Variables needed to calculate centroids
    cr = 0 # counts class r
    xr = 0 # sum of x-components for r
    yr = 0 # sum of y-components for b
    
    cb = 0
    xb = 0
    yb = 0
    for i in range(l):
        if(y[i] == 'r'):
            cr += 1
            xr += x[0][i]
            yr += x[1][i]
        if(y[i] == 'b'):
            cb += 1
            xb += x[0][i]
            yb += x[1][i]
    
    xr = (1/cr) * xr
    yr = (1/cr) * yr
    
    xb = (1/cb) * xb
    yb = (1/cb) * yb
    
    return (xr, yr), (xb, yb)



# Set of classes
Y = ['r', 'b']

# Array of coordinates x with corresponding labels
x = [[-2, -1, 0, 0, 1, 1, 2, 2 ], #x coords
     [-3, -1, 1, -2, 1, -5, 2, 4]] #y coords
y = ['r', 'r', 'b', 'r', 'b', 'r', 'b', 'b']

# Get nearest centroids
r, b = nearest_centroid(x, y, Y)
print('centroid for class r: ', r)
print('centroid for class b: ', b)
