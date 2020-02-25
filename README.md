# University of Arkansas Honors Thesis Source Code
This repository contains code and data used for my undergraduate honors thesis (CSCE 491VH) at the University of Arkansas, from Fall 2019 to Spring 2020.

## Objective
The purpose of this project is to evaluate various classification methods for "air-written" letters (which I will limit to only upper-case letters for simplicity) of the Spanish alphabet. For non-Spanish speakers, this includes the 26 regular letters of the English alphabet, plus the letters Á, É, Í, Ó, Ú, Ü, and Ñ. Note that I will not include Ch, Rr, or Ll as these strings are a combination of already existing letters. I will only focus on _single_ letters.

## Design
To draw in the air, I created a program to track a brightly-colored marker, detect its contours (which should just be a circle), and thus draw colored filled circles which are overlayed on each frame from the video stream. The user presses the 'd' key to start drawing with the marker and again when they are done. The user has the option, when the shell script is executed, to record data (both time series and image), plot a certain saved letter file, and draw a letter for certain classifiers to try to identify.

In the code, I will refer to the letters with accent marks as follows
 * Á: aa
 * É: ee
 * Í: ii
 * Ó: oo
 * Ú: uu
 * Ü: uuu
 * Ñ: nn

All other letters that are also in the English language are represented by themselves (e.g. 'a' for A).

## Classification
Here are the following classification methods I used:
 * ___COMING SOON___

The rest of this document describes the directories of the project.

## Project
To run the program, you must first execute ```run.sh```. Follow the prompts given by the script to record data, plot a certain letter, and classify a drawing.
In the ```letters``` directory, you will find 33 sub-directories named after each of the letters (accented letters are named using the convention defined earlier). In each directory for each letter there are PNG and JSON files to represent the drawing and time series of the drawing, respectively.
