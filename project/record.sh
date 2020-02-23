#!/bin/bash
# Track colored object and record data
# Example of running this script: "$ record.sh a"

letter="$1"

if [ -z "$letter" ]
then
    echo "Error: No cmd line argument given for character to be drawn!"
else
    python capture.py $letter
    echo "Data capture done."
fi
