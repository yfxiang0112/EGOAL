from rdflib import Graph
import pandas as pd
import os
import re
import numpy as np

def findID(s):
    #TODO: process r'N\w{32}'

    s = str(s)

    res = re.findall(r'GO_\d*', s)
    if len(res) == 1:
        return res[0]

    res = re.findall(r'RO_\d*', s)
    if len(res) == 1:
        return res[0]

    res = re.findall(r'N\w{32}', s)
    res = re.findall(r'N\w{32}', s)
    if len(res) == 1:
        return np.NaN

    return s

rdfFile = './rules/KG_RDF.csv'
rdfFIle_filtered = './rules/KG_RDF_filter.csv'

RDF = pd.DataFrame()

if not os.path.exists(rdfFile):
    g = Graph()
    g.parse('./rules/go-plus.owl')
    
    lst_s = []
    lst_p = []
    lst_o = []
    
    print(len(g))
    for s,p,o in g:
        lst_s.append(s)
        lst_p.append(p)
        lst_o.append(o)
    
    RDF['subject'] = lst_s
    RDF['predicate'] = lst_p
    RDF['object'] = lst_o
    
    RDF.to_csv(rdfFile, index=False)

else:
    GO_pattern = r'GO_\d+'
    RO_pattern = r'RO_\d+'

    RDF = pd.read_csv(rdfFile)

    mask = RDF['subject'].str.contains(GO_pattern) | RDF['object'].str.contains(GO_pattern)
    RDF = RDF[mask]
    mask = RDF['predicate'].str.contains(RO_pattern)
    RDF = RDF[mask]
    
    RDF.reset_index(drop=True, inplace=True)
    print(RDF)
    
    RDF['subject'] = RDF['subject'].apply(findID)
    RDF['object'] = RDF['object'].apply(findID)
    RDF['predicate'] = RDF['predicate'].apply(findID)
    RDF.dropna(subset=['subject', 'object'], inplace=True)

    print(RDF)
    RDF.to_csv(rdfFIle_filtered, index=False)
