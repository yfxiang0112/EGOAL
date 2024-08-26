import pandas as pd

from txt2con import EmbeddingConverter

TOP_CNT = 10
''' get 10 most related concepts '''

owl_pth = 'rules/go.owl'
in_pth = 'src/concept_extract/pred_text.txt'
out_pth = 'src/concept_extract/result.txt'


''' initialize text embedding converter '''
embd = EmbeddingConverter(owl_pth, use_vpn=True)

''' initialize data lists '''
concepts = []
con_descps = [[] for _ in range(TOP_CNT)]

''' read description from input file '''

descriptions = []
with open(in_pth, 'r') as f:
    descriptions = f.readlines()


''' iterate instances '''
for d in descriptions:

        ''' compute similarity matrix & most similar concept list '''
        sim = embd.similar_matrix(d)
        sorted_sim = embd.max_sim(TOP_CNT)

        concepts.append(list(sorted_sim))


        ''' record descriptions '''

        for i,c in enumerate(sorted_sim):
            d = embd.get_con_desc(c)
            con_descps[i].append(d)

''' save as dataframe '''
df = {'CONCEPTS':concepts}

df = pd.DataFrame(df)
for i in range(TOP_CNT):
    df[f'CON_DESC{i}'] = con_descps[i]

print(df)
df.to_csv(out_pth)
