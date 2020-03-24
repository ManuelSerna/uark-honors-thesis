# University of Arkansas Honors Thesis Source Code
This repository contains code and data used for my undergraduate honors thesis (CSCE 491VH) at the University of Arkansas, from Fall 2019 to Spring 2020.

## Objective
The purpose of this project is to evaluate various classification methods for "air-written" letters (which I will limit to only upper-case letters) of the Spanish alphabet. For non-Spanish speakers, this includes the 26 regular letters of the English alphabet, plus the letters Á, É, Í, Ó, Ú, Ü, and Ñ. Note that I will not include Ch, Rr, or Ll as these strings are a combination of already existing letters. I will only focus on _single_ letters.

## Design
To draw in the air, I created a program that tracks a brightly-colored marker (neon-ish green in my case), detects the contours of this brightly-colored area, and then draws filled circles which are overlayed onto each frame from the video stream.

In this project, I will refer to the letters with accent marks as follows
 * Á: aa
 * É: ee
 * Í: ii
 * Ó: oo
 * Ú: uu
 * Ü: uuu
 * Ñ: nn

All other letters that are also in the English language are represented by themselves (e.g. 'A' for A).

## Classification
Here are the following classification methods I used:
 * __Dynamic Time Warping__
 * __K-Nearest Neighbors__
 * __Nearest Centroid__
 * __Support Vector Machine__

## Project
To run the program, you must first execute ```run.sh```. Follow the prompts given the script to record data, compare time series, enter test data and classify letters, or plot all data samples.
