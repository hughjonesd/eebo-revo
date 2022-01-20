
from datetime import datetime
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import Levenshtein as lvn

# other possibility is to take a weighted score and a single max
SEM_DIST_MAX = 0.225
LEV_DIST_MAX = 5

def are_neighbours(row, m):
    global NBR_DIST, LEV_DIST

    # is semantic distance small enough?
    row_score = np.asarray(row[1:], dtype = "float")
    row_score = np.expand_dims(row_score, 0)
    m_score   = np.asarray(m.iloc[:, 1:], dtype = "float")
    sem_dist = cosine_similarity(row_score, m_score)
    sem_close = sem_dist < SEM_DIST_MAX
    sem_close = sem_close.squeeze()

    # is levenshtein distance small enough?
    row_word = str(row[0])
    m_words = m.iloc[:, 0]
    lev_close = [lvn.distance(row_word, mw) < LEV_DIST_MAX for mw in m_words]
    
    close = np.logical_and(sem_close, lev_close)

    return close


dnames = ["word", *['d' + str(x + 1) for x in range(500)] ]
dtypes = dict.fromkeys(dnames, "float")
dtypes["word"] = "string"
ws = pd.read_table("data/fasttext-vectors.vec", 
                    dtype     = dtypes,
                    sep       = " ", 
                    skiprows  = 1, 
                    names     = dnames,
                    index_col = False,
                    na_filter = False
                  )

ws = ws.sort_values(by = "word")

words = ws['word']
word_root = dict(zip(words, words))

changed = 1
while changed > 0:
    print(f"{datetime.now()} Changed: {changed}")
    changed = 0
    for ix, word in enumerate( words[:-1] ):
        if ix > 30: exit(0) 
        nbrs = are_neighbours(ws.iloc[ix, ], ws.iloc[(ix+1):, ])
        nbrs = words.iloc[(ix+1):].loc[nbrs]
        for nbr in nbrs:
            # if they don't share a word root, change that
            if word_root[nbr] != word_root[word]:
                changed += 1
                word_root[nbr] = word_root[word]
        print(f"{datetime.now()} Index {ix} Word {word}")
    changed = 0 # to break

with open("data/lemmas.tab", "w") as outfile:
    for word, root in word_root.items():
        print(f"{word}\t{root}\n", file = outfile)



