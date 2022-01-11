
# plan.

# tokenize
# try to lemmatize with the data/eme-lexicon.tab word list
# build a tok2vec layer and create embeddings
#  - for the whole period
#  - for each decade

import spacy

nlp = spacy.load("en_core_web_sm")