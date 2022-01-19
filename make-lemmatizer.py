

from sre_constants import MAX_REPEAT
from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd
import Levenshtein as lvn

SEM_DIST_MAX = 4.5
LEV_DIST_MAX = 5

def is_neighbour(row, m):
    global NBR_DIST, LEV_DIST

    # is semantic distance small enough?
    row_score = np.asarray(row[1:], dtype = "float")
    row_score = np.expand_dims(row_score, 0)
    m_score   = np.asarray(m.iloc[:, 1:], dtype = "float")
    sem_dist = cdist(row_score, m_score)
    sem_close = sem_dist < SEM_DIST_MAX

    # is levenshtein distance small enough?
    row_word = str(row[0])
    m_words = m.iloc[:, 0]
    lev_close = [lvn.distance(row_word, mw) < LEV_DIST_MAX for mw in m_words]
    
    close = np.logical_and(sem_close, lev_close)

    return close


dnames = ["word", *['d'+str(x+1) for x in range(100)] ]
ws = pd.read_table("data/fasttext-vectors.vec", sep = " ", skiprows = 1, 
                     names     = dnames,
                     index_col = False,
                     nrows     = 10000
                   )


ws = ws.sort_values(by = "word")
ws = ws.iloc[5000:, ]

max_r = 50
nbrs = [is_neighbour(ws.iloc[i, :], ws.iloc[:max_r, :]) for i in range(max_r)]

nbrs = np.asarray(nbrs)
nbrs = np.squeeze(nbrs, axis = 1)

[print(f"{ws.iloc[i, 0]}   {ws.iloc[j, 0]}   {nbrs[i, j]}") 
       for i in range(max_r) for j in range(max_r)]

# plan
# Start with the top 10K words. Find the "neighbours" with distance < D, levenshtein < L.
#  - only go forward i.e. word x looks only at words x+1...end
# Add them to a list: <from to>.
# Find the neighbours of the new neighbours, but add them like <origin to> not <neighbour to>.
# Now you can just repeat. And you don't need to redo the original words.
