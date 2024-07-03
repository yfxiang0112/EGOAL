import GEOparse
import pandas as pd
from pandas.io.formats.style import Subset

#gse_path = "data_SOneidensis/GSE102264/GSE102264_series_matrix.csv"
gse_path = "data_SOneidensis/GSE102264_family.soft.gz"
gpl_path = "data_SOneidensis/GSE102264/GPL17650_022828_D_GEO_20090205.txt.gz"
gse = GEOparse.get_GEO(filepath=gse_path)
#gse = GEOparse.get_GEO(geo="GSE102264", destdir="data_SOneidensis")
print(gse)

gse_df = pd.DataFrame

for gpl_name, gpl in gse.gpls.items():
    #print(gpl.columns)
    gpl.table.sort_values(by='ID', ascending = True, inplace = True)
    gpl.table = gpl.table.reset_index()
    gse_df = gpl.table.dropna(subset=['ID'])['ORF']
    break

for gsm_name, gsm in gse.gsms.items():
    print("Name: ", gsm_name, "\n")

    print('characterstic:  ', gsm.metadata['characteristics_ch1'])
    print('treatment:  ', gsm.metadata['treatment_protocol_ch1'])
    print('growth:  ', gsm.metadata['growth_protocol_ch1'])

    '''
    for key, value in gsm.metadata.items():
        print(" - %s : %s" % (key, ", ".join(value)))
    '''
    #print ("Table data:",)
    #print (gsm.table.head())
    #print(gsm.table)

    gsm_val = pd.DataFrame
    gsm.table[gsm_name] = gsm.table['VALUE']
    gsm.table.sort_values(by='ID_REF', ascending = True, inplace = True)
    gsm.table = gsm.table.reset_index()
    gsm_val = gsm.table.dropna(subset=['ID_REF'])[gsm_name]
    #print(gsm_val)

    gse_df = pd.concat([gse_df, gsm_val], axis=1)

    #print(gsm.columns)
    #break


gse_df = gse_df.dropna(subset=['ORF'])
gse_df.sort_values(by= 'ORF', ascending= True, inplace= True)
#gse_df_avg = gse_df.groupby('ORF').mean().reset_index()
print('\n',gse_df)

'''
gse_df = pd.read_csv(gse_path)
print(gse_df)
'''
