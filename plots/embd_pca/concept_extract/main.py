import GEOparse
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from tqdm import tqdm

from txt2con import EmbeddingConverter

TOP_CNT = 10
''' get 10 most related concepts '''

acc_pth = 'dataset/raw/accessions'
owl_pth = 'rules/go.owl'
out_pth = 'dataset/concepts/GSE_concepts.csv'


''' initialize accession list and text embedding converter '''
accessions = pd.read_csv(acc_pth)
embd = EmbeddingConverter(owl_pth, use_vpn=True)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(embd.get_term_embd())
print(pca_result.shape)
#with open('src/concept_extract/pca_con_embd.npy', 'w') as f:
    #f.write(str(pca_result))
np.save('plots/embd_pca/pca_con_embd.npy', pca_result)


''' initialize data lists '''
gsm_names = []
concepts = []
gsm_descps = []
con_descps = [[] for _ in range(TOP_CNT)]

''' init pca vector of all descriptions '''
text_embd = []


''' iterate all gsms '''
for accession in tqdm(accessions['accession'], 'Converting GSE descriptions'):
    gse = GEOparse.get_GEO(geo=accession, destdir="dataset/raw/GSE", silent=True)
    gse_path = f"dataset/raw/GSE/{accession}_family.soft.gz"
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
        #sorted_sim = embd.max_sim(TOP_CNT)

        text_embd.append(embd.get_text_embd()[0])


        #concepts.append(list(sorted_sim))


        ''' record descriptions '''
        gsm_descps.append(description)

        #for i,c in enumerate(sorted_sim):
        #    d = embd.get_con_desc(c)
        #    con_descps[i].append(d)


text_embd = np.array(text_embd)
print(text_embd.shape)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(text_embd)
print(pca_result.shape)
#with open('src/concept_extract/pca_txt_embd.txt', 'w') as f:
    #f.write(str(pca_result))
np.save('plots/embd_pca/pca_txt_embd.npy', pca_result)

#''' save as dataframe '''
#df = {'SAMPLES':gsm_names, 'CONCEPTS':concepts}
#
#df = pd.DataFrame(df)
#df.set_index('SAMPLES', inplace=True)
#df['DESC'] = gsm_descps
#for i in range(TOP_CNT):
#    df[f'CON_DESC{i}'] = con_descps[i]
#
#print(df)
#df.to_csv(out_pth)
