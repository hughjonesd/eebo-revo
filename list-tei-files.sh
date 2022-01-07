#!/bin/sh

# recreate a list of every tei file like:
# zipfile xmlfile

rm tei-files.tab

for zipfile in $(ls data-raw/eebo-zips/*.zip); do
  zipname=$(basename $zipfile)
  # grep xml removes the directory entries e.g. "B36.zip B36/"
  zipinfo -1 $zipfile | sed -e "s/^/$zipname\t/" | grep xml >> tei-files.tab
done
