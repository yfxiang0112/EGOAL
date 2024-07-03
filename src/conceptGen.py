import pandas as pd
import GEOparse
from openai import OpenAI
import os

gse_df = pd.read_csv("data_SOneidensis/accessions")
description = []
openai_ans = []

for accession in gse_df['accession']:
    
    gse = GEOparse.get_GEO(geo=accession, destdir="data_SOneidensis/GSE")
    gse_path = "data_SOneidensis/GSE/" + accession + "_family.soft.gz"
    gse = GEOparse.get_GEO(filepath=gse_path)


    for gsm_name, gsm in gse.gsms.items():
        str = ''
        #print(gsm.metadata.keys())
        if('characteristics_ch1' in gsm.metadata):
            #print('characterstic:  ', gsm.metadata['characteristics_ch1'])
            for s in gsm.metadata['characteristics_ch1']:
                str = str + s + '\n'
        if('treatment_protocol_ch1' in gsm.metadata):
            #print('treatment:  ', gsm.metadata['treatment_protocol_ch1'])
            for s in gsm.metadata['treatment_protocol_ch1']:
                str = str + s + '\n'
        if('growth_protocol_ch1' in gsm.metadata):
            #print('growth:  ', gsm.metadata['growth_protocol_ch1'])
            for s in gsm.metadata['growth_protocol_ch1']:
                str = str + s + '\n'
        description.append(str)


for d in gse_df['description']:
    

gse_df['description'] = pd.Series(description)
print(gse_df)
