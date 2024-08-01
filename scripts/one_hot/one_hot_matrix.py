import pandas as pd
import numpy as np

df_1 = pd.read_csv('../../dataset/concepts/concept_domain.csv', header= None)
df_2 = pd.read_csv('../../dataset/importance/processed_dataset_with_importance.csv')

# drop out the embedding part 
start_col = 2  
num_cols_to_drop = 100
columns_to_drop = df_2.columns[start_col:start_col + num_cols_to_drop].tolist()
df_2 = df_2.drop(columns=columns_to_drop)

# print(df_2)

# one-hot 
unique_elements = df_1.iloc[:, 0].unique()
one_hot_df = pd.DataFrame(columns=unique_elements)
for i in range(len(df_2)):
    row = df_2.iloc[i]
    element = row.iloc[1] 
    one_hot_row = np.zeros(len(unique_elements))
    for elem in eval(element):
        # print(elem)
        if elem in unique_elements:
            # print(elem)
            index = np.where(unique_elements == elem)[0][0]
            one_hot_row[index] = 1
        # assert(0)
        # print('yes')
    one_hot_df.loc[i] = one_hot_row

new_columns = list(df_2.columns[:2]) + list(one_hot_df.columns) + list(df_2.columns[2:])
df_2 = pd.concat([df_2.iloc[:, :2], one_hot_df, df_2.iloc[:, 2:]], axis=1)
df_2 = df_2.reindex(columns=new_columns)

print(df_2)

df_2.to_csv('../../dataset/one-hot/one_hot.csv', index=False)