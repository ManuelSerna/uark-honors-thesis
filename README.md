# University of Arkansas Honors Thesis Source Code
This repository contains code and data used for my undergraduate honors thesis (CSCE 491VH) at the University of Arkansas, from Fall 2019 to Spring 2020.

## Objective
The purpose of this project is to evaluate various classification methods for "air-written" letters (which I will limit to only upper-case letters for simplicity) of the Spanish alphabet. For non-Spanish speakers, this includes the 26 regular letters of the English alphabet, plus the letters Á, É, Í, Ó, Ú, Ü, and Ñ. Note that I will not include Ch, Rr, or Ll as these strings are a combination of already existing letters. I will only focus on _single_ letters.

Here are the following classification methods I used:
 * ___COMING SOON___

The rest of this document describes the directories of the project.

## Project
This directory contains:
 * __Tracker Program__: To record data, run the shell script called ```record.sh x``` where ```x``` is the letter the user wants to draw, to label a letter that has an accent, type the character twice (e.g. ```run.sh aa``` to draw the letter 'A' with an accent mark).
```sh
$ # Record data for the letter n with a tilde
$ record.sh nn
$ # Record data for the letter m
$ record.sh m
$ # And so on...
```
 * __Main Program__: This program, when executed, will allow the user to draw a letter and the program will attempt to classify what was drawn by various methods. ___COMING SOON___
 * __letters__: This is where all the letter data is stored. There are 33 subdirectories for each letter of the Spanish alphabet (including letters with accent marks).
 * __demos__: This directory contains sample images and videos of me testing the tracker and drawing.


## Testing
I test functionality, algorithms, and the like in this directory.
