import pandas as pd
import re
import numpy as np

def id_reg(s):
    pattern = r'SO_*A*\d+'
    res = re.findall(pattern, s) 

    assert len(res)!=0
    #if len(res) != 1:
    #    return np.NaN
    #NOTE: temp

    if res[0].find('_') == -1:
        res[0] = 'SO_'+res[0][2:]

    return res[0]


deg_df = pd.read_csv('dataset/deg/deg_top20_expr.csv', index_col='index')
description_df = pd.read_csv('dataset/deg/group2description.csv')
concept_df = pd.read_csv('dataset/concepts/GSE_concepts.csv', index_col='SAMPLES')


for i in range(20):
    deg_df[str(i)] = deg_df[str(i)].apply(id_reg)


concepts = []
for idx, row in deg_df.iterrows():

    for gsm_idx, concept_row in concept_df.iterrows():
        if gsm_idx == row['GSM']:
            c = concept_row['CONCEPTS']
            c = eval(c)
            concepts.append(c)
            break

deg_df.insert(0, 'CONCEPTS', concepts)

for i in range(20):
    deg_df.rename(columns={str(i):'gene_'+str(i+1)}, inplace=True)
deg_df.drop('GSM', axis=1, inplace=True)


print(deg_df)
deg_df.to_csv('dataset/deg/dataset.csv')
