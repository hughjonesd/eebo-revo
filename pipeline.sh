
# overall pipeline
# could be a makefile

# sh files usually call .R/.py files with the same name

# create metadata on files
sh get-metadata.sh

# make tei-files.tab
sh list-tei-files.sh

# make lexicon from LEME files (also uses clean-eme-lexicon.R)
sh make-eme-lexicon.sh

# create texts from data/tei-files.tab
sh create-text.sh