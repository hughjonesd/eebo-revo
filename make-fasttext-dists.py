
import os 
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool
from Levenshtein import distance as lev_dist
import configsh

lev_dist_array = np.vectorize(lev_dist, otypes="i")
strlen_array = np.vectorize(len, otypes = "i")

# must be this close to something to be considered a 
# potential neighbour
SEMANTIC_CANDIDATE_DIST = 0.1
# two words must be this close to be neighbours
SEMANTIC_MAX_DIST = SEMANTIC_CANDIDATE_DIST
LEV_MAX_DIST = 0.3
similar_words_path = "data/similar-words.tab"

try:
    os.remove(similar_words_path)
except:
    pass

if __name__ == "__main__":
    dnames = ["word", *['d' + str(x + 1) for x in range(configsh.FASTTEXT_DIMS)] ]
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
    ws = ws.iloc[8500:,]

    npws = np.asarray(ws.iloc[:, 1:], dtype = "float32")
    words = np.asarray(ws["word"], dtype = "U50")

    step = 500

    for sr in range(0, npws.shape[0], step):
        print(f"Row {sr}")
        print(datetime.now())
        er = min(npws.shape[0], sr + step)
        npws_subset = npws[sr:er, :]
        words_subset = words[sr:er]

        # step x nrow npws matrix
        # we convert the cosine to a [0, 1] range here  
        dists = cosine_similarity(npws_subset, npws)
        print(f"Similarity quantiles: 1/5/50/95/99 {np.quantile(dists, [0.01, 0.05, 0.5, 0.95, 0.99])}")
        # nrow npws vector
        min_dists = np.min(dists, 0)
        closeish = min_dists < SEMANTIC_CANDIDATE_DIST
        target_words  = words[closeish]

        # could I vectorize twice? Maybe but it's complingcated...
        ldists = [lev_dist_array(words[i], target_words) for i in range(sr, er)]
        ldists = np.asarray(ldists)
        
        # normalize by word length
        word_len1 = strlen_array(words[sr:er]) ** 0.6
        word_len2 = strlen_array(target_words) ** 0.5
        word_len_adjust = np.outer(word_len1, word_len2)
        ldists = ldists/word_len_adjust
        
        # step x nrow target_subset
        nbrs = (ldists < LEV_MAX_DIST) & (dists[:, closeish] < SEMANTIC_MAX_DIST)
        # return indices where nbrs is True, as tuple of arrays (I think)
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
        with open(similar_words_path, "a") as sw:
             np.savetxt(sw, word_pairs, fmt = "%s", delimiter = "\t")
