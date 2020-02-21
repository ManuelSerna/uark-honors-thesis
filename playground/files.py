# Test loading and saving files for time series and image retrieval
# Use JSON as .json files can be read by other programs and is human readable

import json
import os # able to write to directories

letter = 'A'
counter = 1

# Sample time series
x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 0]

data = {}
data['x'] = x
data['y'] = y

# write some arrays to a json file
#'''
# Now with added twist of writing to a subdirectory
here = os.path.dirname(os.path.realpath(__file__))
subdir = letter
out_file = "{}{}.json".format(letter, counter)
file_path = os.path.join(here, subdir, out_file)

# Check subdirectory
if not os.path.isdir(os.path.join(here, subdir)):
    os.mkdir(os.path.join(here, subdir)) # make

# Create file
try:
    with open(file_path, 'w') as file:
        file.write(json.dumps(data, indent=4))
except IOError:
    print("Wrong path provided")
#'''



# Load some arrays from file
'''
file_name = "data.json"
text = open(file_name, 'r')
text_str = text.read()
lists = json.loads(text_str)
text.close()

print('x time series: ', lists['x'])
print('y time series: ', lists['y'])
#'''
