import GEOparse
import pandas as pd
import numpy as np
from tqdm import tqdm

from txt2con import EmbeddingConverter

TOP_CNT = 10

acc_pth = 'dataset/raw/accessions'
owl_pth = 'rules/go.owl'
out_pth = 'dataset/concepts/GSE_concepts.csv'

accessions = pd.read_csv(acc_pth)
embd = EmbeddingConverter(owl_pth, use_vpn=True)

gsm_names = []
concepts = []
gsm_descps = []
con_descps = [[] for _ in range(TOP_CNT)]

for accession in tqdm(accessions['accession'], 'Converting GSE descriptions'):

    gse = GEOparse.get_GEO(geo=accession, destdir="dataset/raw/GSE", silent=True)
    gse_path = f"dataset/raw/GSE/{accession}_family.soft.gz"
    gse = GEOparse.get_GEO(filepath=gse_path, silent=True)

    for gsm_name, gsm in gse.gsms.items():
        gsm_names.append(gsm_name)

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


        sim = embd.similar_matrix(description)
        sorted_sim = embd.max_sim(TOP_CNT)

        concepts.append(list(sorted_sim))



        gsm_descps.append(description)

        for i,c in enumerate(sorted_sim):
            d = embd.get_con_desc(c)
            con_descps[i].append(d)

df = {'SAMPLES':gsm_names, 'CONCEPTS':concepts}

df = pd.DataFrame(df)
df.set_index('SAMPLES', inplace=True)
df['DESC'] = gsm_descps
for i in range(TOP_CNT):
    df[f'CON_DESC{i}'] = con_descps[i]

print(df)
df.to_csv(out_pth)
