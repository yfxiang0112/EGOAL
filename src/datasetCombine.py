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


for f in os.listdir('data_SOneidensis/matrix'):
    df = pd.read_csv('data_SOneidensis/matrix/'+f)

    df = df.drop('Unnamed: 0', axis=1)
    df['GENE'] = df['GENE'].apply(id_regu)

    df = df.dropna(subset=['GENE'])
    df = df.groupby('GENE').mean()
    #df.set_index(keys='GENE')

    # TODO: regularize gene ID
    print(df)
    matrix.append(df)

df = pd.concat(matrix, axis=1)
print(df)
df.to_csv('data_SOneidensis/dataset.csv')
