import pandas as pd
import numpy as np
from tqdm import tqdm

from txt2con import EmbeddingConverter

gse_df = pd.read_csv('dataset/concepts/GSE_concepts.csv', index_col='SAMPLES')
embd = EmbeddingConverter('rules/go.owl', use_vpn=True)

concepts = []

for idx, row in tqdm(gse_df.iterrows(), 'reading gsm data frame', total=len(gse_df)):
    descp = row['DESCRIP']
    assert type(descp)==str
    sim = embd.similar_matrix(descp)

    sorted_sim = embd.max_sim(5)
    concepts.append(sorted_sim)
    #print('-'*50)
    #print(idx, descp)

    #for c in sorted_sim:
    #    print()
    #    print(c, embd.term_dict[c])
    #print('-'*50)

gse_df['CONCEPTS'] = concepts
print(gse_df)
gse_df.to_csv('dataset/concepts/GSE_embd_concepts.csv', index=False)
