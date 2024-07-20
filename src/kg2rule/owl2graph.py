from rdflib import Graph
import pandas as pd
import os
import re
import numpy as np
from scipy.integrate._ivp.radau import P
from tqdm import tqdm

def extrID(s):
    s = str(s)

    idx = 0
    for i in range(len(s)):
        if s[i] == '/':
            idx = i+1
    s = s[idx:]

    return s

##################################################

class KG2Rule():

    def __init__(self, rdf_pth, owl_pth = '', ) -> None:
        if not os.path.exists(rdf_pth):
            if owl_pth=='':
                raise Exception('Need specify path to OWL file when owl is not parsed.')

            self.__readOWL(owl_pth, rdf_pth)

        self.rdf = pd.read_csv(rdf_pth)

        self.rdf['subject'] = self.rdf['subject'].apply(extrID)
        self.rdf['predicate'] = self.rdf['predicate'].apply(extrID)
        self.rdf['object'] = self.rdf['object'].apply(extrID)



    def __readOWL(self, owl_pth :str, out_pth :str):
        '''
        read owl file as rdf graph
        '''

        g = Graph()
        g.parse(owl_pth)
        
        # Create Dict of s,p,o
        df = {'subject':[], 'predicate':[], 'object':[]}
        for s,p,o in tqdm(g, 'Parsing OWL File'):
            df['subject'].append(s)
            df['predicate'].append(p)
            df['object'].append(o)
        
        df = pd.DataFrame(df)
        
        df.to_csv(out_pth, index=False)



    def subGraph(self, con_spec_pth :str, exclude_prdc_pth: str, d :int):
        '''
        Exclude Unused Predicates, and
        Extract Subgraph from parsed RDF (ABL-KG chap 4.3)
        '''

        con_spec = list(pd.read_csv(con_spec_pth, header=None)[0])
        exclude_prdc = list(pd.read_csv(exclude_prdc_pth, header=None)[0])

        mask = ~ self.rdf['predicate'].isin(exclude_prdc)
        self.rdf = self.rdf[mask]
        self.rdf.reset_index(drop=True, inplace=True)

        print('----- Statics of Filtered Predicates -----')
        print(self.rdf.groupby(by='predicate').count(), '\n')

        # TODO: handle most fraquent predicates: owl#annotatedProperty & owl#annotatedSource



        print('----- Extracting Subgraph -----')
        node_expand = con_spec
        node_succ   = []
        mask = [False]*len(self.rdf)
        for i in range(d):
            for idx, row in tqdm(self.rdf.iterrows(), 'Round '+str(i+1)):
                if mask[idx]:
                    continue

                if row['subject'] in node_expand:
                    node_succ.append(row['object'])
                    mask[idx] = True
                #elif row['object'] in node_expand:
                #    node_succ.append(row['subject'])
                #    mask[idx] = True


            node_expand = node_succ
            node_succ = []

        self.rdf = self.rdf[mask]
        self.rdf.reset_index(drop=True, inplace=True)
        print('Extracted Subgraph:\n', self.rdf)

        print('----- Statics of Subgraph Predicates -----')
        print(self.rdf.groupby(by='predicate').count(), '\n')

##################################################

        



#    res = re.findall(r'GO_\d*', s)
#    if len(res) == 1:
#        return res[0]
#
#    res = re.findall(r'[BFR]{1,2}O_\d*', s)
#    if len(res) == 1:
#        return res[0]
#
#    res = re.findall(r'N\w{32}', s)
#    if len(res) == 1:
#        return np.NaN


if __name__ == '__main__':

    owl_pth         = './rules/go.owl'
    rdf_pth         = './rules/KG_RDF.csv'

    filteredRdfPth  = './rules/KG_RDF_filter.csv'
    prdcPth         = 'rules/predicates.csv'
    exclPrdcPth     = 'rules/predicates_exclude.csv'
    conSpecPth      = 'dataset/concept_domain.csv'

    graph = KG2Rule(rdf_pth, owl_pth)

    graph.subGraph(conSpecPth, exclPrdcPth, 5)

#def prdcFilter(s):
#    s = str(s)
#    prdc_to_rm = {'oboInOwl#hasDbXref', 'rdf-schema#label', 'IAO_0000233', 'RO_0002161',\
#                  'oboInOwl#default-namespace', '', '', '',\
#                 }
#
#    if s in prdc_to_rm :
#        return np.NaN
#
#    return s
#
#
#RDF = pd.DataFrame()
#RDF_filtered = pd.DataFrame()
#
#if not os.path.exists(rdfFile):
#
#
##GO_pattern = r'GO_\d+'
#GO_pattern = r'[GBFR]{1,2}O_\d+'
#
#RDF = pd.read_csv(rdfFile)
#
##mask = RDF['subject'].str.contains(GO_pattern) |\
##        RDF['object'].str.contains(GO_pattern) | RDF['predicate'].str.contains(GO_pattern)
##RDF = RDF[mask]
#
##mask = RDF['predicate'].str.contains(RO_pattern)
##RDF = RDF[mask]
#
#RDF.reset_index(drop=True, inplace=True)
#print(RDF)
#
#RDF['subject'] = RDF['subject'].apply(findID)
#RDF['object'] = RDF['object'].apply(findID)
#RDF['predicate'] = RDF['predicate'].apply(findID)
#RDF.dropna(subset=['subject', 'object'], inplace=True)
#
#predicates = list(set(RDF['predicate']))
#predicates = pd.Series(predicates)
#predicates.to_csv(prdcFile, index=False, header=False)
#
#print(RDF)
#RDF.to_csv(rdfFile_filtered, index=False)
