import pandas as pd
import numpy as np
from tqdm import tqdm

def remove_nan(df_subset):
    for column_name, column_data in df_subset.items():
        if column_data.isna().any():
            df_subset = df_subset.drop(column_name, axis=1)
    return df_subset

df = pd.read_csv('dataset/raw/proced/processed_dataset_with_inserted_columns.csv')

packed_data = []

for i in tqdm(range(len(df)), desc="Processing rows"):
    df_subset = df.iloc[i:i+1, 102:]
    new_df = remove_nan(df_subset)
    column_labels = new_df.columns.tolist()
    new_df_list = new_df.values.flatten().tolist()
    new_df_list = [x for x in new_df_list if np.isfinite(x)]
    
    if len(new_df_list) == 0:
        # print(f"Row {i} has no valid data after removing NaN and non-finite values.")
        continue
    
    mean = sum(new_df_list) / len(new_df_list)
    variance = sum((x - mean) ** 2 for x in new_df_list) / len(new_df_list)

    # print(f'{i}', mean, variance)
    
    importance = [(x - mean) ** 2 for x in new_df_list]
    element_importance_pairs = list(zip(column_labels, new_df_list, importance))
    sorted_element_importance_pairs = sorted(element_importance_pairs, key=lambda x: x[2], reverse=True)
    # print(len(sorted_element_importance_pairs))
    top_20_elements = sorted_element_importance_pairs[:1427]
    importance_list = []
    for label, element, imp in top_20_elements:
        importance_list.append((label, imp))
    labeled_importance_series = pd.Series([(label, imp) for (label, imp) in importance_list], index=[f'importance_{j+1}' for j in range(1427)])
    packed_data.append(labeled_importance_series)

packed_df = pd.DataFrame(packed_data)

df.iloc[:, 102:1529] = packed_df.values
df = df.iloc[:, :1529]

df.to_csv('dataset/importance/processed_dataset_with_importance.csv', index=False)
