import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.decomposition import PCA
from sklearn.utils import gen_even_slices

import matplotlib.pyplot as plt
import seaborn as sns


con_embd_df = pd.read_csv('dataset/embedding/embeddings_preprocess_modified.txt', sep=' ', header=None, index_col=0)
goa_df = pd.read_csv('rules/goa_gene2go.csv', header=None, index_col=0)
res_df = pd.read_csv('predict/results/res_0.txt', sep='\t', index_col=0)

gene_embd_matrix = []

for g, row in tqdm(goa_df.iterrows(), total=len(goa_df)):
    concept_set = eval(row[1])

    embd_subdf = con_embd_df.loc[con_embd_df.index.isin(concept_set)]
    #print(embd_subdf)
    gene_embd = embd_subdf.mean(axis=0)
    
    gene_embd_matrix.append(list(gene_embd))

gene_embd_matrix = np.array(gene_embd_matrix)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(gene_embd_matrix)
print(pca_result.shape)
np.save('plots/regu_graph/gene_embd_pca.npy', pca_result)

gene_embd = pca_result.transpose()
gene_embd_df = pd.DataFrame({'x':gene_embd[0], 'y':gene_embd[1]}, index=goa_df.index)

plt.figure(figsize=(20, 15))
sns.scatterplot(data=gene_embd_df, x='x', y='y', size=0.05)
sns.scatterplot(data=gene_embd_df.loc[gene_embd_df.index.isin(res_df.index)], x='x', y='y', color='red', size=5)
plt.title('PCA Result of PCA Components')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.savefig('plots/regu_graph/PCA.png')
plt.show()
