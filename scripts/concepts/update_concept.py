import pandas as pd

raw_dataset = pd.read_csv('dataset/raw/dataset.csv')

#deg_dataset = pd.read_csv('dataset/deg/dataset.csv')
importance_dataset = pd.read_csv('dataset/importance/processed_dataset_with_importance.csv')
onehot_dataset = pd.read_csv('dataset/one-hot/one_hot_pro_y_allone.csv')
onehot_dataset.drop(columns='Unnamed: 0', axis=1, inplace=True)

#deg_dataset['CONCEPTS'] = raw_dataset['CONCEPTS']
importance_dataset['CONCEPTS'] = raw_dataset['CONCEPTS']
onehot_dataset['CONCEPTS'] = raw_dataset['CONCEPTS']


#deg_dataset.to_csv('dataset/deg/dataset.csv', index=False)
importance_dataset.to_csv('dataset/importance/processed_dataset_with_importance.csv', index=False)
onehot_dataset.to_csv('dataset/one-hot/one_hot_pro_y_allone.csv', index=False)
