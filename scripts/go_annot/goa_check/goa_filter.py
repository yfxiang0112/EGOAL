import pandas as pd
from requests import head

goa_df = pd.read_csv('rules/goa_gene2go.csv', header=None, index_col=0)
#print(goa_df[1].apply(lambda x: len(x) > 3))
filtered_df = goa_df[goa_df[1].apply(lambda x: len(eval(x)) >= 3)]
print(filtered_df)
filtered_df.to_csv('rules/goa_gene2go_filtered.csv')
