

import sys
import pandas as pd
import numpy as np

np.random.seed(10271975)

tei_files_path = sys.argv[1]
test_prop = float(sys.argv[2])

tei_files = pd.read_table(tei_files_path, names = ["zip", "xml"])
nrow = tei_files.shape[0]
tei_files["split"] = np.random.choice(["test", "train"], nrow, p = [test_prop, 1 - test_prop])
tei_files.to_csv(tei_files_path, sep = "\t", header = False, index = False)