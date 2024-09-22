import pandas as pd
from tqdm import tqdm

graph = {}

goa_df = pd.read_csv('rules/goa_gene2go.csv', index_col=0, header=None)
rule_df = pd.read_csv('rules/ruleRem.csv', index_col=1, header=None)
goa_rev_df = pd.read_csv('rules/raw_goa/goa_mapping.csv', index_col=0, header=None)

for g, row in tqdm(goa_df.iterrows(), total = len(goa_df)):
    con_set = eval(row[1])
    edge_subdf = rule_df.loc[rule_df.index.isin(con_set)]

    in_node_set = set()
    for _,edge in edge_subdf.iterrows():
        in_node_set.add(edge[3])

    goa_rev_subdf = goa_rev_df.loc[goa_rev_df.index.isin(in_node_set)]
    goa_rev_subdf[1] = goa_rev_subdf[1].apply(eval)
    in_node_genes = set().union(*goa_rev_subdf[1])

    graph.update({g: in_node_genes})

print(graph)
with open('plots/regu_graph/gene_graph', 'w') as f:
    f.write(str(graph))
