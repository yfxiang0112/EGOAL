import pandas as pd
import numpy as np
import re

df_1 = pd.read_csv('scripts/data_onehot/one_hot.csv')
df_2 = pd.read_csv('scripts/data_onehot/one_hot_pro.csv')

# print(df_1)
# print(df_2)

df_1_subset = df_1.iloc[:,-1427:]
pattern = re.compile(r"\('([^']+)', ([^)]+)\)")
weights = list(range(1427, 0, -1))

for index, row in df_1_subset.iterrows():
    for i, elem in enumerate(row):
        match = pattern.match(elem)
        if match:
            key, value = match.groups()
            # print(f"Key: {key}, Value: {float(value)}")
            if key in df_2.columns:
                df_2.loc[index, key] = weights[i]
                # print(df_2.loc[index, key])

df_2.to_csv('scripts/data_onehot/one_hot_pro_y.csv', index=False)
