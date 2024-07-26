import pandas as pd
import numpy as np

df = pd.read_csv('dataset/raw/dataset.csv')
concept_column = df['CONCEPTS']

# print(concept_column[0])

with open('dataset/concepts/all_concept_name.txt', 'r') as file:
    valid_concepts = set(line.strip() for line in file)

def process_concepts(concepts):
    if pd.isna(concepts):
        return None
    concepts_list = eval(concepts)
    filtered_concepts = [concept for concept in concepts_list if concept in valid_concepts]
    return filtered_concepts if filtered_concepts else None

df['CONCEPTS'] = concept_column.apply(process_concepts)
df = df.dropna(subset=['CONCEPTS'])
df = df.rename(columns={df.columns[0]: 'NAME'})
df = df.fillna(np.nan)

df.to_csv('dataset/pca/processed_dataset.csv', index=False)


# Process more
df_pro = pd.read_csv('dataset/pca/processed_dataset.csv')
df_find = pd.read_csv('dataset/pca/reduced_dataset.csv')

processed_concepts = df_pro['CONCEPTS']
reduced_concepts = df_find['CONCEPTS']

new_columns = pd.DataFrame([[0.1] * len(df_pro)] * 100).T  
new_columns.columns = [f'Vector_{i+1}' for i in range(100)]

df_pro = pd.concat([df_pro.iloc[:, :2], new_columns, df_pro.iloc[:, 2:]], axis=1)

for i in range(len(processed_concepts)):
    for j in range(len(reduced_concepts)):
        if processed_concepts[i] == reduced_concepts[j]:
            df_pro.iloc[i, 2:102] = df_find.iloc[j, 1:101].values
            
df_pro.to_csv('dataset/pca/processed_dataset_with_inserted_columns.csv', index=False)
