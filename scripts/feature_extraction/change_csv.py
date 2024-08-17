import pandas as pd

df = pd.read_csv('dataset/importance/processed_dataset_with_importance.csv')

new_column_names = {col: f'importance_value_{i+1}' for i, col in enumerate(df.columns[102:122])}
df.rename(columns=new_column_names, inplace=True)

df.to_csv('dataset/importance/processed_dataset_with_importance.csv', index=False)
