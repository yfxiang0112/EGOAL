import pandas as pd

from owl2graph import KG2Rule
from sg_spec import sg_con_filter


if __name__ == '__main__':
    ''' for raw OWL parsing and reading '''
    owlPth         = 'rules/go.owl'
    rdfPth         = 'rules/KG_RDF.csv'

    ''' for problem specification and subgraph extraction '''
    prdcLstPth      = 'rules/ref/predicates.csv'
    exclPrdcPth     = 'rules/ref/predicates_exclude.csv'
    conSpecPth      = 'dataset/concepts/concept_dom.txt'
    
    ''' for intermediate ruleset '''
    subGraphPth     = 'rules/owl2rule/KG_RDF_subgraph.csv'
    rulePth         = 'rules/owl2rule/ruleMined.csv'
    ruleRemPth      = 'rules/owl2rule/ruleRem.csv'
    contrElimPth    = 'rules/owl2rule/ruleConFree.csv'

    ''' for single gene ruleset and speed opt '''
    goaPth          = 'rules/goa_gene2go.csv'
    conSpecDatPth      = 'dataset/concepts/data_con_dom.txt'
    sgRulePth       = 'rules/single_genes'

    ############################################################

    ''' read concept domain '''
    conSpec = {}
    with open(conSpecPth, 'r') as f:
        conSpec = eval(f.readline())

    conSpecDat = {}
    with open(conSpecDatPth, 'r') as f:
        conSpecDat = eval(f.readline())

    ''' initialize KG to rule converter '''
    graph = KG2Rule(rdf_pth= rdfPth, con_spec= conSpec)

    ''' extract subgraph '''
    subGraphDf = graph.subGraph(exclPrdcPth, 5)
    subGraphDf.to_csv(subGraphPth, index=False)

    ''' mine rule '''
    mined_rule = graph.mineRule(rdf = pd.read_csv(subGraphPth))
    rem_rule = graph.remember(T=3)

    ''' handle contradiction '''
    cfree_rule = graph.contradict_elim()
    rule_df = graph.rule2df() 
    rule_df.to_csv(contrElimPth, index=False, header=False)

    ''' save as single gene rule & high speed ads '''
    gene2go = pd.read_csv(goaPth, header=None, index_col=0)
    for g in gene2go.index:
        rule_filtered = sg_con_filter(g, graph.get_rule(), gene2go, conSpecDat)
        pth = sgRulePth + '/' + g + '_sg_rule.csv'
        graph.rule2df(rule_filtered).to_csv(pth, index=False, header=False)
