
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool

def calc_dists(start_row):
    global npws, step
    end_row = min(npws.shape[0], start_row + step)
    dists = cosine_similarity(npws[start_row:end_row, :], npws)
    return dists

if __name__ == "__main__":
    dnames = ["word", *['d' + str(x + 1) for x in range(500)] ]
    dtypes = dict.fromkeys(dnames, "float32")
    dtypes["word"] = "string"
    ws = pd.read_table("data/fasttext-vectors.vec", 
                        dtype     = dtypes,
                        sep       = " ", 
                        skiprows  = 1, 
                        names     = dnames,
                        index_col = False,
                        na_filter = False, 
                      )
    ws = ws.sort_values("word")
    
    npws = np.asarray(ws.iloc[:, 1:], dtype = "float64")
    
    step = 10000
    calc_dists(0)
    exit(0)
    with Pool(processes = 15) as pool:
        pool.map(calc_dists, range(0, 250001, step))

