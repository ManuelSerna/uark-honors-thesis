import math

# Insert element in between two consecutive elements in a list
# Credit to GeeksforGeeks for tutorial

t = [1, 2, 3, 4, 5]
s = [4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
new = 0 # new element to insert
step = 3



# Input: original list
# Return: modified lengthened list
def insert_between(og_list, step):
    mod_list = og_list[:1]
    prev = mod_list[0]
    
    COUNTER = 0
    
    # Construct new list with added elements
    for i in og_list[1:]:
        # Add new element according to step size
        #NOTE: use the diff in eq_len function to determine how many insertions to make
        if len(mod_list) % step == 0:
            # estimate intermediate term between current and previous element in time series
            new = int((i+prev)/2)
            mod_list.append(new)
            
            COUNTER += 1
            print(' COUNTER-->', COUNTER)
        mod_list.append(i)
        prev = i
    
    return mod_list



# TODO 2: make the lists the same length, only then can I do a proper scaling
# Equalize the length between two time series t1 and t2
def eq_len(t1, t2):
    l1 = len(t1)
    l2 = len(t2)
    
    # Calculate how often to insert new elements into shorter list
    max_len = max(l1, l2)
    min_len = min(l1, l2)
    diff = max_len - min_len
    #step = int(min_len/diff)
    #step = int(math.ceil(max_len/diff))
    step = int(math.ceil(min_len/diff))
    
    print(l1)
    print(l2)
    print('diff: ', diff)
    
    print('  insert between every {} elements'.format(step))
    
    # TODO: find which time series is smaller, and populate with points in between until l1==l2
    if l1 == max_len:
        t2 = insert_between(t2, step)
    else:
        t1 = insert_between(t1, step)
    
    print('new sizes: t1={}; t2={}'.format(len(t1), len(t2)))
    
    return t1, t2

#print(insert_between(t, 3))
u, v = eq_len(s, t)
print(len(u), u)
print(len(v), v)




# NOTE: return sends a specified value back to its caller

# NOTE: yield can produce a sequence of values
# If a body of a def contains a yield, it automatically becomes a generator

# Generator that yields:
# 1 the first time,
# 2 the second time, and
# 3 the third time
def simple_generator():
    yield 1
    yield 2
    yield 3

#for val in simple_generator():
#    print(val)

def next_square():
    i = 1
    
    while True:
        yield i*i
        i += 1
'''
for k in next_square():
    if k > 100:
        break
    print(k)
'''
