
from datetime import datetime
from scipy.spatial.distance import cdist
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
                    na_values = [],
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
        nbrs = are_neighbours(ws.iloc[ix, ], ws.iloc[(ix+1):, ])
        nbrs = words.iloc[(ix+1):].loc[nbrs]
        for nbr in nbrs:
            # if they don't share a word root, change that
            if word_root[nbr] != word_root[word]:
                changed += 1
                word_root[nbr] = word_root[word]

with open("data/lemmas.tab", "w") as outfile:
    for word, root in word_root.items():
        print(f"{word}\t{root}\n", file = outfile)



