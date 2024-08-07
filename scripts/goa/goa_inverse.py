import pandas as pd
from tqdm import tqdm

goa_df = pd.read_csv('rules/goa_mapping.csv', header=None)
print(goa_df)

gene_ids = set()

for gene_lst in goa_df[1]:
    for g in eval(gene_lst):
        gene_ids.add(g)

gene_ids = list(gene_ids)
gene_ids.sort()

#con_ids = [set()]*len(gene_ids)
con_ids = []
for _ in range(len(gene_ids)):
    con_ids.append(set())

print(len(con_ids))

for idx, g in enumerate(tqdm(gene_ids)):
#for idx, g in enumerate(gene_ids):
    for _, row in goa_df.iterrows():
        if g in eval(row[1]):
            con_ids[idx].add(row[0])
    #print(g, con_ids[idx])

goa_inv_df = pd.DataFrame({0:gene_ids, 1:con_ids})
print(goa_inv_df)
goa_inv_df.to_csv('rules/goa_gene2go.csv', index=False, header=False)
