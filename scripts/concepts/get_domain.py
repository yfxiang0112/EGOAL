import pandas as pd

label_df = pd.read_csv('dataset/importance/dataset_onehot.csv')
unlabel_df = pd.read_csv('dataset/unlabel/dataset_unlabel.csv')

goa_df = pd.read_csv('rules/raw_goa/goa_mapping.csv', header=None)
all_con = pd.read_csv('dataset/concepts/all_concept_name.txt', header=None)
all_con = list(all_con[0])
#print(all_con)
#print(con_df['CONCEPTS'])

con_dom = set()
con_dom_data = set()

for con_lst in label_df['CONCEPTS']:
    for s in eval(con_lst):
        if s in all_con:
            con_dom.add(s)
            con_dom_data.add(s)

for con_lst in unlabel_df['CONCEPTS']:
    for s in eval(con_lst):
        if s in all_con:
            con_dom.add(s)
            con_dom_data.add(s)

for con in goa_df[0]:
    con_dom.add(con)

with open('dataset/concepts/concept_dom.txt', 'w') as f:
    f.write(str(con_dom))

with open('dataset/concepts/data_con_dom.txt', 'w') as f:
    f.write(str(con_dom_data))

print(f'len of concept domain:{len(con_dom)}, len of concept subdomain from dataset: {len(con_dom_data)}')
#con_dom = list(con_dom)
#con_dom.sort()
#
#df = pd.DataFrame({'0':con_dom})
#print(df)
#df.to_csv('dataset/concepts/concept_domain.csv', index=False, header=False)
