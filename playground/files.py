# Test loading and saving files for time series and image retrieval
# Use JSON as .json files can be read by other programs and is human readable

import json

# Sample time series
x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 0]

data = {}
data['x'] = x
data['y'] = y

# write some arrays to a json file
#'''
with open("data.json", 'w') as file:
    file.write(json.dumps(data, indent=4))
#'''



# Load some arrays from file
#
file_name = "data.json"
text = open(file_name, 'r')
text_str = text.read()
lists = json.loads(text_str)
text.close()

print('x time series: ', lists['x'])
print('y time series: ', lists['y'])
#'''
