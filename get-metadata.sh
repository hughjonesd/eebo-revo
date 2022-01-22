#!/bin/bash

#SBATCH --mail-type=ALL
#SBATCH --mail-user=davidhughjones@gmail.com
#SBATCH --exclusive
#SBATCH -o get-metadata.sh-%j.out
#SBATCH -e get-metadata.sh-%j.err

for zipfile in $(ls data-raw/eebo-zips/*.zip); do
  zipname=$(basename $zipfile)
  # grep xml removes the directory entries e.g. "B36.zip B36/"
  zipinfo -1 $zipfile | sed -e "s/^/$zipname\t/" | grep xml | python3 get-metadata.py
done
