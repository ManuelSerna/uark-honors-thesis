#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Program: shell script to run the following programs based on user input
#   - capture.py-- record labeled data for a specified letter
#   - plot_data.py-- allows user to plot the time series for a specified letter
#   - analyze_time_series.py-- analyze time series to classify a letter
# Author: Manuel Serna-Aguilera
# University of Arkansas, Fayetteville
# Spring 2020
#*********************************

# NOTE: "$?" is the value most recently returned by a function

# Global vars
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
    echo "  1: Record data."
    echo "  2: Compare time series."
    echo "  3: Classify air-written letter."
    # TODO: include a practice option? Update README if I do
    echo "  0: Exit program."
    echo "*********************************"
    echo "Enter choice below:"
    read choice
    return $choice
}

#=================================
# Function: print general error message
#=================================
error_message () {
    echo "  Error: invalid input! Try again."
}


#---------------------------------
# Continuosly run program until user inputs nothing or exits
#---------------------------------
while [ $choice != '0' ]
do
    # First, prompt user
    prompt
    
    #---------------------------------
    # 1. Record data
    #---------------------------------
    if [ $choice == '1' ]
    then
        echo ""
        echo "  Pick a letter to draw: "
        read letter
        #echo "  Enter letter file number (0-5): "
        #read number
        
        if [[ $letter =~ $re ]]
        then
            echo "  Recording data."
            python record_data.py $letter
            echo "  Data capture done."
        else
            error_message
        fi
    
    #---------------------------------
    # 2. Visualize two time series
    #---------------------------------
    elif [ $choice == '2' ]
    then
        numbers='^[1-9]$' # regular expression for one number
        num2="" # initialize num2 to be empty
        
        #.................................
        # Prompt user
        #.................................
        echo "  Enter FIRST letter to plot:"
        read letter1
        echo "  Enter FIRST letter file number (1-9): "
        read num1
        
        echo "  Enter SECOND letter to plot."
        #echo "  Or press ENTER to skip"
        read letter2
        
        # If user will enter a second letter, check that it will fall into the regular expression
        if [[ ! -z $letter2 ]] && [[ $letter2 =~ $re ]]
        then
            echo "  Enter SECOND letter file number (1-9): "
            read num2
        else
            echo 
        fi
        
        #.................................
        # With inputs, plot time series
        #.................................
        if [[ $letter1 =~ $re ]] && [[ $num1 =~ $numbers ]] && [[ $num2 =~ $numbers ]]
        then
            echo "  Plotting data."
            python visualize_time_series.py $letter1 $num1 $letter2 $num2
        else
            error_message
        fi
        
    #---------------------------------
    # 3. Classify air-written letter
    #---------------------------------
    elif [ $choice == '3' ]
    then
        echo '  TODO: classify drawn letter'
        python analyze_time_series.py
    fi
    
    echo ""
    echo ""
    echo ""
done

echo "Done."
