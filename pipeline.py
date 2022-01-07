

from EEBOIterator import EEBOIterator
from process_tei import get_metadata, get_text
import pandas as pd
from pathlib import Path
import itertools
import os.path

def make_metadata():  
    metadata_file = "data/metadata.csv" 
    eebo_it = EEBOIterator()

    if os.path.exists(metadata_file):
        metadata_df = pd.read_csv(metadata_file)
    else:
        metadata_df = pd.DataFrame(columns = ["id", "date", "author", 
                    "title", "pub_place"])
    
    md_list = list()
    i = 0
    for filepath in eebo_it:
        # id = filepath.name.removesuffix(".P5.xml")
        # if id in metadata_df.id.values:
        #    continue
        xml = filepath.read_text()
        md = get_metadata(xml)
        md_list.append(md)
        i += 1
        if i % 100 == 0:
            metadata_df = metadata_df.append(md_list)
            md_list = list()
            metadata_df.to_csv(metadata_file, index = False)

def make_texts():
    eebo_it = EEBOIterator(debug = True)
    for xml in eebo_it:
        md  = get_metadata(xml)
        raw = get_text(xml)
        data_file = Path("data")/"raw-text"/md["id"]
        with open(data_file, "w") as df:
            df.write(raw)

make_metadata()

# import spacy
# nlp = spacy.blank("en")
# nlp.max_length = 10_000_000
# eebo_iterator = EEBOIterator("data-raw/eebo-zips")
#
# eebo_pipe = nlp.pipe(eebo_iterator, batch_size = 2)
# doc1 = next(eebo_pipe)
# print(doc1)