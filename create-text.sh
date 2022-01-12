#!/bin/sh

while read -r zip xml_file split; do 
  cleaned_file=$(basename -s .P5.xml $xml_file)
  if [ $split == "train" ]; then split=''; fi
  python3 create-text.py $zip $xml_file > data/texts/$split/$cleaned_file
  echo "Created $cleaned_file"
done <data/tei-files.tab 

