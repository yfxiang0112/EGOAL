'''
Concept specification for single gene id
Used in **accelerating** multi-label (3-clf for all genes) ABL
'''
import pandas as pd

def sg_con_filter(gene_id : str, rule_set : set, gene2go: pd.DataFrame):
    if gene_id not in gene2go.index:
        raise Exception('invalid gene id')

    row = gene2go.loc[gene_id]
    concept_set = row[0]
    assert type(concept_set) == set

    rule_filter = set(r for r in rule_set if (r[1] in concept_set or r[3] in concept_set))
    return rule_filter

def sg_iter(rule_set : set, gene2go : pd.DataFrame):
    for g in gene2go.index:
        rule_filter = sg_con_filter(g, rule_set, gene2go)
        #TODO
