#!/bin/bash

if [ -z "$1" ]
	then
		echo "No argument supplied"
        exit 1
fi

directory=$1

for f in $directory/*.text
	do
        echo $f && head -n 1 $f
	done
