
# custom lemmatizer

from spacy.tokens import Token
from spacy.language import Language
import pandas as pd

@Language.factory('EMELemmatizer')
class EMELemmatizer(object):
    def __init__(self, nlp, name):
        # force overwrites any other lemmatizer
        Token.set_extension('eme_lemmas', getter = self.get_lemmas, force = True)
        lt = pd.read_table("data/eme-lexicon.tab", names = ["word", "lexeme"], index_col = "word")
        self.lookup_table = lt["lexeme"].to_dict()
        self.name = name
        self.nlp = nlp

    def __call__(self, doc):
        for token in doc:
            token._.eme_lemmas = self.get_lemmas(token)
        return doc

    def get_lemmas(self, token):
        text = token.text.lower()
        if text in self.lookup_table:
            return [ self.lookup_table[text] ]
        else:
            return []
