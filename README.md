# University of Arkansas Honors Thesis Source Code
This repository contains code, data, etc. used for my undergraduate honors thesis (CSCE 491VH) at the University of Arkansas, from Fall 2019 to Spring 2020.

## Objective
The purpose of this project is to evaluate various classification methods for "air-written" letters (which I will limit to only upper-case letters) of the Spanish alphabet. For non-Spanish speakers, this includes the 26 regular letters of the English alphabet, plus the letters Á, É, Í, Ó, Ú, Ü, and Ñ. Note that I will not include Ch, Rr, or Ll as these strings are a combination of already existing letters. I will only focus on _single_ letters.

## Design
To air-write letters, I created a simple tracker that identifies a specially-colored marker (in my case, a bright green). It first converts the RGB camera frame to the HSI color space, thresholds on hue, saturation, and intensity ranges, and outputs a mask image. The program then finds the edges in the mask image (which would ideally just be the silhouette of the marker tip) and then gets the minimum enclosing circle for the set of edges found. The program uses the center of this circle to write.

## Data
In this project, I will refer to the letters with accent marks as follows
 * Á: AA
 * É: EE
 * Í: II
 * Ó: OO
 * Ú: UU
 * Ü: UUU
 * Ñ: NN

All other letters that are also in the English language are represented by themselves (e.g. 'A' for A).

As of May 2020, I have 3,630 total samples, where 2,640 are set aside for training and 990 for testing.

## Classification
Here are the following classification methods I used:
 * __Dynamic Time Warping__
 * __K-Nearest Neighbors__
 * __Nearest Centroid__
 * __Support Vector Machine__
 * __LeNet Convolutional Neural Network__

## Project
To use the tracker program, record more data, classify data, etc., run the Bash script ```run.sh```. Follow the prompts to execute the desired function.
