
from bs4 import BeautifulSoup, SoupStrainer
import zipfile
import unicodedata

def get_xml_from_line(line):
    """
    Returns the xml text from one zipped file in a line of tei-files.tab
    """
    zip_path, xml_path = line.split("\t")
    return get_xml(zip_path, xml_path)


def get_xml(zip_path, xml_path):
    """
    Returns the xml text from one zipped file.

    * zip_path, not including data-raw/eebo-zips
    * xml_path, within the zip file, including the folder 
      e.g. A1/A123.P5.xml in A1.zip
    """
    zip_path = f"data-raw/eebo-zips/{zip_path}"
    zf = zipfile.ZipFile(zip_path)
    xml = zf.read(xml_path)
    return xml

def get_text(xml):
    """Takes a TCP XML document and returns just the original text"""
    soup = BeautifulSoup(xml, "xml")
    # there may be more than one "text". See the <group> tag.
    body = soup.find('text').body
    gaps = body.find_all("gap", desc = "illegible")
    for g in gaps: g.unwrap()

    #   gap when "illegible": could try to keep guess
    #  g ref = '...' is special chars

    # Paragraph-like tags, denote a gap between contents
    # for now we just surround with newlines
    para_tags = ["item", "p", "label", "postscript", "q", "salute",
                 "signed", "sp", "argument", "opener", "closer", "head",
                 "note", "div1", "div2", "div3", "div4", "div5", 
                 "div6", "div7", "lg", "postscript", "headnote", "tailnote"]
    doc_para_tags = body.find_all(para_tags)
    for t in doc_para_tags: 
        t.insert(0, "\n")
        t.append("\n")
        t.unwrap()

    # Not real text, delete contents
    delete_tags = ["gap", "bibl", "figDesc", "fw", "table", "vid"]
    doc_delete_tags = body.find_all(delete_tags)
    for t in doc_delete_tags: t.decompose()

    # Irrelevant, ignore but keep contents in place
    ignore_tags = ["sub", "sup", "signed", "add", "del", "above", "hi", 
                   "below", "lb", "dateline", "date", "figure", 
                   "l", "milestone", "pb", "ref", "unclear", "g"]
    doc_ignore_tags = body.find_all(ignore_tags)
    for t in doc_ignore_tags: t.unwrap() # how add spaces? do we need?

    choice_tags = body.find_all("choice")
    for t in choice_tags:
        if t.expan is not None:
            t.replace_with(t.expan.string)
        else:
            t.unwrap() # I guess?
    expan_tags = body.find_all("expan")
    for t in expan_tags: 
        if t.ex is not None: 
            t.replace_with(t.ex.string)
        else:
            t.decompose()
    
    # <choice><abbr></abbr><expan></expan>
    # you sometimes want to just replace with expan

    # todo with the text itself (maybe separate fn)
    # - get rid of newlines? (but before we inserted them to have meaning)
    # "f" to s?
    # "v" to u?
    # lowercase everything?
    # get rid of punctuation alone? (probably not via b.s. though)
    # replace cmbAbbrStroke with n sometimes 
    # (maybe a good lemmatizer will deal with this)

    return body.get_text()

def get_metadata(xml):
    """Takes a TCP XML document and returns informative metadata"""
    just_the_header = SoupStrainer("teiHeader")
    soup = BeautifulSoup(xml, "xml", parse_only = just_the_header)
    fd = soup.fileDesc
    id = fd.publicationStmt.find("idno", type = "DLPS").string
    try:
        # just the first title
        title = fd.titleStmt.title
        if title is not None: title = title.string
        author = fd.titleStmt.author
        if author is not None: author = author.string
        date = fd.editionStmt.edition.date
        if date is not None: date = date.string
        pub_place = fd.sourceDesc.biblFull.publicationStmt.pubPlace
        if pub_place is not None: pub_place = pub_place.string
    except:
        raise RuntimeError(f"Problem in id {id}")

    return {'id': id, 'author': author, 'title': title, 'date': date, 
            'pub_place': pub_place}

def normalize_unicode(str):
    return unicodedata.normalize('NFC', str)