
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool
from Levenshtein import distance as lev_dist

lev_dist_array = np.vectorize(lev_dist, otypes="i")
strlen_array = np.vectorize(len, otypes = "i")

SEMANTIC_MAX_DIST = -0.12

if __name__ == "__main__":
    dnames = ["word", *['d' + str(x + 1) for x in range(300)] ]
    dtypes = dict.fromkeys(dnames, "float32")
    dtypes["word"] = "string"
    ws = pd.read_table("data/fasttext-vectors.vec", 
                        dtype     = dtypes,
                        sep       = " ", 
                        skiprows  = 1, 
                        names     = dnames,
                        index_col = False,
                        na_filter = False,
                        # nrows     = 20000,
                      )
    ws = ws.sort_values("word")
    # ws = ws.iloc[8500:,]

    npws = np.asarray(ws.iloc[:, 1:], dtype = "float32")
    words = np.asarray(ws["word"], dtype = "U50")

    step = 1000

    for sr in range(0, npws.shape[0], step):
        print(f"Row {sr}")
        print(datetime.now())
        er = min(npws.shape[0], sr + step)
        npws_subset = npws[sr:er, :]
        words_subset = words[sr:er]

        # step x nrow npws matrix
        # we convert the cosine to a [0, 1] range here  
        dists = cosine_similarity(npws_subset, npws)
        # nrow npws vector
        min_dists = np.min(dists, 0)
        closeish = min_dists < SEMANTIC_MAX_DIST
        target_words  = words[closeish]

        # could I vectorize twice? Maybe but it's complingcated...
        ldists = [lev_dist_array(words[i], target_words) for i in range(sr, er)]
        ldists = np.asarray(ldists)
        # normalize by word length
        word_len1 = np.sqrt(strlen_array(words[sr:er]))
        word_len2 = np.sqrt(strlen_array(target_words))
        ldists = ldists/np.outer(word_len1, word_len2)
        # -- calculate matrix of overall scores and possible neighbours -- 
        # step x nrow target_subset
        
        # scores = dists[:, closeish] + LEV_DIST_WEIGHT * ldists 
        scores = ldists
        # where this is small enough we have candidate neighbours
        nbrs = scores < .2

        # -- find row/column pairs where scores is true; these are candidate words --
        nbrs = nbrs.nonzero()
        word1 = nbrs[0]
        word2 = nbrs[1]
        word1 = words_subset[word1]
        word2 = target_words[word2]
        not_same = word1 != word2
        word1 = word1[not_same]
        word2 = word2[not_same]
        word_pairs = np.stack((word1, word2)).T
        print(word_pairs)
        print(word_pairs.shape)
        with open("data/similar-words.tab", "a") as sw:
             np.savetxt(sw, word_pairs, fmt = "%s", delimiter = "\t")
