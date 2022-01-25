
import networkx as nx
import pandas as pd
from networkx.algorithms.components import connected_components
import configsh

nbrs = pd.read_table("data/similar-words.tab", names = ["from", "to"], 
                     index_col = False, na_filter = False)


gr = nx.convert_matrix.from_pandas_edgelist(nbrs, source = "from", target = "to")

lexemes = connected_components(gr)
with open(configsh.SIMILAR_WORDS_PATH, "w") as f:
    for comp in lexemes:
        comp = list(comp)
        lex = comp[0]
        for word in comp[1:]:
            f.write(f"{word}\t{lex}\n")
