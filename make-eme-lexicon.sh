#!/bin/sh

source ./configsh.py

rm -f $LEME_SCRATCH_DIR/*
mkdir -p $LEME_SCRATCH_DIR

for lexicon in data-raw/LEME/*.txt; do
  python make-eme-lexicon.py $lexicon
done

cat $LEME_SCRATCH_DIR/* | sort > data/eme-lexicon.tab


Rscript clean-eme-lexicon.R data/eme-lexicon.tab
