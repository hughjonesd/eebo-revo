


# Plan -------------

# should communicate document metadata from within the path_generator
# specifically re the spacy implementation
# - should we translate "funny f" to s and u to v?
# how implement the lemmatizer


# Implementation


from pathlib import Path
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import time

# how many bytes (roughly) to return per chunk
n_bytes = 1000

# import all your docs via a generator

def path_generator(paths):
    global n_bytes
    for p in paths:
        if p.is_file():
            print(p)
            with p.open("r") as f:
                lines = f.readlines(n_bytes)
                while len(lines) > 0:
                    yield "".join(lines)
                    lines = f.readlines(n_bytes)


# tokenize
# try to lemmatize with the data/eme-lexicon.tab word list
# build a tok2vec layer and create embeddings
#  - for the whole period
#  - for each decade

nlp = English()

eebo_paths = [path for path in Path("data/texts").glob("*")]

# p = path_generator(eebo_paths)
# print(next(p))
# print(next(p))
# exit()

docs = nlp.pipe(path_generator(eebo_paths), batch_size = 2)

for i, doc in enumerate(docs):
    pass


# Create a blank Tokenizer with just the English vocab
#tokenizer = Tokenizer(nlp.vocab)
#tokenizer()