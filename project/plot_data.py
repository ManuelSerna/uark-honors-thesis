# Plot letter image and time series

import cv2
import json
import matplotlib.pyplot as plt
import os
import sys



# Specify which letter to plot from cmd line
letter = (sys.argv[1]).upper()
counter = sys.argv[2]



# Get directory info and desired sub-directory
def get_dir(subpath=''):
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = 'letters/' + subpath
    return here, subdir

# Fetch and return image
def get_img(name, num):
    # Get current dir
    here, subdir = get_dir(name)
    
    # Fetch image
    in_img = "{}{}.png".format(name, num)
    img_path = os.path.join(here, subdir, in_img)
    img = cv2.imread(img_path)
    img = img[:, :, 2]
    
    return img

# Fetch and return time series JSON file
def get_file(name, num):
    # Get current dir
    here, subdir = get_dir(name)
    
    # Fetch file
    in_data = "{}{}.json".format(name, num)
    data_path = os.path.join(here, subdir, in_data)
    text = open(data_path, 'r') # read file from subdirectory
    text_str = text.read()
    time_series = json.loads(text_str)
    text.close()
    
    return time_series



# Get image and file for drawing 1
img = get_img(letter, counter)

data = get_file(letter, counter)
x = data['x']
y = data['y']



# Stack time series and images into two columns
fig, axs = plt.subplots(3)

fig.suptitle("Letter: {}{}".format(letter, counter))
fig.subplots_adjust(hspace=0, wspace=0)

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
