

from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd
import Levenshtein as lvn

# other possibility is to take a weighted score and a single max
SEM_DIST_MAX = 0.1
LEV_DIST_MAX = 4

def are_neighbours(row, m):
    global NBR_DIST, LEV_DIST

    # is semantic distance small enough?
    row_score = np.asarray(row[1:], dtype = "float")
    row_score = np.expand_dims(row_score, 0)
    m_score   = np.asarray(m.iloc[:, 1:], dtype = "float")
    sem_dist = cdist(row_score, m_score, "cosine")
    sem_close = sem_dist < SEM_DIST_MAX
    sem_close = sem_close.squeeze()

    # is levenshtein distance small enough?
    row_word = str(row[0])
    m_words = m.iloc[:, 0]
    lev_close = [lvn.distance(row_word, mw) < LEV_DIST_MAX for mw in m_words]
    
    close = np.logical_and(sem_close, lev_close)

    return close


# plan
# Start with the top 10K words. Find the "neighbours" with distance < D, levenshtein < L.
#  - only go forward i.e. word x looks only at words x+1...end
# Add them to a list: <from to>.
# Find the neighbours of the new neighbours, but add them like <origin to> not <neighbour to>.
# Now you can just repeat. And you don't need to redo the original words.

dnames = ["word", *['d'+str(x+1) for x in range(500)] ]
dtypes = dict.fromkeys(dnames, "float")
dtypes["word"] = "string"
ws = pd.read_table("data/fasttext-vectors.vec", 
                    dtype     = dtypes,
                    sep       = " ", 
                    skiprows  = 1, 
                    names     = dnames,
                    index_col = False,
                    nrows     = 10000,
                    na_values = [],
                    na_filter = False
                  )

ws = ws.sort_values(by = "word")
ws = ws.iloc[5000:, ]

words = ws['word']
word_root = dict(zip(words, words))

changed = True
while changed:
    for ix, word in enumerate( words[:-1] ):
        changed = False
        nbrs = are_neighbours(ws.iloc[ix, ], ws.iloc[(ix+1):, ])
        nbrs = words.iloc[(ix+1):].loc[nbrs]
        for nbr in nbrs:
            # if they don't share a word root, change that
            if word_root[nbr] != word_root[word]:
                changed = True
                word_root[nbr] = word_root[word]

[print(f"{k} ============ {v}") for k, v in word_root.items()]




