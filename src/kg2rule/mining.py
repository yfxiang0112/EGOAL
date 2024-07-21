def ruleTranslate(s: str, p:str, o:str):
    '''
    Translate an RDF triple <s,p,o> to Horn Clause (~)x | (~)y,
    according to the natural semantic of the predicate.
    '''

    flags = []

    match p:

        case '22-rdf-syntax-ns#first': 
            #TODO
            '''
            counts 1475 in extracted subgraph
            '''
            pass

        case '22-rdf-syntax-ns#rest': 
            '''
            counts 1475 in extracted subgraph
            '''
            pass

        case 'IAO_0100001': 
            '''
            IAO_0100001 'term_replaced_by'
            logic expr: x<->y  =  (~x|y)&(x|~y)
            Definition: Use on obsolete terms, relating the term to another term that can be used as a substitute
            subgraph count: 156 '''
            flags = [(False, True), (True, False)]

        case 'oboInOwl#consider': 
            #TODO
            '''
            counts 95 in extracted subgraph
            '''
            pass

        case 'oboInOwl#hasAlternativeId': 
            '''
            logic expr: x<->y  =  (~x|y)&(x|~y)
            subgraph count: 1015 '''
            flags = [(False, True), (True, False)]

        case 'oboInOwl#inSubset': 
            #TODO
            '''
            counts 1834 in extracted subgraph
            '''
            pass

        case 'owl#disjointWith': 
            '''
            logic expr: ~x|~y
            subgraph count: 26'''
            flags = [(False, False)]

        case 'owl#equivalentClass': 
            '''
            logic expr: x<->y  =  (~x|y)&(x|~y)
            subgraph count: 983 '''
            flags = [(False, True), (True, False)]

        case 'owl#intersectionOf': 
            #TODO
            '''
            subgraph count: 939
            '''
            pass

        case 'owl#inverseOf': 
            '''
            Do NOT process.
            subgraph count: 1 '''
            pass

        case 'owl#onProperty':
            #TODO
            '''
            subgraph count: 1884 '''

            match o:

                case 'BFO_0000050':
                    pass

                case 'BFO_0000051':
                    pass

                case 'BFO_0000066':
                    pass

                case 'RO_0002092':
                    pass

                case 'RO_0002211':
                    pass

                case 'RO_0002212':
                    pass

                case 'RO_0002213':
                    pass

                case _:
                    pass

        case 'owl#propertyChainAxiom':
            #TODO
            '''
            counts 2 in extracted subgraph
            '''
            pass

        case 'owl#someValuesFrom':
            #TODO
            '''
            counts 1884 in extracted subgraph
            '''
            pass

        case 'rdf-schema#subClassOf':
            '''
            logic expr: ~x|y
            subgraph count: 8345 '''
            flags = [(False, True)]
    
        case 'rdf-schema#subPropertyOf':
            '''
            logic expr: ~x|y
            subgraph count: 22 '''
            flags = [(False, True)]

    if s < o:
        return [(f[0], s, f[1], o) for f in flags]
    else:
        return [(f[1], o, f[0], s) for f in flags]
