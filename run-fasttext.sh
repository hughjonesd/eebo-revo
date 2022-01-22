#!/bin/sh

#SBATCH --mail-type=ALL
#SBATCH --mail-user=davidhughjones@gmail.com
#SBATCH --partition=compute-24-128
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=120G
#SBATCH -o run-fasttext.%j.out
#SBATCH -e run-fasttext.%j.err

# create fastText embeddings using all the training files

# about how many files to randomly select for input
n_files=5000

# number of threads to use in fasttext
n_threads=1

# seed RANDOM number generator
RANDOM=1027

tot_files=$(ls data/texts | wc -l)
prob=$((32767*$n_files/$tot_files))

rm data/fasttext-input

for f in data/texts/*; do 
  if [ $RANDOM -le $prob ]; then
    cat $f >> data/fasttext-input
  fi
done
./fastText-0.9.2/fasttext skipgram -input data/fasttext-input -output data/fasttext-vectors -thread $n_threads -epoch 1 -minCount 20 -dim 300 
