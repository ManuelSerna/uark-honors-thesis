#*********************************
# Honors Thesis Hand Tracking and Classification Project
# Program: shell script to run the following programs based on user input
#   - capture.py-- record labeled data for a specified letter
#   - plot_data.py-- allows user to plot the time series for a specified letter
#   - TODO: -- captures air-written letter and classifies letter with various methods
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
    echo "  2: Plot a letter."
    echo "  3: COMING SOON--classify air-written letter"
    # TODO: include a practice option? Update README if I dos
    echo "  0: Exit program."
    echo "*********************************"
    echo "Enter choice below:"
    read choice
    return $choice
}

error_message () {
    echo "  Error: invalid input! Try again."
}



# Continuosly run program until user inputs nothing or exits
while [ $choice != '0' ]
do
    # First, prompt user
    prompt
    
    # Execute programs given choice
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
            python capture.py $letter
            echo "  Data capture done."
        else
            error_message
        fi
    
    elif [ $choice == '2' ]
    then
        echo '  Select a letter to plot.'
        read letter
        echo "  Enter letter file number (0-9): "
        read number
        local numbers='^[0-9]$' # regular expression for one number
        
        if [[ $letter =~ $re ]] && [[ $number =~ $numbers ]]
        then
            echo "  Plotting data."
            python plot_data.py $letter $number
        else
            error_message
        fi
        
    
    elif [ $choice == '3' ]
    then
        echo '  TODO: classify drawn letter'
        # TODO: include classifier program here
    fi
    
    echo "" # filler new-lines
    echo ""
    echo ""
done

echo "Done."
