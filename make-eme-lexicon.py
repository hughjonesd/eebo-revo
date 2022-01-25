
import re
import sys
import os
from lxml import etree
import configsh
# unicode definition of punctuation
re.ASCII = False


lexicon_path = sys.argv[1]
output_path = f"{configsh.LEME_SCRATCH_DIR}/{os.path.basename(lexicon_path)}"
output_file = open(output_path, 'w')

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
    # in fact that ain't so
    lexeme = form.get("lexeme")
    if not isinstance(lexeme, str): return nowt
    lex_match = re.match(r"(.*?)(\(.+\))", lexeme)
    if lex_match is None: return nowt
    lex_word = lex_match[1]
    lex_type = lex_match[2]
    lex_type = lex_type[1:-1] # remove brackets
    # skip multiword lexemes
    if " " in lex_word: return nowt 
    return lex_word, lex_type




for _, wordentry in  etree.iterparse(lexicon_path, tag = "wordentry", 
                                     recover = True):
    lexeme = None
    l_type = None
    for form in wordentry.iter("form"):
        # get rid of "<note>" tags, which are common in one
        # lexicon
        etree.strip_elements(form, "note", with_tail = False) 
        word = etree.tostring(form, method = "text", 
                              encoding = "unicode")
        if word is None: continue
        # form text can be very long, and if so
        # it's unlikely to always have the first word right
        if len(word) > 25: continue
        # can contain spaces or "the ..."
        # or "A...":
        # or a bonus '">' and material around it from bad xml
        word = re.sub(r"^an?\s+", "", word, re.IGNORECASE)
        word = re.sub(r"^the\s+", "", word, re.IGNORECASE)
        word = re.sub(r"^to\s+", "", word, re.IGNORECASE)
        word = re.sub(r"&#182;\s+", "", word)
        word = re.sub(r"^.*?>\W*", "", word)
        # we take the first word, up to spaces:
        try:
            word = word.split()[0]
        except:
            continue

        # get rid of punctuation at the end:
        word = re.sub(r"\W+$", "", word)
        # get rid of dashes:
        word = word.replace("-", "")
        # get rid of '##sp##' which occurs in one lexicon
        word = word.replace("##sp##", "")
        word = word.lower()
        lexeme, l_type = get_lexeme(form)   
        if lexeme is None:
            for xpln in wordentry.iter("xpln"):
                lexeme, l_type = get_lexeme(xpln)
        if lexeme is not None and len(word) > 0:
            output_file.write(f"{word}\t{lexeme}\t{l_type}\n")

    wordentry.clear(keep_tail = True)

output_file.close()
