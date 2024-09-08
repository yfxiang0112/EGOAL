import pandas as pd
onehot_df = pd.read_csv('dataset/importance/dataset_onehot.csv')

print(onehot_df['SO_0002'].sum())
