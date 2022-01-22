#!/bin/sh

#SBATCH --mail-type=ALL
#SBATCH --mail-user=davidhughjones@gmail.com
#SBATCH -o list-TEI-files.sh-%j.out
#SBATCH -e list-TEI-files.sh-%j.err

# recreate a list of every tei file like:
# zipfile xmlfile

tei_files_path='data/TEI-files.tab'
test_prop=0.2

rm $tei_files_path

for zipfile in $(ls data-raw/eebo-zips/*.zip); do
  zipname=$(basename $zipfile)
  # grep xml removes the directory entries e.g. "B36.zip B36/"
  zipinfo -1 $zipfile | sed -e "s/^/$zipname\t/" | grep xml >> $tei_files_path
done

n_files=$(wc -l < $tei_files_path) # using < means we don't get the file name included

python3 test-train-split.py $tei_files_path $test_prop
