import pandas as pd

con_df = pd.read_csv('dataset/concepts/GSE_concepts.csv')
all_con = pd.read_csv('dataset/concepts/all_concept_name.txt', header=None)
all_con = list(all_con[0])
#print(all_con)
#print(con_df['CONCEPTS'])

con_dom = set()

for con_lst in con_df['CONCEPTS']:
    for s in eval(con_lst):
        #con_dom.add(s)
        #NOTE: tmp operation, transfer GO:xxxx to GO_xxxx
        if s in all_con:
            con_dom.add('GO_'+s[3:])

con_dom = list(con_dom)
con_dom.sort()

df = pd.DataFrame({'0':con_dom})
print(df)
df.to_csv('dataset/concepts/concept_domain.csv', index=False, header=False)

