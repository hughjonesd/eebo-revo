

from EEBOIterator import EEBOIterator
from process_tcp import get_metadata, get_text
import pandas as pd
from pathlib import Path
import itertools


def make_metadata():     
    eebo_it = EEBOIterator("data-raw/eebo-zips", debug = True)
    metadata_df = pd.DataFrame(columns = ["id", "date", "author", "title", 
                    "pub_place"])
    
    md_list = list()
    for i, xml in zip(itertools.count(), eebo_it):
        md = get_metadata(xml)
        md_list.append(md)
        if i % 100 == 0:
            metadata_df = metadata_df.append(md_list)
            md_list = list()
            metadata_df.to_csv("data/metadata.csv", index = False)

def make_texts():
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