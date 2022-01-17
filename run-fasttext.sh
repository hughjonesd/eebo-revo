#!/bin/sh

# about how many files to randomly select for input
n_files=50000
# n_files=1000

# seed RANDOM number generator
RANDOM=1027

tot_files=$(ls data/texts | wc -l)
prob=$((32767*$n_files/$tot_files))

for f in data/texts/*; do 
  if [ $RANDOM -le $prob ]; then
    cat $f >> data/fasttext-input
  fi
done
./fastText-0.9.2/fasttext skipgram -input data/fasttext-input -output data/fasttext-vectors -thread 4 -epoch 1 
