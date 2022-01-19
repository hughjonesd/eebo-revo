

import sys
import os
import pandas as pd
import multiprocessing as mp
from process_tei import get_xml_from_line, get_metadata

def process_line(line):
    line = line.rstrip()
    print(line)
    xml = get_xml_from_line(line)
    md = get_metadata(xml)
    return md

if __name__ == "__main__":
    metadata_path = "data/metadata.csv"

    metadata_df = pd.DataFrame(columns = ["id", "date", "author", 
                        "title", "pub_place", "lang"])
    md_list = []

    pool = mp.Pool(mp.cpu_count())

    md_list = pool.map(process_line, sys.stdin.readlines())

    pool.close()

    metadata_df = metadata_df.append(md_list)

    write_header = not os.path.exists(metadata_path)
    with open(metadata_path, 'a', newline = '') as mf:
        metadata_df.to_csv(mf, index = False, header = write_header)



# problems: A47589 and friends; A30498 and friends. Why?
# it doesn't seem to be a whole zip file


