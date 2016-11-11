#!/bin/bash

if [ -z "$1" ]
	then
		echo "No argument supplied"
        exit 1
fi

directory=$1

for f in $directory/*.text
	do
		python -m markdown -o 'html5' -x markdown.extensions.footnotes "$f" > "${f%.text}.html"
	done
