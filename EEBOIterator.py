
from pathlib import Path
import zipfile


class EEBOIterator:
    """
    Iterates through all the zipfiles in a folder
    
    * Extracts items in turn and returns the raw text
    """
    def __init__(self, folder, debug = False, max_files = -1):
        folder = Path(folder)
        self.zip_dir_iterator = folder.iterdir()
        self.zipfile_iterator = None
        self.zipfile = None
        self.debug = debug
        self.max_files = max_files
        self.file_ctr = 0

    def __iter__(self):
        return self

    def get_next_zipfile(self):
        zf = next(self.zip_dir_iterator)
        if self.debug: print(f"Processing {zf}")
        zf = Path(zf) 
        zf_name = zf.stem
        # each file has its own directory, like A1.zip/A1
        self.zipfile = zipfile.ZipFile(zf)
        zipfile_path = zipfile.Path(self.zipfile) / zf_name
        return zipfile_path.iterdir()

    def __next__(self):
        if self.file_ctr == self.max_files:
            raise StopIteration
        if self.zipfile_iterator is None:
            self.zipfile_iterator = self.get_next_zipfile()
        try:
            xml_file = next(self.zipfile_iterator)
            self.file_ctr += 1
        except StopIteration:
            # we have processed all the files, so we reset the zipfile_iterator
            # and recall ourselves
            self.zipfile_iterator = None
            self.zipfile.close()
            return self.__next__() 
        if self.debug: print(f"File {xml_file}")
        xml_text = xml_file.read_text()
        return xml_text