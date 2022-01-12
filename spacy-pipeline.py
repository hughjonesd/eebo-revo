


# Plan -------------

# should communicate document metadata from within the path_generator
# something like:
# from spacy.tokens import Doc, Token, Span
# Doc.set_extension("title", default=None)
# then doc._.title = whatever

# specifically re the spacy implementation
# - should we translate "funny f" to s and u to v?

# how implement the lemmatizer
#  - look up in data/eme-lexicon.tab
#  - if not there, then use levenshtein distance?

#


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
# import all your docs via a generator

def path_generator(paths):
    global n_bytes, md_frame

    for p in paths:
        id = p.name
        metadata = md_frame[md_frame["id"] == id]
        metadata = metadata.to_dict("records") 
        if len(metadata) != 1: raise RuntimeError(f"metadata problem with text id {id}")
        metadata = metadata[0]

        if p.is_file():
            print(p)
            with p.open("r") as f:
                lines = f.readlines(n_bytes)
                while len(lines) > 0:
                    yield ("".join(lines), metadata)
                    lines = f.readlines(n_bytes)


# tokenize
# try to lemmatize with the data/eme-lexicon.tab word list
#   - standard lemmatizer lookup format is just json like {"Argentines": "Argentine", ...}
#   - but a simpler approach might be to subclass the Lemmatizer and just override lookup_lemmatize()
#   - useful example here: https://github.com/Liebeck/spacy-iwnlp
#
# build a tok2vec layer and create embeddings
#  - for the whole period
#  - for each decade

nlp = English()
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
    print(f"Found {sum(found)} out of {len(doc)} lexemes")
    if i >= 20: 
        break



# Create a blank Tokenizer with just the English vocab
#tokenizer = Tokenizer(nlp.vocab)
#tokenizer()