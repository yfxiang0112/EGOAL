import re
from rdflib import Graph


def graph_parse(g : Graph, label_predicates = None) -> dict:
    if label_predicates != None:
        label_prdcs = list(label_predicates)
    else:
        label_prdcs = [
        'http://www.w3.org/2000/01/rdf-schema#label',
        'http://www.w3.org/2002/07/owl#annotatedTarget',
        'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym',
        'http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym',
        'http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym',
        'http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym',
        'http://purl.obolibrary.org/obo/IAO_0000115']

    concept_dscrp = {}
    for s,p,o in g:
        
        if str(p) in label_prdcs:
            p = r'GO_\d+'
            con = re.findall(p, str(s))
            if len(con) != 1:
                continue
            con = con[0]
            s = concept_dscrp.get(con)
            if s == None:
                concept_dscrp.update({con : str(o)})
            else:
                concept_dscrp.update({con : s + '\n' + str(o)})

    return concept_dscrp
