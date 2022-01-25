#!/bin/sh

#SBATCH --mail-type=ALL
#SBATCH --mail-user=davidhughjones@gmail.com
#SBATCH --partition compute-16-64
#SBATCH --ntasks=4
#SBATCH --ntasks-per-node=4
#SBATCH --mem=16G
#SBATCH -o run-fasttext.%j.out
#SBATCH -e run-fasttext.%j.err

# create fastText embeddings using all the training files

module add gcc/11.1.0

source ./configsh.py

# about how many files to randomly select for input
n_files=5000

# number of threads to use in fasttext
n_threads=3

# seed RANDOM number generator
RANDOM=1027

tot_files=$(ls data/texts | wc -l)
prob=$((32767*$n_files/$tot_files))

#rm data/fasttext-input

#for f in data/texts/*; do 
#  if [ $RANDOM -le $prob ]; then
#    cat $f >> data/fasttext-input
#  fi
#done
./fastText-0.9.2/fasttext skipgram -input data/fasttext-input -output data/fasttext-vectors -thread $n_threads -epoch 1 -minCount 10 -dim $FASTTEXT_DIMS -bucket 1000000
