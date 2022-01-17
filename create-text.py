
# for each file
# normalize the unicode

import sys
from process_tei import get_text, get_xml, normalize_unicode, clean_text

zf = sys.argv[1]
xml_path = sys.argv[2]

xml = get_xml(zf, xml_path)
for text in get_text(xml):
    text = normalize_unicode(text)
    text = clean_text(text)
    print(text)


