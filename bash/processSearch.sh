#!/bin/bash

# Script performs the search among running processes.
# The search can be done by "process name", "part of the name" or "id", depending on user's choice.
# If the process is found, it may be killed.

function isProcessRunning(){
	if [ $? = 0 ]
	then
		echo "The process was found. Do you want to kill it? (Y/N)"
		read killProcess
	else
		echo "The process is not running"
	fi
}

echo "Enter how you want to make a search"
echo "(1 - by Process Name, 2 - by Part of the Process Name, 3 - by Process ID)"
read userInput

if [ $userInput = 1 ]
then
	echo "Enter Process Name: "
	read processName
	ps -aux | awk '{print $11}' | grep -w $processName
	isProcessRunning
	if [ $killProcess = "Y" ] ||  [ $killProcess = "y" ]
	then
		kill $(ps -aux | grep -w $processName | awk '{print $2}') 2>/dev/null
		echo "The process was closed."
	fi
elif [ $userInput = 2 ]
then
	echo "Enter the Part of the Process Name: "
	read partProcessName
	ps -aux | awk '{print $11}' | grep $partProcessName
	isProcessRunning
	if [ $killProcess = "Y" ] ||  [ $killProcess = "y" ]
	then
		kill $(ps -aux | grep $partProcessName | awk '{print $2}') 2>/dev/null
		echo "The process was closed."
	fi
elif [ $userInput = 3 ]
then
	echo "Enter Process ID: "
	read processId
	ps -aux | awk '{print $2}' | grep -w $processId
	isProcessRunning
	if [ $killProcess = "Y" ] ||  [ $killProcess = "y" ]
	then
		kill $(ps -aux | awk '{print $2}' | grep -w $processId) 2>/dev/null
		echo "The process was closed."
	fi
fi
