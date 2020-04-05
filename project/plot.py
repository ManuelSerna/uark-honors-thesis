#*********************************
# Module: Plot functions
#   - Use matplotlib to plot time series in different ways
# Author: Manuel Serna-Aguilera
#*********************************

import file_io as f

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



#=================================
# Look at two time series plots side by side
'''
Input:
    - img1: first drawing
    - x1: x time series for first letter
    - y1: y time series for first letter
    - img2: second drawing
    - x2: x time series for second letter
    - y2: y time series for second letter
'''
#=================================
def adjacent_plots(img1, x1, y1, img2, x2, y2):
    print("  Compare two letters.")
    
    # Stack time series and images into two columns
    fig, axs = plt.subplots(constrained_layout = False)
    spec = gridspec.GridSpec(nrows = 3, ncols = 2, figure=fig)
    axs.yaxis.set_major_locator(plt.NullLocator()) # turn off x ticks
    axs.xaxis.set_major_formatter(plt.NullFormatter()) # turn off y ticks
    #fig.suptitle("Compare {}{} and {}{}".format(letter1, num1, letter2, num2))

    # Letter 1
    l1 = fig.add_subplot(spec[0, 0])
    l1.imshow(img1, cmap="hot")
    l1.yaxis.set_major_locator(plt.NullLocator())
    l1.xaxis.set_major_formatter(plt.NullFormatter())

    # x time series for 1
    xt1 = fig.add_subplot(spec[1, 0])
    xt1.set(ylabel="x time series")
    xt1.plot(x1)
    xt1.xaxis.set_major_formatter(plt.NullFormatter())

    # y time series for 1
    yt1 = fig.add_subplot(spec[2, 0])
    yt1.set(ylabel="y time series")
    yt1.plot(y1)

    # Letter 2
    l2 = fig.add_subplot(spec[0, 1])
    l2.imshow(img2, cmap="hot")
    l2.yaxis.set_major_locator(plt.NullLocator())
    l2.xaxis.set_major_formatter(plt.NullFormatter())

    # x time series for 2
    xt2 = fig.add_subplot(spec[1, 1])
    xt2.plot(x2)
    xt2.xaxis.set_major_formatter(plt.NullFormatter())

    # y time series for 2
    yt2 = fig.add_subplot(spec[2, 1])
    yt2.plot(y2)
    
    print("  Displaying adjacent plots. Press 'q' to resume.")
    plt.show()



#=================================
# Overlay the time series for two letters
'''
Input:
    - img1: first drawing (default is a black drawing)
    - x1: x time series for first letter
    - y1: y time series for first letter
    - img2: second drawing (default is a black drawing)
    - x2: x time series for second letter
    - y2: y time series for second letter
'''
#=================================
def overlay_plots(img1=np.zeros((299, 299, 3), np.uint8), x1=[], y1=[], img2=np.zeros((299, 299, 3), np.uint8), x2=[], y2=[]):
    print("  Overlay time series plots.")
    
    # Stack time series and images into two columns
    fig, axs = plt.subplots(constrained_layout = False)
    spec = gridspec.GridSpec(nrows = 3, ncols = 2, figure=fig)
    axs.yaxis.set_major_locator(plt.NullLocator())
    axs.xaxis.set_major_formatter(plt.NullFormatter())
    #fig.suptitle("Compare {}{} and {}{}".format(letter1, num1, letter2, num2))
    
    # Letter 1
    l1 = fig.add_subplot(spec[0, 0])
    l1.imshow(img1, cmap="hot")
    l1.yaxis.set_major_locator(plt.NullLocator())
    l1.xaxis.set_major_formatter(plt.NullFormatter())
    
    # Letter 2
    l2 = fig.add_subplot(spec[0, 1])
    l2.imshow(img2, cmap="hot")
    l2.yaxis.set_major_locator(plt.NullLocator())
    l2.xaxis.set_major_formatter(plt.NullFormatter())
    
    # x time series
    xt = fig.add_subplot(spec[1, :])
    xt.set(ylabel="x time series")
    xt.plot(x1)
    xt.plot(x2, 'tab:red')
    
    # y time series
    yt = fig.add_subplot(spec[2, :])
    yt.set(ylabel="y time series")
    yt.plot(y1)
    yt.plot(y2, 'tab:red')
    
    print("  Displaying overlayed plots. Press 'q' to resume.")
    plt.show()

#=================================
# Overlay the time series for two letters
'''
Input:
    - letter1: character for first letter to plot
    - num1: number identifier for first letter
    - letter2: character for second letter to plot
    - num2: number identifier for second letter
'''
#=================================
def overlay_plots(letter1, num1, letter2, num2):
    print("  Overlay time series plots.")
    
    query1 = f.get_file(name=letter1, num=num1)
    x1 = query1[0]
    y1 = query1[1]
    img1 = f.get_img(name=letter1, num=num1, color='r')
    
    query2 = f.get_file(name=letter2, num=num2, training=True)
    x2 = query2[0]
    y2 = query2[1]
    img2 = f.get_img(name=letter2, num=num2, color='c')
    
    # Stack time series and images into two columns
    fig, axs = plt.subplots(constrained_layout = False)
    spec = gridspec.GridSpec(nrows = 3, ncols = 2, figure=fig)
    axs.yaxis.set_major_locator(plt.NullLocator())
    axs.xaxis.set_major_formatter(plt.NullFormatter())
    fig.suptitle("Compare {}{} and {}{}".format(letter1, num1, letter2, num2))
    
    # Letter 1
    l1 = fig.add_subplot(spec[0, 0])
    l1.imshow(img1, cmap="hot")
    l1.yaxis.set_major_locator(plt.NullLocator())
    l1.xaxis.set_major_formatter(plt.NullFormatter())
    
    # Letter 2
    l2 = fig.add_subplot(spec[0, 1])
    l2.imshow(img2, cmap="hot")
    l2.yaxis.set_major_locator(plt.NullLocator())
    l2.xaxis.set_major_formatter(plt.NullFormatter())
    
    # x time series
    xt = fig.add_subplot(spec[1, :])
    xt.set(ylabel="x time series")
    xt.plot(x1, 'tab:blue')
    xt.plot(x2, 'tab:red')
    
    # y time series
    yt = fig.add_subplot(spec[2, :])
    yt.set(ylabel="y time series")
    yt.plot(y1, 'tab:blue')
    yt.plot(y2, 'tab:red')
    
    print("  Displaying overlayed plots. Press 'q' to resume.")
    plt.show()
