# Read time series contained in a JSON file in some sub-directory

import json
import os

letter = 'A'
counter = 2

# Get directories
here = os.path.dirname(os.path.realpath(__file__))
subdir = letter # name of sub-directory
in_file = "{}{}.json".format(letter, counter) # read from this specific file
file_path = os.path.join(here, subdir, in_file) # path to write file to

# Load some arrays from file

text = open(file_path, 'r') # TODO: adjust var names
text_str = text.read()
lists = json.loads(text_str)
text.close()

print('x time series: ', lists['x'])
print('y time series: ', lists['y'])
