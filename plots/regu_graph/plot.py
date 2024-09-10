import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns
from tqdm import tqdm

con_embd = np.array(0)
txt_embd = np.array(0)

edges = {}
with open('plots/regu_graph/gene_graph', 'r') as f:
    edges = eval(f.readline())

goa_df = pd.read_csv('rules/goa_gene2go.csv', index_col=0, header=None)
gene_embd = np.load('plots/regu_graph/gene_embd_pca.npy')
#txt_embd = np.load('plots/embd_pca/pca_txt_embd.npy')

gene_embd = gene_embd.transpose()
#txt_embd = txt_embd.transpose()
print(gene_embd)

gene_df = pd.DataFrame({'pca0':gene_embd[0], 'pca1':gene_embd[1]}, index=goa_df.index)
#txt_df = pd.DataFrame({'pca0':txt_embd[0], 'pca1':txt_embd[1]})


#plt.figure(figsize=(20, 15))
#sns.scatterplot(data=gene_df, x='pca0', y='pca1', size=5)
#
#for start, ends in tqdm(edges.items()):
#    for end in ends:
#        x_values = [gene_df.loc[start, 'pca0'], gene_df.loc[end, 'pca0']]
#        y_values = [gene_df.loc[start, 'pca1'], gene_df.loc[end, 'pca1']]
#        plt.plot(x_values, y_values, 'k-')
#
#plt.title('PCA Result of PCA Components')
#plt.xlabel('PCA Component 1')
#plt.ylabel('PCA Component 2')
#plt.savefig('plots/embd_pca/PCA.png')
#plt.show()

G = nx.Graph()

# 添加节点及其坐标
for index, row in tqdm(gene_df.iterrows(), total=len(gene_df)):
    G.add_node(index, pos=(row['pca0'], row['pca1']))

# 添加边
for node, neighbors in tqdm(edges.items()):
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# 获取节点位置
pos = nx.get_node_attributes(G, 'pos')

# 绘制图
plt.figure(figsize=(60, 40))
nx.draw(G, pos, with_labels=True, node_size=10, node_color='skyblue', font_size=15, font_color='black')
plt.savefig('plots/regu_graph/graph_all.png')
plt.show()
