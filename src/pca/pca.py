# update

import pandas as pd
import numpy as np

df = pd.read_csv('../../dataset/new_dataset.csv')
concept_column = df['CONCEPTS']
concept_vectors = df.drop(columns=['CONCEPTS', 'CONCEPT'])
concept_groups = df.groupby('CONCEPTS')
concept_dict = {}

for concept, group in concept_groups:
    vectors = group.drop(columns=['CONCEPTS', 'CONCEPT']).values
    concept_dict[concept] = vectors

average_vectors = {}
for concept, vectors in concept_dict.items():
    average_vectors[concept] = np.mean(vectors, axis=0)
result_rows = []

for concept, vector in average_vectors.items():
    result_rows.append([concept] + vector.tolist())

column_names = ['CONCEPTS'] + [f'vector{i+1}' for i in range(100)]
result_df = pd.DataFrame(result_rows, columns=column_names)

result_df.to_csv('../../dataset/reduced_dataset.csv', index=False)

print("平均向量计算完成，结果已保存到 reduced_dataset.csv")