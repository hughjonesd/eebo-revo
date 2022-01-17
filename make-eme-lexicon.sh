#!/bin/sh

mkdir -p data/leme-cleaned

for lexicon in data-raw/LEME/*.txt; do
  python make-eme-lexicon.py $lexicon
done

cat data/leme-cleaned/* | sort > data/eme-lexicon.tab
# rm data/leme-cleaned/*

Rscript clean-eme-lexicon.R data/eme-lexicon.tab
