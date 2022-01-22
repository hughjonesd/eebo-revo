#!/bin/bash

#SBATCH --mail-type=ALL
#SBATCH --mail-user=davidhughjones@gmail.com
#SBATCH -o create-text.sh-%j.out
#SBATCH -e create-text.sh-%j.err
#SBATCH --exclusive
# create the raw EEBO text files from the XML in zips

batchsize=100

mkdir -p data/texts/test

while read -r zip xml_file split; do 
  
  cleaned_file=$(basename -s .P5.xml $xml_file)
  if [ $split = "train" ]; then split=''; fi
  output=data/texts/$split/$cleaned_file

  if [ ! -e $output ]; then
    ((i=i%batchsize)); ((i++==0)) && wait
    python3 create-text.py $zip $xml_file > $output &
    echo "Created $output"
  fi

done <data/TEI-files.tab 

wait

