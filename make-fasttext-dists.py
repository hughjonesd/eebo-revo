
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool
from Levenshtein import distance as lev_dist


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
                        na_filter = False
                      )
    ws = ws.sort_values("word")
    
    npws = np.asarray(ws.iloc[:, 1:], dtype = "float32")
    words = np.asarray(ws["word"], dtype = "str")
    lev_dist_array = np.vectorize(lev_dist, otypes="i")

    step = 1000
    SEMANTIC_MAX_DIST = -0.05
    LEV_DIST_WEIGHT = 3 # where semantic distance weight = 1
    MAX_NBR_SCORE = 3
    for sr in range(0, npws.shape[0] + 1, step):
        print(f"Row {sr}")
        print(datetime.now())
        er = min(npws.shape[0], sr + step)
        npws_subset = npws[sr:er, :]
        # step x nrow npws matrix
        dists = cosine_similarity(npws_subset, npws)
        # nrow npws vector
        min_dists = np.min(dists, 0)
        closeish = min_dists < SEMANTIC_MAX_DIST
        target_subset = npws[closeish, : ] 

        # could I vectorize twice? Maybe but it's complingcated...
        ldists = [lev_dist_array(words[i], words[closeish]) for i in range(sr, er)]
        ldists = np.asarray(ldists)

        # step x nrow target_subset
        scores = dists[:, closeish] + LEV_DIST_WEIGHT * ldists 
        # where this is small enough we have candidate neighbours
        scores < MAX_NBR_SCORE
        # find row/column pairs where scores is true; these are candidate words