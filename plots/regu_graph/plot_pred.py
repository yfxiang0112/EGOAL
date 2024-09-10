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
gene_embd = gene_embd.transpose()
gene_df = pd.DataFrame({'pca0':gene_embd[0], 'pca1':gene_embd[1]}, index=goa_df.index)

res_df = pd.read_csv('predict/results/res_NADK.txt', sep='\t')
gene_res = set(res_df['gene_id'])



G = nx.DiGraph()

# 添加节点及其坐标
for gene, pca_pos in tqdm(gene_df.iterrows(), total=len(gene_df)):
    if gene in gene_res:
#        print(gene)
        G.add_node(gene)
#        print(pca_pos)
        G.add_node(gene, pos=(pca_pos['pca0'], pca_pos['pca1']))
#assert 0

# 添加边
for gene, neighbors in tqdm(edges.items()):
    for neighbor in neighbors:
        if gene in gene_res and neighbor in gene_res:
            G.add_edge(gene, neighbor)

# 获取节点位置
pos = nx.get_node_attributes(G, 'pos')

# 绘制图
nx.draw(G, pos, with_labels=True, node_size=20, node_color='skyblue', font_size=15, font_color='black')
plt.savefig('plots/regu_graph/graph_res.png')
plt.show()
