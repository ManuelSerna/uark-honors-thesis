# Dynamic time warping in python

import math

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



# Increase size of time series
def increase_len(t, new_length):
    s = [t[0]]
    l = len(t)
    diff = new_length - l
    step = int(math.floor(new_length/diff)-1)
    if step <= 1:
        step = 2
    
    while diff > 0:
        for i in range(1, l):
            if i % step == 0 and diff > 0:
                current_val = t[i]
                prev_val = t[i-1]
                est_val = int((current_val + prev_val)/2)
                
                s.append(est_val)
                s.append(t[i])
                diff -= 1
            else:
                s.append(t[i])
        
        # Recalcuate step size according to new output time series size
        if diff > 0:
            t = s # set s to be the new 
            s = [t[0]] # reset s
            
            l = len(t)
            diff = new_length - l
            step = int(math.floor(new_length/diff)-1)
            if step <= 1:
                step = 2
    return s



# Reduce length of time series by estimating distance between two consecutive points
# Input:
# t: raw time series of some length
# new_length: desired length for new time series
# Return: s: reduced time series
def decrease_len(t, new_length):
    s = [t[0]] # reduced time series s
    l = len(t)
    diff = l - new_length
    step = int(math.floor(l/diff))
    if step <= 1:
        step = 2
    
    while diff > 0:
        for i in range(1, l):
            if i % step == 0 and diff > 0:
                current_val = t[i]
                prev_val = t[i-1]
                est_val = int((current_val + prev_val)/2)
                
                s.pop(-1)
                s.append(est_val)
                
                diff -= 1
            else:
                s.append(t[i])
        
        # Recalcuate step size according to new output time series size
        if diff > 0:
            t = s # set s to be the new 
            s = [t[0]] # reset s
            
            l = len(t)
            diff = l - new_length
            step = int(math.floor(l/diff))
            
            if step <= 1:
                step = 2
    return s



# Set length of time series t to some set number
def set_length(t):
    new_length = 150
    l = len(t)
    
    if l < new_length:
        t = increase_len(t, new_length)
    elif l > new_length:
        t = decrease_len(t, new_length)
    
    return t

# min dist should be: 14
#s = [1, 3, 4, 9, 8, 2, 1, 5, 7, 3]
#t = [1, 6, 2, 3, 0, 9, 4, 3, 6, 3]
#d = min_edit_dist(s, t)
#print(d)

a = [1, 8, 12, 5, 7, 9, 11, 15, 12]
print(a)
print(len(a))
at=set_length(a)
print(at)
print(len(at))


#b = [1, 3, 4, 5, 6, 8, 9, 11, 15, 18, 22, 24, 16, 12, 9, 5, 12, 17, 22, 29, 12]
#b = [1, 5, 12, 7, 8, 22, 15, 19, 21, 25]
# NEW b should be [1, 5, 9, 8, 18, 19, 23]

#b = [1, 3, 5, 7, 9, 11, 13, 15, 23, 6, 12, 5, 2, 0, 0, 8, 10]
# above new b should be [1, 4, 8, 15, 9, 3, 4]

#b = [4, 5, 6, 7, 8, 9, 0] # should not be edited

b = [22, 15, 8, 7, 14, 17, 20, 13, 8, 9, 13, 19, 22, 27, 31, 25]
# above new b should be [22, 11, 10, 14, 11, 20, 27]

'''
print(b)
bt=set_length(b)
print(bt)
print(len(bt))
'''
