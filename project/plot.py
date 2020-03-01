#*********************************
# Plot Class
#   - Use matplotlib to plot time series in different ways
# Author: Manuel Serna-Aguilera
#*********************************

import file_io as f

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#=================================
'''
Class attributes
    - letter1: Character for the first letter
    - num1: ID to specify a certain letter within letter1's sub-directory
    - img1: First image for first letter
    - data1: Tuple in the form (x, y) for the x and y time series of img1
    
    NOTE: If no information was provided for the second letter, the class will set the identifiers to "" and the image and data dictionary to null.
    - letter2: Character for the second letter
    - num2: ID to specify a certain letter within letter2's sub-directory
    - img2: Second image for first letter
    - data2: Tuple in the form (x, y) for the x and y time series of img2
    
    - compare: Tells the class whether it can plot two letters or not. This is meant to error check if there was no second letter set.
'''
#=================================
class plot():
    def __init__(self, letter1, num1, letter2="", num2=""):
        # Set first image
        self.letter1 = letter1
        self.num1 = num1
        self.img1 = f.get_img(letter1, num1, 'c') # color cyan
        self.data1 = f.get_file(letter1, num1)
        
        # Set second image
        self.letter2 = letter2
        self.num2 = num2
        self.img2 = None
        self.data2 = None
        
        self.compare = False
        
        # Only if both second letter fields are populated, enable comparing
        if letter2 != "" and num2 != "":
            self.set_img2(letter2, num2)
    
    #---------------------------------
    # Set image 1 name and number ID manually
    '''
    Inputs: 
        - l: letter character
        - n: number identifier for specific file
    '''
    #---------------------------------
    def set_img1(self, l, n):
        self.letter1 = l
        self.num1 = n
        self.img1 = f.get_img(l, n, 'c') # color cyan
        self.data1 = f.get_file(l, n)
    
    #---------------------------------
    # Set image 2 name and number ID and enable comparison
    '''
    Inputs: 
        - l: letter character
        - n: number identifier for specific file
    '''
    #---------------------------------
    def set_img2(self, l, n):
        if not self.compare:
            self.compare = True
        
        self.letter2 = l
        self.num2 = n
        self.img2 = f.get_img(l, n, 'r')
        self.data2 = f.get_file(l, n)
    
    #---------------------------------
    # Plot one letter's time series
    #---------------------------------
    def plot_letter(self):
        print("  Plotting single letter")
        # TODO: plot single letter if time allows
    
    #---------------------------------
    # Compare two images and their time series side-by-side
    #---------------------------------
    def compare_side(self):
        if self.compare:
            print("  Compare two letters.")
            
            # Stack time series and images into two columns
            fig, axs = plt.subplots(constrained_layout = False)
            spec = gridspec.GridSpec(nrows = 3, ncols = 2, figure=fig)
            axs.yaxis.set_major_locator(plt.NullLocator()) # turn off x ticks
            axs.xaxis.set_major_formatter(plt.NullFormatter()) # turn off y ticks
            fig.suptitle("Compare {}{} and {}{}".format(self.letter1, self.num1, self.letter2, self.num2))

            # Letter 1
            l1 = fig.add_subplot(spec[0, 0])
            l1.imshow(self.img1, cmap="hot")
            l1.yaxis.set_major_locator(plt.NullLocator())
            l1.xaxis.set_major_formatter(plt.NullFormatter())

            # x time series for 1
            xt1 = fig.add_subplot(spec[1, 0])
            xt1.set(ylabel="x time series")
            xt1.plot(self.data1[0])
            xt1.xaxis.set_major_formatter(plt.NullFormatter())

            # y time series for 1
            yt1 = fig.add_subplot(spec[2, 0])
            yt1.set(ylabel="y time series")
            yt1.plot(self.data1[1])

            # Letter 2
            l2 = fig.add_subplot(spec[0, 1])
            l2.imshow(img2, cmap="hot")
            l2.yaxis.set_major_locator(plt.NullLocator())
            l2.xaxis.set_major_formatter(plt.NullFormatter())

            # x time series for 2
            xt2 = fig.add_subplot(spec[1, 1])
            xt2.plot(self.data2[0])
            xt2.xaxis.set_major_formatter(plt.NullFormatter())

            # y time series for 2
            yt2 = fig.add_subplot(spec[2, 1])
            yt2.plot(self.data2[1])
        else:
            print("  Could not compare. Second letter not provided.")

    #---------------------------------
    # Compare two images and their time series side-by-side
    #---------------------------------
    def overlay_plots(self):
        if self.compare:
            print("  Overlay time series plots.")
            
            # Stack time series and images into two columns
            fig, axs = plt.subplots(constrained_layout = False)
            spec = gridspec.GridSpec(nrows = 3, ncols = 2, figure=fig)
            axs.yaxis.set_major_locator(plt.NullLocator())
            axs.xaxis.set_major_formatter(plt.NullFormatter())
            fig.suptitle("Compare {}{} and {}{}".format(self.letter1, self.num1, self.letter2, self.num2))
            
            # Letter 1
            l1 = fig.add_subplot(spec[0, 0])
            l1.imshow(self.img1, cmap="hot")
            l1.yaxis.set_major_locator(plt.NullLocator())
            l1.xaxis.set_major_formatter(plt.NullFormatter())
            
            # Letter 2
            l2 = fig.add_subplot(spec[0, 1])
            l2.imshow(self.img2, cmap="hot")
            l2.yaxis.set_major_locator(plt.NullLocator())
            l2.xaxis.set_major_formatter(plt.NullFormatter())
            
            # x time series
            xt = fig.add_subplot(spec[1, :])
            xt.set(ylabel="x time series")
            xt.plot(self.data1[0])
            xt.plot(self.data2[0], 'tab:red')
            
            # y time series
            yt = fig.add_subplot(spec[2, :])
            yt.set(ylabel="y time series")
            yt.plot(self.data1[1])
            yt.plot(self.data2[1], 'tab:red')
        else:
            print("  Could not compare. Second letter not provided.")

    #---------------------------------
    # Show plot from within class
    #---------------------------------
    def show(self):
        print("-----------------------------")
        print("  Data plotted, press 'q' to quit.")
        print("-----------------------------")
        plt.show()
