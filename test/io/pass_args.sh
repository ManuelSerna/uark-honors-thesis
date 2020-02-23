# Pass command line arguments from command line to program 

letter="$1"

# Check if argument is empty string
if [ -z "$letter" ]
then
    echo "Error: ..."
else
    python cmd_ln_args.py $letter
    echo "Done."
fi

echo ""
echo "Exiting."
