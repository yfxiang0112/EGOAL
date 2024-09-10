from typing import Iterable
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns
from tqdm import tqdm

def graph_plot(pred_res: Iterable, out_pth: str, show_plot = True)
    graph_map_pth ='plots/regu_graph/gene_graph' 
    gene_embd_pth = 'plots/regu_graph/gene_embd_pca.npy'
    goa_pth = 'rules/goa_gene2go.csv'

    ''' init edge mappings '''
    edges = {}
    with open(graph_map_pth, 'r') as f:
        edges = eval(f.readline())
    
    ''' init GO annotation & gene embedding positions '''
    goa_df = pd.read_csv(goa_pth, index_col=0, header=None)
    gene_embd = np.load(gene_embd_pth)
    gene_embd = gene_embd.transpose()
    gene_df = pd.DataFrame({'pca0':gene_embd[0], 'pca1':gene_embd[1]}, index=goa_df.index)
    
    
    ''' use directed graph '''
    G = nx.DiGraph()
    
    ''' add gene embedding positions '''
    for gene, pca_pos in tqdm(gene_df.iterrows(), total=len(gene_df)):
        if gene in pred_res:
            G.add_node(gene)
            G.add_node(gene, pos=(pca_pos['pca0'], pca_pos['pca1']))
    
    ''' add edge mappings '''
    for gene, neighbors in tqdm(edges.items()):
        for neighbor in neighbors:
            if gene in pred_res and neighbor in pred_res:
                G.add_edge(gene, neighbor)
    
    
    ''' plot with networkx'''
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=20, node_color='skyblue', font_size=15, font_color='black')
    plt.savefig(out_pth)
    if show_plot:
        plt.show()
