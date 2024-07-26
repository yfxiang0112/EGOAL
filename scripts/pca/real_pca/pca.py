import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE

df = pd.read_csv('dataset/pca/processed_dataset_with_inserted_columns.csv')

num_columns = df.shape[1]

start_index = 102
df_subset = df.iloc[:, start_index:]

df_subset = df_subset.replace([np.inf, -np.inf], np.nan)
imputer = SimpleImputer(strategy='mean')
df_subset_imputed = pd.DataFrame(imputer.fit_transform(df_subset), columns=df_subset.columns)
pca = PCA(n_components=10)
pca_result = pca.fit_transform(df_subset_imputed)
df_subset_pca = pd.DataFrame(pca_result, columns=[f'PC{i+1}' for i in range(10)])
df_new = pd.concat([df.iloc[:, :start_index], df_subset_pca], axis=1)
df_new.to_csv('dataset/pca/processed_dataset_with_10_components.csv', index=False)

print("Yes!")

tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(df_subset_pca)
tsne_df = pd.DataFrame(tsne_result, columns=['TSNE1', 'TSNE2'])
plt.figure(figsize=(10, 7))
sns.scatterplot(x='TSNE1', y='TSNE2', data=tsne_df)
plt.title('t-SNE Result of PCA Components')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.savefig('PCA.png')
plt.show()
