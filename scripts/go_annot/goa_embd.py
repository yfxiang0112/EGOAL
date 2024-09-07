from sentence_transformers import SentenceTransformer
import numpy as np
import os

from tqdm import tqdm

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
            

embd_model = SentenceTransformer("all-MiniLM-L6-v2")

gene_map_dict = {}
with open('predict/gene_mapping.txt', 'r') as f:
    gene_map_dict = eval(f.readline())

prod = list(gene_map_dict.values())
prod_embeddings = embd_model.encode(prod)

term_embeddings = np.load('dataset/embedding/go_txt_embd.npy')
term_idx = []
with open('dataset/embedding/go_embd_idx.txt', 'r') as f:
    term_idx = eval(f.readline())

sim = embd_model.similarity(term_embeddings, prod_embeddings)


goa_dict = {}
#for i, g in tqdm(enumerate(gene_map_dict.keys()), total=len(gene_map_dict.keys())):
for i, g in enumerate(gene_map_dict.keys()):
    sorted_sim, sorted_term = zip(*sorted(zip(sim[i], term_idx), reverse=True))
    #print(sorted_term)
    #goa_dict = {g:c for g,c in zip(gene_map_dict.keys(), sorted_term)}
    goa_dict.update({g: sorted_term[:10]})
    print(i, g)
    print(sorted_sim[:20])
    print(sorted_term[:20], '\n')

    #tmp
    if i>50:
        assert 0
    

#for k,v in goa_dict.items():
#    print(f'{k}\t{v}')

with open('rules/goa_gene2go_new.txt', 'w') as f:
    f.write(str(goa_dict))
