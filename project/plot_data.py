# Plot letter data and display image

import cv2
import json
import matplotlib.pyplot as plt
import os
import sys

# Specify which letter to plot from cmd line
letter = (sys.argv[1]).upper() 
counter = sys.argv[2]

# Stack time series and image in one column
fig, axs = plt.subplots(3)
fig.suptitle("Letter: {}{}".format(letter, counter))
fig.subplots_adjust(hspace=0, wspace=0)



# Get directory info
here = os.path.dirname(os.path.realpath(__file__))
sub_dir = 'letters/' + letter

# Get image
in_img = "{}{}.png".format(letter, counter)
img_path = os.path.join(here, sub_dir, in_img)
img = cv2.imread(img_path)
img = img[:, :, 2]

# Get time series JSON file data
in_data = "{}{}.json".format(letter, counter)
data_path = os.path.join(here, sub_dir, in_data)
text = open(data_path, 'r') # read file from subdirectory
text_str = text.read()
time_series = json.loads(text_str)
text.close()

# Extract time series
x = time_series['x']
y = time_series['y']
#print('x time series: ', x)
#print('y time series: ', y)



# Plot image and time series
axs[0].imshow(img, cmap="hot")
axs[0].yaxis.set_major_locator(plt.NullLocator())
axs[0].xaxis.set_major_formatter(plt.NullFormatter())

axs[1].plot(x)
axs[1].set(ylabel="x time series")

axs[2].plot(y, 'tab:red')
axs[2].set(xlabel = "frame", ylabel="y time series")

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

print("-----------------------------")
print("  Data plotted, press 'q' to exit.")
print("-----------------------------")

plt.show()
