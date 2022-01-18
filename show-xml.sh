#!/bin/sh

text=$1

file2=$(echo $text | cut -c 1-2)
file3=$(echo $text | cut -c 1-3)

find_file () {
   	path="data-raw/eebo-zips/$1.zip"
	echo "path is $path"
	if [ -e $path ]; then
		unzip -l $path | grep -q $text
		if [ $? -eq 0 ]; then
			zip_path="$1/$text.P5.xml"
			unzip -c $path $zip_path
			exit
		fi
	fi 
}

find_file $file2
find_file $file3

