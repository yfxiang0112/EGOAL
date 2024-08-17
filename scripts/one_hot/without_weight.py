import pandas as pd
import re
from tqdm import tqdm

df_1 = pd.read_csv('dataset/one-hot/one_hot.csv')
df_2 = pd.read_csv('dataset/one-hot/one_hot_pro.csv')

# 选择 df_1 的最后 20 列
df_1_subset = df_1.iloc[:, -1427:]

# 正则表达式模式
pattern = re.compile(r"\('([^']+)', ([^)]+)\)")

# 遍历 df_1_subset 的每一行
for index, row in tqdm(df_1_subset.iterrows()):
    for elem in row:
        match = pattern.match(elem)
        if match:
            key, value = match.groups()
            if key in df_2.columns:
                df_2.loc[index, key] = 1

# 保存修改后的 df_2 到 CSV 文件
df_2.to_csv('dataset/one-hot/one_hot_pro_y_allone.csv', index=False)