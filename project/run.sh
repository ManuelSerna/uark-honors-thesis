#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Purpose: This Bash script can execute a variety of programs, whose functionalities are described in the prompt.
#
# Here is a rundown of what each program called by this script does:
#   - record_data.py: Record data for training data set (option 1) or testing data set (option 4).
#   - plot_data.py: Compare the time series plots for two given letters.
#   - visual_letters.py: Plot all letter data onto a scatter plot.
#   - classify_data.py: Given training data, compute the accuracies of all classifiers for every letter.
#
# Author: Manuel Serna-Aguilera
# University of Arkansas, Fayetteville
# Spring 2020
#*********************************

# NOTE: "$?" is the value most recently returned by a function

# Choice for which program to execute
choice='00'

# When writing/reading files, all names will fall into the following regular expression
# a-z, or aa, ee, ii, oo, uu, uuu, nn
re='^([a-z]|aa|ee|ii|oo|uu|uuu|nn)$'



#=================================
# Function: print choices and prompt
#=================================
prompt () {
    echo "*********************************"
    echo "Actions to execute"
    echo "  1: Enter training data."
    echo "  2: Plot (training) time series."
    echo "  3: Plot (training) data."
    echo "  4: Enter test data."
    echo "  5: Classify recorded test data."
    echo "  6: Demo tracking and classification."
    echo ""
    echo "  0: Exit program."
    echo "*********************************"
    echo "Enter choice below:"
    read choice
    return $choice
}

error_message () {
    echo "  Error: invalid input! Try again."
}



#=================================
# Continuosly run program until user inputs nothing or exits
#=================================
while [ $choice != '0' ]
do
    # First, prompt user
    prompt
    
    #---------------------------------
    # 1. Record training data
    #---------------------------------
    if [ $choice == '1' ]
    then
        echo ""
        echo "  Enter true label for training data:"
        read letter
        
        if [[ $letter =~ $re ]]
        then
            echo "  Recording training data."
            python record_data.py '1' $letter
            echo "  Training data capture done."
        else
            error_message
        fi
    
    #---------------------------------
    # 2. Plot two time series from training data
    #---------------------------------
    elif [ $choice == '2' ]
    then
        echo "  Plot training data time series."
        
        echo "  Letter 1:"
        read letter1
        echo "  Letter ID 1:"
        read num1
        
        echo "  Letter 2:"
        read letter2
        echo "  Letter ID 2:"
        read num2
        
        python plot_data.py $letter1 $num1 $letter2 $num2
        
    #---------------------------------
    # 3. Plot training data samples
    #---------------------------------
    elif [ $choice == '3' ]
    then
        data_type='d'
        echo "  Plotting all data samples."
        echo -e "  Plot:\n[d]: all data samples\n[c]: all centroids"
        read data_type
        
        python visual_letters.py $data_type
    
    #---------------------------------
    # 4. Record testing data
    #---------------------------------
    elif [ $choice == '4' ]
    then
        echo "  Enter true label for test data:"
        read letter
        
        if [[ $letter =~ $re ]]
        then
            echo "  Recording testing data."
            python record_data.py '2' $letter
            echo "  Testing data capture done."
        else
            error_message
        fi
        
        echo ""
    
    #---------------------------------
    # 5. Classify test data
    #---------------------------------
    elif [ $choice == '5' ]
    then
        echo "  Writing results to file."        
        python classify_data.py
    
    #---------------------------------
    # 6. Demo--capture air-written letter and attempt to classify it.
    #---------------------------------
    elif [ $choice == '6' ]
    then
        echo "  Enter true label:"
        read letter
        
        python demo.py $letter
        
    fi # end considering $choice
    
    echo ""
    echo ""
done
echo "Done."
