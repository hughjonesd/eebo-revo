
from bs4 import BeautifulSoup


def get_text(xml):
    """Takes a TCP XML document and returns just the original text"""
    soup = BeautifulSoup(xml, "xml")
    # there may be more than one "text". See the <group> tag.
    body = soup.text.body
    gaps = body.find_all("gap", desc = "illegible")
    gaps.unwrap()

    gaps = body.find_all("gap")
    for g in gaps: g.decompose()
    # Different tags:
    #   g contains special characters, sometimes hyphens
    #   <g ref="char:cmbAbbrStroke"/> abbreviates one or more chars. Maybe just
    #   replace with a single "ambiguous character"?
    # Paragraph-like tags (could just replace with space?): 
    #   item, p, label, postscript, q, salute, signed, sp
    #     argument, opener, closer, head, hi, note
    #   div1, div2... div7
    #   lg ("verse" of poetry)
    #   postscript
    #   tailnote & headnote
    # Not real text, delete contents
    #   gap (except when "illegible"?)
    #   bibl
    #   figDesc
    #   fw (running head)
    #   table (we don't know what goes where)
    #   vid
    # Irrelevant, ignore but keep contents in place (add spaces!)
    #   sub, sup, signed, add, del, above, below, lb
    #   dateline, date (though might be useful for metadata!)
    #   figure (may have text within "head")
    #   l (line of poetry)
    #   milestone
    #   pb (page break)
    #   ref (marks text)
    #   unclear (doubtful text)


def get_metadata(xml):
    """Takes a TCP XML document and returns informative metadata"""
    soup = BeautifulSoup(xml, "xml")
    fd = soup.TEI.teiHeader.fileDesc
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


if __name__ == "__main__":
    from EEBOIterator import EEBOIterator
    eebo_it = EEBOIterator("data-raw/eebo-zips")
    text1 = next(eebo_it)
    metadata = get_metadata(text1)
    print(metadata)
