
# overall pipeline
# could be a makefile

# sh files usually call .R/.py files with the same name
# if possible, policy decisions should be in the .sh 
# files and passed to scripts as arguments


# start R in the project directory. It should auto-install renv.
# Run renv::restore() to install needed R libraries

# You'll need python 3.9
# One approach via conda
conda create env
conda activate env
conda install python=3.9

# Create a python virtual environment:
python3 -m venv env

# And activate it:
source env/bin/activate

# Install libraries with pip
python3 -m pip install -r requirements.txt

# download and make fastText
wget https://github.com/facebookresearch/fastText/archive/v0.9.2.zip
unzip v0.9.2.zip
cd fastText-0.9.2
make

# get the eebo zipfiles from dropbox if you haven't already
sh download-eebo-zips.sh

all: run-fasttext
.PHONY: all

# create metadata on files
data/metadata.csv:
	sh get-metadata.sh

# make data/TEI-files.tab, list of files
# also decide which is test, which is train
data/TEI-files.tab: data/metadata.csv
	sh list-tei-files.sh

# make lexicon from LEME files 
# also uses clean-eme-lexicon.R
make-eme-lexicon: 
	sh make-eme-lexicon.sh

# create texts from data/TEI-files.tab
# also uses process_tei.py, a python library
create-text: data/TEI-files.tab
	sh create-text.sh
.PHONY: create-text

fasttext_vectors = data/fasttext-vectors.bin data/fasttext-vectors.vec

${fasttext_vectors}: create-text
	sh run-fasttext.sh

# run FastText to create vectors
run-fasttext: ${fasttext_vectors}
.PHONY: run-fasttext

# using vectors make word pairs to treat as "same"
data/similar-words.tab: run-fasttext
	python3 make-fasttext-dists.py

# using word pairs from the above in data/similar-words.tab, make lexicon
data/fasttext-lexicon.tab: data/similar-words.tab
	python3 make-fasttext-lexicon.py

