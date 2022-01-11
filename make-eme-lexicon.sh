
for lexicon in data-raw/leme/*.txt; do
  python make-eme-lexicon.py $lexicon
done

cat data/leme-cleaned/* | sort > data/eme-lexicon.tab
# rm data/leme-cleaned/*

R clean-eme-lexicon.R data/eme-lexicon.tab
