import GEOparse
import pandas as pd
import numpy as np
from pandas.io.formats.style import Subset
import os
from tqdm import tqdm
import re

accessions = pd.read_csv("data_SOneidensis/accessions")

ORF_pattern = r'SO_*A*\d+'

#for accession in tqdm(accessions['accession'], 'Processing GSEs:'):
for accession in accessions['accession']:

    if os.path.exists("data_SOneidensis/matrix/" + accession + "_expr_mat.csv"):
        continue

    gse = GEOparse.get_GEO(geo=accession, destdir="data_SOneidensis/GSE", silent=True)
    gse_path = "data_SOneidensis/GSE/" + accession + "_family.soft.gz"
    gse = GEOparse.get_GEO(filepath=gse_path, silent=True)

    '''
    #gse_path = "data_SOneidensis/GSE102264/GSE102264_series_matrix.csv"
    gse_path = "data_SOneidensis/GSE102264_family.soft.gz"
    gpl_path = "data_SOneidensis/GSE102264/GPL17650_022828_D_GEO_20090205.txt.gz"
    gse = GEOparse.get_GEO(filepath=gse_path)
    #gse = GEOparse.get_GEO(geo="GSE102264", destdir="data_SOneidensis")
    print(gse)
    '''

    
    # check GPL

    gse_df = pd.DataFrame()
    gpl = None
    gpl_name = None

    #if len(gse.gpls.items()) == 1:
    for n,g in gse.gpls.items():
        gpl = g
        gpl_name = n
        break
    '''
    else:
        #TODO
        #print(accession, ', has multiple GPLs\n----------------------------------------\n')
        continue
    '''

    ########################################

    # check non-empty GSM table 
    non_empty = 0
    for _,s in gse.gsms.items():
        if not s.table.empty:
            non_empty += 1
    if non_empty==0:
        continue

    ########################################
    # switch GPL

    print(accession, gpl_name)

    ORF_col_name = ''
    log_flag = True

    match gpl_name:

        case 'GPL17650':
            ORF_col_name = 'ORF'
            #log_flag = False

        case 'GPL3253':
            ORF_col_name = 'ORF'

        case 'GPL16721':
            ORF_col_name = 'ORF'

        case 'GPL15821':
            ORF_col_name = 'ORF'

        case 'GPL14177':
            ORF_col_name = 'ORF'
            log_flag = False

        case 'GPL10101':
            ORF_col_name = 'ORF'
            log_flag = False

        case 'GPL7055':
            ORF_col_name = 'ORF'

        case 'GPL27952':
            ORF_col_name = 'ACCESSION_STRING'

        case 'GPL16797':
            #TODO
            continue

        case 'GPL15823':
            continue

        case 'GPL8434':
            ORF_col_name = 'ID'
            log_flag = False

        case _:
            print('unknown GPL:\n', gpl_name, '\n', gpl.table,'\n')
            for _, gsm in gse.gsms.items():
                print(gsm.table['ID_REF'])
                break
            gpl.table.to_csv('test_gpl.csv')
            exit()

    #print(gpl.columns)
    gpl.table.sort_values(by='ID', ascending = True, inplace = True)
    gpl.table = gpl.table.reset_index()
    gse_df = pd.DataFrame(gpl.table.dropna(subset=['ID'])[ORF_col_name])
    gse_df['GENE'] = gse_df[ORF_col_name]
    gse_df = gse_df.drop(ORF_col_name, axis=1)

    
    for gsm_name, gsm in gse.gsms.items():
        #print("Name: ", gsm_name, "\n")
    
        #print('characterstic:  ', gsm.metadata['characteristics_ch1'])
        #print('treatment:  ', gsm.metadata['treatment_protocol_ch1'])
        #print('growth:  ', gsm.metadata['growth_protocol_ch1'])
    
        '''
        
        for key, value in gsm.metadata.items():
            print(" - %s : %s" % (key, ", ".join(value)))
        '''
        #print ("Table data:",)
        #print(gsm.table)
    
        gsm_val = pd.DataFrame()

        gsm.table[gsm_name] = gsm.table['VALUE']
        gsm.table.sort_values(by='ID_REF', ascending = True, inplace = True)
        gsm.table = gsm.table.reset_index()
        gsm_val = gsm.table.dropna(subset=['ID_REF'])[gsm_name]
        #print(gsm_val)
    
        gse_df = pd.concat([gse_df, gsm_val], axis=1)

        #if not log_flag:
            #print(gse_df[gsm_name])
        #    gse_df[gsm_name] = np.log2(gse_df[gsm_name])
    
        #print(gsm.columns)
        #break
    
    gse_df = gse_df.dropna(subset=['GENE'])
    gse_df.sort_values(by= 'GENE', ascending= True, inplace= True)

    gse_df = gse_df[gse_df['GENE'].str.contains(ORF_pattern, regex=True)]

    gse_df = gse_df.reset_index()
    gse_df = gse_df.drop('index', axis=1)
    #gse_df_avg = gse_df.groupby('ORF').mean().reset_index()
    #print('\n',gse_df)
    
    '''
    gse_df = pd.read_csv(gse_path)
    '''
    gse_df.to_csv("data_SOneidensis/matrix/" + accession + "_expr_mat.csv")
    #print(gse_df)

    '''
    case _:
        print(gpl_name)
        print(gpl.columns)
        print(gpl.table)

        for gsm_name, gsm in gse.gsms.items():
            print(gsm.columns)
            print(gsm.table['ID_REF'])
    
            break
        exit()
    
    '''
