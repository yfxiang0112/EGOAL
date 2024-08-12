import pandas as pd
import numpy as np
from requests import head
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from rdflib import Graph
import os
import re

#NOTE: when use vpn
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

gse_df = pd.read_csv('dataset/concepts/GSE_concepts.csv', index_col='SAMPLES')
print('\n----- initializing sentence bert model -----\n')
model = SentenceTransformer("all-MiniLM-L6-v2")

print('\n----- parsing GO owl -----')
g = Graph()
g.parse('rules/go.owl')

concept_dscrp = {}

label_prdcs = [
'http://www.w3.org/2000/01/rdf-schema#label',
'http://www.w3.org/2002/07/owl#annotatedTarget',
'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym',
'http://purl.obolibrary.org/obo/IAO_0000115']

for s,p,o in tqdm(g, 'parsing owl'):

    if str(p) in label_prdcs:
        p = r'GO_\d+'
        con = re.findall(p, str(s))
        if len(con) != 1:
            continue
        con = con[0]
        s = concept_dscrp.get(con)
        if s == None:
            concept_dscrp.update({con : str(o)})
        else:
            concept_dscrp.update({con : s + '\n' + str(o)})
        #d = concept_dscrp[con]

#print(concept_dscrp)

#for gsm, row in gse_df.iterrows():
#    descrp = row['DESCRIP']
#    embeddings = model.encode(descrp)

gsm_dscrp = list(gse_df['DESCRIP'])
concepts = list(concept_dscrp.keys())
term_dscrp = list(concept_dscrp.values())

gsm_embeddings = model.encode(gsm_dscrp)
term_embeddings = model.encode(term_dscrp)

print('\n----- embedding result -----')

print(gsm_embeddings.shape)
print(term_embeddings.shape)
sim = model.similarity(gsm_embeddings, term_embeddings)
print(sim)
print(sim.shape)

pd.DataFrame(sim).to_csv('dataset/embedding/similarity.csv', index=False, header=False)

max_idx = np.argmax(sim, axis=1)
max_con = [(concepts[i], term_dscrp[i]) for i in max_idx]
print(max_con)

#embedding = pd.read_csv('dataset/embedding/embeddings_preprocess_modified.txt', sep=' ', header=None, index_col=0)
#print(embedding)
