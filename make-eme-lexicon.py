
import sys
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

output_path = "data/eme-lexicon.tab"
lexicon_path = sys.argv[1]

def get_lexeme(node):
    """Returns a lexeme and type, or (None, None)"""
    nowt = (None, None)
    # You only want ones with lang=en
    # but lang isn't always set
    if node.get("lang") is not None and node.get("lang") != "en":   
        return nowt

    # lexeme can be in form, or in xpln
    # there can be multiple lexeme attributes
    # i.e. not valid xml :P
    # we just grab the first and pray
    # documentation says that multiple lexemes should
    # be separated by |
    lexeme = form.get("lexeme")
    # foo(n)
    

for _, wordentry in  etree.iterparse(lexicon_path, tag = "wordentry", 
                                     recover = True):
   """
   <wordentry type="h"><form lang="en" lexeme="absurdity(n)">Absurditie,</form> 
  <xpln lang="en">a thing clean contrary (or at least wise irksom)
  too reason, suche a thing as it greeueth a man too heere it,
  irksomnesse, fondnesse.</xpln></wordentry>
   """
    del lexeme
    for form in wordentry.iter("form"):
        word = form.text
        # form text can be very long; can contain spaces or "the ..."
        # may be mix of lower and upper
        if len(word) >= 25: continue
        word = word.lstrip()
        word = word.rstrip()
        lexeme, l_type = get_lexeme(form)   
        if lexeme is None:
            for xpln in wordentry.iter("xpln"):
                lexeme, l_type = get_lexeme(xpln)

    # write word, lexeme, type to 
    output_file.write(f"{word}\t{lexeme}\t{l_type}\t")
    wordentry.clear(keep_tail = True)
