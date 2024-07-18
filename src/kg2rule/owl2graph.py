from rdflib import Graph
import pandas as pd
import os
import re
import numpy as np

def findID(s):
    #TODO: process r'N\w{32}'

    s = str(s)

    idx = 0
    for i in range(len(s)):
        if s[i] == '/':
            idx = i
    s = s[idx+1:]
    return s


    '''
    res = re.findall(r'GO_\d*', s)
    if len(res) == 1:
        return res[0]

    res = re.findall(r'[BFR]{1,2}O_\d*', s)
    if len(res) == 1:
        return res[0]

    res = re.findall(r'N\w{32}', s)
    if len(res) == 1:
        return np.NaN
    '''

    return s

rdfFile = './rules/KG_RDF.csv'
rdfFile_filtered = './rules/KG_RDF_filter.csv'
prdcFile = './rules/predicates.csv'

RDF = pd.DataFrame()
RDF_filtered = pd.DataFrame()

if not os.path.exists(rdfFile):
    # parse owl file as rdf graph
    g = Graph()
    g.parse('./rules/go.owl')
    
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


#GO_pattern = r'GO_\d+'
GO_pattern = r'[GBFR]{1,2}O_\d+'

RDF = pd.read_csv(rdfFile)

#mask = RDF['subject'].str.contains(GO_pattern) |\
#        RDF['object'].str.contains(GO_pattern) | RDF['predicate'].str.contains(GO_pattern)
#RDF = RDF[mask]

#mask = RDF['predicate'].str.contains(RO_pattern)
#RDF = RDF[mask]

RDF.reset_index(drop=True, inplace=True)
print(RDF)

RDF['subject'] = RDF['subject'].apply(findID)
RDF['object'] = RDF['object'].apply(findID)
RDF['predicate'] = RDF['predicate'].apply(findID)
RDF.dropna(subset=['subject', 'object'], inplace=True)

predicates = list(set(RDF['predicate']))
predicates = pd.Series(predicates)
predicates.to_csv(prdcFile, index=False)



print(RDF)
RDF.to_csv(rdfFile_filtered, index=False)
