import pandas as pd

from owl2graph import KG2Rule
from sg_spec import sg_con_filter


if __name__ == '__main__':
    owlPth         = './rules/go.owl'
    rdfPth         = './rules/KG_RDF.csv'

    prdcLstPth         = 'rules/predicates.csv'
    exclPrdcPth     = 'rules/predicates_exclude.csv'
    conSpecPth      = 'dataset/concepts/concept_domain.csv'
    #filteredRdfPth  = './rules/KG_RDF_filter.csv'
    subGraphPth     = 'rules/KG_RDF_subgraph.csv'
    rulePth         = 'rules/ruleMined.csv'
    ruleRemPth      = 'rules/ruleRem.csv'
    contrElimPth    = 'rules/ruleConFree.csv'

    goaPth          = 'rules/goa_gene2go.csv'
    sgRulePth       = 'rules/single_genes'

    graph = KG2Rule(rdfPth, conSpecPth, owlPth)

    subGraphDf = graph.subGraph(exclPrdcPth, 5)
    subGraphDf.to_csv(subGraphPth, index=False)

    mined_rule = graph.mineRule(rdf = pd.read_csv(subGraphPth))
    rem_rule = graph.remember(T=3)
    cfree_rule = graph.contradict_elim()

    rule_df = graph.rule2df() 
    rule_df.to_csv(contrElimPth, index=False, header=False)

    gene2go = pd.read_csv(goaPth, header=None, index_col=0)
    for g in gene2go.index:
        rule_filtered = sg_con_filter(g, graph.get_rule(), gene2go)
        pth = sgRulePth + '/' + g + '_sg_rule.csv'
        graph.rule2df(rule_filtered).to_csv(pth, index=False, header=False)

