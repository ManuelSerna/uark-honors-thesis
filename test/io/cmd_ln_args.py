# Example program to take in arguments from command line

import string
import sys # extract args

#print(sys.argv[1])

letter = (sys.argv[1]).upper()
count = 1

some_file = "{}{}.json".format(letter, count)
some_img = "{}{}.png".format(letter, count)

print("file: ", some_file)
print("image: ", some_img)
