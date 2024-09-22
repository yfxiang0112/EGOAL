import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#for i in range(5):
df = pd.read_csv('predict/results-prelim/res_0.txt', sep='\t', index_col='gene_id')

#with open('predict/rel_gene_lst.txt', 'r') as f:
#    rel_gene_lst = eval(f.readline())
#    rel_gene_lst = list(rel_gene_lst)
#rel_gene_lst = ['SO_3370', 'SO_2912', 'SO_0107', 'SO_0104', 'SO_0770', 'SO_2345', 'SO_1776', 'SO_1778', 'SO_1779', 'SO_1780', 'SO_0624', 'SO_1329']
#rel_gene_lst_nad = ['SO_3370', 'SO_2912', 'SO_0107', 'SO_0104', 'SO_0770', 'SO_2345']
#rel_gene_lst_mem = ['SO_1776', 'SO_1778', 'SO_1779', 'SO_1780']
#rel_gene_lst_mtb = ['SO_0624', 'SO_1329']

with open('predict/wetlab_gene_lst.txt', 'r') as f:
    wetlab_gene_lst = list(eval(f.readline()))

#filtered_df = df.loc[df.index.isin(rel_gene_lst)]
filtered_df = df.loc[wetlab_gene_lst]

#filtered_df['group'] = 'NAD+ synthesis'
#filtered_df.loc[rel_gene_lst_mem, 'group'] = 'membrane protein'
#filtered_df.loc[rel_gene_lst_mtb, 'group'] = 'lactate metabolism'
filtered_df['classification confidence'] = filtered_df['conf']


mean_all = df['conf'].mean()
mean_first_50 = df.head(50)['conf'].mean()

plt.figure(figsize=(6,8))
sns.barplot(x=filtered_df.index, y=filtered_df['classification confidence'], palette='viridis', width=0.4)

plt.axhline(mean_all, color='r', linestyle='--', label=f'mean conf of all genes: {mean_all:.3f}')
plt.axhline(mean_first_50, color='b', linestyle='--', label=f'mean conf of top50 genes: {mean_first_50:.3f}')
plt.xticks(rotation=45)

plt.legend()

#plt.show()
plt.savefig(f'predict/results-prelim/plot_0.png')
