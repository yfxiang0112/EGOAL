'''
Concept specification for single gene id
Used in **accelerating** multi-label (3-clf for each gene) ABL
'''
import pandas as pd

def sg_con_filter(gene_id : str, rule_set : set, gene2go : pd.DataFrame, dataset_con_dom : set):
    if gene_id not in gene2go.index:
        raise Exception('invalid gene id')

    row = gene2go.loc[gene_id]
    concept_set = eval(row[1])
    assert type(concept_set) == set

    #concept_set = concept_set.union(dataset_con_dom)

    rule_filter = set(r for r in rule_set if (r[1] in concept_set and r[3] in dataset_con_dom))
    rule_filter_rev = set(r for r in rule_set if (r[1] in dataset_con_dom and r[3] in concept_set))
    return rule_filter.union(rule_filter_rev)

#def sg_iter(rule_set : set, gene2go : pd.DataFrame):
#    for g in gene2go.index:
#        rule_filter = sg_con_filter(g, rule_set, gene2go)
#        #TODO serialization

if __name__ == '__main__':

    contrElimPth    = 'rules/owl2rule/ruleConFree.csv'
    rule = pd.read_csv(contrElimPth, header=None)
