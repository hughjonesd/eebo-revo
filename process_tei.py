
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree
import zipfile
import unicodedata
import re

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
    # soup = BeautifulSoup(xml, "xml")
    doc = etree.fromstring(xml)

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

    to_unicode = lambda x: etree.tostring(x, method = "text", encoding = "unicode")
    for text in doc.findall(".//{*}text"):
        body = text.find(".//{*}body") # only one, we hope
        for _, elem in etree.iterwalk(body, tag = [*para_tags, *ignore_tags, *delete_tags]):
            # lxml plan: iterate tags and only output text:
            #  - in para_tags, surrounded by \n...\n
            #  - in ignore_tags
            #  - delete everything in gaps, except illegible gaps which we treat like ignore_tags
            if elem.tag in para_tags:
                yield "".join(["\n", to_unicode(elem), "\n"])
            elif elem.tag in ignore_tags:
                yield to_unicode(elem)
            elif elem.tag in delete_tags:
                pass # need to make sure we then skip everything in it
            elif elem.tag == tei_ns + "gap" and elem.desc == "illegible":
                yield to_unicode(elem)
            elif elem.tag == tei_ns + "choice":
                expan = elem.find("{*}expan")
                if expan is not None:
                    yield to_unicode(expan)
            elif elem.tag == tei_ns + "expan" and elem.get("ex") is not None:
                yield elem.get("ex")

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

trans_table = str.maketrans({"v":"u", "ſ":"s"})
def clean_text(text):
    global trans_table
    # remove punctuation
    # all u to v
    # all funny-s to s
    text = re.sub(r"[^\w \t\n]", "", text)
    text = text.casefold()
    text = text.translate(trans_table)
    return text
