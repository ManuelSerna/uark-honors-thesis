# Plot chracter data

import json
import matplotlib.pyplot as plt

# TODO: take in letter argument from command line
char = 'A' # TODO: make sure to upper case input
counter = 1

# Get data from JSON file
file_name = "{}{}.json".format(char, counter)
text = open(file_name, 'r')
text_str = text.read()
lists = json.loads(text_str)
text.close()

x = lists['x']
y = lists['y']

#print('x time series: ', x)
#print('y time series: ', y)

# Plot time series
plt.figure()

plt.subplot(211)
plt.grid(True)
plt.plot(x)
plt.ylabel('x coordinates')

plt.subplot(212)
plt.grid(True)
plt.plot(y)
plt.ylabel('y coordinates')

plt.show()
