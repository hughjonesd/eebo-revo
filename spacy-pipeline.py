
# Plan -------------

# specifically re the spacy implementation

# - should we translate "funny f" to s and u to v?

# how implement the lemmatizer
#  - look up in data/eme-lexicon.tab
#  - if not there, then use levenshtein distance?
#  - after the first run use word distance? (how document?)

# how to create embeddings?
#  - for the whole period
#  - for each decade

# Implementation

from pathlib import Path
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import time
import pandas as pd
from EMELemmatizer import EMELemmatizer

# how many bytes (roughly) to return per chunk
n_bytes = 1000
md_frame = pd.read_csv("data/metadata.csv")
stop_after_n_docs = -1
# import all your docs via a generator

def path_generator(paths):
    global n_bytes, md_frame

    for i, p in enumerate(paths):
        id = p.name
        metadata = md_frame[md_frame["id"] == id]
        metadata = metadata.to_dict("records") 
        if len(metadata) != 1: raise RuntimeError(f"metadata problem with text id {id}")
        metadata = metadata[0]

        if p.is_file():
            print(i)
            with p.open("r") as f:
                lines = f.readlines(n_bytes)
                while len(lines) > 0:
                    yield ("".join(lines), metadata)
                    lines = f.readlines(n_bytes)

# nlp = English()
nlp = spacy.load("en_core_web_sm")

eebo_paths = [path for path in Path("data/texts").glob("*")]

eme_lemmatizer = nlp.add_pipe("EMELemmatizer", after = "tok2vec")
docs = nlp.pipe(path_generator(eebo_paths), batch_size = 2, as_tuples = True, 
                disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
nlp.enable_pipe("EMELemmatizer")

for i, (doc, context) in enumerate(docs):
    # for tok in doc[:200]:
    #     print(f"{tok}\t\t\t\t\t{tok._.eme_lemmas}")
    found = [len(tok._.eme_lemmas) for tok in doc]
    # print(f"Found {sum(found)} out of {len(doc)} lexemes")
    if i == stop_after_n_docs: 
        break
