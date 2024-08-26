import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

con_embd = np.array(0)
txt_embd = np.array(0)

con_embd = np.load('plots/embd_pca/pca_con_embd.npy')
txt_embd = np.load('plots/embd_pca/pca_txt_embd.npy')

con_embd = con_embd.transpose()
txt_embd = txt_embd.transpose()
print(con_embd)

con_df = pd.DataFrame({'pca0':con_embd[0], 'pca1':con_embd[1]})
txt_df = pd.DataFrame({'pca0':txt_embd[0], 'pca1':txt_embd[1]})


plt.figure(figsize=(10, 7))
sns.scatterplot(data=con_df, x='pca0', y='pca1')
sns.scatterplot(data=txt_df, x='pca0', y='pca1', color='red')
plt.title('PCA Result of PCA Components')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.savefig('plots/embd_pca/PCA.png')
plt.show()
