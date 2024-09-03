import pandas as pd

df = pd.read_csv('dataset/importance/dataset_onehot.csv')
col_names = [f'SO_{i:04d}' for i in range(1,4759)]
expr_portion = []

for c in col_names:
    if c not in df.columns:
        continue
    sum_val = df[c].sum()
    len_val = len(df[c])
    expr_portion.append((c, sum_val/len_val))

inv_cols = [col for col in expr_portion if col[1]>.7]
print(inv_cols)
