import pandas as pd

df_exp = pd.read_csv('predict/results/res_NADK.txt', sep='\t')
df_ctr = pd.read_csv('predict/results-ref/res_0.txt', sep='\t')

#df_filter = df_exp.iloc[df_exp['gene_id'] in df_ctr['gene_id']]
df_filter = df_exp[~df_exp['gene_id'].isin(df_ctr['gene_id'])]
df_filter.reset_index(inplace=True)
df_filter.drop(columns=['index'], inplace=True)
print(df_filter)
df_filter.to_csv('predict/results-ref/res_NADKvsGADPH.txt', sep='\t', index=False)
