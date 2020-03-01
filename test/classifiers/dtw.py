# Dynamic time warping in python

infty = 9999

# time series t1 and t2
def min_edit_dist(t1, t2):
    # Get lengths n and m
    n = len(t1)+1
    m = len(t2)+1
    
    # Create (n+1 x m+1) list and zero-initialize
    result = [[0 for i in range(n)] for j in range(m)]
    
    # Fill in 0th row and 0th column to have t2's and t1's elements respective as initial values for the algorithm to work
    for i in range(0, n-1):
        result[i+1][0] = t1[i]
    for j in range(0, m-1):
        result[0][j+1] = t2[j]
    
    # Initialize all other elements to "infinity"
    for i in range(1, n):
        for j in range(1, m):
            result[i][j] = infty
    result[0][0] = 0
    result[1][1] = 0
    
    # Find minimum edit distance
    for i in range(1, n):
        for j in range(1, m):
            #cost = abs(t1[i]-t2[j])
            dist = abs(result[i][0]-result[0][j])
            result[i][j] = dist + min(
                result[i-1][j],# insertion
                result[i][j-1],# deletion
                result[i-1][j-1] # match
                )
    
    #for row in result:
    #    print(row)
    
    return result[n-1][m-1]

# min dist should be: 14
s = [1, 3, 4, 9, 8, 2, 1, 5, 7, 3]
t = [1, 6, 2, 3, 0, 9, 4, 3, 6, 3]

d = min_edit_dist(s, t)
print(d)
