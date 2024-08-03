import pandas as pd
import numpy as np

df_1 = pd.read_csv('../../dataset/one-hot/one_hot.csv')
df_2 = pd.read_csv('../../dataset/raw/dataset.csv')

# print(df_1)
# print(df_2)

labels = df_2.columns[2:]
start_col = df_1.shape[1] - 20

if start_col + len(labels) > df_1.shape[1]:
    new_columns = df_1.columns.tolist() + [f'new_col_{i}' for i in range(df_1.shape[1], start_col + len(labels))]
    df_1 = df_1.reindex(columns=new_columns)

new_columns = df_1.columns.tolist()
new_columns[start_col:start_col+len(labels)] = labels
df_1.columns = new_columns

df_1.iloc[:, start_col:start_col+len(labels)] = 0
df_1.to_csv('../../dataset/one-hot/one_hot_pro.csv')