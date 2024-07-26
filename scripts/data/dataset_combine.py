import pandas as pd
import numpy as np
import os
import re

matrix = []
pattern = r'SO_*A*\d+'

def id_regu(s):
    res = re.findall(pattern, s) 
    if len(res) != 1:
        return np.NaN

    if res[0].find('_') == -1:
        res[0] = 'SO_'+res[0][2:]

    return res[0]


for f in os.listdir('dataset/raw/matrix'):
    df = pd.read_csv('dataset/raw/matrix/'+f)

    df = df.drop('Unnamed: 0', axis=1)
    df['GENE'] = df['GENE'].apply(id_regu)

    df = df.dropna(subset=['GENE'])
    df.rename(columns={'GENE':'SAMPLES'}, inplace=True)
    df = df.groupby('SAMPLES').mean()
    #df.set_index(keys='GENE')

    # TODO: regularize gene ID
    #print(df)
    matrix.append(df)

df = pd.concat(matrix, axis=1)
df = df.transpose()

con_df = pd.read_csv('dataset/raw/GSE_concepts.csv')
con_df.set_index('SAMPLES', inplace=True)
print(con_df)

df = df.reindex()
df.sort_index(inplace=True)
#df.set_index('SAMPLES', inplace=True)

con_df = con_df.loc[df.index]
con_df.drop_duplicates(inplace=True)
df.insert(0, 'CONCEPTS', con_df['CONCEPTS'], allow_duplicates=True)

print(df)
df.to_csv('dataset/raw/dataset.csv')
