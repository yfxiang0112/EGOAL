import pandas as pd
import re
import numpy as np

def id_reg(s):
    pattern = r'SO_*A*\d+'
    res = re.findall(pattern, s) 
    if len(res) != 1:
        return np.NaN

    if res[0].find('_') == -1:
        res[0] = 'SO_'+res[0][2:]

    return res[0]


deg_df = pd.read_csv('dataset/deg/deg_top20_expr.csv', index_col='index')
embedding_df = pd.read_csv('dataset/pca/processed_dataset_with_10_components.csv', index_col='NAME')
description_df = pd.read_csv('dataset/deg/group2description.csv')
concept_df = pd.read_csv('dataset/concepts/GSE_concepts.csv')

for i in range(20):
    deg_df[str(i)] = deg_df[str(i)].apply(id_reg)

print(deg_df)
print(embedding_df)
print(description_df)
print(concept_df)

vec_list = []
for idx, row in deg_df.iterrows():
    description = description_df[idx][0]
    vec = []
    concepts = []
    #print(description)
    #for _,concept_row in concept_df.iterrows():
    #    if concept_row['DESCRIP'] == description:
    #        concepts = concept_row['CONCEPTS']
    #        concepts = eval(concepts)
    #        concepts.sort()

    for vec_idx,vec_row in embedding_df.iterrows():
        #print(vec_idx, row['GSM'])
        if vec_idx == row['GSM']:
        #vec_concepts = eval(vec_row['CONCEPTS'])
        #vec_concepts.sort()
        #if vec_concepts == concepts:
            vec = list(vec_row[1:101])
            break
        #break

    if vec==[]:
        print('vector not found:', idx, description, concepts)
                
    vec_list.append(vec)

#deg_df['VEC'] = vec_list
deg_df.insert(0, 'vector', vec_list)
for i in range(20):
    deg_df.rename(columns={str(i):'gene_'+str(i+1)}, inplace=True)
deg_df.drop('GSM', axis=1, inplace=True)

print(deg_df)
deg_df.to_csv('dataset/deg/dataset.csv')
