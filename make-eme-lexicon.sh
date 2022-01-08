
for lexicon in data-raw/LEME/*.txt; do
  make-eme-lexicon.py $lexicon
done