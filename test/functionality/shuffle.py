# Shuffle two lists' elements such that their corresponding elements' positions are still consistent

import random

arr1 = [1, 2, 3, 4]
arr2 = ['x', 'x', 'y', 'z']

print("The original list 1 : " + str(arr1)) 
print("The original list 2 : " + str(arr2)) 
  
# Shuffle two lists with same order 
# Using zip() + * operator + shuffle() 
temp = list(zip(arr1, arr2)) 
random.shuffle(temp) 
res1, res2 = zip(*temp) 
  
# Printing result 
print("List 1 after shuffle : " + str(list(res1))) 
print("List 2 after shuffle : " + str(list(res2))) 
