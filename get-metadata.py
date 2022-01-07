

import sys
import os
import pandas as pd
from process_tei import get_xml_from_line, get_metadata

metadata_path = "data/metadata.csv"

metadata_df = pd.DataFrame(columns = ["id", "date", "author", 
                    "title", "pub_place"])
md_list = []

for line in sys.stdin.readlines():
    line = line.rstrip()
    print(line)
    xml = get_xml_from_line(line)
    md = get_metadata(xml)
    md_list.append(md)

metadata_df = metadata_df.append(md_list)

write_header = not os.path.exists(metadata_path)
with open(metadata_path, 'a', newline = '') as mf:
    metadata_df.to_csv(mf, index = False, header = write_header)






