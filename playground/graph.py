# Graph a list with matplotlib

import json
import matplotlib.pyplot as plt

# Get data from JSON file
file_name = "data.json"
text = open(file_name, 'r')
text_str = text.read()
lists = json.loads(text_str)
text.close()

x = lists['x']
y = lists['y']

print('x time series: ', x)
print('y time series: ', y)

# Plot time series
plt.figure()

plt.subplot(211)
plt.grid(True)
plt.plot(x, x, 'bo')
plt.ylabel('x coordinates')

plt.subplot(212)
plt.grid(True)
plt.plot(y, y, 'ro')
plt.ylabel('y coordinates')

plt.show()
