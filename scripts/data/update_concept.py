import pandas as pd

raw_dataset = pd.read_csv('dataset/raw/dataset.csv')

deg_dataset = pd.read_csv('dataset/deg/dataset.csv')
importance_dataset = pd.read_csv('dataset/importance/processed_dataset_with_importance.csv')

deg_dataset['CONCEPTS'] = raw_dataset['CONCEPTS']
importance_dataset['CONCEPTS'] = raw_dataset['CONCEPTS']


deg_dataset.to_csv('dataset/deg/dataset.csv', index=False)
importance_dataset.to_csv('dataset/importance/processed_dataset_with_importance.csv', index=False)
