import pandas as pd
import GEOparse
from openai import OpenAI
import os
from tqdm import tqdm

accessions = pd.read_csv("dataset/accessions")

gsm_df = pd.DataFrame()
gsm_names = []
descriptions = []
openai_ans = []

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

mdl = 'gpt-3.5-turbo'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

for accession in tqdm(accessions['accession'], 'Parsing GSE file:'):
#for accession in accessions['accession']:
    
    gse = GEOparse.get_GEO(geo=accession, destdir="dataset/GSE", silent=True)
    gse_path = "dataset/GSE/" + accession + "_family.soft.gz"
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
        descriptions.append(description)

gsm_df['SAMPLES'] = pd.Series(gsm_names)
gsm_df['DESCRIP'] = pd.Series(descriptions)
print(gsm_df)

cnt = 0

for d in tqdm(gsm_df['description'], 'Translating GO concept with OpenAI:'):
#for d in gsm_df['description']:
    completion = client.chat.completions.create(
            model=mdl,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': "Please summmerise conditions of the experiment from the following descriptions, and translate it to concept names in gene ontology (https://purl.obolibrary.org/obo/go.owl) and tell me their gene ontology ID:" + d}
            ]
    )

    ans = completion.choices[0].message.content
    openai_ans.append(ans)

    '''
    print(ans)
    if(cnt > 5):
        break
    cnt += 1
    '''
    
gsm_df['OPENAI_ANS'] = pd.Series(openai_ans)

gsm_df.sort_values(by=['SAMPLES'])
gsm_df.to_csv("dataset/GSE_concepts.csv")
