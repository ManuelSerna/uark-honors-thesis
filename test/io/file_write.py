# Test loading and saving files for time series and image retrieval
# Use JSON as .json files can be read by other programs and is human readable

import json
import os # able to interact with directories

letter = 'A'
counter = 2

# Sample time series
x = [2, 5, 6, 3, 1]
y = [6, 6, 9, 5, 2]

data = {}
data['x'] = x
data['y'] = y

# Write some arrays to a json file
# Now with added twist of writing to a subdirectory
here = os.path.dirname(os.path.realpath(__file__))
subdir = 'subdir/' + letter # name of sub-directory
out_file = "{}{}.json".format(letter, counter) # write data to this file
file_path = os.path.join(here, subdir, out_file) # path to write file to
print(file_path)

# Check subdirectory
if not os.path.isdir(os.path.join(here, subdir)):
    os.mkdir(os.path.join(here, subdir)) # make

# Create file
try:
    with open(file_path, 'w') as file:
        file.write(json.dumps(data, indent=4))
    print(" Wrote to path: ", file_path)
except IOError:
    print("Wrong path provided")
