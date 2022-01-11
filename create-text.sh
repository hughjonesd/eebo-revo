#!/bin/sh

while read -r zip xml_file; do 
  cleaned_file=$(basename -s .P5.xml $xml_file)
  python3 create-text.py $zip $xml_file > data/texts/$cleaned_file
  echo "Created $cleaned_file"
done <data/tei-files.tab 

