#!/bin/bash

# This is a simple User Management script that 
# allows to create, modify and delete users.

# Define the usage function
function usage {
  echo "Usage: $0 [create|modify|delete] [username] [full name] [password]"
  exit 1
}

# Check if the correct number of arguments are provided
if [ $# -ne 4 ]; then
  usage
fi

# Define the variables
action=$1
username=$2
fullname=$3
password=$4

# Perform the action based on the first argument
case $action in
  "create")
    # Create the user account
    useradd -c "$fullname" -m -s /bin/bash "$username"
    echo "$username:$password" | chpasswd
    echo "User account created successfully."
    ;;

  "modify")
    # Modify the user account
    usermod -c "$fullname" -s /bin/bash "$username"
    echo "$username:$password" | chpasswd
    echo "User account modified successfully."
    ;;

  "delete")
    # Delete the user account
    userdel -r "$username"
    echo "User account deleted successfully."
    ;;

  *)
    # Display the usage message if the action is not recognized
    usage
    ;;
esac

exit 0

