
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree
import zipfile
import unicodedata
import re

def get_xml_from_line(line):
    """
    Returns the xml text from one zipped file in a line of TEI-files.tab
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
        lang = soup.profileDesc.langUsage.language.get("ident")
    except:
        raise RuntimeError(f"Problem in id {id}")

    return {'id': id, 'author': author, 'title': title, 'date': date, 
            'pub_place': pub_place, 'lang': lang}


def to_unicode(elem):
    """Returns the text of an element as unicode."""
    text = etree.tostring(elem, method = "text", encoding = "unicode")
    return text


def get_text(xml):
    """Takes a TCP XML document and returns just the original text"""
    doc = etree.fromstring(xml)

    lang = doc.find("./{*}teiHeader/{*}profileDesc/{*}langUsage/{*}language").get("ident")
    if lang != "eng":
        return
    
    para_tags = ["item", "p", "label", "postscript", "q", "salute",
                 "signed", "sp", "argument", "opener", "closer", "head",
                 "note", "div1", "div2", "div3", "div4", "div5", 
                 "div6", "div7", "lg", "postscript", "headnote", "tailnote"]
    
    ignore_tags = ["sub", "sup", "signed", "add", "del", "above", "hi", 
                    "below", "lb", "dateline", "date", "figure", 
                    "l", "milestone", "pb", "ref", "unclear", "g"]

    delete_tags = ["gap", "bibl", "figDesc", "fw", "table", "vid"]

    tei_ns = "{http://www.tei-c.org/ns/1.0}"  
    para_tags = [tei_ns + t for t in para_tags]
    ignore_tags = [tei_ns + t for t in ignore_tags]
    delete_tags = [tei_ns + t for t in delete_tags]
    for text in [*doc.findall(".//{*}text[@{http://www.w3.org/XML/1998/namespace}lang='eng']"), 
                 *doc.findall(".//{*}text[@{http://www.w3.org/XML/1998/namespace}lang='unk']")]:
        body = text.find(".//{*}body") # only one, we hope
        for eol_hyphen in body.findall(".//{*}g[@ref='char:EOLhyphen']"):
            eol_hyphen.clear(keep_tail = True)
        for abbr_stroke in body.findall(".//{*}g[@ref='char:cmbAbbrStroke']"):
            abbr_stroke.tail = "~" + abbr_stroke.tail
            abbr_stroke.clear(keep_tail = True)
        for margin_note in body.findall(".//{*}note[@place='margin']"):
            margin_note.clear(keep_tail = True)
        etree.strip_elements(body, *delete_tags, with_tail = False)
        yield(to_unicode(body))

    # still todo:
    # replace <choice> ... <expan></expan> </choice> just with contents of expan
    # <expan ex="blah" /> just with blah


def normalize_unicode(str):
    return unicodedata.normalize('NFC', str)


# remove punctuation
# all u to v
# all funny-s to s
# . and , to space
trans_table = str.maketrans({
                            "v" : "u", 
                            "ſ" : "s", 
                            "." : " ", 
                            "," : " ", 
                            ";" : " ", 
                            ":" : " ",
                            })
def clean_text(text):
    global trans_table
    text = text.translate(trans_table)
    text = re.sub(r"[^\w \t\n~]", "", text)
    text = text.casefold()
    return text
