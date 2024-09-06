import GEOparse
import pandas as pd
import numpy as np
from tqdm import tqdm

from txt2con import EmbeddingConverter

TOP_CNT = 10
''' get 10 most related concepts '''

#acc_pth = 'dataset/raw/accessions'
#owl_pth = 'rules/go.owl'
#out_pth = 'dataset/concepts/GSE_concepts.csv'
#geo_dst = 'dataset/raw/GSE'

acc_pth = 'dataset/unlabel/accessions-all'
owl_pth = 'rules/go.owl'
out_pth = 'dataset/unlabel/unlabel_concepts.csv'
geo_dst = 'dataset/unlabel/GSE'


''' initialize accession list and text embedding converter '''
accessions = pd.read_csv(acc_pth)
embd = EmbeddingConverter(owl_pth, use_vpn=True)

''' initialize data lists '''
gsm_names = []
concepts = []
#gsm_descps = []
#con_descps = [[] for _ in range(TOP_CNT)]


''' iterate all gsms '''
for accession in tqdm(accessions['accession'], 'Converting GSE descriptions'):
    accession = str(accession)
    gse = GEOparse.get_GEO(geo=accession, destdir=geo_dst, silent=True)
    gse_path = f"{geo_dst}/{accession}_family.soft.gz"
    gse = GEOparse.get_GEO(filepath=gse_path, silent=True)

    for gsm_name, gsm in gse.gsms.items():
        if gsm_name in gsm_names:
            continue

        gsm_names.append(gsm_name)


        
        ''' generate GSM description '''
        description = ''
        if('characteristics_ch1' in gsm.metadata):
            for s in gsm.metadata['characteristics_ch1']:
                description = description + s + '\n'
        if('treatment_protocol_ch1' in gsm.metadata):
            for s in gsm.metadata['treatment_protocol_ch1']:
                description = description + s + '\n'
        if('growth_protocol_ch1' in gsm.metadata):
            for s in gsm.metadata['growth_protocol_ch1']:
                description = description + s + '\n'


        ''' compute similarity matrix & most similar concept list '''
        sim = embd.similar_matrix(description)
        sorted_sim = embd.max_sim(TOP_CNT)

        concepts.append(list(sorted_sim))


        #NOTE: tmp
        with open('dataset/unlabel/concepts.txt', 'w') as f:
            f.write(str(concepts))


        ''' record descriptions '''
        #gsm_descps.append(description)

        #for i,c in enumerate(sorted_sim):
        #    d = embd.get_con_desc(c)
        #    con_descps[i].append(d)

''' save as dataframe '''
df = {'SAMPLES':gsm_names, 'CONCEPTS':concepts}

df = pd.DataFrame(df)
df.set_index('SAMPLES', inplace=True)
#df['DESC'] = gsm_descps
#for i in range(TOP_CNT):
#    df[f'CON_DESC{i}'] = con_descps[i]

print(df)
df.to_csv(out_pth)
