# Regular expressions practice

echo "Edit file to change regular expression."
echo "Enter string to test against: "
read input

# NOTE: start regular expressions with the "^" and end them with "$" to indicate the start and end

re='^[0-9]$' # only one number 0-9

if [[ $input =~ $re ]]
then
    echo "Pass."
else
    echo "Fail."
fi
