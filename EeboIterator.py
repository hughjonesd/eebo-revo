
from pathlib import Path
import zipfile

class EeboIterator:
    """
    Iterates through all the zipfiles in a folder
    
    * Extracts items in turn and returns the raw text
    """
    def __init__(self, folder):
        folder = Path(folder)
        self.zip_dir_iterator = folder.iterdir()
        self.zipfile_path = None
        self.zipfile_iterator = None

        # add all the zip files

    def __iter__(self):
        return self

    def __next__(self):
        if (self.zipfile_path is None):
            try:
                zf = next(self.zip_dir_iterator)
                print(f"Processing {zf}")
                zf = Path(zf)
            except StopIteration:
                # we're done! 
                raise 
            zf_name = zf.stem
            # each file has its own directory, like A1.zip/A1
            try:
                self.zipfile_path = zipfile.Path(zf)/zf_name
            except:
                print(zf)
                raise
        if (self.zipfile_iterator is None):
            self.zipfile_iterator = self.zipfile_path.iterdir()

        try:
            xml_file = next(self.zipfile_iterator)
            return xml_file.read_text()
        except StopIteration:
            # we have processed all the files, so we reset the zipfile_path
            # and recall ourselves
            self.zipfile_path = None
            self.zipfile_iterator = None
            self.__next__() 


if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_sm", disable = ["ner", "parser"])
    nlp.max_length = 10_000_000

    eebo_iterator = EeboIterator("data-raw/eebo-zips")

    eebo_pipe = nlp.pipe(eebo_iterator, n_process = 2, batch_size = 2)
    doc1 = next(eebo_pipe)
    print(doc1)