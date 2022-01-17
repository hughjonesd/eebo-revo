
# overall pipeline
# could be a makefile

# sh files usually call .R/.py files with the same name
# if possible, policy decisions should be in the .sh 
# files and passed to scripts as arguments


# get the eebo zipfiles from dropbox if you haven't already
sh download-eebo-zips.sh

# create metadata on files
sh get-metadata.sh

# make data/tei-files.tab, list of files
# also decide which is test, which is train
sh list-tei-files.sh

# make lexicon from LEME files 
# also uses clean-eme-lexicon.R
sh make-eme-lexicon.sh

# create texts from data/tei-files.tab
# also uses process_tei.py, a python library
sh create-text.sh

# run FastText to create vectors
sh run-fasttext.sh